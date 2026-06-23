# blog
[![Deploy Hugo site](https://github.com/madneal/blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/madneal/blog/actions/workflows/deploy.yml)

## Architecture

```mermaid
flowchart LR
    source["madneal/blog<br/>content, config, assets"]
    theme["hugo-nuo<br/>theme submodule"]
    actions["GitHub Actions<br/>Hugo build"]
    pagesRepo["madneal.github.io<br/>published files"]
    site["madneal.com"]

    source --> actions
    theme --> actions
    actions -->|generates public/| pagesRepo
    pagesRepo -->|GitHub Pages| site

    classDef repo fill:#eef6ff,stroke:#4f8cc9,color:#17324d;
    classDef build fill:#fff5d7,stroke:#c28a00,color:#3f2b00;
    classDef live fill:#eaf7ec,stroke:#4f9a5f,color:#17391d;
    class source,theme,pagesRepo repo;
    class actions build;
    class site live;
```

`madneal/blog` is the source repository. It keeps the posts, Hugo configuration,
layout overrides, static files, and the `hugo-nuo` theme pointer. GitHub Actions
builds the site into `public/`, then publishes that generated output to
`madneal/madneal.github.io` for GitHub Pages to serve at `madneal.com`.

## Deployment

Pushing to `master` runs GitHub Actions to build the Hugo site and publish `public/`
to `madneal/madneal.github.io`.

The source repository needs a `GH_PAGES_TOKEN` secret with permission to push to
`madneal/madneal.github.io`.

The Hugo theme is tracked as a submodule from `madneal/hugo-nuo`, so theme
changes can be maintained independently from the blog content.
