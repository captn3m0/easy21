from features import FeatureExtractor
from easy21 import Action

def test_feature_extractor():
  f = FeatureExtractor((10,12), Action.HIT)
  f = f.features()
  assert(f[18:] == [0] * 18)
  assert(f[0:12] == [0] * 12)
  assert(f[12:18] == [0,0,1,1,0,0])

def test_extractor_at_extreme():
  f = FeatureExtractor((10,21), Action.STICK)
  f = f.features()
  assert(f[0:35] == [0] * 35)
  assert(f[35] == 1)