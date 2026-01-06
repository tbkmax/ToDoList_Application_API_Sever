#!/usr/bin/env bash
# Health check script for Nginx endpoint.
# Usage: ./check_health.sh; echo exit_code:$?
# Default URL: http://127.0.0.1/

set -o pipefail

URL="${1:-http://127.0.0.1/}"
http_code=$(curl -s -L -o /dev/null -w "%{http_code}" --max-time 5 "$URL")

if [ "$http_code" = "200" ]; then
  exit 0
else
  echo "health check failed: HTTP $http_code" >&2
  exit 1
fi
