import argparse
import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as silkie

try:
    import matplotlib.pyplot as plt
except:
    pass

def reportTargetConclusions(theory, i2s, whitelist,plotWindow=None):
    if plotWindow is not None:
        plt.cla()
    conclusions = silkie.dflInference(theory,i2s=i2s,plotWindow=plotWindow)
    conclusions = silkie.idx2strConclusions(conclusions, i2s)
    for c in conclusions.defeasiblyProvable:
        if c[0] in whitelist:
            print(c)
    if plotWindow is not None:
        plt.draw()
        plt.pause(0.001)
        input("Press ENTER to continue")

def main():
    parser = argparse.ArgumentParser(prog="flammability_example", description="Run an example for the silkie reasoner.", epilog="")
    parser.add_argument('-v', '--visualize', action='store_true', help='Enable visualization')
    arguments = parser.parse_args()
    doVisualize = arguments.visualize
    
    plotWindow = None
    if doVisualize:
        fig, plotWindow = plt.subplots(figsize=(7,7))
    
    rulesO1 = silkie.loadDFLRules('./rules_option1.dfl')
    rulesO2 = silkie.loadDFLRules('./rules_option2.dfl')
    factsFireO2 = silkie.loadDFLFacts('./facts_sandpile.dfl')
    factsFireO2 = silkie.loadDFLFacts('./facts_fireO2.dfl', factsFireO2)
    factsFireClF3 = silkie.loadDFLFacts('./facts_sandpile.dfl')
    factsFireClF3 = silkie.loadDFLFacts('./facts_fireClF3.dfl', factsFireClF3)
    factsBothFires = silkie.loadDFLFacts('./facts_sandpile.dfl')
    factsBothFires = silkie.loadDFLFacts('./facts_fireO2.dfl', factsBothFires)
    factsBothFires = silkie.loadDFLFacts('./facts_fireClF3.dfl', factsBothFires)
    
    theoryO2_opt1, s2iO2_opt1, i2sO2_opt1, theoryStrO2_opt1 = silkie.buildTheory(rulesO1,factsFireO2,{},debugTheory=True)
    theoryClF3_opt1, s2iClF3_opt1, i2sClF3_opt1, theoryStrClF3_opt1 = silkie.buildTheory(rulesO1,factsFireClF3,{},debugTheory=True)
    theoryBoth_opt1, s2iBoth_opt1, i2sBoth_opt1, theoryStrBoth_opt1 = silkie.buildTheory(rulesO1,factsBothFires,{},debugTheory=True)
    
    theoryO2_opt2, s2iO2_opt2, i2sO2_opt2, theoryStrO2_opt2 = silkie.buildTheory(rulesO2,factsFireO2,{},debugTheory=True)
    theoryClF3_opt2, s2iClF3_opt2, i2sClF3_opt2, theoryStrClF3_opt2 = silkie.buildTheory(rulesO2,factsFireClF3,{},debugTheory=True)
    theoryBoth_opt2, s2iBoth_opt2, i2sBoth_opt2, theoryStrBoth_opt2 = silkie.buildTheory(rulesO2,factsBothFires,{},debugTheory=True)
    
    for scnSpec in [(theoryO2_opt1, i2sO2_opt1, 'Option 1, O2 fire'), (theoryClF3_opt1, i2sClF3_opt1, 'Option 1, ClF3 fire'), (theoryBoth_opt1, i2sBoth_opt1, 'Option 1, Both fires'), (theoryO2_opt2, i2sO2_opt2, 'Option 2, O2 fire'), (theoryClF3_opt2, i2sClF3_opt2, 'Option 2, ClF3 fire'), (theoryBoth_opt2, i2sBoth_opt2, 'Option 2, Both fires')]:
        theory, i2s, msg = scnSpec
        print('==========\n%s' % msg)
        
        reportTargetConclusions(theory, i2s, ['protectedFrom', '-protectedFrom', 'hasDisp', '-hasDisp'], plotWindow=plotWindow)

if __name__ == '__main__':
    main()
