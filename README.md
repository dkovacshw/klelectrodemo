# K-L Electro demo

Static Hungarian electrician website. No npm installation or runtime server needed.

## Editing and validation

Edit page content in `scripts/rebuild_blue.py`, shared styles in `assets/css/blue.css`,
and navigation behavior in `assets/js/blue.js`. Historical grant text is in
`content/grants.html`. Rebuild HTML after content changes:

```sh
python scripts/rebuild_blue.py
python scripts/check_site.py
```

The repository root is the GitHub Pages demo: intentionally **noindex**.
Publish using Settings > Pages > Deploy from a branch > main > /(root).
The 404 page assumes the repository name is klelectrodemo.

## Production on klelectro.hu

```sh
python scripts/rebuild_blue.py --production
python scripts/check_site.py --production
```

Upload the contents of `.build/production/` to the production document root.
Every content page, including `/referenciak/`, uses index/follow. Review the
included Apache `.htaccess` for your host before deployment. GitHub Pages does
not run Apache redirect rules. Production assets are copied from the demo source.

See `SEO-REVIEW.md` for the review and information needed for future project pages.
