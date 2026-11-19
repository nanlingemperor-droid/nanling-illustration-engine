# Nanling Illustration Engine

Python-first illustration and asset pipeline for Nanling Daozang.

## Features
- Procedural scientific SVG illustrations: planet concepts, Kardashev scale, and technology flow diagrams.
- Import existing artwork and optimize raster images to WebP with Pillow.
- Generate a JSON catalog and a responsive gallery.
- Publish static assets through GitHub Pages using GitHub Actions.
- Keep original AI artwork in `assets/inbox/`; the Python pipeline only copies and optimizes it.

> Python can generate diagrams and procedural illustrations. It does not itself create photorealistic text-to-image AI artwork. Existing AI-created artwork can be imported into the catalog.

## Quick start

Python 3.11+:

```bash
pip install -r requirements.txt
python generator.py generate-all
python generator.py build
```

Generated files are written to `site/assets/` and `site/catalog.json`.

## Add artwork
Put licensed artwork you own or are allowed to use in `assets/inbox/`. Add an optional same-named JSON file for title/category/description/creator/license. Then run `python generator.py build`.

## GitHub Pages
Open **Settings → Pages** and choose **GitHub Actions** as the deployment source. Pushes to `main` run `.github/workflows/pages.yml`.

After the first successful deployment:
- Gallery: `https://nanlingemperor-droid.github.io/nanling-illustration-engine/`
- Catalog: `https://nanlingemperor-droid.github.io/nanling-illustration-engine/catalog.json`

## Blogger
See `docs/blogger-integration.md`. The integration is intended for the Wanxiang/Nanling Daozang template only. Do not change the main blog template.

Never commit API keys, passwords, or private data.
