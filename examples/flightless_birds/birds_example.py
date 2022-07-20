import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as silkie

import time

def runExample(mode=None,exceptions=10, iterations=1):
    if mode not in ['fast', 'slow', 'reified_exceptions']:
        mode = 'fast'
    with open("rules.dfl","w") as outfile:
        _ = outfile.write("0: bird(?x) => flies(?x)\n")
        if 'fast' == mode:
            for k in range(exceptions):
                _ = outfile.write("%d: P%d(?x) => -flies(?x)\n%d > 0\n" % (k+1,k+1,k+1))
        elif 'slow' == mode:
            for k in range(exceptions):
                _ = outfile.write("%d: bird(?x), P%d(?x) => -flies(?x)\n%d > 0\n" % (k+1,k+1,k+1))
        elif 'reified_exceptions':
            _ = outfile.write("X: bird(?x), Exception(?x) => -flies(?x)\nX > 0\n")
            for k in range(exceptions):
                _ = outfile.write("%d: P%d(?x) => Exception(?x)\n" % (k+1,k+1))
    if 1 < iterations:
        rules = silkie.loadDFLRules('rules.dfl')
        factsWillFly = silkie.loadDFLFacts('facts_will_fly.dfl')
        factsWontFly = silkie.loadDFLFacts('facts_wont_fly.dfl')
        start_benchmark = time.perf_counter()
        for k in range(iterations):
            theoryF, s2iF, i2sF, theoryStrF = silkie.buildTheory(rules,factsWillFly,{},debugTheory=True)
            theoryNF, s2iNF, i2sNF, theoryStrNF = silkie.buildTheory(rules,factsWontFly,{},debugTheory=True)
            conclusionsF = silkie.dflInference(theoryF)
            conclusionsF = silkie.idx2strConclusions(conclusionsF, i2sF)
            conclusionsNF = silkie.dflInference(theoryNF)
            conclusionsNF = silkie.idx2strConclusions(conclusionsNF, i2sNF)
        end_benchmark = time.perf_counter()
        print('Benchmark in mode \"%s\" with %d exceptions for %d iterations: %f\n\n' % (str(mode), exceptions, iterations, end_benchmark-start_benchmark))
        return       
    start_loadRules = time.perf_counter()
    rules = silkie.loadDFLRules('rules.dfl')
    end_loadRules = time.perf_counter()
    factsWillFly = silkie.loadDFLFacts('facts_will_fly.dfl')
    factsWontFly = silkie.loadDFLFacts('facts_wont_fly.dfl')
    start_buildTheory = time.perf_counter()
    theoryF, s2iF, i2sF, theoryStrF = silkie.buildTheory(rules,factsWillFly,{},debugTheory=True)
    theoryNF, s2iNF, i2sNF, theoryStrNF = silkie.buildTheory(rules,factsWontFly,{},debugTheory=True)
    end_buildTheory = time.perf_counter()
    start_dflInference = time.perf_counter()
    conclusionsF = silkie.dflInference(theoryF)
    conclusionsF = silkie.idx2strConclusions(conclusionsF, i2sF)
    conclusionsNF = silkie.dflInference(theoryNF)
    conclusionsNF = silkie.idx2strConclusions(conclusionsNF, i2sNF)
    end_dflInference = time.perf_counter()
    print('\"%s\" theory with %d exceptions' % (str(mode), exceptions))
    print('Loaded rules in %f sec' % (end_loadRules - start_loadRules))
    print('Built theories in %f sec' % (end_buildTheory - start_buildTheory))
    print('Ran DFL inference in %f sec' % (end_dflInference - start_dflInference))
    print('Theory (will-fly version):\n%s\n\tConclusions:\n%s\n\nTheory (will-not-fly version)\n%s\n\tConclusions:\n%s\n' % (theoryStrF, str(conclusionsF.defeasiblyProvable), theoryStrNF, str(conclusionsNF.defeasiblyProvable)))
    os.remove('rules.dfl')

def main():
    runExample(mode='slow', exceptions=10, iterations=1000)
    runExample(mode='slow', exceptions=100, iterations=1000)
    runExample(mode='fast', exceptions=10, iterations=1000)
    runExample(mode='fast', exceptions=100, iterations=1000)
    runExample(mode='reified_exceptions', exceptions=10, iterations=1000)
    runExample(mode='reified_exceptions', exceptions=100, iterations=1000)
    runExample(mode='slow',exceptions=10)
    runExample(mode='slow',exceptions=100)
    runExample(mode='slow',exceptions=1000)
    runExample(mode='slow',exceptions=10000)
    runExample(mode='slow',exceptions=100000)
    runExample(mode='slow',exceptions=1000000)
    runExample(mode='fast',exceptions=10)
    runExample(mode='fast',exceptions=100)
    runExample(mode='fast',exceptions=1000)
    runExample(mode='fast',exceptions=10000)
    runExample(mode='fast',exceptions=100000)
    runExample(mode='fast',exceptions=1000000)
    runExample(mode='reified_exceptions',exceptions=10)
    runExample(mode='reified_exceptions',exceptions=100)
    runExample(mode='reified_exceptions',exceptions=1000)
    runExample(mode='reified_exceptions',exceptions=10000)
    runExample(mode='reified_exceptions',exceptions=100000)
    runExample(mode='reified_exceptions',exceptions=1000000)


if __name__ == "__main__":
    main()

