#!/bin/sh
set -eu

flask --app app.main db upgrade
exec "$@"

