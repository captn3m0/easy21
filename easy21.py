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

  """
  Card scores can be positive or negative
  depending on the color
  """
  def score(self):
    if self.color == Color.RED:
      return -self.value
    else:
      return self.value
class Easy21:
  def state(self):
    return (self.dealer, self.player)

  def dealerScore(self):
    return self.dealer

  def playerScore(self):
    return self.player

  def __init__(self):
    self.terminal = False
    self.stick = False
    # Draw 2 black cards for dealer and player
    self.dealer = random.randint(1,10)
    self.player = random.randint(1,10)

  """ This just implements our probability distribution for card draws """
  def drawCard(self):
    v = random.randint(1,10)
    c = random.choice([Color.RED, Color.BLACK, Color.BLACK])
    return Card(c, v)

  def isTerminal(self):
    return (self.terminal == True)

  def step(self, action):
    if action == Action.HIT:
      # Draw a new card
      c = self.drawCard()
      self.player += c.score()
      if self.player > 21 or self.player < 1:
        self.terminal = True
        return (self, -1)
      return (self, 0)
    elif action == Action.STICK:
      while self.dealer < 17:
        self.dealer += self.drawCard().score()
      self.terminal = True
      if self.dealer < 1 or self.dealer > 21:
        return (self, 1)
      elif self.dealer > self.player:
        return (self, -1)
      elif self.dealer < self.player:
        return (self, 1)
      else:
        return (self, 0)
    else:
      raise Exception("Invalid action")
