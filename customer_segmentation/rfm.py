import pandas as pd
from datetime import datetime
from dateutil.parser import parse
from warnings import filterwarnings




def is_date(string, fuzzy=False):
	try:
		if isinstance(string, str):
			input_str=string
		else:
			input_str=string.tostring()
		parse(input_str, fuzzy=fuzzy)
		return True
	except ValueError:
		return False


# group into different numeric tiers
def set_tier_numeric(df):
	if df.tier == 'Platinum':
		return 0
	elif df.tier == 'Gold':
		return 1
	elif df.tier == 'Silver':
		return 2
	else:
		return 3
		
		
# group into different tiers
def get_tier(df):
	if df['RFMScore'] >= 10:
		return 'Platinum'
	elif (df['RFMScore'] >= 8) and (df['RFMScore'] < 10):
		return 'Gold'
	elif (df['RFMScore'] >= 6) and (df['RFMScore'] < 8):
		return 'Silver'
	else:
		return 'Bronze'
		

# group into 3 Frequncy tiers
def set_F(df):
	if df['Frequency'] >= 4:
		return 3
	elif (df['Frequency'] >= 2) and (df['Frequency'] < 4):
		return 2
	else:
		return 1
		


def predictUsingRFM(self):
	### **Recency, Frequency, Monetary (RFM) Analysis**
	print('Predicting with RFM')
	df = self._df
	ids = self._Id
	fre = self.model_args['frequency']
	rec = self.model_args['recency']
	mon = self.model_args['monetory']
	
	#print(df.head())
	
	if not all(item in df.columns for item in [ids, fre, rec, mon]):
		raise Exception('Provided columns are not avialble in the input dataframe!!!')
		
		
	if not is_date(df[rec][0]):
		raise Exception(f'Column {rec} is not a datetime column, Hence it can\'t be used for recency!!!')
	
	from datetime import datetime, date
	datetime_obj = date.today()
	
	num_features = [x for x in df.columns if ((df[x].dtypes == 'int64') | (df[x].dtypes == 'float64'))]
	features = df[[ids, fre, rec]]

	for i in features:
		print(f'Total unique value in {i} is {len(df[i].unique())}')
		
		
	# Taking month and year from timestamp feature
	pd.options.mode.chained_assignment = None

	df['CreateDate'] = pd.to_datetime(df[rec])
	df['CreateMonth'] = df['CreateDate'].dt.month
	df['CreateYear'] = df['CreateDate'].dt.year

	df['CreateMonth2'] = df['CreateMonth'].astype(str)
	df['CreateMonth2'] = df['CreateMonth2'].apply(lambda x: x.zfill(2))
	df['Deal_Created_MY'] = df['CreateYear'].astype(str)+df['CreateMonth2'].astype(str)
	
	# Calculate each metric invoice
	# InvoiceDate is actually Deal Create Date. Named just for calculation purposes
	df_rfm = df.groupby(ids).agg({'CreateDate': lambda x: (datetime_obj - x.dt.date.max()).days + 1, # Recency
												fre: lambda x: len(x.unique()), # Frequency
												mon: lambda x: x.sum()})

	# Rename the columns
	df_rfm.rename(columns={'CreateDate':'Recency',
							fre:'Frequency',
							mon:'Monetary'}, inplace=True)
	
	# This replaces the negative recency days with zero as some Deal Create Date may be in the future (observed in Deals data)
	df_rfm.loc[df_rfm.Recency < 0,'Recency'] = 0

	## **Recency segmentation**

	# Recency segmentation using quartile
	df_rfm['R'] = pd.qcut(df_rfm['Recency'], q=4, labels=[4, 3, 2, 1])

	# Calculate Q1, Q2, Q3 of recency
	df_rfm['Recency'].quantile([0.25, 0.5, 0.75, 1.0]).reset_index()
	
	# Monetary segmentation using quartile
	df_rfm['M'] = pd.qcut(df_rfm['Monetary'].astype('float'), q=4, labels=[1, 2, 3, 4])
	
	
	df_rfm['F'] = df_rfm.apply(set_F, axis=1)
	#input_dirrfmnew= os.path.join('Source','rfmnew.csv')
	#df_rfm.to_csv(input_dirrfmnew)

	# Calculate RFMSegment and RFMScore
	df_rfm['RFMSegment'] = df_rfm['R'].astype('string') + df_rfm['F'].astype('string') + df_rfm['M'].astype('string')
	df_rfm['RFMScore'] = df_rfm['R'].astype('int') + df_rfm['F'].astype('int') + df_rfm['M'].astype('int')
	
	
	# Grouping customers by RFMScore
	df_seg_mean = df_rfm.groupby('RFMScore').agg({
		'Recency':'mean', 
		'Frequency':'mean', 
		'Monetary':['mean', 'count']}).round(2).reset_index()
		
		
	df_rfm['tier'] = df_rfm.apply(get_tier, axis=1)
	
	
	df_rfm['Cluster'] = df_rfm.apply(set_tier_numeric, axis=1 )
	
	return df_rfm
	
	