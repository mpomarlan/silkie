import requests
import json
import os
import sys

import math

cpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cpath, '../../src'))
sys.path.append(os.path.join(cpath, './ease_lexical_resources/src'))

import silkie.silkie as silkie
import dfl.dlquery as dl

def loadExampleScene():
    worldState = json.loads(open("./affordance_check.scene").read())
    dgr = {'kitchenStateIn': worldState}
    r = requests.post("http://localhost:54321/abe-sim-command/to-set-kitchen", data=bytes(json.dumps(dgr), "utf-8"))
    response = json.loads(r.text)
    print(response)
    dws = {'kitchen': '?kitchen-state-1'}
    r = requests.post("http://localhost:54321/abe-sim-command/to-get-kitchen", data=bytes(json.dumps(dws), "utf-8"))
    worldState = json.loads(r.text)['response']
    return worldState

def showDFLTypes(worldState):
    retq = {}
    ws = worldState['?kitchen-state-1']
    for o in ws:
        retq[o] = {}
        if ('customStateVariables' in ws[o]) and ('fn' in ws[o]['customStateVariables']) and ('dfltype' in ws[o]['customStateVariables']['fn']):
            retq[o]['text'] = ws[o]['customStateVariables']['fn']['dfltype']
    return retq

def addHighlightLabels(onObjects, label, oldHighlights):
    retq = oldHighlights.copy()
    for o in onObjects:
        if o not in retq:
            retq[o] = {}
        retq[o]['label'] = label
    return retq

def clearHighlights(highlights):
    for h in highlights:
        dhl = {'object': h}
        highlights[h] = {}
        r = requests.post("http://localhost:54321/abe-sim-command/to-remove-highlight", data=bytes(json.dumps(dhl), "utf-8"))

def updateHighlights(highlights, oldHighlights):
    clearHighlights(oldHighlights)
    for h in highlights:
        dhl = {'object': h}
        if 'text' in highlights[h]:
            dhl['text'] = highlights[h]['text']
        if 'label' in highlights[h]:
            dhl['label'] = highlights[h]['label']
        r = requests.post("http://localhost:54321/abe-sim-command/to-add-highlight", data=bytes(json.dumps(dhl), "utf-8"))

def areClose(d, worldState):
    ws = worldState['?kitchen-state-1']
    a = d[0]
    b = d[1]
    pa = ws[a]['position']
    pb = ws[b]['position']
    dx = [x-y for x,y in zip(pa, pb)]
    print(d, math.sqrt(dx[0]*dx[0] + dx[1]*dx[1] + dx[2]*dx[2]))
    return 1 > math.sqrt(dx[0]*dx[0] + dx[1]*dx[1] + dx[2]*dx[2])
    

def whatCanContain(worldState):
    ws = worldState['?kitchen-state-1']
    istAnswer = set(dl.whatHasDisposition('dfl:contain.v.wn.stative.Instrument'))
    retq = set()
    for o in ws:
        if ('customStateVariables' in ws[o]) and ('fn' in ws[o]['customStateVariables']) and ('dfltype' in ws[o]['customStateVariables']['fn']) and (ws[o]['customStateVariables']['fn']['dfltype'] in istAnswer):
            retq.add(o)
    return retq

def whatCanContainWater(worldState):
    ws = worldState['?kitchen-state-1']
    istAnswer = set(dl.whatToolsCanPerformTaskOnObject('dfl:contain.v.wn.stative', 'dfl:water.n.wn.food'))
    retq = set()
    for o in ws:
        if ('customStateVariables' in ws[o]) and ('fn' in ws[o]['customStateVariables']) and ('dfltype' in ws[o]['customStateVariables']['fn']) and (ws[o]['customStateVariables']['fn']['dfltype'] in istAnswer):
            retq.add(o)
    return retq

def whatCanBeCarried(worldState):
    ws = worldState['?kitchen-state-1']
    istAnswer = set(dl.whatHasDisposition('dfl:hold.v.wn.contact.Theme'))
    retq = set()
    for o in ws:
        if ('customStateVariables' in ws[o]) and ('fn' in ws[o]['customStateVariables']) and ('dfltype' in ws[o]['customStateVariables']['fn']) and (ws[o]['customStateVariables']['fn']['dfltype'] in istAnswer):
            retq.add(o)
    return retq

def whatIsDangerous(worldState):
    ws = worldState['?kitchen-state-1']
    rules = silkie.loadDFLRules('rules.dfl')
    facts = silkie.loadDFLFacts('facts.dfl')
    theory, s2i, i2s, theoryStr = silkie.buildTheory(rules,facts,{},debugTheory=True)
    conclusions = silkie.dflInference(theory)
    conclusions = silkie.idx2strConclusions(conclusions, i2s)
    retq = set()
    for c in conclusions.defeasiblyProvable:
        if c[0] in ['potentiallyThreatens']:
            retq.add((c[1], c[2], 'potential'))
    return retq

def whatCanBoilWaterIn(worldState, dangers):
    susceptibles = [x[1] for x in dangers]
    potentials = whatCanContainWater(worldState).intersection(whatCanBeCarried(worldState))
    return potentials.difference(susceptibles)

def main():
    worldState = loadExampleScene()
    typeHighlights = showDFLTypes(worldState)
    dl.buildCache()
    updateHighlights(typeHighlights, {})
    input("Press a key to highlight which objects here are containers ...")
    print("    answer %s" % str(whatCanContain(worldState)))
    affHighlights = addHighlightLabels(whatCanContain(worldState), 'selected', typeHighlights)
    updateHighlights(affHighlights, typeHighlights)
    input("Press a key to highlight which objects here are containers for potable water ...")
    print("    answer %s" % str(whatCanContainWater(worldState)))
    clearHighlights(affHighlights)
    affHighlights = addHighlightLabels(whatCanContainWater(worldState), 'selected', typeHighlights)
    updateHighlights(affHighlights, typeHighlights)
    input("Press a key to highlight which objects here are containers for potable water and can be carried by hand ...")
    print("    answer %s" % str(whatCanContainWater(worldState).intersection(whatCanBeCarried(worldState))))
    clearHighlights(affHighlights)
    affHighlights = addHighlightLabels(whatCanContainWater(worldState).intersection(whatCanBeCarried(worldState)), 'selected', typeHighlights)
    updateHighlights(affHighlights, typeHighlights)
    input("Press a key to highlight potential dangers ...")
    dangers = whatIsDangerous(worldState)
    dangersAdj = set([])
    for d in dangers:
        if areClose(d, worldState):
            dangersAdj.add((d[0], d[1], "acute"))
        else:
            dangersAdj.add(d)
    print("    answer %s" % str(dangersAdj))
    clearHighlights(affHighlights)
    affHighlights = addHighlightLabels([x[0] for x in dangersAdj if 'potential' == x[2]] + [x[1] for x in dangersAdj if 'potential' == x[2]], 'warning', typeHighlights)
    affHighlights = addHighlightLabels([x[0] for x in dangersAdj if 'acute' == x[2]] + [x[1] for x in dangersAdj if 'acute' == x[2]], 'danger', affHighlights)
    updateHighlights(affHighlights, typeHighlights)
    input("Press a key to highlight which objects would be good to boil water in on the gas stove ...")
    print("    answer %s" % str(whatCanBoilWaterIn(worldState, dangersAdj)))
    clearHighlights(affHighlights)
    affHighlights = addHighlightLabels(whatCanBoilWaterIn(worldState, dangersAdj), 'selected', typeHighlights)
    updateHighlights(affHighlights, typeHighlights)
    input("Press a key to remove all highlights and exit ...")
    clearHighlights(affHighlights)

if __name__ == "__main__":
    main()

