# Typography refinement

The direction is a bold, editorial portfolio with clear supporting information.
Keep DM Sans and the existing black canvas; give the hierarchy more contrast and
make small text easier to read. The specific sizes below are design decisions for
this portfolio, not accessibility thresholds or a copied design-system scale.

## Research applied

- [Carbon: style strategies](https://carbondesignsystem.com/elements/typography/style-strategies/)
  distinguishes expressive reading/exploration from compact task controls. Apply
  that distinction here with prominent headings, quieter navigation and clear
  project metadata. Keep each role consistent throughout the site.
- [GOV.UK: type scale](https://design-system.service.gov.uk/styles/type-scale/)
  combines size and leading into a consistent rhythm, uses relative units, and
  avoids shrinking mobile text excessively. This informed the shared rem-based
  scale and removal of the previous 9–10px mobile labels.
- [GOV.UK: bold text](https://design-system.service.gov.uk/styles/font-override-classes/)
  recommends selective emphasis. The new headings are bold while paragraphs
  remain regular, so emphasis still communicates hierarchy.
- [W3C: Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)
  describes resizing without losing content or functionality. Relative font
  sizes, wrapping metadata, and responsive columns support that goal. This pass
  checks responsive layout; it does not claim a complete WCAG conformance audit.

## Shared roles

Implemented in `dist/turtle-alt/typography.css` on the homepage and approach page.
The existing hover cursor retains its reference-specific 20px/160px treatment.

| Role                            | Weight | Sizing and rhythm                                                            |
| ------------------------------- | ------ | ---------------------------------------------------------------------------- |
| Hero, section, contact headings | 700    | Fluid size with rem bounds, 1.02–1.08 leading, tightly tracked               |
| Project and article titles      | 600    | 22–36px equivalent depending on role, 1.15–1.25 leading                      |
| Navigation and calls to action  | 600    | 14px equivalent; compact controls 12px on mobile                             |
| Labels and metadata             | 500    | 12–14px equivalent, 1.5 leading; tracking only on uppercase labels           |
| Paragraphs                      | 400    | 16px equivalent; 18px about-section copy on larger screens, 1.6–1.65 leading |
| Quotes and approach statements  | 500    | 24–50px equivalent depending on role, looser leading than headings           |

Project metadata stacks on smaller screens. Expertise entries use one column on
mobile so the larger type has enough room. Headline wrapping and compact header
spacing are tuned at 320px as well as 390px. Existing words and destinations remain.

## Numi color treatment

Replaced the plum/raspberry cover background with pale cool stone and neutral
shadows. The existing phone composition and interface supply the color. The Numi
hero showcase uses a coordinating `#e3e8e4` background. The refined cover was made
with built-in Image Generation; its [edit prompt](dist/img/covers/numi-cover-refined-prompt.txt)
and [asset](dist/img/covers/numi-cover-refined.webp) are retained alongside the original.
