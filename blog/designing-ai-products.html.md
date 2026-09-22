Source: https://imdennie.com/blog/designing-ai-products.html

Updated: 2026-09-22

[All writing  ](https://imdennie.com/blog/) AI & design

# Designing AI products: 6 lessons from building an AI nutrition app

Dennie Ordynskyi · July 2026 · 7 min read

Classic software is deterministic: the user taps, the same thing happens, every time. AI products are different in a way that changes the design job at its root — **they're probabilistic.** Sometimes brilliant, sometimes wrong, always uncertain, never instant. Most of what we know about interface design quietly assumes none of those things.

I learned this the practical way, designing and building [Numi](https://getnumi.app) — an iOS app where you photograph your meal and AI estimates the calories, macros and micronutrients. A camera, a plate of food, and a model that is confidently almost-right many times a day: it's a perfect little laboratory for AI UX. Here are the six lessons I keep reusing.

## 1. Design for "almost right" as the normal case

A food photo is ambiguous. Is that yogurt or sour cream? 200g of rice or 300g? The model will commit to an answer either way. If your interface presents that answer as fact, every small miss erodes trust — and users don't tell you, they just leave.

In Numi, an analysis is a proposal, not a verdict: the breakdown appears as editable parts, and adjusting any of them is a one-tap interaction, not a buried edit screen. The pattern generalizes: **make the AI's output the starting point of a conversation the user can win in one move.** Correction isn't an error state — it's a primary flow, and it deserves primary-flow design attention.

## 2. Correction is also your data flywheel

When fixing the AI is effortless, users do it — and each fix tells the product something true. Numi builds what I call a "Metabolic Fingerprint": accumulated context that makes tomorrow's guidance more personal than today's. None of that works if corrections feel like filing a complaint. Design the correction loop first and the personalization gets built for free.

## 3. Latency is a design material now

Models take seconds, and seconds are an eternity in an interface. You can't remove the wait, so you have to spend it. The rules I follow:

- **Acknowledge instantly.** The tap must produce visible motion in under 100ms, even though the answer is seconds away.
- **Show meaningful progress, not a spinner.** Staged feedback ("reading the plate → identifying items → estimating portions") keeps trust alive and makes the intelligence legible.
- **Deliver value progressively.** If the food items appear before the micronutrients are ready, ship the items first. Something honest early beats everything late.

## 4. Never make the human feel stupid — or idle

The worst AI experiences do one of two things: they make the user feel interrogated by a machine ("was this helpful? rate 1–5!") or they reduce the user to a spectator. People don't want to operate an AI; they want to get on with their day with less friction. In Numi the entire interaction is: point camera, glance, maybe one adjustment, done. The AI is the plumbing, not the show. If your users spend their time managing the model instead of living their life, the design has failed no matter how good the model is.

## 5. Set the confidence, don't hide it

There's a temptation to present AI output with maximum confidence because it demos better. Resist it. There's an equal temptation to plaster percentages and disclaimers everywhere. Resist that too — numbers like "87% confident" mean nothing to a person holding a fork. The middle path is **calibrated presentation**: firm language and visual weight when the model is on solid ground, softer framing ("looks like…") and an inviting edit affordance when it isn't. Users learn the product's honesty within days, and honesty compounds.

## 6. The failure states are the product

Dark plate in a dim restaurant. A smoothie (opaque cup, mystery contents). A photo of a menu instead of food. Every AI product has these — inputs the model can't do much with. The lazy design punts ("Analysis failed, try again"). The good design has a plan: ask one clarifying question, offer graceful manual entry that respects the work already done, remember the correction for next time. When teams show me AI features, I look at the sad paths before anything else — that's where you can tell whether a designer thought about the model or just decorated it.

## A starter checklist for your first AI feature

**Before you ship, answer these:**

- What does the user see in the first 100ms after asking?
- What exactly happens when the model is wrong — and how many taps does the fix take?
- Does the language match the model's actual reliability, or the demo's?
- What are the three most common "bad inputs," and what's designed for each?
- Does a correction make the product better tomorrow?
- Could the user accomplish the task with less involvement in the AI, not more?

The meta-lesson after shipping one of these: AI is a new design material, the way touch was in 2008. It has grain, strengths and failure modes, and the designers who learn its texture firsthand — by building with it, not reading about it — are the ones who'll define the next decade of products. That story is here: [I shipped two iOS apps solo](https://imdennie.com/blog/shipping-apps-solo-with-ai.html).

Read next

[ Building in public · 8 min read

### I shipped two iOS apps solo — what AI changed about being a designer

Read the story →  ](https://imdennie.com/blog/shipping-apps-solo-with-ai.html) [ Careers in design · 9 min read

### How to become a product designer in 2026 — advice from 14 years in

Read the guide →  ](https://imdennie.com/blog/how-to-become-a-product-designer.html)

**Dennie Ordynskyi** is a product designer with 14+ years of experience, currently designing large-scale consumer products at DraftKings. He's also the founder and designer of [Numi](https://getnumi.app) (AI nutrition) and [Tysha](https://apps.apple.com/us/app/tysha-baby-sleep-sounds/id6783016339) (baby sleep) on the App Store. More at [imdennie.com](https://imdennie.com/) · [LinkedIn](https://www.linkedin.com/in/dennieo/).
