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

## Follow-up: bolder typography and neutral Numi background

The user requested stronger text, a better Numi background, and typography research
before implementation. Research and the resulting type roles are recorded in
`typography-notes.md`, with primary sources from Carbon, GOV.UK, and W3C.

Visual target: the existing alternate site, adjusted according to this request.
Baseline captures: `type-before-hero.png`, `type-before-work.png` (896 × 924), and
`type-before-approach.png` (1280 × 720). Final captures use the corresponding
`type-after-*.png` names and identical viewports. Same evidence directory as above.
`type-comparison-hero.png`, `type-comparison-work.png`, and
`type-comparison-approach.png` place baseline left and implementation right at
native screenshot resolution, with no cropping or density rescaling. The first
two comparisons are 1792 × 924; approach is 2560 × 720. State: menu closed,
homepage at top/work respectively, approach at top. These compare the requested
refinement, not pixel fidelity to the older light type.

Required surfaces reviewed:

- Typography: DM Sans retained, four weight roles, 700 display / 600 titles and
  actions / 500 labels and statements / 400 body. Body text 16–18px equivalent;
  checked rendered small text is at least 12px. Shared rem-based scale, tighter
  heading tracking, more generous paragraph leading, balanced headline phrases.
  Browser confirmed the 700 face loaded. Cursor keeps its approved 20px treatment.
- Rhythm: original section structure and project grid retained. Metadata wraps
  or stacks; mobile expertise uses one column to accommodate larger readable type.
- Colors: brighter muted text; Numi cover and showcase use a quiet pale stone
  background, allowing the interface colors to stand out. Other covers unchanged.
- Images: inspected the refined Numi cover at full resolution and in the grid.
  Three phones and real interface remain closely preserved, with minor generated
  screen-edge/food-image differences. Original cover retained. Built-in imagegen
  prompt saved alongside the refined asset.
- Copy: normalized visible text matches the previous commit on both pages.
  Project destinations, galleries, and hover annotations preserved.

Iteration findings:

1. [P2, fixed] At 320px the larger header label wrapped and the hero's second line
   broke awkwardly. Reduced compact-header padding and tuned the mobile display
   scale. Final `type-mobile-hero.png` shows complete controls and intended phrases.
2. [P2, fixed] Larger expertise headings risked overflowing the two narrow columns.
   Mobile now uses one column. `type-mobile-work-expertise.png` shows the final
   390px work section and 320px expertise section, including readable supporting text.
3. [P2, fixed] Isolated final words in mobile headline wrapping weakened the type
   rhythm. Balanced each headline phrase and grouped short endings without forcing
   unbreakable text. Recaptured home and approach mobile states.
4. [P2, fixed] Independent review found cursor.css overriding the shared Learn more
   text size. Removed that declaration; the element now inherits the new type role.

Mobile evidence: `type-mobile-hero.png`, `type-mobile-work-expertise.png`, and
`type-mobile-approach.png` show 390px and 320px frames within a 1280 × 720 capture.
Read-only measurements inside both page frames found document width equal to
viewport width, no section/header/footer horizontal overflow, and 12px minimum
checked rendered text. No physical-device or full 200% zoom audit claimed.

Focused typography is legible in the full-resolution heading and project-caption
comparisons; separate crops were unnecessary. Verified menu opening/closing,
View project cursor, font loading, and all 80 local references across both pages.
No browser errors or warnings. Formatting and git whitespace checks pass.

- [x] Research typography approaches before changes.
- [x] Refine both alternate pages and Numi color treatment.
- [x] Verify desktop and mobile rendering and correct found issues.
- [x] Preserve existing content and destinations.

No remaining P0/P1/P2 issues within this refinement scope.

final result: passed

## Follow-up: closer Turtle hover behavior

Scope, live-source observations, screenshots, three-step flow, and verification
limits are recorded in `hover-notes.md`. The approved output is the implemented
alternate site, supported by a scoped comparison report.

- [P2, fixed] Earlier 160px cursor obscured substantially more product UI than
  Turtle's live 80px CSS circle. Matched the 80px circle and retained 12px labels.
- [P2, fixed] Scrolling removed the old cursor until the mouse moved. Scroll now
  rechecks the element underneath the last mouse coordinates and updates mode.
- [P2, fixed] Exit visibility cut off fading. Opacity now handles entry/exit;
  keyboard, blur, viewport exit, media changes, and dialogs restore native cursor.
- [P2, fixed] Global hidden styling suppressed rolling-text duplicates during
  implementation. A scoped override restores them; accessible names stay singular.
- [P2, fixed] A white control cursor disappeared on white pill hovers. These pills
  now use a dark compact dot.

Verified the actual default/link/project/service states, 1.01 project zoom,
stationary-pointer scroll, keyboard focus, menu Enter/Escape, gallery Next/Escape,
and Approach navigation. Reviewed the final reference/implementation crop side
by side at native scale. Labels, circle geometry, contrast, and surrounding
product images are clear. Homepage 390/320px and Approach 320px captures show no
horizontal overflow or clipped header labels. Browser logs are clean. Syntax,
formatting, and git whitespace checks pass. Touch and reduced-motion fallbacks
were reviewed in code, without claiming a physical-device or OS-setting test.

The new 80px circle and 12px label intentionally supersede earlier notes referring
to the 160px/20px cursor. Existing bold typography and Numi color remain intact.
No remaining P0/P1/P2 issues within this hover refinement scope.

final result: passed

## Follow-up: rounded elements, individual details, and lime primary actions

The user requested more rounded elements and a more individual feel, then specified
`#B1FA1E` for primary actions. Kept the accepted layout, bold type, project covers,
and contextual hover behavior, while refining the existing shapes.

- Shared radii: 28px cards and 40px large panels; 20px/24px on narrow screens.
  Portraits repeat a larger bottom-right curve (96px desktop / 64px mobile).
- Rounded showcase, project images, navigation sheet, portrait/collage frames,
  contact-section top edge, and gallery. Product tabs now sit in a rounded tray.
- Small asymmetric number stamps and circular arrow backgrounds add repeated
  details without enclosing the text sections in additional cards.
- Primary buttons use exactly `#B1FA1E`, dark `#080808` text/arrows, and a lighter
  `#C2FF49` hover. Browser computed colors confirm both pages. Text contrast is
  approximately 15.8:1 normally and 16.9:1 on hover. Primary hover cursor is dark.
- Versioned the changed shared assets after preview caching retained old button
  colors; refreshed both pages and verified the new stylesheet URLs and colors.

Visual comparison: `rounded-comparison-hero.png` and
`rounded-comparison-work.png`, each 1792 × 924, show the baseline left and final
implementation right. Both source captures are 896 × 924, without cropping or
rescaling. Same hero/work anchors and closed menus. The hero includes the final
lime color; typography/content remain aligned. Project corners remove only the
background edges, preserving the composed screens. Compared both images together
and checked complete portrait framing in `rounded-about.png`,
`rounded-approach.png`, and `rounded-approach-mobile.png`.

Verification:

- [P2, fixed] Tablet navigation wrapped two labels at 701px. Fluid gaps and nowrap
  labels now keep every item on one line without menu or document overflow.
- [P2, fixed] Rounded showcase clipping could conceal link focus. The containing
  panel now displays the focus outline; verified with actual Shift+Tab navigation.
- Tab switching works by mouse and arrow keys; selected state and focus remain
  visible. At 320px the tray fits three 84px-wide, 44px-high buttons without clipping.
- Homepage checked at 320px and 701px; Approach artwork/contact checked at 390px.
  Document widths equal viewport widths. Full portrait, caption, product artwork,
  and contact action fit. Screenshots live alongside the comparisons above.
- Verified the lime hover color and dark compact cursor in the browser. Runtime
  logs are clean. Read-only review, JavaScript syntax, formatting, and whitespace
  checks pass. These checks do not constitute a full accessibility/device audit.

No remaining P0/P1/P2 issues within this rounded-shape and action-color scope.

final result: passed

## Follow-up: DraftKings Predictions neon green

The user replaced the prior hex preference with the neon green used by
[DraftKings Predictions](https://predictions.draftkings.com/en). Inspected the
live public header action: default computed background `rgb(177, 255, 20)`
(`#B1FF14`), hover `rgb(206, 255, 109)` (`#CEFF6D`). Source capture:
`neon-reference.png` in the existing evidence directory.

Updated shared primary-action tokens to those two colors and refreshed the
stylesheet version on both alternate pages. Browser checks confirm the homepage
and Approach actions render `#B1FF14`, and the homepage hover renders `#CEFF6D`.
Dark text, arrows, and the compact hover cursor remain visible. Text contrast
against `#080808` is 16.39:1 normally and 17.31:1 on hover. Final visual capture:
`neon-after-hero.png`. Layout and responsive rules were not changed in this pass.
Whitespace check passes; no remaining issues within this color-only scope.

final result: passed

## Follow-up: synchronize cached interaction assets

The user reported unchanged color and missing cursor/hover behavior, then confirmed
that refreshing resolved it. Inspection of their selected tab found the expected
`#B1FF14`, visible View project cursor, fine-pointer mode, 14 enhanced text links,
and no browser errors. The disappearance was not reproduced during inspection.

Found a cache-versioning hazard: newer versioned cursor JavaScript was paired with
unversioned cursor CSS; navigation JavaScript and text-hover CSS were also
unversioned. Updated all seven alternate CSS/JS references on each page to the same
fresh revision. This includes both coupled interaction pairs and the color styles.
No cursor behavior or color values changed. Both sets of local asset paths resolve,
and formatting/whitespace checks pass. The user confirmed the refreshed interaction
was working before this additional cache hardening.

final result: passed

## Follow-up: complete neon palette integration

Reviewed all 13 portfolio pages for first-party color drift. Shared
`dist/palette.css` now defines the canonical `#B1FF14` action, `#CEFF6D` hover,
dark foreground, theme-aware green text, soft fills, borders, focus and selection.
Both alternate pages and every linked Story, Resume, blog and case-study page
consume it. Final asset revision: `20260915-palette-2`.

1. Homepage and Approach — passed. Removed purple logo dots, selected tabs,
   number stamps, link states, focus rings and tinted interface surfaces. Arrows
   now mask the existing SVG with currentColor, so icons and labels respond
   together. Verified hero actions, selected tabs with arrow-key navigation,
   Approach current navigation, writing hover and mobile controls at 320px.
2. Linked pages — passed for palette scope. Story, Resume and all six blog pages
   share theme-aware accents. All three case studies use shared navigation,
   buttons, focus and footer links while retaining product branding, swatches
   and screenshots. Rendered Story and an article in light/dark modes, Resume,
   blog index, Numi, Tysha and Karta (including dark case controls).
3. Interaction and integration — passed. The approved white 80px project/story
   cursor remains visible; green pill hovers retain the dark compact cursor.
   Both alternate pages fit at 320px without document overflow. Browser logs
   contain no warnings/errors for the inspected pages. All 13 palette imports,
   73 local assets, arrow mask, 38 inline scripts, 16 JSON blocks and alternate
   JavaScript syntax were checked; no missing asset or token dependency found.

Fixed findings:

- [P2] Accent colors were scattered across independent declarations and older
  stylesheets; they now reference shared semantic tokens.
- [P2] White foreground on neon selection and skip links would be unreadable;
  shared dark foreground gives 16.39:1 contrast on the primary fill.
- [P2] Neon text/progress on light surfaces would be faint; theme-aware green
  text gives 5.80–6.83:1 on tested light surfaces, with dark-theme neon retained.
- [P2] The UX-for-ML article referenced a missing duplicate `/blog.css`; removed
  that import and retained its valid shared stylesheet.

Evidence in the existing turtle-alt evidence directory: `palette-before-hero.png`,
`palette-after-hero.png`, `palette-before-expertise.png`,
`palette-after-expertise.png`, `palette-showcase-focus.png`,
`palette-work-hover.png`, `palette-writing-hover.png`, `palette-approach.png`,
`palette-home-mobile.png`, `palette-approach-mobile.png`, `palette-story-light.png`,
`palette-story-dark.png`, `palette-resume.png`, `palette-blog.png`,
`palette-blog-article-light.png`, `palette-blog-article-dark.png`,
`palette-case-numi.png`, `palette-case-tysha.png`, `palette-case-karta-dark.png`.
Viewed the matched before/after expertise screenshots together at 1280×720:
layout and type are preserved, with clear green badges and matching arrows.

Some cached case markup initially showed the old controls; reload verified the
new HTML and computed neon values. Final coupled asset revisions are synchronized
again. Product imagery and case-study brand presentations intentionally retain
their original colors. Checks cover this palette change, not a full accessibility,
physical-device, print-output, or cross-browser audit.

final result: passed
