#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginc/conf.d/default.conf
nginx -gt 'daemon off;'