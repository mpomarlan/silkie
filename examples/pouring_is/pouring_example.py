import os
import sys

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath,'../../src'))

import silkie.silkie as silkie

def reportTargetConclusions(theory, i2s, whitelist, inds=None, bl=None):
    if inds is None:
        inds = []
    if bl is None:
        bl = []
    conclusions = silkie.dflInference(theory)
    conclusions = silkie.idx2strConclusions(conclusions, i2s)
    for c in sorted(list(conclusions.defeasiblyProvable)):
        if c[0] in whitelist:
            print(c)
    for i in sorted(inds):
        print(' -- %s results' % i)
        for c in sorted(list(conclusions.defeasiblyProvable)):
            if (not c[0].startswith('-')) and (c[0] not in bl) and (i in c[1:]):
                print(c)

def main():
    rules = silkie.loadDFLRules('./rules.dfl')
    # TODO: the loading function is in-place. Should have the option to return a new object and leave the original one untouched.
    facts_goal = silkie.loadDFLFacts('./base_facts.dfl')
    facts_goal = silkie.loadDFLFacts('./facts_goal.dfl', facts_goal)
    facts_goal_and_ini = silkie.loadDFLFacts('./base_facts.dfl')
    facts_goal_and_ini = silkie.loadDFLFacts('./facts_goal.dfl', facts_goal_and_ini)
    facts_goal_and_ini = silkie.loadDFLFacts('./facts_ini.dfl', facts_goal_and_ini)
    facts_goal_and_ini_and_open = silkie.loadDFLFacts('./base_facts.dfl')
    facts_goal_and_ini_and_open = silkie.loadDFLFacts('./facts_goal.dfl', facts_goal_and_ini_and_open)
    facts_goal_and_ini_and_open = silkie.loadDFLFacts('./facts_ini.dfl', facts_goal_and_ini_and_open)
    facts_goal_and_ini_and_open = silkie.loadDFLFacts('./facts_open.dfl', facts_goal_and_ini_and_open)
    facts_goal_and_ini_and_open_above = silkie.loadDFLFacts('./base_facts.dfl')
    facts_goal_and_ini_and_open_above = silkie.loadDFLFacts('./facts_goal.dfl', facts_goal_and_ini_and_open_above)
    facts_goal_and_ini_and_open_above = silkie.loadDFLFacts('./facts_ini.dfl', facts_goal_and_ini_and_open_above)
    facts_goal_and_ini_and_open_above = silkie.loadDFLFacts('./facts_open.dfl', facts_goal_and_ini_and_open_above)
    facts_goal_and_ini_and_open_above = silkie.loadDFLFacts('./facts_above.dfl', facts_goal_and_ini_and_open_above)

    # Considering here a sequence of inference problems. 
    # The idea is that each problem results in answers for the robot about what to do and what to look for, which produce the inputs for the subsequent problem.
    theory_goal, s2i_goal, i2s_goal, theoryStr_goal = silkie.buildTheory(rules,facts_goal,{},debugTheory=True)
    goals_goal = ['coffeeNotInCup', 'coffeeInBowl']
    theory_goal_and_ini, s2i_goal_and_ini, i2s_goal_and_ini, theoryStr_goal_and_ini = silkie.buildTheory(rules,facts_goal_and_ini,{},debugTheory=True)
    goals_goal_and_ini = ['coffeeNotInCup', 'coffeeInBowl', 'requirement_coffeeNotInCup', 'requirement_coffeeInBowl']
    theory_goal_and_ini_and_open, s2i_goal_and_ini_and_open, i2s_goal_and_ini_and_open, theoryStr_goal_and_ini_and_open = silkie.buildTheory(rules,facts_goal_and_ini_and_open,{},debugTheory=True)
    goals_goal_and_ini_and_open = ['coffeeNotInCup', 'coffeeInBowl', 'requirement_coffeeNotInCup', 'requirement_coffeeInBowl', 'requirement_requirement_coffeeNotInCup', 'requirement_requirement_coffeeInBowl']
    theory_goal_and_ini_and_open_above, s2i_goal_and_ini_and_open_above, i2s_goal_and_ini_and_open_above, theoryStr_goal_and_ini_and_open_above = silkie.buildTheory(rules,facts_goal_and_ini_and_open_above,{},debugTheory=True)
    goals_goal_and_ini_and_open_above = ['coffeeNotInCup', 'coffeeInBowl', 'requirement_coffeeNotInCup', 'requirement_coffeeInBowl', 'requirement_requirement_coffeeNotInCup', 'requirement_requirement_coffeeInBowl', 'requirement_requirement_requirement_coffeeNotInCup', 'requirement_requirement_requirement_coffeeInBowl']

    bl = ['combine', 'follows']
    
    for scnSpec in [(theory_goal, i2s_goal, goals_goal, 'Pouring: want coffee in the bowl, what to look for'), (theory_goal_and_ini, i2s_goal_and_ini, goals_goal_and_ini, 'Pouring: coffee not in bowl, what must happen to get it there'), (theory_goal_and_ini_and_open, i2s_goal_and_ini_and_open, goals_goal_and_ini_and_open, 'Pouring: suppose containers are open, what should happen for the entry/exit to happen'), (theory_goal_and_ini_and_open_above, i2s_goal_and_ini_and_open_above, goals_goal_and_ini_and_open_above, 'Pouring: the liquid must fall from one into the other container, what should happen for that to happen?')]:
        theory, i2s, inds, msg = scnSpec
        print('==========\n%s' % msg)
        #reportTargetConclusions(theory, i2s, ['E_byProcess', 'E_threatenedBy', 'E_byGoal', 'E_hasRole', 'hasRole', 'hasFiller', 'preferredTrajector', 'preferredRelatum'])
        reportTargetConclusions(theory, i2s, ['enables', 'Q_position', 'Q_velocity', 'Q_opening'], inds, bl)
        #reportTargetConclusions(theory, i2s, ['follows', 'combine'])

if __name__ == '__main__':
    main()
