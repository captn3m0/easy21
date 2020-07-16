from easy21 import Action

"""
Use a binary feature vectorφ(s,a) with 3∗6∗2 = 36 features.
Each binary featurehas a value of 1 iff (s,a) lies within the cuboid
of state-space corresponding to that feature, and the action corresponding
to that feature.  The cuboids havethe following overlapping intervals:

dealer(s) ={[1,4],[4,7],[7,10]}
player(s) ={[1,6],[4,9],[7,12],[10,15],[13,18],[16,21]}
a={hit,stick}

•dealer(s) is the value of the dealer’s first card (1–10)
•sum(s) is the sum of the player’s cards (1–21)
"""

class FeatureExtractor:
  """ Takes a state, and returns the corresponding feature vector as a tuple """
  def __init__(self, state, action):
    self.feature_vector = []
    dealer = state[0]
    player = state[1]
    for a in [Action.HIT, Action.STICK]:
      for dealer_feature_boundaries in [[1,4],[4,7],[7,10]]:
        for player_feature_boundaries in [[1,6],[4,9],[7,12],[10,15],[13,18],[16,21]]:
          if dealer >= dealer_feature_boundaries[0] and dealer <= dealer_feature_boundaries[1] and player >= player_feature_boundaries[0] and player<= player_feature_boundaries[1] and action == a:
            self.feature_vector.append(1)
          else:
            self.feature_vector.append(0)

  def features(self):
    return self.feature_vector
