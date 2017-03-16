import os

from flask import Flask, abort, redirect, request
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.contrib.cache import SimpleCache

import requests
from decouple import config


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

cache = SimpleCache()

JENKINS_SERVER = config('JENKINS_SERVER', default='https://ci.us-west.moz.works')


def get_build_id(jobname, branch='master'):
    cache_key = '{}:{}'.format(jobname, branch)
    build_id = cache.get(cache_key)
    if build_id is None:
        build_id = get_latest_build_id(jobname, branch)
        cache.set(cache_key, build_id, 60 * 15)

    return build_id


def get_latest_build_id(jobname, branch='master'):
    api_url = '{}/job/{}/job/{}/lastBuild/api/json'.format(JENKINS_SERVER, jobname, branch)
    data = requests.get(api_url).json()
    return data.get('id')


@app.route('/')
def home():
    jobname = request.args.get('jobname')
    branch = request.args.get('branch', 'master')
    if not (jobname and branch):
        abort(404)

    build_id = get_build_id(jobname, branch)
    if not build_id:
        abort(404)

    return redirect('{}/blue/organizations/jenkins/{}/detail/{}/{}/pipeline/'.format(
        JENKINS_SERVER, jobname, branch, build_id))

