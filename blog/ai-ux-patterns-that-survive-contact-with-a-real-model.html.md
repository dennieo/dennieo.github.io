Source: https://imdennie.com/blog/ai-ux-patterns-that-survive-contact-with-a-real-model.html

Updated: 2026-09-23

[All writing  ](https://imdennie.com/blog/)

AI interfaces

# AI UX patterns that survive contact with a real model

Dennie Ordynskyi · September 2026 · 11 min read

If you are searching for AI UX patterns, you probably want a list you can apply this week, not a taxonomy. Here is the short version: the patterns that hold up in production are the ones that assume the model is usually right rather than right, and design the interface around the gap. That means results presented as proposals you confirm, waits that show understanding rather than progress, numbers the user can audit, and a genuine empty state where the AI has nothing worth saying. Everything below comes from building and shipping [Numi](https://numi.app), a vision-based food tracker, where a wrong answer becomes a wrong number in someone's day, and from a set of patterns I tried first and pulled out.

## Why most AI UX pattern lists do not survive shipping

Most published patterns describe the happy path: a prompt input, a streaming response, a thumbs up and thumbs down. Those are components, not patterns. They describe what the interface contains rather than which decision it makes when the model is uncertain, slow, or confidently wrong.

The useful unit of an AI pattern is a decision under a specific failure mode. So each pattern below is written as: the failure it absorbs, what I built, and what I built first that did not work.

One framing sits under all of them. **A model's output is a proposal, not a verdict.** A model commits to an answer whether or not the answer is correct, and it does so with the same visual confidence either way. If the interface renders that as fact, every near-miss becomes silent damage: the user does not notice, does not correct, and the record quietly drifts. Treating output as a proposal is not humility for its own sake. It is the only way a wrong answer produces a correction instead of a corrupted history.

## Pattern 1: Correction-first results

**Absorbs:** the model being close but not right.

In Numi, photographing a meal returns items with quantities and macros. The first version I built showed the analysis as a clean summary card with an edit affordance behind a tap. It looked finished. It tested well in the sense that people liked looking at it.

It was wrong, because the finished look told people the answer was settled. Corrections dropped off, and what I got instead was quiet acceptance of numbers that were sometimes 30 percent out on portion size. The interface had made agreeing cheaper than checking.

So the result screen became a list where every item is visibly adjustable in one tap, and confirmation is an explicit action. The consequence I care about is not accuracy in the model sense, it is that **being wrong is a normal state of the interaction rather than an error state**. Nothing apologises. Nothing turns red. You change 200g to 150g and move on.

The falsifiable claim: in any AI product where output feeds a persistent record, the correction path is the most load-bearing screen you have, and it is almost always the least designed one. If you can name the visual design of your correction flow off the top of your head and it is just "an edit icon", you have not built this pattern.

### How to apply it

- Make the edit target the same size as the confirm target. If confirming is a big button and editing is a small pencil, you have expressed a preference.
- Never require a mode switch to correct. "Tap to edit" as a separate state adds a decision before the correction.
- Log corrections as a first-class event. They are your only honest accuracy signal, and far more informative than thumbs up and thumbs down.

## Pattern 2: Latency as understanding

**Absorbs:** multi-second inference you cannot engineer away.

Vision analysis takes seconds. No amount of optimisation makes it instant, and pretending otherwise produces a worse product than accepting it. You cannot fake instant, so the design job is deciding what those seconds communicate.

A spinner communicates "something is happening elsewhere". A staged sequence communicates "your meal is being understood". In Numi the wait shows the analysis progressing through what it is actually doing: the image being read, items being identified, portions being estimated. The user watches comprehension accumulate rather than watching time pass.

What I learned is that **perceived competence during latency is an interface decision, not a model property**. The same model, behind a spinner, feels slower and less capable than behind a staged reveal, because the spinner gives the user nothing to attribute the delay to. Attribution is the whole trick. Time spent on something you can see being done reads as work. Time spent on nothing reads as failure.

### How to apply it

- Map your pipeline stages and expose them, in the real order, at their real speeds. Fake stages get noticed the moment one of them takes an inconsistent length of time.
- Show partial output the moment it exists. Two identified items on screen beats four items three seconds later.
- Do not animate a progress bar to a percentage you cannot compute. A bar that stalls at 90 percent is worse than no bar.

## Pattern 3: Deterministic numbers with stated inputs

**Absorbs:** the user needing to act on a figure they cannot verify.

Numi shows a health score. The obvious implementation is to ask the model for a score out of 100. I did not do that, and this is the decision I would defend hardest.

A model-generated score cannot be checked, argued with, or learned from. If it says 62, there is no follow-up question with an answer. The user's only options are to believe it or ignore it, and after the novelty wears off almost everyone ignores it. A deterministic score computed from named inputs behaves differently: you can see which inputs moved it, disagree with the weighting, and predict what tomorrow's number will be. That predictability is what keeps a number in use.

The rule I now apply: **when the user has to act on a number, explainable beats accurate.** A rougher number they can reason about drives better behaviour than a more sophisticated one they cannot. Use the model for the parts that need judgement, such as identifying what is in the photo, and use arithmetic for the parts the user is going to argue with.

## Pattern 4: The silence state

**Absorbs:** having nothing specific to say, on a screen designed to say something.

This is the pattern I see skipped most often, so I will name it plainly. **The silence state is a designed condition in which an AI feature renders nothing because it has nothing specific enough to justify rendering.** Not a placeholder, not a generic encouragement, not a tip of the day. Absent.

Generic output is a trust leak. "Great choice!" reads as machinery rather than attention, and the damage is not confined to that one line. One obviously canned sentence retroactively makes the good insights around it look canned too, because the user now knows the system is willing to produce filler. You cannot recover credibility per-item once the user has decided the whole surface is decoration.

My threshold in Numi: an insight has to cite something real about this person today, such as what they ate, what is left in their targets, or what changed this week. If it cannot, the slot does not render. Layouts have to be built to survive that, which is the actual engineering cost of the pattern and the reason people avoid it. A card that collapses cleanly to nothing is more work than a card that always has text in it.

### How to apply it

- Write the gate before the prompt. Decide what data must exist for an insight to be worth showing, and check it in code.
- Ban whole categories of output rather than filtering case by case. No congratulation without a specific figure. No advice without a specific number attached.
- Design the collapsed layout first, so silence is not a hole in the page.

## Pattern 5: The autonomy ladder, with the user on the rungs

**Absorbs:** the system knowing something the user has not agreed to act on.

There are three separable things an AI feature can do: **detect**, **suggest**, and **act**. Most products collapse them, and collapsing them is where the trust breaks.

Numi keeps them apart. Noticing that someone has plateaued is one thing. Proposing a change to their targets is a second thing. Changing the targets is a third, and it requires a confirmation. An app that silently rewrote a target would have taken a decision the person can neither see nor argue with, and when they later noticed their numbers had moved they would have no way to reconstruct why.

The current agent conversation is rediscovering this as progressive delegation, and the shipped lesson has not changed: **a system earns the next rung visibly, one confirmed suggestion at a time, or it never earns it at all.** Users do not grant autonomy on the basis of stated capability. They grant it after watching a specific class of suggestion be right several times. Which means your interface needs to make that track record visible, or the trust never accumulates anywhere the user can see it.

## Pattern 6: Design for the worst hour of use

**Absorbs:** the demo being a poor model of real conditions.

This one is not strictly an AI pattern, but it governs which of the others you get right, so it belongs on the list.

[Tysha](https://tysha.app) is a sleep sound app, and its brief was a single scenario: one hand, lights off, a baby on the other arm, 3am. From that came every constraint that mattered. Sound in under a second. Fully offline. Nothing to sign into. No decision to make before audio plays.

Notice what that brief rules out. It rules out a personalisation onboarding flow. It rules out anything that needs a network round trip. It rules out clever recommendations, because at 3am a recommendation is one more thing to read. A feature list would have added all three.

Applied to AI features specifically: **work out the worst hour your feature will be used in, and check each pattern against it.** Multi-second latency is fine when someone is sitting down at lunch and not fine when they are standing in a queue. A correction flow that requires reading is fine on a laptop and not fine one-handed. A product judged in its worst hour earns a loyalty that demo-hour polish never does.

## Pattern 7: The fixed deadline as a design instrument

**Absorbs:** scope drift in features whose value is unproven.

[Meraki](https://merakistudio.dev) delivers a site in seven days. The interesting effect of that is not speed, it is that it forces one question to be answered on day one: what must this business's website do first? Decisions that would drift for a month in an open-ended project get made in an afternoon when the ship date is real. The deadline does the prioritising.

AI features are unusually prone to the drift the deadline prevents, because there is always another prompt to try and another edge case to handle, and none of that work has a natural stopping point. Boxing a feature into a fixed window forces the honest question: is this feature good enough to ship at all, or does it need to fall back to the silence state? Both answers are useful. Endless refinement is not.

## Patterns I tried and removed

Worth listing, because the popular AI UX pattern collections tend to include some of these:

- **Confidence percentages on output.** I tried surfacing model confidence next to items. It shifted the burden of interpretation to the user without giving them anything to do with it. "78 percent confident" does not tell you whether to check the portion. Making everything equally editable was a better answer than labelling some things as shaky.
- **Thumbs up and thumbs down.** Cheap to build, near-worthless as signal in a product where the user is already correcting real values. The correction itself tells you what was wrong and what the right answer was. A thumbs down tells you nothing actionable.
- **Chat as a general entry point.** A text box invites arbitrary requests, and every request outside the supported set produces a small failure. Fixed affordances that always work beat an open input that mostly does. I wrote separately about [what actually breaks in chatbot UX](https://imdennie.com/blog/chatbot-ux-design-what-actually-breaks-in-production).
- **Apologetic error copy.** "Sorry, I couldn't quite get that" frames a normal outcome as a malfunction. In a correction-first interface the model being slightly off is expected, and the copy should sound like it.

## A checklist you can run against your own AI feature

- Can the user change every value the model produced, in one tap, without entering an edit mode?
- Does your loading state show what is being understood, or only that something is happening?
- For every number the user is expected to act on, can you name the inputs that produced it?
- Is there a code path where your AI surface renders nothing, and does the layout survive it?
- Are detect, suggest, and act separate steps, with the user on the last one?
- Does the feature still work one-handed, offline, or in whatever your worst hour is?
- Do you log corrections as a metric, and do you look at them more often than you look at engagement?

If the honest answer to five of those is no, the model is not your problem.

[← All writing](https://imdennie.com/blog/)
