from easy21 import Easy21, Color,Action

def test_easy21_init_game():
  g = Easy21()
  assert(len(g.player) == 1)
  assert(len(g.dealer) == 1)
  assert(g.player[0].color == Color.BLACK)
  assert(g.dealer[0].color == Color.BLACK)
  for i in range(1,1000):
    c = g.drawCard()
    assert(c.value < 11)
    assert(c.value > 0)

def test_losing():
  g = Easy21()
  r = None
  while True:
    x,r = g.step(Action.HIT)
    if r == -1:
      break
  assert(r == -1)

def test_losing_by_early_stick():
  g = Easy21()
  r = None
  g,r = g.step(Action.STICK)
  assert(r == -1)