#%%
#Import libraries
import pandas as pd
import numpy as np

#%%
#Upload data
asv = pd.read_excel('/Users/madelaineleitman/Downloads/DongLab/Depression/ASV_depression.xlsx')
map = pd.read_excel('/Users/madelaineleitman/Downloads/DongLab/Depression/Sample_Sheet.xlsx')

#%%
#Add ASV column
asv['ASV'] = ['ASV' + str(i + 1) for i in range(len(asv))]

#%%
#Choose columns
asv = asv.iloc[:,11:]
asv = asv.drop(columns=['All Samples'])

#%%
#Export file
asv.to_csv('/Users/madelaineleitman/Downloads/DongLab/Depression/cleaned_ASV_depression.csv')