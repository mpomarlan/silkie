# Proof theory for defeasible logic

By proof theory we mean some procedure that converts premises into conclusions. The basic approach for defeasible logic is to consider a "provability chain", and to define rules for when conclusions can be added to it. In defeasible logic, conclusions can be of the forms:

* +Dx: x is a strictly provable statement, i.e. it has been established with certainty and no further information will change it
* -Dx: x is not strictly provable; note that this does not mean that x's negation is strictly provable however -- both x and its negation could be -D
* +dx: x is a defeasibly provable statement, i.e. it has been established based on available evidence but more information may result in it being overturned
* -dx: x is not defeasible provable. As before, both a statement x and its negation may be -d.

Defeasible logic has several mathematically nice properties, which are proved in the literature but we will not revisit the proofs here. Let -x be the negation of x. Then the properties of defeasible logic are:

* defeasible consistency: unless strict rules insert inconsistency, it will never be inferred that both +dx and +d-x hold for any x.
* coherence: it will never be inferred that both +Dx and -Dx hold, nor will it ever be inferred that both +dx and -dx hold.

Further, assuming a transitive rule priority relation, a few more useful properties can be inferred:
* Cut: if a defeasible theory and a set of facts allows the inferring of conclusion q, and the same theory and the set of facts plus q allows inferring a conclusion p, then the theory and the original set of facts also allows inferring p.
* Cautious Monotony: if a defeasible theory and a set of facts allows inferring conclusion q, and the same theory and facts also allows inferring p, then the same theory and facts plus q allows inferring p.

We will now present the rules to add conclusions to a provability chain. These rules depend on the features required of the defeasible logic, thus there will be several subsections below. However, all defeasible logics share the same proof theory for strict rules.

A conclusion +Dx can be added to the provability chain if:

```
x is a fact OR
there exists a strict rule r with consequent x such that
    for all p in the antecedent of r, +Dp is already on the provability chain
```

A conclusion -Dx can be added to the provability chain if:
```
x is not a fact AND
for all strict rules r with consequent x,
    there is p in the antecedent of r such that -Dp is already on the provability chain
```

The flavors of defeasible logic below refer to how two questions are to be tackled by the logic. These are:

* ambiguity: if a conclusion cannot be established either way, does that impact further inferences that may depend on the conclusion?
* what counts as a case for a conclusion: are a team of rules allowed to offer support together, or must there be some rule that could establish the conclusion alone?

Ambiguity of conclusions can arise in defeasible logic when a conclusion has both applicable supporting rules and applicable opposing rules, without there being a clear cut priority between them. In such cases, the logic is always skeptical, and will not take sides on the conclusion either way. However, further inferences may depend on the ambiguous conclusion. Consider the following example:

Quakers are (usually) pacifists
Republicans are (usually) not pacifists
Pacifists do not continue wars
Republicans (usually) continue wars
Nixon is both a Quaker and a Republican

Without any priority between the statements above, all versions of defeasible logic will agree that it is impossible to tell whether Nixon is a pacifist or not, i.e. the pacifist conclusion is ambiguous.

However, depending on their stance on ambiguity, we may have:
* ambiguity blocking: we have no reason to surmise about Nixon's pacifism either way, but we have some evidence that as a Republican he will continue a war, therefore we conclude he will continue a war.
* ambiguity propagation: we have no reason to surmise about Nixon's pacifism either way, so we must keep also refrain from any inference that depends on this conclusion as well. Thus, we cannot conclude either way about Nixon continuing a war.

Depending on application, either version may be more appropriate.

## Ambiguity blocking, individual defeat

We may add a +dx conclusion to the provability chain if:

```
+Dx is on the provability chain already OR
there exists a defeasible (or strict) rule r with conclusion x, such that
    for all p in the antecedent of r, +dp is on the provability chain already AND
        +D-x is NOT on the provability chain already AND
        for every rule s that opposes x, we have
            there is some q in the antecedent of s such that -dq is on the provability chain OR
            r > s
```

We may add a -dx conclusion to the provability chain if:

```
-Dx is on the provability chain already AND
for all rules supporting x,
    there exists p in the antecedent of r such that -dp is on the provability chain already OR
        +D-x is on the provability chain already OR
        there exists a rule s opposing x such that
            for all q in the antecedent of s, +dq is on the provability chain already AND
            it is not the case that r > s
```

## Ambiguity blocking, team defeat

We may add a +dx conclusion to the provability chain if:

```
+Dx is on the provability chain already OR
there exists a defeasible (or strict) rule r with conclusion x, such that
    for all p in the antecedent of r, +dp is on the provability chain already AND
        +D-x is NOT on the provability chain AND
        for every rule s that opposes x, we have
            there is some q in the antecedent of s such that -dq is on the provability chain OR
            there is some rule r' supporting x such that for all p' in the antecedent of r', +dp' is on the provability chain AND r' > s
```

We may add a -dx conclusion to the provability chain if:

```
-Dx is on the provability chain already AND
for all rules supporting x,
    there is p in the antecedent of r such that -dp is on the provability chain already OR
        +D-x is on the provability chain already OR
        there is some rule s that opposes x such that
            for all q in the antecedent of s, +dq is on the provability chain already AND
            for all rules r' supporting x, either there is some p' in the antecedent of r' such that -dp' is on the provability chain OR it is not the case that r' > s
```
