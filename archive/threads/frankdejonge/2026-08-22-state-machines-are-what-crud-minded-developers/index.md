---
title: "State machines are what CRUD-minded developers create when trying to model processes."
type: archive
source: twitter
source_url: "https://x.com/frankdejonge/status/2091060039448461736"
author: "Frank de Jonge"
handle: frankdejonge
post_id: "2091060039448461736"
date: 2026-08-22
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - frankdejonge
description: "State machines are what CRUD-minded developers create when trying to model processes."
in_reply_to: ""
---

## Source

- URL: https://x.com/frankdejonge/status/2091060039448461736
- Author: Frank de Jonge (@frankdejonge)
- Posted: 2026-08-22 07:08:58

## Thread

**1/** **@frankdejonge** ^2091060039448461736

State machines are what CRUD-minded developers create when trying to model processes.

**2/** **@_joshd** ^2091282447233347801

**@frankdejonge**

Event sourcing and state machines aren't mutually exclusive though. You can totally use a state machine to represent how you roll a sequence of events into the current state, and IME you'll have fewer bugs if you reason explicitly about those states and transitions

**3/** **@frankdejonge** ^2091411590281068981

**@_joshd**

In event sourcing, you cannot deny what happened in the past, you have to deal with it. In a state machine those would be rejected as transitions. So they’re not mutually exclusive until that happens.

**4/** **@_joshd** ^2091413430888780150

**@frankdejonge**

If you're doing CQRS you can't deny that a command was sent but you certainly can deny that your system executes the command as sent. Notably if the command would put an entity in a disallowed state. You can't retroactively disallow a transition in ES, but you also can't in CRUD.

**5/** **@frankdejonge** ^2091512632414982551

**@_joshd**

I'm not sure what your point is. What your describing is correct, but has very little to do with comparing event sourcing to state machines imo. If something happened in ES you can pretend it didn't, which just means you're not modelling what happened. You can still guard rules.

**6/** **@_joshd** ^2091558477143650424

**@frankdejonge**

I'm saying that avoiding defining your allowed states and transitions will not help you and bugs, it'll just make it harder to detect them

**7/** **@frankdejonge** ^2091584635079672045

**@_joshd**

Allowed states mean nothing when it is enforced upon reconstitution. It’s denying history that already happened.

**8/** **@_joshd** ^2091605404472254700

**@frankdejonge**

I don't know what you're imagining my proposal is. You have to be able to represent every state transition that has ever happened. You don't have to continue to allow that transition in the future. Explicit enumeration of state transitions is better than implicit.

**9/** **@frankdejonge** ^2091606504029683942

**@_joshd**

What kind of industry or problem domain do you work in/on? Might help me understand your responses better

**10/** **@_joshd** ^2091634264966308037

**@frankdejonge**

Two sided service marketplace. And so, simplifying a bit, the example I'm thinking of is that services have states like scheduled / in-progress / completed, where the transition "complete" only makes sense for in-progress services. What example are you picturing?

**11/** **@frankdejonge** ^2091761233179414804

**@_joshd**

What happens when multiple things need to happen before you can be in progress or scheduled? Like each side needs to agree to terms and they need confirm once the other side has specified their proposal?

**12/** **@_joshd** ^2091764442833010794

**@frankdejonge**

Then a single state machine likely isn't the right modeling tool. You could force your architecture there but you shouldn't. State machine is for when you've got one entity which can be in one of a small set of mutually exclusive states. You'll know if your problem matches.

**13/** **@frankdejonge** ^2091765099874648556

**@_joshd**

In my experience, people often cannot say, unless it’s rooted in undeniable hard facts that cannot change. Any business process can change or become more complex in one area or another.

**14/** **@frankdejonge** ^2091765804819767481

**@_joshd**

And by the conditions you’re attaching, you could only use it in relatively simple cases, which in a sense makes the point of it being a lesser option. Things often start out simple and then grow in utility and complexity over time. So how can you tell when it stays simple?

**15/** **@_joshd** ^2091768683811271118

**@frankdejonge**

Yes. My opinion is that you should use the least expressive domain model you can get away with. You *could* express any business process using three tables [entity, relationship, event] (or even just [entity] or just [event]) but you shouldn't.

**16/** **@_joshd** ^2091769529915572604

**@frankdejonge**

Or perhaps I should say "least flexible" rather than "least expressive". It's generally pretty easy to replace a state machine with more bespoke logic, and if you need to do that you just accept that your code is slightly harder to reason about. Bespoke->state machine is hard.

**17/** **@frankdejonge** ^2091783448956452931

**@_joshd**

I think this is where we differ in stance perhaps. I tend to optimise for change yet defer as much YAGNI-stuff as possible. The optimising for change means I can defer things to later without being hit by it. Which means most things stay as simple as possible, yet some are not.

**18/** **@_joshd** ^2091792273797464085

**@frankdejonge**

Yeah, makes sense. Where the best point between future-proofing and YAGNI is for you will depend on the relative costs of complexity and of making changes. I work on a small team which ships daily, so changes are a worthwhile price to be able to hold the whole system in our heads

**19/** **@_joshd** ^2091792694238687397

**@frankdejonge**

If a schema change will require looping in 10 stakeholders and allotting time in the quarterly roadmap, then perhaps a bit of extra complexity in the form of a permissive schema is worth it to avoid that friction.

**20/** **@frankdejonge** ^2091794124567351484

**@_joshd**

I work in a compliance startup, ~5 teams, and for us it's mostly about not designing trap-door decisions. Anything that is reversible can be done with taking more risk, anything that is not, we scrutinise. We use ES to make many things a non-trapdoor decision.

**21/** **@_joshd** ^2091928950092214699

**@frankdejonge**

Makes sense. We're mostly not that hardcore on ES, though anything that touches money or legal documents or such we make sure the source of truth is append-only, which is sort of like ES if you squint.
