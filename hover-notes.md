# Turtle-inspired hover refinement

The requested follow-up focuses on the mouse behavior of [Turtle Design](https://turtle.design/), adapted to the existing alternate homepage and approach page. The heavier typography and neutral Numi cover from the preceding round remain the visual baseline.

## Reference and implementation

Inspected the live homepage's default cursor, buttons, services, and project images on 14 September 2026. Source behavior was checked against the rendered styles and the site's cursor/project/service scripts.

| Interaction               | Live reference                          | Implemented treatment                                           |
| ------------------------- | --------------------------------------- | --------------------------------------------------------------- |
| Normal movement           | 32px ring, 8px immediate dot            | Same sizes, smoothly following ring                             |
| Links and buttons         | 16px solid dot                          | Same size; dark on pills that turn white                        |
| Project and service hover | 80px white circle, 10px uppercase label | 80px circle, 12px label for readability                         |
| Cursor transition         | 180ms default, 280ms circle growth      | Same timings, 200ms label crossfade and 90ms entry delay        |
| Project image             | 1.01 scale, 200ms transition            | Same scale and timing                                           |
| Navigation and CTA text   | Vertical text swap around 300ms         | 300ms text swap; decorative duplicate hidden from accessibility |
| Service feedback          | Expanding service row and arrow travel  | 12px arrow travel within our existing text-rich grid            |

The reference's 80px CSS circle supersedes the previous 160px interpretation of the supplied screenshots. The circle now reveals more of each product cover. We kept our project compositions, content, type system, and service layout.

## Captured flow and findings

1. **Move across a project cover.** The prior circle was twice the reference's CSS size. Reduced it to 80px, crossfaded contextual labels, and reduced image zoom. Comparison below shows Turtle on the left and the implementation on the right, both at native pixel scale.

   ![Turtle and portfolio project cursor comparison](/Users/dennie/.codex/visualizations/2026/09/14/01a0a148-7bf3-7513-9c14-683e50bdf772/turtle-alt/hover2-comparison-project.png)

2. **Move to a service or ordinary link.** Services show Learn more; ordinary controls use a compact dot and static links roll their text. Fixed a conflict with the global hidden rule that initially concealed the duplicate. Fixed insufficient cursor contrast over white buttons.

   ![Learn more service cursor](/Users/dennie/.codex/visualizations/2026/09/14/01a0a148-7bf3-7513-9c14-683e50bdf772/turtle-alt/hover2-after-service.png)

3. **Scroll, switch to the keyboard, and open a gallery.** The cursor now hit-tests the stationary mouse position on scroll. Tab restores the native cursor and visible focus. Menu Enter/Escape and gallery Next/Escape work. Open dialogs retain native cursor handling.

   ![Visible keyboard focus with decorative cursor suspended](/Users/dennie/.codex/visualizations/2026/09/14/01a0a148-7bf3-7513-9c14-683e50bdf772/turtle-alt/hover2-keyboard.png)

## Verification and limits

- Browser checked default, link, project, and service states; stationary-pointer scroll; keyboard focus; menu opening/closing; Linc gallery navigation and dismissal; and navigation to Approach.
- Homepage checked at 390px and 320px; Approach at 320px. Document and header widths equal the viewport width. Header labels remain readable and unclipped.
- Browser console reported no errors or warnings. JavaScript syntax, formatting, and git whitespace checks pass.
- Cursor decorations are aria-hidden. Original link text and destinations remain intact; duplicated visual text is aria-hidden. Touch/coarse-pointer rules keep the native interface, and reduced-motion rules remove following lag, text animation, and image zoom.
- Touch and reduced-motion handling were reviewed in code; no physical touch-device or OS preference test was performed. Screenshots alone do not establish animation quality or comprehensive accessibility conformance.

Evidence files live beside the images linked above. The 640×240 comparison uses reference crop (260,98)–(580,338) and implementation crop (82,339)–(402,579), with no rescaling. Full captures are `hover2-reference-project.png`, `hover2-reference-service.png`, `hover2-before-project.png`, and `hover2-after-*.png`. Narrow-screen captures are `hover2-mobile390.png`, `hover2-mobile320.png`, and `hover2-approach320.png`.
