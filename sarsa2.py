from montecarlo import MonteCarlo
import operator
from features import FeatureExtractor
from sarsa import Sarsa
from easy21 import Action,Easy21
from math import pow
from pyx import *

class Sarsa2(Sarsa):
  ALPHA = 0.01
  GAMMA = 1
  EPSILON = 0.05

  def __init__(self, l):
    self.w = [0] * 36
    self._lambda = l

  def reset(self):
    self.E = [0] * 36

  def epsilon(self, s):
    return Sarsa2.EPSILON

  """
  Q = dotproduct (x, w)
  where x is the feature vector
  and w is the weights
  """
  def Q(self, state, action):
    X = FeatureExtractor(state, action).features()
    return sum([feature*weight for feature,weight in zip(X,self.w)])

  def greedy_action(self, s):
    if self.Q(s, Action.HIT) > self.Q(s,Action.STICK):
      return Action.HIT
    else:
      return Action.STICK

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
      # Initialize Q to zero for "all" states
      # Our lookup table is only for interesting states
      # So we hack around by putting Q = 0
      if game.isTerminal():
        Q = 0
      else:
        Aprime = self.epsilon_greedy_action(Sprime)
        Q = self.Q(Sprime,Aprime)
      """ This is our TD error """
      delta = R + Sarsa2.GAMMA * Q - self.Q(S,A)
      features = FeatureExtractor(S, A).features()
      self.update(delta, features)
      S = Sprime
      A = Aprime

  def mean_squared_error(self, q2):
    e = 0
    for s in q2:
      e+= pow(self.Q(s,Action.HIT) - q2[s][Action.HIT], 2)
      e+= pow(self.Q(s,Action.STICK) - q2[s][Action.STICK], 2)
    return e

  def update(self, delta, features):
    self.E = [(e * Sarsa2.ALPHA * delta)+f for f,e in zip(features,self.E)]
    delta_w = [e * Sarsa2.ALPHA * delta for e in self.E]
    self.w = [w+d for w,d in zip(self.w, delta_w)]

if __name__ == "__main__":
  g = graph.graphxy(width=30, x=graph.axis.linear(min=100,max=1000), y=graph.axis.linear(), key=graph.key.key(pos="bl"))
  plots = []
  """ Re-calculate V* """
  m = MonteCarlo()
  for i in range(1,50000):
    m.run()

  for _l in [e/10.0 for e in range(0, 11, 1)]:
    print("Training Sarsa(%s) with Linear Function Approximation" % _l)
    s = Sarsa2(_l)
    c1 = []
    c2 = []
    for j in range(1,1001):
      s.run()
      if j % 100 == 0:
        c1.append(j)
        e = s.mean_squared_error(m.q)
        c2.append(e)
        if j % 100 == 0:
          print("Error = %2f" % e)
    title = "Sarsa-LFA(%s)" % _l
    v = graph.data.values(title=title, x=c1, y=c2)
    plots.append(v)
  g.plot(plots, [graph.style.line([color.gradient.Rainbow])])
  g.writeSVGfile("sarsa-lfa-errors")
