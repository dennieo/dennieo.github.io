# Turtle-inspired alternate homepage

Branch: `codex/turtle-inspired-alt`, based on `master`.
Preview: `python3 -m http.server 4173 --bind 127.0.0.1` from the repository root.
Scope: alternate homepage using existing portfolio content, images, case studies, and static hosting. No deployment or remote push.

## Visual evidence

Source: https://turtle.design/ (homepage). Its headline and reel change over time.
Evidence directory: `/Users/dennie/.codex/visualizations/2026/09/14/01a0a148-7bf3-7513-9c14-683e50bdf772/turtle-alt/`

- Source visual truth: `reference.png`, 390 × 844 pixels.
- Implementation: `alternate.png`, desktop viewport 896 × 924 pixels.
- Mobile implementation: `mobile.png`, a 390 × 844 CSS-pixel iframe inside the browser capture.
- Normalized side-by-side comparison: `comparison.png`, 780 × 844 pixels; source left, implementation right. Mobile implementation cropped from (253,20) to (643,864), removing only the surrounding test harness. Both content captures are 390 × 844, at 1 image pixel per CSS pixel.
- State: homepage at top, default Numi showcase, menu closed. Source animation frame differs because the reference cycles through projects.

## Findings and comparison history

1. [P2, fixed] Tysha showcase inherited the Numi montage offset, clipping the second promotional image. Removed that offset for Tysha, used contained images, and recaptured the showcase. Both complete promotional images now fit the panel.
2. [P2, fixed] Hiding the mobile showcase line break joined words ("logging.More"). Restored the break. Final mobile capture and normalized comparison show the corrected two-line headline.
3. No remaining P0/P1/P2 findings within this alternate-design scope.

## Required fidelity surfaces

- Typography: DM Sans supplies the same restrained, rounded grotesque direction without copying the reference's proprietary typeface. Large regular-weight headings, tight tracking, muted supporting copy. Mobile headline fits at 320 and 390 pixels.
- Spacing: generous black space, simple header, pill buttons, large product imagery, thin section rules. The paired 390-pixel captures confirm the shared hierarchy. The alternate intentionally adds a portfolio introduction and colored product showcase; it is an adaptation, not a pixel clone.
- Colors: near-black base, white foreground, muted gray text, vivid blue primary actions. Project colors come from the user's own product assets.
- Images: existing Numi, Tysha, Karta, Linc, and portrait artwork. No copied Turtle logos or project artwork. Numi montage intentionally clips at panel edges; complete source images are available in case studies. Tysha promotional images retain their embedded text.
- Content: personal portfolio language replaces agency messaging. Existing project names, experience, recommendation excerpt, contact destination, blog routes, resume, and case-study routes retained. Secondary pages keep their existing designs.
- Focused checks: inspected the project grid, Tysha image containment, menu, gallery, and mobile headline/showcase text at readable scale in browser captures.

## Interaction and technical verification

- Menu open/close, anchor navigation, and focus transfer verified.
- Numi/Tysha/Karta showcase changes verified; keyboard Home navigation returns to Numi.
- All five project galleries open. Next, Previous wrapping, and Escape dismissal verified; native dialog handles focus containment and the script restores trigger focus.
- Numi case-study link opened the existing case study successfully; browser back returns to the homepage.
- Email CTA remains a mailto link. No message was sent.
- Mobile layout verified in 390- and 320-pixel frames; document width equals viewport width at both sizes.
- Desktop preview checked at 896 pixels. Browser viewport overrides were unreliable, so no claim is made about a separate 1440-pixel visual pass or physical-device testing.
- All 61 static href/src references checked for missing local assets, routes, and anchors: no errors.
- JavaScript syntax check and git whitespace check passed. Files formatted with Prettier 3.6.2.
- Browser console checked: no errors or warnings observed.
- Reduced-motion CSS disables transitions and smooth scrolling; not separately emulated in-browser.

## Implementation checklist

- [x] Create alternate branch.
- [x] Build responsive homepage and retain existing destinations.
- [x] Verify visual direction and fix cropping/wrapping issues.
- [x] Verify primary navigation and gallery interactions.
- [x] Keep local preview available for review.

final result: passed

## Follow-up: My approach page

Added `approach.html` after the user's “See our approach” reference. The homepage hero now links to it with “See my approach”; the main menu includes Approach. Shared navigation and year behavior moved into `navigation.js`, preserving the homepage showcase/gallery script.

Source: https://turtle.design/approach. Same evidence directory as above:
- `approach-reference.png` and `approach-desktop.png`: 1280 × 720 screenshots, both at the top of the page, menu closed.
- `approach-comparison.png`: 2560 × 720 side-by-side comparison, reference left and implementation right, no density scaling before compositing.
- `approach-mobile.png`: 390-pixel mobile iframe within the browser screenshot.

Visual assessment: shared black canvas, light grotesque type, generous spacing, thin divider, and split imagery/text layout. Dennie's wordmark, navigation, real portrait and Linc artwork, factual personal copy, and larger opening type intentionally adapt the source for a personal portfolio. The page keeps the existing alternate design's colors and font. No Turtle branding or team photographs were reused.

Focused checks: inspected split artwork and paragraph scale in-browser. Fixed a mobile sentence-joining issue by retaining heading line breaks. Moved the portrait caption to the top so the overlapping product image no longer covers it; recapture shows the complete caption. No remaining P0/P1/P2 issues in the scoped adaptation.

Verified approach menu → homepage work, homepage showcase switching after extracting shared navigation, homepage “See my approach” → new page, all 99 combined static references across both pages, JS syntax, and whitespace. Browser console had no errors/warnings. Mobile visually inspected at 390 pixels. A second read-only review found no further navigation, local-link, or factual-copy issues. No deployment.

final result: passed

## Follow-up: contextual hover cursor

User clarified that the reference is Turtle's mouse-over behavior, supplying screenshots of the circular LEARN MORE and VIEW PROJECT cursors. Added the matching interactive treatment to the existing alternate branch.

- Cursor: 160-pixel white circle, 20-pixel black uppercase text, two lines, centered on the pointer. Smooth position interpolation and scale-in; reduced motion follows immediately without transitions.
- Targets: project images/showcase/approach project cards → View project; Linc/archive buttons → View gallery; expertise links → Learn more; writing rows → Read story. Header links, small buttons, and product tabs keep conventional pointers.
- Existing project CTA pills disappear only while their target has the custom pointer. They return on mouse exit or keyboard use. Expertise regions are real links with persistent Learn more labels.
- Enhancement is aria-hidden, pointer-events:none, and requires a fine hover-capable mouse. Touch/pen pointers and keyboard navigation keep native behavior. Reviewed media/pointer guards; no physical touch-device test claimed.
- Browser verified View project, Learn more, View gallery; position tracking (target x=360, cursor x=359.848 after settling); target exit; Tab cleanup; gallery opening cleanup; Escape dismissal and restored gallery-trigger focus. No console errors or warnings observed. Source review found no additional actionable issues.
- Source screenshots: user attachments `Screenshot 2026-09-14 at 22.00.40.png` and `Screenshot 2026-09-14 at 22.00.47.png`.
- Evidence in the directory above: `hover-learn-more.png` and `hover-view-project.png` (896 × 924 browser captures); `hover-comparison.png` (400 × 400, source left/implementation right). The paired comparison uses 200 × 200 crops around the 160-pixel circles, without resizing. It verifies circle size, fill, typography, line break, and overlay placement; background portfolio content intentionally differs.
- No remaining P0/P1/P2 issues. JavaScript syntax, whitespace, and interactive target annotations checked.

final result: passed

## Follow-up: composed project covers

Created four 1536 × 1024 presentation covers from the existing Numi, Tysha, Karta,
and Linc screens using built-in Image Generation. Exact prompts and source lists
are in `dist/img/covers/README.md`. WebP encoding totals 491,456 bytes. Original
screens remain in their project folders and case studies; generated small text,
icons, and chart details may differ slightly, so these covers serve as presentation
mockups rather than exact UI records.

Visual source: the user's `Screenshot 2026-09-14 at 22.01.21.png` from Turtle.
Karta most closely follows its large desktop upper-right and three mobile panels
across the lower-left. Numi and Tysha use layered phones; Linc uses two desktop
windows. Product-specific colors, light, and shadows unify the covers. No reference
product content or external text/cursor/toast is included in the generated assets.

- All four covers were inspected at full resolution and in the project grid.
- Replaced the old CSS collages with contained 3:2 images. Both rows keep complete
  screen compositions within the cards, with a small hover zoom and live cursor.
- Desktop browser inspection at 896 pixels; mobile inspection in 390- and
  320-pixel frames. No clipping or horizontal overflow observed visually.
- Verified the View project cursor over Numi and Karta, Karta case-study navigation,
  Linc gallery opening/dismissal, loaded assets, and gallery cursor cleanup.
- 53 local homepage references resolve. Git whitespace check and formatting pass.
  No browser errors or warnings observed. Read-only review confirmed preserved
  destinations and interactions; corrected the asset notes' reference attribution.
- Evidence in the same directory: `covers-desktop-hover.png`,
  `covers-desktop-second-row.png`, `covers-karta-hover.png`, `covers-mobile.png`,
  and `covers-mobile-second-row.png`.
- `covers-comparison.png`: 1440 × 500, supplied reference left, final Karta cover
  right. Reference crop (58,35)–(1722,1191) removes the webpage border; each image
  is proportionally reduced to fit a 720 × 500 panel with black letterboxing.
  The supplied cursor/toast remains visible only in the reference for context.
  Comparison checks composition, relative screen scale, spacing, colors, shadows,
  and device framing. Different product UI and 3:2 framing are intentional.

No remaining P0/P1/P2 issues within this cover-presentation scope.

final result: passed
