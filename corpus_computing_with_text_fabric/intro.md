Introduction
============

Text-Fabric is a model for representing text and annotations in such a way
that you can do computational research on your materials of interest.
It helps you to turn your research results into new annotations and share
them for usage by others.
It will gently nudge you to store all data involved in your research in such a
way that it is 
[FAIR](https://www.go-fair.org/fair-principles/),
i.e. Findable, Accessible, Interoperable, and Reusable.

Text-Fabric uses a minimalistic (XML-free) representation of corpus data and defines an API for that.
This API will let you navigate your data, search it, display it and recombine it.
Moreover, it will help you to deliver your data in any form you need to feed your favorite analysis tools.

Working with Text-Fabric is a practice, and the best way to learn a practice is not
by reading about it, but by doing it.
The problem is that (ancient) text corpora are works at the center of centuries of culture and study,
during which unique ways of representation and interpretation have been developed.

Yet, when we study those corpora now, by means of computational techniques, it turns out that there is
quite a bit of common ground between the corpora.
Whether you study the Hebrew Bible or the Arabic Q'uran or the Akkadian Clay Tablets, you find yourself
in need to search, browse, count, cluster, and categorize the elements of your texts.

Text-Fabric itself is abstract. Nothing in its code is geared to a specific corpus, a specific language,
a specific kind of annotation. It is this abstraction that lies at the heart of its power and simplicity.
But it also makes it more difficult to learn for people that are intimate with their corpus of interest but
less so with the concepts of computation and data modeling.

That's why we provide complete sets of tutorials for a dozen or so wildly different corpora,
from very old Uruk (4000 BC) to modern Neo Aramaic, with the Bible somewhere in between, not to speak of a big
swath of (classical and patristic) Greek Literature and hundreds of letters between Dutch colonial agents
and their superiors at home. 

In computer science we adhere the noble practice of DRY: don't repeat yourself.
Programming languages have wonderful devices to extract the common parts from your code and state them once
and for all.
For explanatory purposes, however, DRY is the wrong kind of efficiency.
We'll repeat lavishly, because we also believe in unity of context: whe you learn new things, we like to
do so in a consistent context: our corpus of interest.
