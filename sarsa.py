from montecarlo import MonteCarlo
from easy21 import Action,Easy21
from math import pow
from pyx import *

class Sarsa(MonteCarlo):
  GAMMA = 1
  def __init__(self, l):
    super().__init__()
    self._lambda = l

  def reset(self):
    self.E = {}
    for dealer in range(1, 11):
      for player in range(1, 22):
        self.E[(dealer, player)] = {
          Action.HIT: 0,
          Action.STICK: 0
        }
  """ Runs one single episode """
  def run(self):
    self.reset()
    game = Easy21()
    S = game.state()
    A = self.epsilon_greedy_action(S)
    while not game.isTerminal():
      Aprime = None
      game,R = game.step(A)
      Sprime = game.state()
      self.N[S][A] += 1
      self.E[S][A] += 1
      # Initialize Q to zero for "all" states
      # Our lookup table is only for interesting states
      # So we hack around by putting Q = 0
      if game.isTerminal():
        Q = 0
      else:
        Aprime = self.epsilon_greedy_action(Sprime)
        Q = self.q[Sprime][Aprime]
      """ This is our TD error """
      alpha = self.alpha(S,A)
      delta = R + Sarsa.GAMMA * Q - self.q[S][A]
      self.update(alpha, delta)

      S = Sprime
      A = Aprime

  def mean_squared_error(self, q2):
    q1 = self.q
    e = 0
    for s in q1:
      e+= pow(q1[s][Action.HIT] - q2[s][Action.HIT],2 )
      e+= pow(q1[s][Action.STICK] - q2[s][Action.STICK],2)

    return e

  def update(self, alpha, delta):
    for s in self.q:
      for a in [Action.HIT, Action.STICK]:
        self.q[s][a] += alpha * delta * self.E[s][a]
        self.E[s][a] = Sarsa.GAMMA * self._lambda * self.E[s][a]

if __name__ == "__main__":
  g = graph.graphxy(width=100, x=graph.axis.linear(min=1, max=1000), y=graph.axis.linear(), key=graph.key.key(pos="br", dist=0.1))
  plots = []
  """ Re-calculate V* """
  m = MonteCarlo()
  for i in range(1,50000):
    m.run()

  for _l in [e/10.0 for e in range(0, 11, 1)]:
    print("Training Sarsa(%s)" % _l)
    s = Sarsa(_l)
    c1 = []
    c2 = []
    for j in range(1,10001):
      s.run()
      if j % 100 == 0:
        c1.append(j)
        e = s.mean_squared_error(m.q)
        c2.append(e)
        if j % 1000 == 0:
          print("Error = %2f" % e)
    title = "Sarsa(%s)" % _l
    v = graph.data.values(title=title, x=c1, y=c2)
    plots.append(v)
    # styles.append(graph.style.line())
  g.plot(plots, [graph.style.line([style.linestyle.solid, color.gradient.Rainbow])])
  g.writeSVGfile("error")
