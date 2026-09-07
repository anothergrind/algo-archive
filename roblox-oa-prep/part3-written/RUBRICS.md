# Part 3 — Rubrics

**Draft your answers first.** Back to the questions: [README.md](README.md)

A general note before the specifics. Every one of these questions is scored on the same
underlying axis: **does this person reason, or do they perform?** Graders read hundreds
of these. Concrete beats fluent every time — a specific number, a named trade-off, a
decision you actually made. Anything that could have been written by someone who has
never done the thing reads as noise.

---

## Q1 — Why Roblox?

### What a strong answer looks like

- **Names something only true of Roblox.** The obvious candidates: it is a platform
  where the users are also the creators; the economy is real money flowing to
  teenagers; the client runs on everything from a phone to a console; the engine and
  the marketplace and the moderation problem are all one product. Pick one and go deep
  rather than listing four.
- **Connects to something you have actually done.** Played it, built a game in it,
  reverse-engineered something, or a genuine parallel from other work — a system with
  user-generated content, a marketplace, a real-time simulation.
- **Says what you want to work on**, specifically enough that it implies you know how
  the company is organised.
- **Is honest about scale of interest.** "I want to work on the physics engine" is
  strong if true. Faked passion is transparent and worse than measured interest.

### Weak answer

> Roblox is an exciting company at the forefront of the metaverse, and I have always
> been passionate about gaming. I would love to be part of a team that is changing how
> people connect online. I am a fast learner and I believe my skills would be a great
> fit for the culture here.

### Why it fails

Swap "Roblox" for any game company and the paragraph is unchanged — which means it
carries zero information about you. "Metaverse" is a press-release word, not something
an engineer there would say about their own work. "Passionate about gaming" is a claim
with no evidence attached. And the last sentence is about what you want, framed as what
you offer, with nothing concrete in it. Three sentences, nothing learned.

---

## Q2 — The over-engineered design

### What a strong answer looks like

- **Treats it as a question, not a verdict.** You believe it is over-engineered; you
  have been there three weeks. The strong move is to ask what the flexibility is for,
  because the most likely explanation is that a four-year engineer knows about a
  requirement you do not.
- **Goes to the person first.** Directly, privately, quickly — not to the mentor, not
  to a group channel, not by quietly building your own version.
- **Makes the disagreement concrete.** "This adds a week" is arguable. "This adds a
  week and here is the simpler version I sketched, what breaks in it?" is a technical
  conversation someone can answer.
- **States a resolution path.** If you still disagree after the conversation: whose
  call is it, what would change your mind, and how do you commit to a decision that
  went against you without sulking.
- **Notices the schedule.** Waiting a week for the mentor is itself a cost on a ten-week
  project — the answer should acknowledge that rather than defaulting to "wait".

### Weak answer

> I would respect my teammate's experience since they have been there four years and I
> am just an intern. I would go along with their design and focus on my own part of the
> project. If it became a real problem later I could bring it up with my mentor when
> they got back.

### Why it fails

It resolves the tension by deferring entirely, which reads as conflict avoidance rather
than judgement. Seniority is offered as a reason to not ask a question — but asking
"what is the flexibility for?" costs nothing and is exactly what a good junior engineer
does. It also defers the escalation to a hypothetical future where the cost has already
been paid. Nothing here shows the candidate can hold a technical position or update
from one.

---

## Q3 — The wrong number

### What a strong answer looks like

- **Discloses immediately and without being asked.** This is the entire question. Any
  answer that hedges on whether to raise it has failed regardless of how well it is
  written.
- **Goes to the people who acted on the number** — your mentor, your manager, whoever
  repeated it upward — not just a correction buried in the final slide.
- **Leads with the correction, not the excuse.** State the right number, then what went
  wrong, then what you have already done about it.
- **Fixes the process, not just the number.** How did a wrong number survive four weekly
  updates? Add the check that would have caught it.
- **Keeps proportion.** The project is still positive. Strong answers correct the record
  without theatrical self-flagellation, and still present the work with confidence.

### Weak answer

> I would double-check my calculations to make sure it was definitely wrong. If it was,
> I would update the number in my final presentation so the correct figure is the one
> people see. Since the project is still positive overall, I do not think it would
> change the conclusions much.

### Why it fails

"Update it in the presentation" is a silent correction — the people who repeated that
number for a month are never told they were wrong, and may find out in front of an
audience. The reasoning then rationalises the omission ("does not change the
conclusions much"), which is the candidate deciding on behalf of others what they are
entitled to know. Verifying first is fine, but it is the only proactive step here, and
it is being used as a delay. This question is a screen for integrity under mild
incentive to stay quiet, and this answer fails it while sounding reasonable.

---

## Q4 — Polish versus new feature

### What a strong answer looks like

- **Asks who the work is for.** Polishing serves the team that inherits the code; a
  second feature mostly serves the intern's own narrative. Naming that asymmetry
  honestly is the strongest single move available.
- **Identifies the deciding fact rather than guessing.** Is the first feature actually
  shipping? To whom? Is anyone blocked on it? Will anyone maintain it after you leave?
  A week of polish on something that will not ship is waste; a week of polish on
  something going to production is the obvious answer.
- **Rejects the framing where appropriate.** Often the right answer is neither extreme:
  two days of tests and a handover doc, then a small scoped extension.
- **Names the failure mode of the other branch.** Unfinished second features are a real
  cost to the team — a half-built thing to delete is worse than nothing.
- **Says who they would ask.** This is a one-line conversation with a mentor, and
  saying so is a strength, not a dodge — provided you also say what you would do.

### Weak answer

> I would polish the existing feature because quality is more important than quantity.
> Shipping something half-finished would reflect badly on me and create technical debt
> for the team. It is always better to do one thing well than two things badly.

### Why it fails

It reaches the defensible conclusion by reciting maxims rather than reasoning, so it
would produce the same answer if the facts were reversed. "Quality over quantity" and
"one thing well" are not analysis. Nothing is asked about whether the feature ships,
who maintains it, or what the second feature would be — and the one concrete
consideration offered, "reflect badly on me", is about the candidate rather than the
work. The question explicitly asked for reasoning, not a conclusion, and this supplies
only the conclusion.

---

## Q5 — Tail latency versus everyone

### What a strong answer looks like

- **Refuses to answer it as a pure numbers question.** 10× for 5% versus 1.2× for 100%
  is roughly a wash in aggregate; the decision is entirely about *who those 5% are* and
  *what the absolute numbers are*.
- **Asks for the absolute latencies.** 10 s → 1 s for 5% is a completely different
  decision from 200 ms → 20 ms. A 1.2× on something already fast is invisible; on
  something slow it is meaningful.
- **Asks who the tail is.** Worst-case users are often not random — they are the users
  on the worst devices, the worst networks, or with the most content. At Roblox that
  skews toward exactly the emerging markets and low-end hardware the company cares
  about. It can also be the biggest creators. Either way the 5% is probably not a
  uniform sample.
- **Considers whether the tail is a bug.** A 10× available for one slice often means
  something is pathological there, and pathological cases tend to spread.
- **Commits.** After laying out the considerations, pick one and say what would flip it.
  A strong answer usually leans tail, for the reasons above, but the lean matters less
  than the reasoning and the explicit flip condition.

### Weak answer

> I would go with the 1.2× improvement for everyone, because it helps the most users.
> 5% is a small fraction, so optimising for them would not be the best use of
> engineering time. Making a change that benefits 100% of users is a bigger overall
> impact for the same cost.

### Why it fails

It picks a branch instantly by counting users, which is the trap the question is
built around. No question is asked about the absolute numbers, so the candidate cannot
know whether 1.2× is even perceptible. The 5% is treated as a uniform random sample of
users when it is almost certainly a structured group. And the answer offers no
condition under which it would change — it is a conclusion with no handle on it, which
tells the grader nothing about how the person would behave when the facts arrived.

---

## Q6 — A time you were wrong

### What a strong answer looks like

- **Actually wrong, and technically wrong.** Not "I was wrong to underestimate how long
  something would take" and not a disguised strength. A belief about how a system
  behaved that turned out to be false.
- **Real STAR structure**, with Action doing most of the work. A common failure is
  spending three sentences on Situation and one on what was actually done.
- **Names how you found out**, because the question asks. Best case: a mechanism you
  put in place caught it — a test, a metric, a colleague you invited to review. Worse
  but honest: a user or an outage told you.
- **Says what changed afterwards.** A specific habit, check, or test that exists now
  and did not before. This is the payload of the whole answer.
- **Is proportionate about blame.** Owns it without either deflecting or performing
  guilt.

### Weak answer

> I once thought a bug was caused by the frontend, but after a lot of debugging I
> realised it was actually a backend issue. I learned that it is important to check
> your assumptions and not jump to conclusions. Since then I always try to be thorough
> when I debug.

### Why it fails

There is no situation, no stakes, and no detail — "a bug" and "a backend issue" could
describe anything, so the grader cannot tell whether this happened or whether it was
hard. The lesson is a platitude that follows from nothing specific, and "I always try
to be thorough" is not a mechanism; it is an intention. The question asks how you found
out, and the answer says "a lot of debugging", which skips the only interesting part.
Nothing here would look different if the candidate had made it up.

---

## Scoring yourself

For each answer, check honestly:

1. Could this have been written by someone who never had the experience? If yes, add
   specifics.
2. Would it read identically if the facts of the scenario were reversed? If yes, you
   recited a maxim instead of reasoning.
3. Does it contain at least one number, name, or concrete detail?
4. Does it end somewhere — a decision, a mechanism, a changed behaviour?
5. Is it under 200 words?

Falling short on 1 or 2 is what separates a mid answer from a strong one. Most people
fail those two and pass the rest.
