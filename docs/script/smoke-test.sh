#!/usr/bin/env bash

set -euo pipefail

BASE_URL="${APP_BASE_URL:https://github.com/GreninjaBoy23D/Capstone-Respiretory.git}"
ENDPOINT="${SMOKE_ENDPOINT:-/api/items}"
EXPECT="${SMOKE_EXPECT:-oat milk}"
TIMEOUT_SECONDS="${SMOKE_TIMEOUT:-30}"

fail() {
  printf 'SMOKE FAIL: %s\n' "$1" >&2
  exit 1
}

# --- Hop 1: is anything listening at all? ------------------------------------
deadline=$(( $(date +%s) + TIMEOUT_SECONDS ))
until curl -fsS -o /dev/null "${BASE_URL}${ENDPOINT}" 2>/dev/null; do
  if [ "$(date +%s)" -ge "$deadline" ]; then
    fail "nothing answered at ${BASE_URL}${ENDPOINT} within ${TIMEOUT_SECONDS}s (client -> route hop)"
  fi
  sleep 1
done

# --- Hop 2: does the route return a body we can read? ------------------------
body="$(curl -fsS "${BASE_URL}${ENDPOINT}")" || fail "request to ${ENDPOINT} returned a non-2xx status (route -> service hop)"
[ -n "$body" ] || fail "response body was empty (service -> data store hop)"

# --- Hop 3: did the data come from the data store? ---------------------------
# EXPECT is a value that exists ONLY because a seeded row exists. If you can
# pass this check with the database stopped, you are not testing the skeleton.
if ! printf '%s' "$body" | grep -q "$EXPECT"; then
  preview="$(printf '%s' "$body" | tr -d '\n' | cut -c1-200)"
  fail "response did not contain the seeded value '${EXPECT}' (data store hop). Got: ${preview}"
fi

printf 'SMOKE OK: %s%s returned the seeded row (%s). The skeleton walks.\n' \
  "$BASE_URL" "$ENDPOINT" "$EXPECT"
