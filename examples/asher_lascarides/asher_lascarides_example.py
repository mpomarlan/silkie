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
    factsDudley = silkie.loadDFLFacts('./facts_base.dfl')
    factsDudley = silkie.loadDFLFacts('./facts_example_dudley.dfl', factsDudley)
    factsAwkward = silkie.loadDFLFacts('./facts_example_awkward_narration.dfl')
    
    theoryNarration, s2iNarration, i2sNarration, theoryStrNarration = silkie.buildTheory(rules,factsNarration,{},debugTheory=True)
    theoryCausation, s2iCausation, i2sCausation, theoryStrCausation = silkie.buildTheory(rules,factsCausation,{},debugTheory=True)
    theoryElaboration, s2iElaboration, i2sElaboration, theoryStrElaboration = silkie.buildTheory(rules,factsElaboration,{},debugTheory=True)
    theoryBackground, s2iBackground, i2sBackground, theoryStrBackground = silkie.buildTheory(rules,factsBackground,{},debugTheory=True)
    theoryResult, s2iResult, i2sResult, theoryStrResult = silkie.buildTheory(rules,factsResult,{},debugTheory=True)
    theoryIncoherent, s2iIncoherent, i2sIncoherent, theoryStrIncoherent = silkie.buildTheory(rules,factsIncoherent,{},debugTheory=True)
    theoryDudley, s2iDudley, i2sDudley, theoryStrDudley = silkie.buildTheory(rules,factsDudley,{},debugTheory=True)
    theoryAwkward, s2iAwkward, i2sAwkward, theoryStrAwkward = silkie.buildTheory(rules,factsAwkward,{},debugTheory=True)
    
    for scnSpec in [(theoryNarration, i2sNarration, 'Narration: Max stood up. John greeted him.'), (theoryCausation, i2sCausation, 'Causation: Max fell. John pushed him.'), (theoryElaboration, i2sElaboration, 'Elaboration: The council built the bridge. The architect drew up the plans.'), (theoryBackground, i2sBackground, 'Background: Max opened the door. The room was dark.'), (theoryResult, i2sResult, 'Result: Max switched off the light. The room was dark.'), (theoryIncoherent, i2sIncoherent, 'Incoherent: Max won the race. Max was home. (expecting no positive relation identified here.)'), (theoryDudley, i2sDudley, 'Dudley Doorite: The bimetallic strip changed shape. The temperature fell.'), (theoryAwkward, i2sAwkward, 'Awkward narration: Max stood up. John greeted him. Max got up slowly.')]:
        theory, i2s, msg = scnSpec
        print('==========\n%s' % msg)
        reportTargetConclusions(theory, i2s, ['narration', '-narration', 'explanation', '-explanation', 'elaboration', '-elaboration', 'background', '-background', 'result', '-result'])

    factsEvening = silkie.loadDFLFacts('./facts_example_discourse_pop.dfl')
    theoryEvening, s2iEvening, i2sEvening, theoryStrEvening = silkie.buildTheory(rules,factsEvening,{},debugTheory=True)
    print('==========\n%s' % "Discourse pop: Guy had a lovely evening. He had a meal. He ate salmon. He ate cheese. He won a competition.")
    reportTargetConclusions(theoryEvening, i2sEvening, ['narration', 'explanation', 'elaboration', 'background', 'result'])

    factsBoss = silkie.loadDFLFacts('./facts_example_boss.dfl')
    theoryBoss, s2iBoss, i2sBoss, theoryStrBoss = silkie.buildTheory(rules,factsBoss,{},debugTheory=True)
    print('==========\n%s' % "Boss example: John arrived late for work. He had taken the bus. He had totalled his car. His boss summoned him to his office.")
    reportTargetConclusions(theoryBoss, i2sBoss, ['narration', 'explanation', 'elaboration', 'background', 'result'])

    factsBossPromotion = silkie.loadDFLFacts('./facts_example_boss.dfl')
    factsBossPromotion = silkie.loadDFLFacts('./facts_example_boss_promotion.dfl', factsBossPromotion)
    theoryBossPromotion, s2iBossPromotion, i2sBossPromotion, theoryStrBossPromotion = silkie.buildTheory(rules,factsBossPromotion,{},debugTheory=True)
    print('==========\n%s' % "Boss example, with an extra narration: John arrived late for work. He had taken the bus. He had totalled his car. His boss summoned him to his office. John's promotion chances seemed low.")
    reportTargetConclusions(theoryBossPromotion, i2sBossPromotion, ['narration', 'explanation', 'elaboration', 'background', 'result'])

    factsBossIncoherent = silkie.loadDFLFacts('./facts_example_boss.dfl')
    factsBossIncoherent = silkie.loadDFLFacts('./facts_example_boss_incoherent.dfl', factsBossIncoherent)
    theoryBossIncoherent, s2iBossIncoherent, i2sBossIncoherent, theoryStrBossIncoherent = silkie.buildTheory(rules,factsBossIncoherent,{},debugTheory=True)
    print('==========\n%s' % "Boss example, with an extra sentence that cannot be coherently related: John arrived late for work. He had taken the bus. He had totalled his car. His boss summoned him to his office. John had brought his car to a garage.")
    reportTargetConclusions(theoryBossIncoherent, i2sBossIncoherent, ['narration', 'explanation', 'elaboration', 'background', 'result'])

    factsGarage = silkie.loadDFLFacts('./facts_example_garage.dfl')
    theoryGarage, s2iGarage, i2sGarage, theoryStrGarage = silkie.buildTheory(rules,factsGarage,{},debugTheory=True)
    print('==========\n%s' % "Garage example: John arrived late for work. He had taken the bus. He had totalled his car. John had brought his car to the garage.")
    reportTargetConclusions(theoryGarage, i2sGarage, ['narration', 'explanation', 'elaboration', 'background', 'result'])

if __name__ == '__main__':
    main()

