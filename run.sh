#!/bin/bash
set -exo pipefail

exec gunicorn app:app -b 0.0.0.0:${PORT:-5000} -w ${WEB_CONCURRENCY:-2} --error-logfile - --access-logfile - --log-level ${LOGLEVEL:-info}
