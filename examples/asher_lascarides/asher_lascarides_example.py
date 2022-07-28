import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as silkie

def reportTargetConclusions(theory, i2s, whitelist):
    conclusions = silkie.dflInference(theory)
    conclusions = silkie.idx2strConclusions(conclusions, i2s)
    for c in conclusions.defeasiblyProvable:
        if c[0] in whitelist:
            print(c)

def main():
    rules = silkie.loadDFLRules('./rules.dfl')
    factsNarration = silkie.loadDFLFacts('./facts_base.dfl')
    factsNarration = silkie.loadDFLFacts('./facts_example_narration.dfl', factsNarration)
    factsCausation = silkie.loadDFLFacts('./facts_base.dfl')
    factsCausation = silkie.loadDFLFacts('./facts_example_causation.dfl', factsCausation)
    
    theoryNarration, s2iNarration, i2sNarration, theoryStrNarration = silkie.buildTheory(rules,factsNarration,{},debugTheory=True)
    theoryCausation, s2iCausation, i2sCausation, theoryStrCausation = silkie.buildTheory(rules,factsCausation,{},debugTheory=True)
    
    for scnSpec in [(theoryNarration, i2sNarration, 'Narration: Max stood up. John greeted him'), (theoryCausation, i2sCausation, 'Causation: Max fell. John pushed him')]:
        theory, i2s, msg = scnSpec
        print('==========\n%s' % msg)
        reportTargetConclusions(theory, i2s, ['narration', '-narration', 'explanation', '-explanation'])

if __name__ == '__main__':
    main()
