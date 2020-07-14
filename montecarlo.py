from easy21 import Action, Easy21
import random
import json
from pyx import *

"""
Apply Monte-Carlo control to Easy21.
Initialise the value function to zero.
Use a time-varying scalar step-size of
αt= 1/N(st,at) and and e-greedy exploration strategy  with e-t=N0/(N0+N(st)),  where

N0=  100  is  a  constant,

N(s)  isthe number of times that stateshas been visited,

andN(s,a) is the numberof times that actionahas been selected from states.

Feel free to choose analternative value forN0, if it helps producing better results.

Plot the optimalvalue functionV∗(s) = maxaQ∗(s,a) using similar axes to the following figuretaken from Sutton and Barto’s Blackjack example.
"""

class MonteCarlo:
  """ With 50, it takes us 50 episodes before we have a 50-50 explore/exploit ratio"""
  N0 = 50

  """ Runs one single episode """
  def run(self):
    game = Easy21()
    G = None
    walk = []
    while True:
      s = game.state()
      action = self.epsilon_greedy_action(s)
      self.N[s][action] += 1
      game,G = game.step(action)
      # We break if the game has ended
      walk.append((s,action))
      if game.isTerminal():
        break
    assert(G in [0,-1,1])
    for s, action in walk:
      self.q[s][action] = self.q[s][action] + self.alpha(s, action) * (G - self.q[s][action])

  """ this is the argmax for our value function """
  def greedy_action(self, s):
    if self.q[s][Action.HIT] > self.q[s][Action.STICK]:
      return Action.HIT
    else:
      return Action.STICK

  """ Our optimum value function """
  def write_v_star(self):
    dealer = range(1, 11)
    player = range(1, 21)
    with open('vstar.txt', 'w') as f:
      for d in dealer:
        for p in player:
          s = (d, p)
          action = self.greedy_action(s)
          q = self.q[s][action]
          f.write("%s %s %s\n" %(d,p,q))

  def epsilon_greedy_action(self, s):
    if random.random() <= self.epsilon(s):
      return random.choice([Action.HIT, Action.STICK])
    else:
      return self.greedy_action(s)

  def __init__(self):
    self.episodeCount = 10000
    # Our value function
    # the keys are tuples of (dealerScore, playerScore, action) = R
    # and the value is another dict for looking up the action.
    self.q = {}
    self.N = {}
    # state counter = N(s,a) is the number of times that action a has been selected from state s
    # the key here is (dealerScore, playerScore)[action]
    # and the value is a Number
    for dealer in range(1, 11):
      for player in range(1, 22):
        self.q[(dealer,player)] = {
          Action.HIT: 0,
          Action.STICK: 0
        }
        self.N[(dealer, player)] = {
          Action.HIT: 0,
          Action.STICK: 0
        }

  """
  N(s,a) is the numberof times that action a has been selected from states
  """
  def N_s_a(self, s, a):
    return self.N[s][a]

  def N_s(self, s):
    return self.N[s][Action.HIT] + self.N[s][Action.STICK]

  """ This is our decaying epsilon to reduce exploration once we have N0 samples """
  def epsilon(self, s):
    n = self.N_s(s)
    return self.N0/(self.N0 + n)

  """ time-varying scalar step-size """
  def alpha(self, s, a):
    return 1/(self.N_s_a(s, a))

  def plot_v_star(self):
    self.write_v_star()
    g = graph.graphxyz(size=4)
    g.plot(graph.data.file("vstar.txt", x=1, y=2, z=3), [graph.style.grid()])
    g.writeSVGfile("montecarlo")

if __name__ == "__main__":
  m = MonteCarlo()
  for i in range(1,50000):
    m.run()
  m.plot_v_star()

  for i in range(1,11):
    print(m.q[(i, 11)])