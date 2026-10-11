# mathematics-of-investment-and-portfolio-management — full book reader

Live reader: https://nutdnuy.github.io/mathematics-of-investment-and-portfolio-management/

The full reader replaces the former overview at the same URL, so existing bookshelf links now lead to readable chapters. Nuth confirmed public publication rights on 2026-10-11. See reader/RIGHTS.md.

This is a disclosed transcription draft, not a fully reviewed edition. The original PDF and chapter downloads are included, and page review labels remain accurate.

## Build and update

Run `python3 scripts/build.py` to validate the SHA-256 snapshot manifest and all local HTML file/anchor references, then export `_site/`. Push to main publishes through GitHub Actions.

The editable source project is `mathematics-of-investment-and-portfolio-management-notes`. Rebuild there with `python3 scripts/build_site.py --public-draft`, refresh `reader/` and `reader-manifest.json`, and run the public build. Do not manually mark pages reviewed. Legacy topics.html and library.html remain available.
