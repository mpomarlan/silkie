- Facts to infer
    - Can we pour?
    - Does the current facts points to liquid spilled?
    - Is there an overflow?
    - What to do if there is a spilling or an overflow?

- Facts and what is inferred
0:  => Liquid(tea)
1:  => poursTo(teapot, cup)
2: Container(cup), Container(teapot), hasOpening(cup, openCup), hasOpening(teapot, open), near(teapot, cup), within(open, openCup) => canPourTo(teapot, cup)
3: inside(tea, teapot) => -outside(tea, teapot)
4: near(teapot, cup) => near(cup, teapot)
5: Container(teapot), Liquid(tea), inside(tea, teapot), outside(out, teapot), passThrough(tea, open), willBeAt(tea, out) => Opening(open)
6: Container(cup), Container(teapot), contains(teapot, tea), outside(outsidecup, cup), partOf(t1, tea), poursTo(teapot, cup), willBeAt(t1, outsidecup) => isSpilled(t1)
7:  => near(cup, teapot)
8: contains(teapot, tea), isSpilled(t1), partOf(t1, tea), poursTo(teapot, cup) => moveTowards(teapot, cup)
9: contains(teapot, tea) => inside(tea, teapot)
10:  => hasOpening(cup, openCup)
11:  => contains(teapot, tea)
12:  => Container(teapot)
13: Container(teapot), Liquid(tea), hasOpening(teapot, open), inside(tea, teapot), outside(out, teapot), willBeAt(tea, out) => passThrough(tea, open)
14:  => hasOpening(teapot, open)
15:  => willBeAt(t1, outsidecup)
16: Container(teapot), Liquid(tea), hasOpening(teapot, open), inside(tea, teapot), outside(out, teapot), willBeAt(tea, out) => -canAvoid(tea, open)
17:  => within(open, openCup)
18:  => willBeAt(tea, out)
19:  => Container(cup)
20: Container(teapot), Liquid(tea), contains(teapot, tea) => canPour(teapot, tea)
21:  => outside(outsidecup, cup)
22:  => outside(out, teapot)
23:  => partOf(t1, tea)
24: near(cup, teapot) => near(teapot, cup)


