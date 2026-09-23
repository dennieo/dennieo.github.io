# Open Studio homepage — current design QA

Date: 2026-09-19. User selected the first displayed design mockup.

## Visual evidence

Source visual truth: `/Users/dennie/.codex/generated_images/01a0bb1c-eb48-73c1-a948-9fd9a150df8a/exec-0430f4c0-2fee-4842-95ab-4dc9c26a81fa.png` (1003 × 1568).

Evidence root: `/Users/dennie/.codex/visualizations/2026/09/19/01a0bb1c-eb48-73c1-a948-9fd9a150df8a/open-studio/`.

- Implementation: `desktop-final.png`, 1003 × 1300 pixels, matching 1003 × 1300 CSS viewport, devicePixelRatio 1, homepage at top, light theme, gallery closed.
- Combined comparison: `comparison-final.png`, source left and implementation right. Both cropped to the same top 1003 × 1300 region; no density scaling or stretching.
- Focused typography comparison: `typography-comparison.png`, matching y210–610 crops from the combined image. Hero copy, line breaks, weights and primary link are readable at native size.
- Mobile: `mobile.png`, 390 × 844; `mobile-320.png`, 320 × 800. Same homepage state.
- Wide desktop: visually inspected at 1440 × 900; no overflow.
- An initial comparison mistakenly stretched a viewport capture vertically, and a full-page browser capture rendered at an inconsistent scale. Both were rejected as fidelity evidence. The final comparison uses the native-size viewport capture and equal crops only.

## Findings and comparison history

- [P2, fixed] At 320px, the hero broke into three lines with “build” isolated. Added a 32px headline size below 360px; `mobile-320.png` confirms two complete lines with no overflow.
- Increased the muted metadata contrast from #717987 to #697380 before final capture.
- No remaining actionable P0/P1/P2 findings in this homepage scope.

## Required fidelity surfaces

- Typography: DM Sans, bold tight-tracked two-line hero, quieter supporting paragraph, direct navigation, medium-weight section and project headings. Hero scale, line wrapping and hierarchy closely match the selected design; small differences in the raster mock’s letterforms are expected.
- Layout: white page, 5.4vw gutters, airy introduction, thin facts divider, open two-column work grid, square image corners and simple underlined links. Mobile uses a single-column grid and visible navigation. Karta and Linc continue the grid below Numi and Tysha, retaining existing work before About; this extends the short concept intentionally.
- Colors: #ffffff background, #101b1e headings, #505862 body and #697380 metadata. Product artwork retains its own colors. No surrounding dark surface or neon controls.
- Assets: the initial implementation reused existing covers. The subsequent artwork refresh below supersedes those covers with four new coordinated compositions based on actual product screens. Arrows reuse the existing source asset.
- Content: selected intro and first project captions match the concept. About and contact copy are shorter and factual. All original case-study destinations, five project galleries, story, approach, resume and writing remain reachable. Secondary pages were originally left unchanged; the site-wide extension below now supersedes that scope.

## Functional verification

- Browser: Work anchor, Numi case-study navigation and return to homepage.
- All five galleries opened: Linc, MyGoTrainer, Shipshape, Chatbox, E-commerce. Next and Previous wrap, Escape closes, and focus returns to the triggering button.
- Contact anchor reveals the correct mailto action. No email sent.
- Mobile at 320 and 390px and desktop at 1003 and 1440px have document width equal to viewport width.
- Homepage browser console: no errors or warnings observed.
- 36 static homepage references and anchor targets plus all 20 gallery image files checked: no missing targets.
- JavaScript syntax and git whitespace checks passed.
- Focus styles, native dialog semantics, reduced-motion behavior and semantic navigation are present. No physical-device or full assistive-technology audit claimed.

## Implementation checklist

- [x] Implement the selected visual direction in the existing static site.
- [x] Preserve existing project and secondary-page destinations.
- [x] Compare native-size source and implementation captures.
- [x] Fix narrow-screen wrapping and recheck.
- [x] Check navigation, galleries, assets and console.
- [x] Keep local preview available. No publishing or remote push.

Earlier design history is preserved in `design-qa-turtle-history.md`.

## Artwork refresh — 2026-09-19

- Replaced all four featured homepage covers: Numi, Tysha, Karta, and Linc. Numi and Tysha screenshots came from their public websites; Karta from its public demo dashboard and guest menu. Linc uses existing original project screens because no current public URL was supplied.
- Source images, exact generation prompts, and provenance are in `dist/img/covers/open-studio/`. These are image-generated presentation compositions; fine text and icons can differ from source screens. Original galleries remain unchanged.
- All four production WebP files are 1340 × 1174, totaling 423,118 bytes. The responsive containers use `object-fit: contain`, preserving the full composition at desktop and mobile sizes.
- Evidence in the same evidence root: `artwork-desktop-row1.png` and `artwork-desktop-row2.png` at 1280 × 720, plus `artwork-mobile.png` at 390 × 844. Inspected all desktop covers and mobile Karta/Linc; all four mobile images loaded at 342 × 299 with no horizontal overflow.
- `artwork-comparison.png` compares the new Numi source at its rendered size (left) with the actual browser crop (right), 559 × 489 each. Source is reduced proportionally to presentation size; no vertical stretching.
- No console errors or warnings observed. Linc gallery opens, Escape closes, and focus returns to the cover. Destinations and gallery scripts are unchanged.
- No remaining actionable P0/P1/P2 findings for this artwork scope. No publishing or remote push.

## All remaining pages — 2026-09-19

Scope: three case studies (Numi, Tysha, Karta), story, approach, resume, writing index, and all five articles. The search-verification HTML file remains untouched.

### Visual target and evidence

The user approved the Open Studio homepage and its new project artwork, then requested the same design across the remaining pages. The approved homepage is the visual-system reference; these pages adapt its typography, white background, ink colors, generous spacing, thin rules, and open layouts to their own content.

Evidence directory: `/Users/dennie/.codex/visualizations/2026/09/19/01a0bb1c-eb48-73c1-a948-9fd9a150df8a/open-studio/pages/`.

- All 12 page tops captured at 1280 × 720 and 390 × 844, in filenames ending `-desktop.png` and `-mobile.png`.
- All desktop and mobile captures visually inspected, including the five articles.
- `home-and-approach-comparison.png`: approved homepage left, approach page right, matching 1280 × 720 viewports at page top; no scaling or stretching. Shared header, typography, and spacing reviewed against the reference.
- `case-detail-desktop.png` and `resume-detail-desktop.png` cover longer content layouts. Story chapters were also inspected after using the intro anchor.
- Case-study covers reuse the approved generated artwork. Detailed product screenshots, portrait artwork, and article illustrations retain their originals.

### Findings and fixes

- Fixed the Tysha mobile title breaking at the hyphen in “half-asleep”; recaptured `case-tysha-mobile.png` confirms the phrase remains together.
- Replaced the story's scroll-dependent text reveal with static, accessible chapter headings. Updated its metadata to reflect the new presentation.
- Standardized the newest essay's previously separate template to the same article typography and breadcrumb treatment.
- Removed obsolete theme, cursor, parallax, and menu scripts from these pages rather than leaving controls tied to missing elements. Shared navigation is visible at every tested width.
- No remaining actionable P0/P1/P2 visual findings in this scope.

### Verification

- Every page loaded at 1280px, 390px, and 320px, with document width equal to viewport width. All headings remained visible; no reveal-related hidden content.
- Existing article and case-study paragraphs retained; story framing copy and presentation labels updated. Resume gained a visible section label.
- HTML nesting, unique IDs, and 214 local file/anchor references checked with no failures.
- Clicked through story chapters, the case-study reading anchor, Tysha → Karta, footer → writing index, writing index → article → all writing, and writing → resume.
- Resume Save as PDF action still calls native printing and has a dedicated print stylesheet. The button was invoked without a console error; a saved PDF and physical print output were not inspected.
- Browser console showed no errors or warnings. Shared JavaScript syntax and git whitespace checks passed.
- Preview remains local. No deployment, commit, or remote push.

final result: passed

## Numi simulator artwork refresh — 2026-09-23

- Replaced all four decision-section images with current Numi simulator captures generated from the app’s built-in three-month demo seed: 88 days of history, mock meals and photos, weight trend, hydration, fasting state, and nutrition insights.
- The four production WebP files are 660 × 1434 and total 205 KB. They preserve the simulator aspect ratio and render without a decorative image background.
- Updated the Logging, Home, and Insights copy and alt text to describe the current released interface shown in each capture.
- Regenerated the Numi Markdown mirror and combined LLM document; updated the discovery sync and validation scripts for the new image names and stylesheet cache key.
- Verified the decision layout in the local browser, including the meal-history, Home, and Progress rows. Discovery checks and git whitespace checks pass.
- Full-resolution source captures are stored in `numi-simulator-refresh/` under the task’s visual evidence directory.

final result: passed

## Numi image-section repair — 2026-09-22

- Audited the live case study and found three screenshots attached to the wrong decision labels: the weekly report appeared under Logging, the fasting/home screen appeared under Insights, and the meal analysis appeared under Fasting.
- Corrected the sequence to meal analysis → Home → weekly report → fasting state, matching each screenshot to its section copy and alt text.
- Restored alternating desktop image placement and reserved the full phone-image dimensions before lazy loading. This removes the collapsed image rows and the resulting page jumps while keeping the transparent, background-free presentation.
- Verified all four image files load at their native 490 × 1000 dimensions. Desktop rows render at 255 × 520; mobile rows reserve 216 × 440 with no horizontal overflow.
- Evidence and the accepted before/after comparison are stored in `numi-image-audit/` under the task’s visual evidence directory.

final result: passed

## Discovery and release QA — 2026-09-22

- Extended the approved visual system to the sixth article that was already present on the live site, preserving its full article text and publication date.
- Added unique descriptions, canonical URLs, Open Graph and X card metadata, one consistent favicon, and linked structured data for all 14 public pages.
- Added page-specific social images, Markdown alternatives for every page, `llms.txt`, combined `llms-full.txt`, and a 14-URL sitemap. Numi is consistently described as released on the App Store.
- Added `scripts/sync-discovery.py` so discovery files can be regenerated from the public HTML, plus `scripts/check-discovery.py` for repeatable validation.
- Verified 256 local links and anchors with no missing targets. Structured data parses on all pages, discovery validation passes, and git reports no whitespace errors.
- Browser QA passed on the homepage, the newest article, and the Numi case study at 390px: meaningful content rendered, no horizontal overflow or framework overlay appeared, and no console warnings or errors were observed.

final result: passed
