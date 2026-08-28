---
title: "One of the biggest misunderstandings I see about quaternions is their dimensionality."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/1482866185490161667"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "1482866185490161667"
date: 2022-01-17
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "One of the biggest misunderstandings I see about quaternions is their dimensionality."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/1482866185490161667
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2022-01-17 00:03:43

## Thread

**1/** **@EricLengyel** ^1482866185490161667

One of the biggest misunderstandings I see about quaternions is their dimensionality. Despite having 4 components, quaternions are three dimensional things that live and work in 3D space. 1/2

**2/** **@EricLengyel** ^1482866187092447233

• Quaternions arise as the geometric products of 3D vectors.
• These produce sums of scalars and 3D bivectors.
• That's 4 numbers per quaternion, but it's a combination of things that exist in the 3D geometric algebra.
• Each quaternion has an equivalent 3×3 matrix, not 4×4.

**3/** **@gottfired** ^1483900885721882627

**@EricLengyel**

That’s a bit too simplified. While normalized quaternions can be interpreted as rotation in Euclidean space. Quaternions are a 4 dimensional vector space. They are also a skew field which was the original interpretation of Hamilton as extension of real numbers.

**4/** **@EricLengyel** ^1483902691075977217

**@gottfired**

Yes, quaternions form an abstract 4D vector space, but that is not geometrically significant. Each of the components of a quaternion (and more generally, a 3D multivector) is one of 8 possible combinations of 3 *physical dimensions*. In that way, quaternions are undoubtedly 3D.

**5/** **@gottfired** ^1484553067773190149

**@EricLengyel**

I guess best comparison would be complex numbers which are a field. Normalized they are one dimensional representing 2d rotations. But that’s just a geometric interpretation. Complex numbers are useful in maths/physics for many other reasons.

**6/** **@gottfired** ^1484553117131808770

**@EricLengyel**

Same for quarternions. Geometry is just one subset and only for normalized quats which repr 3d rotations.

**7/** **@EricLengyel** ^1485149260953780225

**@gottfired**

Quaternions are homogeneous and do not need to be normalized, though it is often convenient to do so. In general, a quaternion of any magnitude transforms v with qvq⁻¹, but if q is unit length, then this simplifies to qvq̃ (where ~ is the reverse / conjugate).

**8/** **@gottfired** ^1485162418422620162

**@EricLengyel**

That’s exactly my point. If you explain complex numbers you’d never say that C only has 1 dof. Only as 2d rots this interpretation makes sense. But C is used almost exclusively for other stuff than representing rotations where a simple angle is good enough.

**9/** **@gottfired** ^1485163979974533123

**@EricLengyel**

But quats are useful outside of their convenience in 3d gfx as better Euler angles without gimbal lock. Same as C is very useful arguably way more so than the rotation interprets which afaik is hardly used.
