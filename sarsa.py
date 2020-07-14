from montecarlo import MonteCarlo
from easy21 import Action,Easy21

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

  def update(self, alpha, delta):
    for s in self.q:
      for a in [Action.HIT, Action.STICK]:
        self.q[s][a] += alpha * delta * self.E[s][a]
        self.E[s][a] = Sarsa.GAMMA * self._lambda * self.E[s][a]

if __name__ == "__main__":
  """ Re-calculate V* """
  m = MonteCarlo()
  for i in range(1,50000):
    m.run()

  for i in range(0, 1):
    l = i * 0.1
    s = Sarsa(l)
    for j in range(1,1000):
      s.run()
    if i == 0 or i == 10:
      print("plot learning curve here")