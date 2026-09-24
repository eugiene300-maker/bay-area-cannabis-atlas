# LOUD LOCAL

Purple Lotus sponsored San Jose consumer resource. Static, multipage site.

Live: https://eugiene300-maker.github.io/bay-area-cannabis-atlas

## Structure

- `dist/` — the published website (HTML, local images, sitemap, RSS, llms.txt). Deployed as-is.
- `src/` — shared CSS and browser scripts, copied into `dist/assets/` by the build.
- `data/` — site config (`config.json`: site kind and canonical URL), editorial content, articles, photo credits and fetched source data.
- `scripts/` — `build.py` (static page generator, Python 3.12+), `refresh.py` (source fetcher that keeps the last good data on failure), `check.py` (HTML, link, asset and schema checks), `test-*.cjs` (Node tests).

## Commands

```
python3 scripts/refresh.py   # fetch public source data
python3 scripts/build.py     # regenerate dist/
python3 scripts/check.py     # validate pages, links, assets, schema
npm test                     # calculator and sharing tests
```

## Deployment

Primary address: https://eugiene300-maker.github.io/bay-area-cannabis-atlas/ (GitHub Pages, published by `.github/workflows/pages.yml` on every push to `main` and after each scheduled refresh). Canonical URLs, the sitemap and llms.txt point to this address; it is set in `data/config.json`.

Mirrors on other static hosts: output directory `dist`. To keep the canonical pointing at the primary address, use no build command. To give a mirror its own canonical and sitemap, use build command `python3 scripts/build.py` with Python 3.12+ and set the `SITE_URL` environment variable to that host's address.

## Local culture section

`data/local-places.json` holds the place profiles and `data/local-editions.json` is an append-only list of dated weekly editions (the home page shows the latest). New editions are added by hand: each needs `date`, `ends`, `range`, `reviewed`, `title`, `intro` and `items` (`id`, `label`, `title`, `text`, `source`). `scripts/refresh-local.py` checks the original sources weekly via `.github/workflows/local-source-monitor.yml` and flags changes in `data/local-source-status.json`; it does not write editions.

## Content boundaries

No products are sold here. No medical recommendations, dosing instructions, live-stock claims, verified-license badges or guaranteed delivery times. Sponsor links use `rel="sponsored"`. Photo credits and licenses are listed on the Sources page and in `IMAGE-SOURCES.md`.
