Source: https://imdennie.com/blog/ux-for-machine-learning-the-interface-is-a-measuring-device.html

Updated: 2026-09-22

[All writing  ](https://imdennie.com/blog/)

Design & ML

# UX for machine learning: the interface is a measuring device

Dennie Ordynskyi · September 2026 · 8 min read

UX for machine learning differs from ordinary product UX in one specific way: every screen you build is simultaneously a control surface and a measuring device. Deterministic software takes input and returns the same output forever. An ML feature returns a guess, and whatever your interface makes easy to inspect and cheap to fix becomes the only part of that guess you ever get feedback on. So the layout is not just how the model is presented. It is what the model will learn about next, and what it will stay blind to.

That is the whole discipline compressed into a sentence. The rest of this piece is what it actually costs in practice, using decisions from features I have shipped and kept running.

## UX for machine learning has three time horizons, not one

Most design writing about ML covers a single inference: input goes in, prediction comes out, how do we show it. That is the easy third. A deployed ML product operates on three clocks at once, and they conflict.

- **Seconds.** One inference. Latency, loading state, how the result is framed when it lands.
- **The session.** The person disagrees with something and either fixes it or abandons the flow. This is where trust is won or lost, and it is the part with the least design attention in most products.
- **Months.** The model is now shaped by your correction UI. Personalisation, drift, and the slow question of whether the feature is still being used at all.

Design each screen for the clock it actually lives on. A loading animation is a seconds problem. A confirm-or-fix control is a session problem. Whether the thing degrades quietly over half a year is a months problem, and no amount of polish on the first two will save you from it.

## Checkability bias: the interface decides your training set

Here is the pattern I would most like other people to name and use, because it cost me the most to notice.

**Checkability bias:** a machine learning product only receives corrections for outputs the interface renders checkable. Everything else is silently accepted, so it looks correct in your data whether it is or not.

Numi analyses a photo of a meal and returns a breakdown: what the food is, roughly how much of it, and the nutrition that follows. Two things in that output have completely different feedback profiles.

Portion size is checkable. The person is holding the plate. If the model says one egg and there were two, they know, they can see the field, and fixing it takes a tap. Corrections arrive constantly.

Micronutrients are not checkable. Nobody looks at a potassium figure and thinks "that's off by fifteen percent." There is no ground truth in the room. So corrections on those fields arrive at approximately zero, forever, no matter how wrong they are.

If you read the correction logs naively, you conclude the model is weakest exactly where the interface is strongest at exposing it. That is backwards, and it is a trap that scales: the fields you designed well look worst, and the fields nobody can verify look flawless. Any prioritisation done off that data drifts toward polishing what is already visible.

The practical consequence: before you ship an ML surface, list every field and mark which ones the user can actually verify. That list is your real feedback surface. Treat the rest as unmeasured, not as accurate.

## Only ask for confirmation where the user holds ground truth

The obvious response to uncertainty is to ask. Put a confirm control on everything, let the person be the arbiter, ship it. This makes products worse, and it took me a while to work out why.

A confirmation control is a claim about the user. It says: you know this better than the model does. When that is true, the interaction is respectful and fast. When it is false, you have handed someone a decision they have no basis for making, and they feel it immediately. Asking a person to confirm a micronutrient estimate does three bad things at once: it produces noise instead of signal, it teaches them nothing, and it makes the fields they could verify feel just as arbitrary as the ones they cannot.

So the test I use now, before adding any confirm-or-fix affordance:

- **Does the person have ground truth the model lacks?** If yes, confirmation is the right control and should be one tap.
- **Is it derived from something they do have ground truth on?** Then let them fix the upstream value and recompute. Do not make them edit the derivative.
- **Neither?** Show it as an estimate with its inputs visible, and do not ask. A number nobody can check should never wear a checkbox.

Correcting a portion in Numi recalculates everything downstream from it. That is one edit against ground truth the person definitely has, and it moves the whole panel. The alternative, a form of twelve editable nutrition fields, would be technically more flexible and practically dead.

The claim behind all this, stated plainly so it can be argued with: **a model's output is a proposal, not a verdict.** An interface that renders a prediction as fact turns every near-miss into damage the person cannot see. Rendering it as something you confirm or fix makes being wrong a normal, expected part of the interaction rather than an error state, and that difference is load-bearing. The correction path is the most important screen in an ML product and reliably the least designed one.

## You cannot fake instant, so design the wait to show understanding

Vision analysis takes seconds. No engineering effort removes that; you can shave it, you cannot eliminate it. What is fully under design control is what those seconds communicate.

A single indeterminate spinner says: something is happening, possibly nothing, please wait. Staged progress that names what is being worked out says: this is being understood, in this order, and here is how far it has got. Same duration. Very different read on competence.

The generalisation is worth keeping: perceived competence during latency is an interface decision, not a model property. Two products on the identical model, with identical response times, will be judged differently on how good the model is, purely on how the wait was staged. If your ML feature is slow and you have exhausted the engineering, the remaining work is not performance work. It is copy and sequencing.

## When the user has to act on a number, explainable beats accurate

This is the trade I would defend hardest, because it looks like settling for less.

Numi's health score is deterministic. Stated inputs, fixed rules, same meal in gives the same number out. A language model could almost certainly produce a more nuanced score. I did not use one, and the reason is not accuracy.

A score a model produced cannot be checked, argued with, or learned from. When a person sees it drop and asks why, the honest answer is a shrug. There is no lever. A deterministic score with visible inputs can be interrogated: it went down because of this, so here is what to change. That is the property that keeps a number in use after the novelty has worn off.

So the rule: **if the user is expected to act on a number, the number needs a mechanism they can inspect.** Accuracy without explicability is fine for ranking, retrieval, and anything happening behind the scenes. It fails the moment you ask someone to change their behaviour because of it.

## Silence is a state, and almost nobody builds it

Generic output is a trust leak. "Great choice!" reads as machinery rather than attention, and one obviously canned line contaminates the credible ones around it. Users are extremely good at spotting the template, and once they have spotted one, they discount all of them.

The rule I hold to: an insight either cites something real about this person today, what they ate, what is left, what changed this week, or it does not render at all. No fallback string. No encouraging filler when there is nothing to say.

Which means the empty state is a designed feature, not a gap. Here is the falsifiable version: **if your ML feature has no condition under which it renders nothing, it will be ignored within weeks of daily use.** Something that always speaks is something the eye learns to skip. Something that speaks only when it has a reason gets read.

## Autonomy is a ladder: detect, suggest, act

The last structural decision. There are three separable capabilities, and products routinely collapse them into one.

- **Detect.** Notice a pattern and say so. "Your intake has been flat for two weeks."
- **Suggest.** Propose a specific change, with the reason attached, and wait.
- **Act.** Make the change and report it afterwards.

Numi keeps these separate on purpose. An app that silently rewrites your targets has taken a decision you can neither see nor contest, and when you eventually notice, you cannot tell which of your numbers were yours. Detection is nearly free in trust terms. Action is expensive and has to be earned.

Earned how: one confirmed suggestion at a time, visibly. A system that has proposed twenty things and been accepted nineteen times has a case for acting unprompted on the twentieth kind of thing. A system that acts on day one has no case and no recovery. The agent tooling of the last two years is rediscovering this as "progressive delegation", and the shipped lesson has not changed: the rung is granted by the user, not claimed by the product.

## What I would measure instead of accuracy

Model accuracy is an engineering metric. It tells you very little about whether the interface around the model is working. Three things I find more informative:

- **Correction rate per field.** Not aggregate. Per field, read against the checkability list from earlier. A field with zero corrections is either perfect or unverifiable, and you need to know which.
- **Corrections per session over time, with session count flat.** Falling corrections against steady usage suggests the model is genuinely fitting the person. Falling corrections against falling usage means people gave up.
- **Silence ratio.** How often the insight surface renders nothing. If that number is zero, you are producing filler and you will pay for it in attention.

None of this is about making the model better. It is about the fact that in a machine learning product the interface is part of the system under test, and it is generating the data you will use to judge everything else. Build it as though it were, because it is. If you want the same argument applied to a specific product surface rather than to method, the work behind these decisions is at [imdennie.com](https://imdennie.com).

[← All writing](https://imdennie.com/blog/)
