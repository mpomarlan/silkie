import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as silkie

def reportTargetConclusions(theory, i2s, whitelist):
    conclusions = silkie.dflInference(theory)
    conclusions = silkie.idx2strConclusions(conclusions, i2s)
    for c in sorted(list(conclusions.defeasiblyProvable)):
        if c[0] in whitelist:
            print(c)

def main():
    rules = silkie.loadDFLRules('./rules.dfl')
    backgroundFacts = {}#silkie.loadDFLFacts('./backgroundFacts.dfl')
    facts = silkie.loadDFLFacts('./facts.dfl')
    
    theory, s2i, i2s, theoryStr = silkie.buildTheory(rules,facts,backgroundFacts,debugTheory=True)
    
    for scnSpec in [(theory, i2s, 'Pouring')]:
        theory, i2s, msg = scnSpec
        print('==========\n%s' % msg)
        #reportTargetConclusions(theory, i2s, ['E_byProcess', 'E_threatenedBy', 'E_byGoal', 'E_hasRole', 'hasRole', 'hasFiller', 'preferredTrajector', 'preferredRelatum'])
        reportTargetConclusions(theory, i2s, ['isA', 'hasTrajector', 'hasExcluder', 'hasExcludee', 'hasSource', 'hasDestination', 'Q_position', 'Q_velocity', 'Q_opening'])
        #reportTargetConclusions(theory, i2s, ['follows', 'combine'])

if __name__ == '__main__':
    main()
