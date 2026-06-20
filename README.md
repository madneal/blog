# blog
[![Deploy Hugo site](https://github.com/madneal/blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/madneal/blog/actions/workflows/deploy.yml)

## Deployment

Pushing to `master` runs GitHub Actions to build the Hugo site and publish `public/`
to `madneal/madneal.github.io`.

The source repository needs a `GH_PAGES_TOKEN` secret with permission to push to
`madneal/madneal.github.io`.

The Hugo theme is tracked as a submodule from `madneal/hugo-nuo`, so theme
changes can be maintained independently from the blog content.
