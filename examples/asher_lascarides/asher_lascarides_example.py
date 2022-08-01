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
    factsElaboration = silkie.loadDFLFacts('./facts_base.dfl')
    factsElaboration = silkie.loadDFLFacts('./facts_example_elaboration.dfl', factsElaboration)
    factsBackground = silkie.loadDFLFacts('./facts_base.dfl')
    factsBackground = silkie.loadDFLFacts('./facts_example_background.dfl', factsBackground)
    factsResult = silkie.loadDFLFacts('./facts_base.dfl')
    factsResult = silkie.loadDFLFacts('./facts_example_result.dfl', factsResult)
    factsIncoherent = silkie.loadDFLFacts('./facts_base.dfl')
    factsIncoherent = silkie.loadDFLFacts('./facts_example_incoherent.dfl', factsIncoherent)
    
    theoryNarration, s2iNarration, i2sNarration, theoryStrNarration = silkie.buildTheory(rules,factsNarration,{},debugTheory=True)
    theoryCausation, s2iCausation, i2sCausation, theoryStrCausation = silkie.buildTheory(rules,factsCausation,{},debugTheory=True)
    theoryElaboration, s2iElaboration, i2sElaboration, theoryStrElaboration = silkie.buildTheory(rules,factsElaboration,{},debugTheory=True)
    theoryBackground, s2iBackground, i2sBackground, theoryStrBackground = silkie.buildTheory(rules,factsBackground,{},debugTheory=True)
    theoryResult, s2iResult, i2sResult, theoryStrResult = silkie.buildTheory(rules,factsResult,{},debugTheory=True)
    theoryIncoherent, s2iIncoherent, i2sIncoherent, theoryStrIncoherent = silkie.buildTheory(rules,factsIncoherent,{},debugTheory=True)
    
    for scnSpec in [(theoryNarration, i2sNarration, 'Narration: Max stood up. John greeted him.'), (theoryCausation, i2sCausation, 'Causation: Max fell. John pushed him.'), (theoryElaboration, i2sElaboration, 'Elaboration: The council built the bridge. The architect drew up the plans.'), (theoryBackground, i2sBackground, 'Background: Max opened the door. The room was dark.'), (theoryResult, i2sResult, 'Result: Max switched off the light. The room was dark.'), (theoryIncoherent, i2sIncoherent, 'Incoherent: Max won the race. Max was home. (expecting no positive relation identified here.)')]:
        theory, i2s, msg = scnSpec
        print('==========\n%s' % msg)
        reportTargetConclusions(theory, i2s, ['narration', '-narration', 'explanation', '-explanation', 'elaboration', '-elaboration', 'background', '-background', 'result', '-result'])

    factsEvening = silkie.loadDFLFacts('./facts_example_discourse_pop.dfl')
    theoryEvening, s2iEvening, i2sEvening, theoryStrEvening = silkie.buildTheory(rules,factsEvening,{},debugTheory=True)
    print('==========\n%s' % "Discourse pop: Guy had a lovely evening. He had a meal. He ate salmon. He ate cheese. He won a competition.")
    reportTargetConclusions(theoryEvening, i2sEvening, ['narration', 'explanation', 'elaboration', 'background', 'result'])


if __name__ == '__main__':
    main()

