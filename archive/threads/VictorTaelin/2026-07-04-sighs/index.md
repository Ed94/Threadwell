---
title: "*sighs*"
type: archive
source: twitter
source_url: "https://x.com/VictorTaelin/status/2073406569459368226"
author: "Taelin"
handle: VictorTaelin
post_id: "2073406569459368226"
date: 2026-07-04
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
description: "*sighs*"
in_reply_to: ""
---

## Source

- URL: https://x.com/VictorTaelin/status/2073406569459368226
- Author: Taelin (@VictorTaelin)
- Posted: 2026-07-04 14:00:22

## Thread

**1/**

*sighs*

it is already depressing enough that most of you can't understand my posts, but not being able to distinguish them from some technically illiterate SF CEO who thinks they'd proven quantum physics or some shit is another level of stupid

problem is, when I write too technically, it tends to just flop, which is why I have to resort to these "AI good!" and "AI bad!" posts that, I admit, may sound a bit over-excited sometimes. that said, the proof is simple enough to be explainable in a way you all can appreciate, so, I'll give it a shot. with you, in its full glory, how Fable contributed to Bend's consistency proof, why it was incredible and, yes, very valid

first: consistency is basically a word that means: "can we trust this language to formalize mathematics?". or, equivalently, can someone prove a false statement in it? imagine if someone found a proof of 2+2 = 5 in Lean. that person would be able to use this falsehood to perform arbitrary type-level rewrites, and, thus, prove any theorem (like riemann's hypothesis!) trivially, in a few lines of code. that wouldn't net them $1 million, but it would make for a legendary issue on Lean's GitHub, immediately invalidating any proof checked by Lean and undermining the language's credibility. I obviously don't want that to happen to Bend2

fortunately, the techniques for constructing a consistent proof system are well known, even though details vary case by case. it usually involves two main parts: first, prove it is sound (i.e., that evaluating an expression can't change this type). honestly, that's just the "show us your implementation is not hopelessly buggy". it is the easy part.

the second part is much more difficult:

"prove every well typed program in your language terminates"

this is necessary because infinite loops allow one to encode "paradoxes" (like "this sentence is false") and, to explain it in a very silly way, these paradoxes "confuse" the type checker, and allow you to prove falsehoods. so, if I want people to trust Bend as a proof language, I must be able to convince them there's no way to express an infinite loop in it. programs like "while (true)" must be, somehow, banned by our compiler. but how?

the way most proof assistants (like Lean) do it is to 1. not have loops to begin with, 2. ban any kind of non-structural recursion. that means that, to call a function recursively, you must ensure that arguments are getting smaller. that's fairly standard, and fairly easy to do.

so, is that it?

unfortunately, that's not enough, because, in functional languages, there's another way for infinite loops to manifest: self-replicating λ-terms. for example, consider the following Python program:

evil = (lambda f: f(f))(lambda f: f(f))
print evil

it hangs forever, even though it has no loops and no recursion. turns out it is very easy to accidentally let some variation of "evil" to creep in, and "evil" allows one to prove falsehoods.  for example, if the set of all sets contains itself, you can summon evil via Girard's paradox. and if you allow recursive datatypes to store functions, then, you can summon evil via Curry's paradox:

data Evil { bad(f : Evil -> Evil) } // this would break Lean!

that problem is not exclusive to proof languages. a similar paradox once caused a crisis in mathematics itself! in 1901, Russel proposed a legendary proof of a false statement in naive set theory, which was THE foundation of mathematics back then. the news was that math itself was broken, and every proof ever written by humanity would to be untrusted. crazy times! of course, this has since been "patched". today, we call it "naive" set theory for a reason! but this shows how hard it is to design a consistent proof system. humanity failed to do so for millenniums!

in Rocq, Lean and Agda, the way they avoid these self-replicating λ's is via a series of "patches" - i.e., human engineered antibodies to kill the paradoxes we found in the past. for example, the 'Evil' datatype above is syntactically forbidden by disabling certain shapes of recursive datatypes ("positivity checker"), and Girard's paradox is avoided by having an infinite universe of types ("universe hierarchy"). this disables the "does the set of all sets contain itself" paradox, which, in turn, disables the `evil = λf.f(f) λf.f(f)` summoned by it.

this is all solid and stablished, and people are very confident Lean and others are trustworthy. that said - and that's where I tend to change things - I argue that's overkill. while these restrictions indeed avoid paradoxes, they're also very strict, and ban perfectly valid programs. for example, it is impossible to write a fast interpreter (i.e., via HOAS) in these, and alternatives (like PHOAS) are very contrived. this makes these languages substantially less practical. Bend aims to be a proof language that is also viable as a real world programming language, so, it is of my interest to find more permissive termination argument. and that's what I was working on, with the help of Fable

my argument goes like this: first, only allow recursion when arguments decrease. so far, this is the same approach used by Lean and others, nothing new here. now, we must find a way to avoid self-replicating λ-terms (like `λf.f(f) λf.f(f)`) from creeping in. that's where we detour. instead of positivity checker and universe hierarchies, I simply re-use a feature of Quantitative Type Theory (QTT) - which, in short, is an industry standard way to have O(1) arrays in an FP lang, and which Bend *already implements* - to forbid non-linear lambdas. In other words, in Bend, lambdas must be used linearly, and, thus, cannot be cloned, and that's enforced by the already existing QTT system.

this simple addition is sufficient to prevent all incarnations of `evil = λf.f(f) λf.f(f)` in one strike, cutting the evil in the bud, and ensuring Bend is terminating, as it easily exhausts every known way to introduce non-termination:

- infinite loops → there are no loops

- infinite recursion → only allow decreasing recursion

- self-duplicating λ-terms → lambdas can't be cloned

from termination, consistency follows easily.

and that's it. this is *obviously* correct and so easy I'm sure even you're confident you can't write infinite loops in Bend. aren't you?

now, I must be very clear here. these are all *my* design choices. I didn't ask an AI "pls build a consistent proof language" and then got flattered into thinking I'm a genius. I studied the subject 10 fucking years and used AI to aid me materialize and double check my ideas. this is the antidote I found to AI psychosis. I call it "competency"

that said, if the solutions are mine, how Fable helped here?

well, the argument per se is obviously sound, and nobody serious would contest it. the problem is that implementing a proof assistant is hard, and it is easy to introduce accidental bugs that detour from the intended semantics.

turns out the way that Bend2 wasn't faithful to my intention, for a reason that is legitimately hard to see, and that Fable identified never the less. 

QTT, as described in the original paper, allowed "relaxing" its checks a bit on certain places of the code. this is important for usability, and harmless to proof languages that use QTT (like Idris2), because they don't rely on QTT for termination. but Bend2 does, and these relaxed checks allowed  lambdas to be cloned in some circumstances. Fable read my termination argument, studied the QTT paper, audited the implementation, and found that inconsistency, handing me a proof of Falsehood! full proof below ↓

that was Fable's contribution, and, if you can't see how incredible this is, I don't know what could possibly impress you.

as for the solution, Fable proposed a few. all bad. my fix was to split Type in two sorts: one for arbitrary types, and other for lower order values. this lets me have the relaxed checks on positions where lambdas cannot occur, while still ensuring lambdas cannot be cloned and, therefore, self replicate. this is the "elegant proof" I mentioned in the post below!

![](https://pbs.twimg.com/media/HMY3SbQWAAAGmrp?format=jpg&name=orig)
Branches: [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Rafa_Schwinger-no-i-prefer-the-previous-angry-rhetoric-pls]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-NickChapmn-y-combinators-dont-have-valid-types-so-you-are]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-ETazou-i-understood-5-but-i-still-enjoyed-it]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-fecklesstit-u-the-best-man-keep-it-up]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-AutorRecomienda-fable-simplemente-hizo-de-placa-base-pitando-para]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-MancerAI_-its-lonely-sometimes-eh-im-excited-about-your]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-ThePremiseOfIt-theres-an-emergent-ai-psychosis-psychosis-in]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-willyrgf-wow-thats-impressive-best-argument-on-the-quality]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-o1lo01ol1o-do-you-allow-for-non-termination-on-total]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-WayneBrown6922-i-began-following-you-when-i-scrolled-across-an]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-MoisasADR-os-caras-acham-que-s-eles-s-o-superinteligentes]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-billylevin-this-is-so-cool-and-inspiring-not-that-i]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-taxilogiker-russel-antinomy]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-anghel4d-im-a-big-fan-of-interaction-combinators-and-i]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-mprado-loved-this-long-post-version-of-yours-you-should]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-trinitotolukeno-karpathy-said-he-had-ai-psychosis-for-a-while-and]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-yacineMTB-its-not-how-many-likes-you-get-its-likes-from-who]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-marunarh-most-of-you-cant-understand-my-posts-of-course]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Unblinking3Y3-bro-you-dont-hafta-grug-post-to-be-popular-with]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-okiwano-im-curious-what-comes-after-bend2-bend3-or-are]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-YgorIsm-texto-mt-bem-escrito-ficou-bem-mais-f-cil-de]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-0xAgathosDaimon-the-real-crime-is-those-idiots-not-knowing-who]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-pakatanatakata-lemme-aske-gpt-for-translating-your-hieroglyph]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-RizwanKhuharo-angry-ones-always-get-attention-on-internet]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-iabom-sigh-true-brother-we-smart-people-are-alone-no]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-RealSchmebulog-sorry-im-not-very-technical-did-you-mean-ai-good]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-VincentLejeune-the-more-ai-advances-the-more-we-need-very-high]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-LeeeeeeeeeT_-i-once-implemented-a-type-checker-for]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-zyansheep-in-my-language-im-trying-to-do-termination-by]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-SdoGtnepreS-dont-let-them-get-you-down-they-can-barely-see]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-habibislop-this-is-a-very-naive-and-ignorant-question-but]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-carmim_13-adorei-ler-esse-post-timo-poder-ler-de-voc-essas]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Foxfire1st-you-speak-simply-into-a-mixed-space-where-most]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-itisnotsavio-one-question-does-bend-have-an-unscoped-lambda]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-esa_was_taken-is-another-good-example-this-is-happening-to-both]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-An0o0o0o0n-im-not-going-to-read-all-that-im-happy-for-you-or]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-adelbucetta-sometimes-the-problem-isnt-explaining-something]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Juanpinha11-i-never-thought-you-had-ai-psychosis-but-the-fact]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Kinch_ahoy-i-got-interested-in-bend-for-its-prosaic]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Trevor62271128-i-cant-really-comprehend-what-bend2-will-be]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-donalfellows-if-you-have-a-system-that-provably-must-terminate]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-SoritesMinor-keep-posting-and-ill-keep-reading-or-trying-to]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-LusciousPear-i-love-this-shit]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-rom1504-very-cool-indeed-hard-but-important-to-pick-the]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Kmmer11133-i-enjoyed-reading-this-post-i-think-that-what]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-IncidentNoodle-this-is-a-great-post-i-cant-pretend-that-i-really]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-qonundrai-man-i-love-what-ur-doing-keep-going-one-of-the]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-noam_yy-i-presume-the-issue-was-in-duplication-inside-0]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-misterclayt0n-many-such-cases-https-x-com-misterclayt0n-status]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-altansukhbatbay-high-quality-post]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-EttoreMariotti-thanks]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-kylemarieb-this-write-up-was-really-well-done-thank-you-for]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-kekmaomaster-taelin-ive-been-following-you-since-the-beginning]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-mikejt4-youre-not-allowed-to-praise-fable-you-must-bag]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-dlbydq-these-guys-have-no-idea-what-theyre-talking-about]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-charlesthefool-do-people-not-study-lambda-calculus-in-college-or]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-0xbadface1-what-do-you-mean-by-arguments-to-recursion]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Pitometsu-impossibility-to-write-fast-interpreter-looks]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Pitometsu-qtt-approach-for-this-is-very-elegant-indeed]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-TheeKruger-i-think-this-is-a-super-legible-digestible]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-04-Court_Reinland-this-is-an-s-tier-post-1-it-proves-non-slop]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-_machi47-im-not-reading-all-that-but-damn-hope-it-works]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-real_philogy-dont-you-want-to-be-able-to-copy-lambdas-though]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-theodorvaryag-this-post-is-not-a-rebuttal-to-a-query-about-ai]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-IanCSU-sure-i-read-all-that]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-Siggis_Man-this-is-the-antidote-i-found-to-ai-psychosis-i]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-phtn458-bro-keep-posting-like-you-do-one-day-well-have]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-SinghSwapneil-are-languages-built-on-bend-incapable-of]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-SteveMoraco-legend]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-dan_tiema-i-didnt-expect-id-read-all-of-this-but-i-did-cant]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-eshear-to-someone-who-doesnt-understand-the-actual]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-Orbiter777-fable-is-educated-c]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-waefrebeorn-i-have-an-entire-math-proofs-section-in-my-maths]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-n3ovice-dont-try-to-market-yourself-youre-not-running-for]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-MadisonP94618-it-was-easy-to-read-and-i-think-i-understood-most]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-Snafxemp-loved-ur-rant-these-types-of-posts-deserves]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-nudistofdespair-you-gave-it-a-great-shot-thanks-for-an-engaging]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-KleeneAlgebra-i-disagree-on-the-consistency-is-enough-to-do]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-ant1m4tt3r-stupid-question-alert-in-bends-syntax-what-is-the]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-bewajitolulope-feels-like-the-precise-symbolic-analogue-of]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-05-JaredC1728-quality-over-quantity]], [[archive/threads/VictorTaelin/2026-07-04-sighs/2026-07-06-SGuergachi-hopefully-useful-data-point]]
