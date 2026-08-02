#!/usr/bin/env bash

set -euo pipefail

site_dir="${1:-public}"
errors=0

if [[ ! -d "$site_dir" ]]; then
  printf 'SEO check failed: output directory does not exist: %s\n' "$site_dir" >&2
  exit 1
fi

while IFS= read -r -d '' file; do
  # Hugo emits redirect-only alias pages for the first paginator page.
  if grep -q 'http-equiv="refresh"' "$file"; then
    continue
  fi

  title_count=$(grep -o '<title>' "$file" 2>/dev/null | wc -l | tr -d ' ' || true)
  description_count=$(grep -o 'name="description"' "$file" 2>/dev/null | wc -l | tr -d ' ' || true)
  canonical_count=$(grep -o 'rel="canonical"' "$file" 2>/dev/null | wc -l | tr -d ' ' || true)

  if [[ "$title_count" -ne 1 ]]; then
    printf 'SEO check failed: expected one title in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
  if [[ "$description_count" -ne 1 ]] || grep -q 'name="description" content=""' "$file"; then
    printf 'SEO check failed: expected one non-empty description in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
  if [[ "$canonical_count" -ne 1 ]]; then
    printf 'SEO check failed: expected one canonical link in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
done < <(find "$site_dir" -type f -name '*.html' -print0)

while IFS= read -r -d '' file; do
  if ! grep -q '^title:' "$file"; then
    printf 'SEO check failed: missing title in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
  if ! grep -Eq '^(description|summary):[[:space:]]*[^[:space:]]' "$file"; then
    printf 'SEO check failed: missing description or summary in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
  if grep -Eq '^description:[[:space:]]*(""|'"'"''"'"')?[[:space:]]*$' "$file"; then
    printf 'SEO check failed: empty description in %s\n' "$file" >&2
    errors=$((errors + 1))
  fi
done < <(find content -type f -name '*.md' -print0)

for required_file in "$site_dir/sitemap.xml" "$site_dir/robots.txt"; do
  if [[ ! -s "$required_file" ]]; then
    printf 'SEO check failed: missing or empty %s\n' "$required_file" >&2
    errors=$((errors + 1))
  fi
done

if [[ "$errors" -gt 0 ]]; then
  printf 'SEO check found %d error(s).\n' "$errors" >&2
  exit 1
fi

printf 'SEO check passed for %s.\n' "$site_dir"
