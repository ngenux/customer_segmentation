import pandas as pd
from sklearn.cluster import KMeans
from warnings import filterwarnings
from sklearn.metrics import silhouette_score
from kneed import KneeLocator


def getBestKWithElbow(K, df):
	sse = {}
	for k in K:
		kmeans = KMeans(n_clusters=k)
		kmeans.fit(df)
		sse[k] = kmeans.inertia_
	#getting optimal cluster value with max score
	kn = KneeLocator(
				 x=list(sse.keys()), 
				 y=list(sse.values()), 
				 curve='convex', 
				 direction='decreasing'
				 )
	optimal = kn.knee
	#printing result
	print('Optimal number of clusters is: ',str(optimal))
	
def getBestKWithSilhouette(K, df):
	scores = []
	for k in K:
		kmeans = KMeans(n_clusters=k)
		cls_assignment = kmeans.fit_predict(df)
		scores.append(silhouette_score(df,cls_assignment))
	#getting optimal cluster value with max score
	optimal = K[scores.index(sorted(scores,reverse=True)[0])]
	#printing result
	print('Optimal number of clusters is: ',str(optimal))
	return optimal


def predictUsingKMeans(self):
	print('Predicting with KMeans')
	#print(self._Id)
	#print(self._df)
	#print(self.model_args['K'])
	if not (self._Id in self._df.columns ):
		raise Exception(f'Provided ID column {self._Id} is not avialble in the input dataframe!!!')
	lower = 2
	upper = self.model_args['K']
	K=range(lower,upper)
	df = self._df
	#print(df.columns)
	df.drop("CustomerID", axis = 1, inplace=True)
	optimal_k = getBestKWithElbow(K, df)
	optimal_k = getBestKWithSilhouette(K, df)
	kmeans = KMeans(n_clusters=optimal_k)
	cls_assignment = kmeans.fit_predict(df)
	self._df['cluster']=cls_assignment
	return self._df