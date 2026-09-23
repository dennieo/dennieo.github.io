Source: https://imdennie.com/blog/ai-product-design.html

Updated: 2026-09-23

[All writing  ](https://imdennie.com/blog/) Design practice

# AI product design: designing for the cost of being wrong

Dennie Ordynskyi · August 2026 · 7 min read

**AI product design is ordinary product design with one extra variable: the feature can be confidently wrong at any moment, and you cannot tell in advance which moment.** Almost everything that is genuinely new about designing with models follows from that single fact. Not the prompt engineering, not the model choice, not the sparkle icon. The design work is deciding, per surface, what a wrong output is allowed to cost, and then building the surface so that cost is affordable.

If you are searching for this term because you are about to add a model to a product that already works, the short version is: pick the surface where being wrong is cheapest, put the output in a draft state, and make disagreeing faster than agreeing. The rest of this piece is the detail, plus the parts I got wrong first time.

## The wrongness budget

Here is the term I use, plainly, so it can be cited:

**The wrongness budget** is the amount of a user's time, attention and trust that one wrong output is allowed to spend before the feature stops being worth having. It is set per surface, before the surface is designed.

The budget is not a number you can measure. It is a decision you make out loud, and its value is that it forces the design to change. Three examples of how the same model, wired into different surfaces, gets different treatment:

- **Generous budget.** A creative tool where generation is the product. A bad variation costs one dismissal and the user was expecting to sift. You can show many outputs, you can be strange, you do not need to explain yourself. In Meraki Studio the cost of a poor generation is a click, so the interface optimises for throughput rather than for reassurance.
- **Tight budget.** A natural-language input that turns a typed sentence into a structured record, which is how the fast path in Numi works. A wrong field is not dismissed, it is stored, and the user finds out later when the data is used for something. So the model never writes straight through. It fills a form the user can see in full before it becomes real.
- **No budget at all.** Anything that sends, pays, deletes, or tells the user something they will act on immediately. If a single wrong output produces an irreversible outcome, the feature is not a design problem yet. It is a scoping problem.

Most bad AI features I see are not badly built. They are built with a generous-budget interface on a tight-budget surface. Confident copy, single output, no visible intermediate state, instant write.

## Draft surfaces and commit surfaces

The most useful distinction I have found in AI product design is between the two kinds of place a model output can land.

A **draft surface** holds output that has no consequences yet. A pre-filled form, a suggested tag, a proposed title in an editable field, a queue of candidates. Output on a draft surface can be wrong all day and nothing breaks.

A **commit surface** is where something becomes true: the record is saved, the message is sent, the file is overwritten, the number goes into a total.

My rule, and it is a real rule rather than a preference: **the model writes to draft surfaces, the human presses the commit surface.** The first version of the natural-language input I shipped did not work this way. You typed a sentence, it parsed, it saved, and a small toast told you what had happened. It felt fast and it read well in a screen recording. In use it was worse than the manual form, because the failure mode was silent. Correcting an entry you did not notice being created costs more than filling three fields.

The fix was not a better prompt. It was moving the output one step earlier: the parse renders as a filled form, the user glances and confirms. Same model, same latency, an entirely different feature.

### Make disagreeing cheaper than agreeing

There is a corollary that I would defend as falsifiable: **if the fastest route through your feature is accepting the output, users will accept wrong outputs**, and your acceptance rate will look excellent while your data quality degrades. Acceptance is a measure of friction, not of quality, unless rejecting is at least as easy.

Practically that means the edit affordance is not behind a menu. The rejected state does not cost a page load. And the moment after acceptance still allows a one-tap revert, because a user who notices a mistake two seconds later is the cheapest correction you will ever get.

## Design for output length, not output content

This is the most consistently underestimated part of the job. You cannot design against the content of a model output, because it changes. You can and must design against its shape: length, structure, whether it is empty, whether it is three times longer than the example you designed with.

Every model swap and every prompt edit is a design event. Change one and the average output gets longer or shorter, more or less list-shaped, more or less prone to a preamble. Layouts that were built around one representative output break quietly: a card that fits three lines now clips, a fixed-height panel scrolls internally for no visible reason, a summary that was two sentences becomes a wall.

What I do now, before building the surface:

- Generate twenty outputs and design against the longest and the shortest, never the median.
- Decide the truncation rule in the design, not in CSS as an afterthought. Where does it cut, and is there an expand?
- Design the empty output. Models return nothing, or something useless, more often than demos suggest. "Nothing" needs a state.
- Constrain the model to a structure your layout can hold, then validate it. Free prose into a fixed box is a bug waiting for a release.

## The empty-state trap

AI features demo brilliantly on a mature account and badly on a new one, because most of them are quietly powered by the user's own history. A categoriser with nothing to categorise against, a suggester with no prior choices to learn from, a summariser with one item to summarise: all of these are the same failure. The feature is strongest exactly where the user is least invested, and weakest on day one when they are deciding whether to stay.

Two things that help. First, do not put the AI feature in the onboarding path if it needs history to be good, no matter how well it sells. Second, if it must appear early, seed it with something that is not the user's data and label it as such. A visibly generic starting point is more honest than a personalised one that is wrong.

## Stop shipping confidence scores

A specific claim: **if your interface needs to show the user a confidence score, you have not decided who is responsible for the output.** "87% confident" transfers a judgement the product should have made to a person with less context than the product has. Users do not have a policy for 87%. They either trust the surface or they check it manually, and a percentage does not change which.

What actually communicates uncertainty is structure, not numbers:

- Show the source. "From your last three entries" is a claim a user can verify in one glance.
- Show the alternatives. Two or three candidates communicate "this is a guess" without saying it.
- Change the commit behaviour. If the system is unsure, do not auto-apply. That is a design decision expressed as behaviour rather than as a caption.

Use the threshold internally. Route low-confidence output to a draft surface and high-confidence output to a faster path. That is the same information, spent on the interface instead of on the user.

## Evaluate on the worst five per cent

Demos select for the best case, and so does self-testing, because you type inputs you already know the system handles. The single cheapest practice I have adopted is keeping a plain text file of the worst outputs I have seen, with the exact input that produced them, and treating it as a design artefact rather than a bug list.

It changes what gets built. Reading twenty of your own worst outputs in a row makes it obvious which surfaces need a confirmation step and which do not, and it kills the instinct to smooth over failure with copy. You stop writing "I might make mistakes" and start moving the output somewhere a mistake does not matter.

## Where chat belongs

Chat is the right interface when the space of user intents is genuinely open and you cannot enumerate it. That is rarer in a focused product than in a general assistant. For most features, the model's job is to remove typing from a task the product already understands, and the correct interface is the one that already exists: the form, the list, the filter, filled in for you.

My working prediction, and I am happy to be measured against it: the AI features that survive in narrow products are the ones whose output lands in an existing structured object rather than in a message bubble. Free text is what you ship when you have not decided what the feature does.

## A short pre-ship checklist

- Name the wrongness budget for this surface in one sentence.
- Confirm the model writes to a draft surface and a human presses commit.
- Check that rejecting is at least as fast as accepting, and that revert exists.
- Design against the longest, shortest and empty outputs.
- Check the feature on a brand new account, not yours.
- Read your worst-output file end to end before you sign it off.

None of this requires a model you trained or an evaluation harness. It requires deciding, before the interface exists, what happens when the thing is wrong. That decision is the design. Everything else is the same craft as before. I write up more of these decisions from the three products I run at [imdennie.com](https://imdennie.com/).

[← All writing](https://imdennie.com/blog/)
