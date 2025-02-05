<img alt="Silkie -- defeasible logic reasoner logo, showing a stylized silkie chicken." src="Main.png" width="300" />

# silkie

This is a reasoner for defeasible logic, the Billington version and its team defeat/no team defeat, ambiguity propagation/blocking variants, with an option for loop detection. The goal here is to construct a fast reasoner tailored to applications related to robotics, in particular rapid commonsense-like reasoning to analyze perceptual results and (re)configure control and perception modules. Thus, silkie makes a distinction between "background" knowledge, which can be large, and situational knowledge, which usually is smaller in size, and lazily uses background knowledge only if called upon by inferences starting from situational knowledge. 

For a deeper overview of defeasible logic -- its proof theory and various features --, see [the PhD thesis of Ho Pun Lam, "On the Derivability of Defeasible Logic" (School of Information Technology and Electrical Engineering, The University of Queensland, 2012)](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=af3ab919ac4ac8b927c8f179b9ce52dba81285ad).

## Dependencies

Outside of standard python packages (and in the future, standard C headers), NONE. A deliberately small dependency footprint is part of the desiderata behind silkie. It should therefore be possible to run this on a very wide variety of platforms, OSes, python versions etc.

## Defeasible logic (a very short intro)

Defeasible logic is a rule-based inference system which allows reasoning with defaults and exceptions. That is, one can specify what would be reasonable to infer in some situation, absent further information, while also specifying how some of these conclusions may be changed or retracted if more information is available. The prototypical, simple example of a defeasible inference pattern would be the following:

"Birds (usually) fly."
"Penguins are birds."
"Penguins do not fly."
"Tweety is a penguin."

"Therefore, Tweety is a bird, but also, Tweety does not fly."

Note that one could rewrite the rules of the example so that a defeasible mechanism is not necessary: one can say birds, unless they are penguins, fly. However, it is possible that other exceptions exist -- sick birds do not fly, dead birds don't fly etc. There may also be exceptions to the exceptions -- penguins don't fly, but maybe they count as flying when boarding a plane.

Thus, insisting that a rule is always correct -- what in technical terms is called monotonic reasoning -- may result in very complicated rules that are not just difficult to develop and maintain, but also reason with. A rule that requires the checking of all of its exceptions will not be practical to use when the exceptions number in the millions.

Defeasible logic offers a mechanism that, essentially, updates the rules for you, and only performs the checks necessary in a particular situation: it will not check all exceptions, just those that could plausibly arise given the facts at hand. Further, unlike most non-monotonic inference systems, defeasible logic is computationally efficient because its method of inserting non-monotonicity can be evaluated quickly: when rules have conflicting conclusions, a priority relation between rules decides who wins.

(This in contrast with other non-monotonic inference methods that look for a "simplest model", i.e. a collection of conclusions that is in some sense minimal. This is typically expensive as a large set of possibilities has to be compared.)

More detailed presentations of the underlying mechanism are beyond the scope of this readme (but is provided in the documentation attached to the code). We will however look at examples of defeasible theories to see how these can be written. For the example of birds and penguins above, we have:

```
r1: bird(?x) => canFly(?x)
r2: penguin(?x) => bird(?x)
r3: penguin(?x) => -canFly(?x)

r3 > r1

penguin(tweety)
```

In the above, "=>" is a "defeasible implication" operator, saying that if we can believe the left side (the antecedent) of this operator, then we have reason to believe the right side (the consequent).

Both antecedent and consequent are conjunctions of terms. In this example, the antecedents only contain one term, but this need not be the case in general. Each term is a proposition, made up of a predicate and some arguments, such as "bird(?x)" (which says "some entity ?x is a bird") or "bird(tweety)" (which says the entity called tweety is a bird). Terms can be negated, here shown with the symbol "-". A term and its negation are always in conflict and cannot both be believed at once.

"r1", "r2" and so on are rule names, which are arbitrary and optional; the only requirement is that each rule, if it has a name, it has one different from all other rules. Variable names are useful to assert rule priority relations, such as "r3 > r1" which says that if both rules are applicable, i.e. their left hand sides are both believed, and their conclusions conflict (which in this example they do), then we only have reason to believe the conclusion of r3, and not r1.

Variables are denoted by question marks in front of a name, e.g. "?x"; a variable can be bound to any entity the reasoner is told about. To perform reasoning, rules have to be grounded, which means all variables in all terms in a rule are bound to -- ie. replaced by -- some entities. Binding a variable replaces all instances of that variable inside a rule to the same entity. There may be several bindings possible for a variable, which will generate several grounded versions of a rule.

Note that a variable exists only inside a rule. Two rules may have variables with the same name (as above) but these are different variables and may, in principle, be bound to different entities.

Through inference, defeasible logic arrives at conclusions of the following types:
* strictly provable: a term is provable with certainty; this is only possible via strict rules, from strict facts.
* defeasibly provable: a terms is defeasible provable, i.e. believed based on the available evidence, but may be overturned by further information.
* strictly unprovable: there is no chain of strict rules that can proceed from known facts to the term.
* defeasibly unprovable: there is no undefeated chain of defeasible rules that proceed from known facts to the term.

An important observation here is that while a term and its negation are never defeasibly provable together, it is possible for both of them to be defeasibly unprovable at once -- in such a case, we simply don't know either way.

## Supported features of the propositional defeasible logic language

* strict rules
* defeasible rules
* defeaters
* rule priorities
* one term per consequent
* conflict sets are pairs of a term and its negation

## Supported features for the predicate version

* at most two arguments per predicate
* all variables in the consequent must appear in antecedent (no existential rules)

## Using silkie

Silkie is intended as a library/package to be imported in a larger executable. It can read files in DFL format (a custom format, described below). Several examples show both some theory and fact files, and how to invoke silkie as a reasoning procedure.

One difference compared to other implementations is a separation for silkie between "background" and situation facts. Background facts can be many, but to speed up reasoning, these are only called upon if there is some chain of inference, starting from situation facts, which requires them.

### DFL format

Silkie uses a custom format based on the notational conventions from papers by Guido Governatori and his collaborators (such as Ho Pun Lam). While the same extension is used, some files are used as "theory" files describing rules, and others are "facts" files describing basic assertions taken as true at the beginning of inference.

For both theory and fact files, lines beginning with the "#" character are comments and ignored.

For theory files:

* non-comment lines are either rule assertions or priority assertions
* a priority assertion line has the format ruleName1 > ruleName2
* a rule assertion line has the format ruleName: term1, term2, ... OPERATOR termR
* rule names are optional, in which case the : character is also ommitted
* OPERATOR can be one of -> (strict rule), => (defeasible rule), or ~> (defeater: blocks conflicting conclusions, but does not impose its own)

## Work in progress

* a C implementation with Python wrapper
* existential rules
* multi-term consequents
* mutex sets (sets of terms where no two of them can be true together) for more complex conflict relations
* conflict sets (sets of terms that cannot be all true together) for more complex conflict relations
* "groupings" for conclusions (similar to modalities but do not stack)
* align serialization options to other rule based reasoners, in particular [Guido Governatori's implementation](https://github.com/gvdgdo/Defeasible-Deontic-Logic).

## Thanks

To [@larshurrelb](https://www.github.com/larshurrelb) for the logo.
