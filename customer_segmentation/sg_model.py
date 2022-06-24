from .strategy import Strategy
from .kmeans import predictUsingKMeans
from .rfm import predictUsingRFM


switcher = {
    'kmeans': Strategy(predictUsingKMeans),
    'rfm': Strategy(predictUsingRFM)
    }

def selectModel(algorithm,df,Id,kwargs):

    strat = switcher.get(algorithm, "Not a valid model input")

    return strat