from strategy import Strategy
from kmeans import predictUsingKMeans
from rfm import predictUsingRFM


def selectModel(algorithm,df,Id,kwargs):

    switcher = {
                'kmeans': Strategy(predictUsingKMeans),
                'rfm': Strategy(predictUsingRFM)
             }

    strat = switcher.get(algorithm, "Not a valid model input")

    return strat