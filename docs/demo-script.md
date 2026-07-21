# RyderShare Intelligence demo — 30 min (20 talk + 10 Q&A)

## Pre-flight (before anyone joins)

- Demo from your laptop at **localhost:8791**. The new map exists only in the local build, so
  don't demo from prototype.staging.baton.io unless we push tonight.
- Reload the tab right before you start—a reload resets every approval and puts the demo back
  to its opening state.
- Keep a safety-net tab at `localhost:8791/index.html?intel=1#/agents`, which boots straight
  into the enabled feed if anything goes sideways mid-demo.
- Run the click path twice tonight; the whole demo is about a dozen clicks.

## The shape

The Veritasium engine is a misconception the room already believes, stated confidently and
then broken. Ours: **give customers enough visibility and the problems take care of
themselves**. After the hook, the demo runs three question→answer loops, and each loop opens
with the question the room is silently asking—an audience that has committed to a question
watches the answer differently.

## 0:00–2:00 — The hook (no product on screen)

**SAY:** For ten years this industry has run on one belief: give the customer real-time
visibility and the chaos goes away. We believed it too—RyderShare shows Dana, the
transportation manager at Summit Beverage Group, every one of her 60 loads, live, on a map.

**ASK THE ROOM:** So what time does Dana's day start?

**SAY:** 5:30 in the morning, because the visibility didn't remove her work, it moved the
work onto her screen and left the doing to her. The screen shows her the storm, the late
loads, and the rate spike, and then it waits for her to handle every single one. Today I
want to show you what happens when the platform does the work and Dana approves it.

## 2:00–4:00 — Enable it

**DO:** Open the splash. Read the title line off the screen. Click Enable and narrate over
the ~5-second activation.

**SAY:** This is RyderShare as Dana knows it today, and this switch is the product: eight AI
agents that watch her freight around the clock, grounded in the RyderShare records that
already run her loads. There is nothing new for the customer to implement, because the
system of record is already ours.

## 4:00–10:00 — Loop 1: What did it do while she slept?

**DO:** Land on Autopilot. Point at the header: "Your agents worked overnight—5 things need
you." Walk the timeline briefly (analytics cards, the overnight entries), then open the
storm card → Review details.

**SAY:** Dana opens her laptop at 8am and this is the whole job: five decisions, with
everything else already handled. Thursday's tropical system puts 6 of her loads at risk, and
the agent built a mitigation plan overnight—[read the plan off the panel]. Here is what the
plan costs, and here is what doing nothing costs. [point at the counterfactual]

**DO:** Click one Adjust picker so the room watches the cost math recompute live, then
Approve. The card collapses to a green receipt and the needs-you count drops.

**SAY:** Dana just spent ninety seconds on a decision that used to be her whole morning.

This approval is the money moment of the demo—let the receipt land before you move on.

## 10:00–14:00 — Loop 2: Why should anyone trust it?

**SAY (pose it before they do):** The question every operator asks next is what happens when
the AI gets it wrong.

**DO:** Switch to the Agents tab. Open one agent's audit panel—the storm approval from two
minutes ago is sitting at the top, stamped "Just now."

**SAY:** Every action lands in an audit trail with the time first and the approver attached,
and anything that touches money or capacity requires a person to sign off—the agent drafts
the move and Dana approves it. The trust model is the same one Ryder already runs with its
own account teams; we made it inspectable.

## 14:00–17:00 — Loop 3: What is it worth?

**DO:** Back to Autopilot. Open the Market watch cards, then the rate chart panel.

**SAY:** Spot rates are up 14% since April, so the Adaptive Capacity agent flagged two
brokerage lanes worth locking into dedicated rates—about $3,400 a month below spot—and one
soft dedicated lane worth flexing out for roughly $2,200 a month. Each move carries the
chart that justifies it, and each one needs sign-off from both sides.

**DO:** Approve both, then click the ask-bar prompt: "Why was my June invoice higher?"

**SAY:** And when Dana has a question the feed doesn't answer, she asks her own records
directly and gets an answer grounded in her actual loads.

## 17:00–19:00 — Close the loop

**DO:** Point at the header, which now reads all clear. Switch to Network and zoom out
slowly to the full continent.

**SAY:** This is the network those agents are watching—every load and every lane across the
US, Canada, and Mexico, 24 hours a day. RyderShare put Dana's supply chain on a screen, and
RyderShare Intelligence puts it on autopilot.

**THE ASK:** name the next step you want from this room—my suggestion is two Dedicated
customers as design partners for a fall pilot, but tailor this line to what you actually
want to walk out with.

## 19:00–20:00 — Hand to Q&A

## Q&A prep (likely questions, one-line answers)

- **Is this live?** It is a vision prototype on synthetic data, and every capability maps to
  records RyderShare already holds today—the build question is sequencing, and the PRD
  covers it.
- **What happens when the AI is wrong?** Nothing moves without a human approval, every
  action is in the audit trail, and money or capacity changes need sign-off from both sides.
- **How is this different from project44 or FourKites?** A visibility vendor's product ends
  at the alert, while Ryder runs the trucks, the drivers, and the contracts—so the same
  platform that spots the problem can execute the fix.
- **What does it take to build?** An agent layer over the RyderShare data we already
  operate, phased—no rip-and-replace.
- **Which customers first / what's the pricing?** Fold both into pilot design rather than
  answering cold.

## Timing discipline

If you're running long, cut the ask-bar beat in Loop 3 and go straight to the close. Never
cut the storm approval—the receipt drain is the demo.
