import model
import pandas as pd

def fetch_customer_segments(algorithm, df,Id,**kwargs):
	"""
		Gets algortithm, input data and id columns and returns customers along with their clusters
		
		Parameters
		----------
		algorithm : str
			The name of the clustering algorithm to use: it is either kmeans or rfm as of now
		df : DataFrame
			The dataframe containg the processed input the data
		Id : str
			The name of the column that is used to identify customer ID
		**kwargs : dict 
			dictionary containing positional arguments to pass to func
			
		Returns
		----------
		df : DataFrame
			The dataframe containg the customer ID and its corresponding cluster number
			
		
	"""
	strat = model.selectModel(algorithm,df,Id,kwargs)
	isString = isinstance(strat, str)
	df1 = pd.DataFrame()
	if not isString:
		strat._Id = Id
		strat._df = df
		strat.model_args=kwargs
		df1 = strat.execute()
	return df1
	
	
if __name__ == "__main__":
	algorithm = "kmeans"
	# from sklearn.preprocessing import MinMaxScaler
	# data = pd.read_csv("C:/Users/DayanandChalla/Downloads/Wholesale customers data.csv")
	# categorical_features = ['Channel', 'Region']
	# continuous_features = ['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']
	# for col in categorical_features:
		# dummies = pd.get_dummies(data[col], prefix=col)
		# data = pd.concat([data, dummies], axis=1)
		# data.drop(col, axis=1, inplace=True)
	# mms = MinMaxScaler()
	# mms.fit(data)
	# data_transformed = mms.transform(data)
	data_transformed = pd.read_csv("C:/Users/DayanandChalla/Downloads/Mall_Customers.csv")
	#print(data_transformed.head())
	data_transformed.drop(["Gender"], axis = 1, inplace=True)
	config = {'K': 11}
	df = fetch_customer_segments(algorithm,data_transformed,"CustomerID",**config)
	print(df)