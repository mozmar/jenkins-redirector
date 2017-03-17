## Jenkins Redirector

A tiny Flask app to discover the latest job ID for a particular [multibranch pipeline][] job on Jenkins
and redirect to the [Blue Ocean][] view of that job.

### Configuration

Configuration is done via environment variables. The following are available:

```bash
# Jenkins server base URL
JENKINS_SERVER=https://your-jenkins-server-domain.com

# Repo URL. Used on the home page.
GITHUB_URL=https://github.com/you/your-fork-of-this-app/

# number of minutes to cache build IDs per job and branch
CACHE_MINUTES=30
```

You can set those locally in a `.env` file or with actual environment variables.

### Docker

Build your image:

```bash
$ docker build -t jenkins-redirector .
```

Run the thing:

```bash
$ docker run -it -p 5000:5000 -e CACHE_MINUTES=1 jenkins-redirector
```

### Deployment

Deploys well as-is to [Dokku][] and [Deis][]. Should work well on [Heroku][] as well, but might require some tweaks.

[multibranch pipeline]: https://jenkins.io/blog/2015/12/03/pipeline-as-code-with-multibranch-workflows-in-jenkins/
[Blue Ocean]: https://jenkins.io/projects/blueocean/
[Dokku]: http://dokku.viewdocs.io/dokku/
[Deis]: https://deis.com/
[Heroku]: https://www.heroku.com/
