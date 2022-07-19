import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as silkie

def reportTargetConclusions(theory, i2s, whitelist):
    conclusions = silkie.dflInference(theory)
    conclusions = silkie.idx2strConclusions(conclusions, i2s)
    for c in conclusions.defeasiblyProvable:
        if (c[0] in whitelist) and (c[1] != c[2]):
            print(c)

def main():
    rules = silkie.loadDFLRules('./rules.dfl')

    factsRoadTripPath = silkie.loadDFLFacts('./facts_roadtrip_base.dfl')
    factsRoadTripPath = silkie.loadDFLFacts('./facts_roadtrip_path.dfl', factsRoadTripPath)
    factsRoadTripMedium = silkie.loadDFLFacts('./facts_roadtrip_base.dfl')
    factsRoadTripMedium = silkie.loadDFLFacts('./facts_roadtrip_path.dfl', factsRoadTripMedium)
    factsRoadTripMedium = silkie.loadDFLFacts('./facts_roadtrip_medium.dfl', factsRoadTripMedium)
    factsRoadTripContainer = silkie.loadDFLFacts('./facts_roadtrip_base.dfl')
    factsRoadTripContainer = silkie.loadDFLFacts('./facts_roadtrip_path.dfl', factsRoadTripContainer)
    factsRoadTripContainer = silkie.loadDFLFacts('./facts_roadtrip_medium.dfl', factsRoadTripContainer)
    factsRoadTripContainer = silkie.loadDFLFacts('./facts_roadtrip_container.dfl', factsRoadTripContainer)
    factsBlocksHenceProtects = silkie.loadDFLFacts('./facts_uses_base.dfl')
    factsBlocksHenceProtects = silkie.loadDFLFacts('./facts_uses_blocks_hence_protects.dfl', factsBlocksHenceProtects)
    factsProtectsHenceBlocks = silkie.loadDFLFacts('./facts_uses_base.dfl')
    factsProtectsHenceBlocks = silkie.loadDFLFacts('./facts_uses_protects_hence_blocks.dfl', factsProtectsHenceBlocks)

    theory_roadTripPath, s2i_roadTripPath, i2s_roadTripPath, theoryStr_roadTripPath = silkie.buildTheory(rules,factsRoadTripPath,{},debugTheory=True)
    theory_roadTripMedium, s2i_roadTripMedium, i2s_roadTripMedium, theoryStr_roadTripMedium = silkie.buildTheory(rules,factsRoadTripMedium,{},debugTheory=True)
    theory_roadTripContainer, s2i_roadTripContainer, i2s_roadTripContainer, theoryStr_roadTripContainer = silkie.buildTheory(rules,factsRoadTripContainer,{},debugTheory=True)

    theory_blocksHenceProtects, s2i_blocksHenceProtects, i2s_blocksHenceProtects, theoryStr_blocksHenceProtects = silkie.buildTheory(rules,factsBlocksHenceProtects,{},debugTheory=True)
    theory_protectsHenceBlocks, s2i_protectsHenceBlocks, i2s_protectsHenceBlocks, theoryStr_protectsHenceBlocks = silkie.buildTheory(rules,factsProtectsHenceBlocks,{},debugTheory=True)
    
    for scnSpec in [(theory_roadTripPath, i2s_roadTripPath, 'Road trip, "path"'), (theory_roadTripMedium, i2s_roadTripMedium, 'Road trip, "medium"'), (theory_roadTripContainer, i2s_roadTripContainer, 'Road trip, "container"')]:
        theory, i2s, msg = scnSpec
        print('==========\n%s' % msg)
        reportTargetConclusions(theory, i2s, ['passThrough', '-passThrough', 'canAvoid', '-canAvoid'])

    print('==========\n%s' % "Container uses: blocks hence protects")
    reportTargetConclusions(theory_blocksHenceProtects, i2s_blocksHenceProtects, ['protectedFrom', '-protectedFrom'])
    print('==========\n%s' % "Container uses: protects hence blocks")
    reportTargetConclusions(theory_protectsHenceBlocks, i2s_protectsHenceBlocks, ['blocks', '-blocks'])
    

if __name__ == "__main__":
    main()

