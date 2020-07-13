from enum import Enum, auto
import random

class Action(Enum):
  HIT = auto()
  STICK = auto()

class Color(Enum):
  RED = auto()
  BLACK = auto()

class Card:
  def __init__(self, color, value):
    if value < 1 or value >10:
      raise Exception("Invalid Card Value")
    if not isinstance(color, Color):
      raise Exception("Invalid Color")

    self.color = color
    self.value = value

  def black(self):
    return self.color == Color.BLACK

  def red(self):
    return self.color == Color.RED

class Easy21:

  def score(self, hand):
    score = 0
    for card in hand:
      if card.black():
        score += card.value
      elif card.red():
        score -= card.value
      else:
        raise Exception("Invalid card color")
    return score

  def dealerScore(self):
    return self.score(self.dealer)

  def playerScore(self):
    return self.score(self.player)

  def __init__(self):
    self.stick = False
    self.dealer = [self.drawBlack()]
    self.player = [self.drawBlack()]

  """ Used for the starting player and dealer draws """
  def drawBlack(self):
    v = random.randint(1,10)
    return Card(Color.BLACK, v)

  """ This just implements our probability distribution for card draws """
  def drawCard(self):
    v = random.randint(1,10)
    c = random.choice([Color.RED, Color.BLACK, Color.BLACK])
    return Card(c, v)

  def step(self, action):
    if action == Action.HIT:
      self.player.append(self.drawCard())
      if self.playerScore() > 21 or self.playerScore() < 1:
        return (self, -1)
      return (self, None)
    elif action == Action.STICK:
      while self.dealerScore() < 17:
        self.dealer.append(self.drawCard())
      if self.dealerScore() < 1 or self.dealerScore() > 21:
        return (self, -1)
      if self.dealerScore() > self.playerScore():
        return (self, -1)
      elif self.dealerScore() < self.playerScore():
        return (self, 1)
      else:
        return (self, 0)
    else:
      raise Exception("Invalid action")
