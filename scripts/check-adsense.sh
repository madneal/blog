#!/usr/bin/env bash

set -euo pipefail

site_dir="${1:-public}"
client_id="${ADSENSE_CLIENT:-ca-pub-5932835142675120}"
publisher_id="${client_id#ca-}"
errors=0

if [[ ! -d "$site_dir" ]]; then
  printf 'AdSense check failed: output directory does not exist: %s\n' "$site_dir" >&2
  exit 1
fi

if [[ ! -s "$site_dir/ads.txt" ]]; then
  printf 'AdSense check failed: missing or empty %s/ads.txt\n' "$site_dir" >&2
  errors=$((errors + 1))
elif ! grep -Fxq "google.com, $publisher_id, DIRECT, f08c47fec0942fa0" "$site_dir/ads.txt"; then
  printf 'AdSense check failed: expected publisher entry is missing from %s/ads.txt\n' "$site_dir" >&2
  errors=$((errors + 1))
fi

while IFS= read -r -d '' file; do
  # Hugo emits redirect-only alias pages for the first paginator page.
  if grep -q 'http-equiv="refresh"' "$file"; then
    continue
  fi

  if ! grep -Fq "adsbygoogle.js?client=$client_id" "$file"; then
    printf 'AdSense check failed: loader is missing from %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
  if [[ "$(grep -Fo "adsbygoogle.js?client=$client_id" "$file" | wc -l | tr -d ' ')" -ne 1 ]]; then
    printf 'AdSense check failed: loader must appear once in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
done < <(find "$site_dir" -type f -name '*.html' -print0)

if [[ "$errors" -gt 0 ]]; then
  printf 'AdSense check found %d error(s).\n' "$errors" >&2
  exit 1
fi

printf 'AdSense check passed for %s.\n' "$site_dir"
