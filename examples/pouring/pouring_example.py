import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as reasoner

def reportTargetConclusions(theory, i2s, whitelist):
    conclusions = reasoner.dflInference(theory)
    conclusions = reasoner.idx2strConclusions(conclusions, i2s)
    for c in conclusions.defeasiblyProvable:
        if (c[0] in whitelist) and (c[1] != c[2]):
            print(c)

def main():
    rules = reasoner.loadDFLRules('./rules.dfl')

    factsPour = reasoner.loadDFLFacts('./facts_pour.dfl')
    factsPour = reasoner.loadDFLFacts('./facts_opening.dfl', factsPour)
    factsPour = reasoner.loadDFLFacts('./facts_spill.dfl', factsPour)

    theory_canPour, s2i_canPour, i2s_canPour, theoryStr_canPour = \
    reasoner.buildTheory(rules,factsPour,{},debugTheory=True)

    print(theoryStr_canPour)
    reportTargetConclusions(theory_canPour, i2s_canPour, ['canPourTo'])







if __name__ == "__main__":
    main()


