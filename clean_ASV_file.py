#%%
#Import libraries
import pandas as pd

#%%
#Upload data
asv = pd.read_excel('/Users/madelaineleitman/Downloads/DongLab/Depression/ASV_depression.xlsx')
map_to_group = pd.read_excel('/Users/madelaineleitman/Downloads/DongLab/Depression/Sample_Sheet.xlsx')
map_to_id = pd.read_excel('/Users/madelaineleitman/Downloads/DongLab/Depression/ASV_depression.xlsx', sheet_name='Metadata')

#%%
#Add ASV column
asv['ASV'] = ['ASV' + str(i + 1) for i in range(len(asv))]

#%%
asv_mapping = asv.iloc[:,0:12]

#%%
#Choose columns
asv = asv.iloc[:,11:]
asv = asv.drop(columns=['All Samples'])

#%%
#Add Sample ID to map
map_to_group.rename(columns={'Sample Type': 'Sample ID'}, inplace=True)
map_to_group['Sample ID'] = ['Sample' + str(i + 1) for i in range(len(map_to_group))]

#%%
#Create dict
sample_dict = dict(zip(map_to_id.iloc[1,:].tolist(), map_to_id.columns.tolist()))
sample_dict = dict(list(sample_dict.items())[2:])
#%%

sample_dict = {value: key for key, value in sample_dict.items()}

#%%

for col in asv.columns:
    print(col)
    if col == 'ASV':
        asv.rename(columns={col: 'ASV'}, inplace=False)
    else:
        print(sample_dict[col])
        asv.rename(columns={col: sample_dict[col]}, inplace=True)

#%%

one_codex_ids = map_to_group['One Codex ID'].tolist()
id_to_sample = dict(zip(one_codex_ids, map_to_group['Sample ID']))

#%%
#Change column names
for col in asv.columns:
    print(col)
    if col == 'ASV':
        asv.rename(columns={col: 'ASV'}, inplace=False)
    else:
        print(id_to_sample[col])
        asv.rename(columns={col: id_to_sample[col]}, inplace=True)

#%%
asv.rename(columns = {'ASV': 'OTU ID'}, inplace=True)

#%%
# Save the modified DataFrame to a text file
output_file_path = '/Users/madelaineleitman/Downloads/DongLab/Depression/cleaned_ASV_depression.txt'
asv.to_csv(output_file_path, sep='\t', index=False)

#%%
#Save mapping file
output_file_path = '/Users/madelaineleitman/Downloads/DongLab/Depression/mapping_depression.csv'
map_to_group.to_csv(output_file_path)

#%%
#Save ASV to taxa file
output_file_path = '/Users/madelaineleitman/Downloads/DongLab/Depression/asv_mapping_depression.csv'
asv_mapping.to_csv(output_file_path)