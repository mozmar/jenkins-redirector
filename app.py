import re

from flask import Flask, abort, redirect
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.contrib.cache import SimpleCache

import requests
from decouple import config


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

cache = SimpleCache()

JENKINS_SERVER = config('JENKINS_SERVER', default='https://ci.us-west.moz.works')
HOME_REDIRECT = config('HOME_REDIRECT', default='https://github.com/mozmar/jenkins-redirector')
NAME_RE = re.compile(r'^[\w-]+$')


def validate_names(*names):
    return all(NAME_RE.match(name) for name in names)


def get_build_id(jobname, branch='master'):
    cache_key = '{}:{}'.format(jobname, branch)
    build_id = cache.get(cache_key)
    if build_id is None:
        build_id = get_latest_build_id(jobname, branch)
        if build_id:
            cache.set(cache_key, build_id, 60 * 15)

    return build_id


def get_latest_build_id(jobname, branch='master'):
    api_url = '{}/job/{}/job/{}/lastBuild/api/json'.format(JENKINS_SERVER, jobname, branch)
    resp = requests.get(api_url)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        return None

    try:
        data = resp.json()
    except Exception:
        return None

    return data.get('id')


@app.route('/<jobname>/', defaults={'branch': 'master'})
@app.route('/<jobname>/<branch>/')
def job_redirect(jobname, branch):
    if not validate_names(jobname, branch):
        abort(400)

    build_id = get_build_id(jobname, branch)
    if not build_id:
        abort(404)

    return redirect('{}/blue/organizations/jenkins/{}/detail/{}/{}/pipeline/'.format(
        JENKINS_SERVER, jobname, branch, build_id))


@app.route('/')
def home():
    return redirect(HOME_REDIRECT, 301)
