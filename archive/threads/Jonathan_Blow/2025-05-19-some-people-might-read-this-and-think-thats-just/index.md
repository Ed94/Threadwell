---
title: "Some people might read this and think, that's just not my world, I am stuck in this world where software breaks all the time and everything I build is disposable."
type: archive
source: twitter
source_url: "https://x.com/Jonathan_Blow/status/1924509394416632250"
author: "Jonathan Blow"
handle: Jonathan_Blow
post_id: "1924509394416632250"
date: 2025-05-19
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "Some people might read this and think, that's just not my world, I am stuck in this world where software breaks all the time and everything I build is disposable."
in_reply_to: ""
---

## Source

- URL: https://x.com/Jonathan_Blow/status/1924509394416632250
- Author: Jonathan Blow (@Jonathan_Blow)
- Posted: 2025-05-19 16:56:09

## Thread

**1/** **@Jonathan_Blow** ^1924509394416632250

Some people might read this and think, that's just not my world, I am stuck in this world where software breaks all the time and everything I build is disposable.

Even if that is kind of the case for you, there is still good news, because this isn't an all-or-nothing problem. It's a dial that can be turned; you can turn that dial in a direction that reduces flailing and results in more-stable long-term progress.

You don't have to remove all the dependencies, because every dependency you remove contributes to stability. Even getting rid of 1/3 of your dependencies can do amazing things.

You can look at all the things you depend on and divide them into two categories: major and minor. Major dependencies are things that, realistically, you are never going to have your own version of. I am never going to make my own graphics API, so those count as major dependencies for me (DirectX12, Vulkan, Metal, etc). I am not going to write my own CPU-side font rasterization, so anything I choose to use there (FreeType, stb_truetype) goes in that category.

With Major Dependencies, you limit your contact surface with them: You call only the functions you really need, and you do this only from the surface of your program -- you don't build data structures deep into your program that propagate the particular data structures or API decisions of any of these systems. A good API author will help you do this (stb_truetype), a bad API author will be trying as hard as they can to screw you up and force you to become tied to their system forever (anything from Microsoft or Apple).

Understanding that many API authors are hostile can cause a big change of perspective here, and once you see it, the correct tactics become much more obvious.

So, that's the major dependencies. Minor dependencies are things that are smaller, and that you want to use much more thoroughly throughout your program: for systems programmers this might be a data structure like an expanding array or hash table, for Web, maybe there are some string or file operations that you like to do.

Minor dependencies can be eliminated and it's not even hard. You just do one at a time: hey, I need this data structure, I have been importing this other code to provide that functionality, I have suffered X, Y and Z problems because of this, how about if I just implement my own simple version of this one thing?

People can get scared of implementing core stuff like this, because they look at the implementation they are using now, and it looks huge and complicated and hard to reproduce. But the thing to realize is most of this implementation is spam. It is mostly doing things for people who are not you, for reasons you don't necessarily agree with, chosen by a decision-making method that is deeply flawed. Your own implementation can be cleaner and smaller, and it can give you good feelings when you go look at it. You don't need all the functionality of the thing you are importing; you only need 8% of the functionality. Implementing that is easy.

Once you do this a few times, you have your own stable body of code that you bring with you from project to project. It won't break unless you mess with it. You can keep improving it if you want, incrementally over time, but the cost of this is small because this code represents stable algorithms that don't change with fashion, so work on this is never forced.

Every big company has their own internal version of this, but the problem in that scenario is that a big company is full of people who want different things, and have varying levels of decision-making skill, so these usually end up not so good. But when it's your own personal thing, it can in fact be very good, and help make you happy on a daily basis.

And, your software will break much less often. Which is great.

@NotAShelf
@ThePrimeagen

https://x.com/Jonathan_Blow/status/1923414922484232404

Branches: [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-JBrooksBSI-a-practical-example-is-burgerlib-used-over-an-30]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-lunarchstudios-i-frequently-find-that-making-my-own-small-tool]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-i99bproton-do-you-regard-standard-library-as-external]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-glodarev-i-dont-know-how-making-things-from-scratch-became]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-MatthewREHayden-wait-you-havent-taken-the-signed-distance]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-thepanta82-in-the-web-world-theres-a-common-wisdom-against]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-nicomuellerAT-isnt-the-amazing-capability-that-drove-this]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-angsthotep-i-was-trying-to-explain-this-to-my-colleagues-but]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-saarw-the-warning-against-hostile-apis-that-you-mention]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-SpaceSamurai63-love-your-post-interestingly-almost-all-of-it]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-andriishafar-finally-we-agree-on-something-programmers-should]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-JimmyTheXploder-i-like-the-discussion-around-dependencies-and]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-bousquetm-i-once-started-a-project-on-xna-but-it-got]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-19-schulkinator-ive-had-folks-ask-me-why-i-like-to-build]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-the_yuyoyuppe-the-paragraph-about-limiting-the-contact-surface]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-ReginaHarsanyi-you-should-be-friends-with-time-based-media]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-a_cerbic-ive-said-this-for-a-long-time-you-can-either-pull]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-kentwengland-and-if-your-os-provided-the-major-dependencies]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-donlucastuff-this-is-the-epitome-of-a-slippery-slope-argument]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-H8weaver-also-you-are-less-likely-to-get-stuck-in-the-we]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-20-Hannomalie1-the-paragraph-about-spam-really-hits-hard-and-i]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-21-snowfrogdev-how-do-you-see-these-principles-apply-for]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-21-Floorislava-its-really-bad-and-getting-much-worse-peep-all]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-21-LimilyRipple-another-thing-that-contributes-to-resistance-to]], [[archive/threads/Jonathan_Blow/2025-05-19-some-people-might-read-this-and-think-thats-just/2025-05-24-ValentinGh39378-making-your-own-tools-vs-learning-how-to-use]]
