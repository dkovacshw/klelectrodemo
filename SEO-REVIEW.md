# Focused SEO review

The homepage stays concise. Existing service routes, design, logo, placeholders,
contact details and lightweight animations are preserved.

## Improvements

- References cards provide short factual descriptions and visible links to related services.
- The references hub uses CollectionPage schema, with its existing breadcrumbs.
- Service overview and reference card headings use H2 below the page H1.
- The standard-library Python generator is tracked alongside its source content.
- Demo and production builds have explicit indexing modes and automated checks.

## Project pages need genuine source material

No Teva or HELL project claims, external client links, dates, technical challenges,
or new case-study pages were added. Only the five existing reference captions
support the current cards; the live references page could not be fetched during
this review. The owner confirmed that further verified details are not yet available.

For a substantial future project, collect: approved client name, work performed,
location, date if known, equipment specifications, meaningful technical details,
and permission for photos and attribution. Publish a dedicated page only when
this supports useful content beyond a caption. Link it from the references hub,
then link relevant services and contact from the project page. Add its canonical,
breadcrumb and sitemap entry. Client backlinks must be genuinely arranged;
the website cannot create those by adding outgoing links.

## Deployment distinction

The repository root is the GitHub Pages demo and deliberately uses noindex.
Production output is generated separately with index/follow, including References.
Canonical and sitemap URLs identify klelectro.hu in both modes.
Do not deploy the demo root to the production domain.

## Performance and remaining checks

No new JavaScript, dependencies, fonts or remote embeds were added. Photos remain
Kép helye placeholders. Actual Core Web Vitals require measurements after hosting;
static checks and browser layout checks cannot establish field performance.
Verify redirects and response headers on production, then submit its sitemap.
