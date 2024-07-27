#%%
import numpy as np
import pandas as pd

#%%
asv_map = pd.read_csv('/Users/madelaineleitman/Downloads/DongLab/Depression/asv_mapping_depression.csv')

#%%
asv_map = asv_map.iloc[:,[0,5,6,7,8,9,10,11]]

#%%

for i,row in asv_map.iterrows():
    cols = ['Type', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    if row['Type'] != 'Bacteria':
        for col in cols:
            row[col] = np.nan
    elif pd.isna(row['Phylum']):
        cols = cols[1:]
        for col in cols:
            row[col] = row['Type']
    elif pd.isna(row['Class']):
        cols = cols[2:]
        for col in cols:
            row[col] = row['Phylum']
    elif pd.isna(row['Order']):
        cols = cols[3:]
        for col in cols:
            row[col] = row['Class']
    elif pd.isna(row['Family']):
        cols = cols[4:]
        for col in cols:
            row[col] = row['Order']
    elif pd.isna(row['Genus']):
        cols = cols[5:]
        for col in cols:
            row[col] = row['Family']
    elif pd.isna(row['Species']):
        cols = cols[6:]
        for col in cols:
            row[col] = row['Genus']

    #add prefix
    asv_map.at[i,'Type'] = 'k__' + str(row['Type'])
    asv_map.at[i,'Phylum'] = 'p__' + str(row['Phylum'])
    asv_map.at[i,'Class'] = 'c__' + str(row['Class'])
    asv_map.at[i,'Order'] = 'o__' + str(row['Order'])
    asv_map.at[i,'Family'] = 'f__' + str(row['Family'])
    asv_map.at[i,'Genus'] = 'g__' + str(row['Genus'])
    asv_map.at[i,'Species'] = 's__' + str(row['Species'])

    #combine taxon info and separate by '; '
    asv_map['Taxon'] = asv_map.apply(lambda row: '; '.join(row[1:].values.astype(str)), axis=1)

#%%
for i,row in asv_map.iterrows():
    cols = ['Type', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    if row['Type'] != 'Bacteria':
        for col in cols:
            row[col] = np.nan
    elif pd.isna(row['Phylum']):
        cols = cols[1:]
        for col in cols:
            row[col] = row['Type']
    elif pd.isna(row['Class']):
        cols = cols[2:]
        for col in cols:
            row[col] = row['Phylum']
    elif pd.isna(row['Order']):
        cols = cols[3:]
        for col in cols:
            row[col] = row['Class']
    elif pd.isna(row['Family']):
        cols = cols[4:]
        for col in cols:
            row[col] = row['Order']
    elif pd.isna(row['Genus']):
        cols = cols[5:]
        for col in cols:
            row[col] = row['Family']
    elif pd.isna(row['Species']):
        cols = cols[6:]
        for col in cols:
            row[col] = row['Genus']

    #add prefix
    asv_map.at[i,'Type'] = 'k__' + str(row['Type'])
    asv_map.at[i,'Phylum'] = 'p__' + str(row['Phylum'])
    asv_map.at[i,'Class'] = 'c__' + str(row['Class'])
    asv_map.at[i,'Order'] = 'o__' + str(row['Order'])
    asv_map.at[i,'Family'] = 'f__' + str(row['Family'])
    asv_map.at[i,'Genus'] = 'g__' + str(row['Genus'])
    asv_map.at[i,'Species'] = 's__' + str(row['Species'])

    #combine taxon info and separate by '; '
    asv_map['Taxon'] = asv_map.apply(lambda row: '; '.join(row[1:].values.astype(str)), axis=1)

#%%
# Define columns to be updated
cols = ['Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']

# Function to update taxonomy information
def update_taxonomy(row):
    if row['Type'] != 'Bacteria':
        row[cols] = np.nan
    else:
        for col in cols:
            if pd.isna(row[col]):
                row[col] = row[cols[cols.index(col) - 1] if cols.index(col) > 0 else 'Type']
    return row

# Apply the update function
asv_map = asv_map.apply(update_taxonomy, axis=1)

# Add prefixes
asv_map['Type'] = 'k__' + asv_map['Type'].astype(str)
asv_map['Phylum'] = 'p__' + asv_map['Phylum'].astype(str)
asv_map['Class'] = 'c__' + asv_map['Class'].astype(str)
asv_map['Order'] = 'o__' + asv_map['Order'].astype(str)
asv_map['Family'] = 'f__' + asv_map['Family'].astype(str)
asv_map['Genus'] = 'g__' + asv_map['Genus'].astype(str)
asv_map['Species'] = 's__' + asv_map['Species'].astype(str)

# Combine taxon info and separate by '; '
asv_map['Taxon'] = asv_map.apply(lambda row: '; '.join(row[1:].values.astype(str)), axis=1)

#%%
asv_map_clean = asv_map.iloc[:,[0,-1]]

#%%
asv_map_clean.to_csv('/Users/madelaineleitman/Downloads/DongLab/Depression/asv_mapping_depression_clean.tsv', sep= '\t', index=False)