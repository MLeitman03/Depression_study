# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
# File paths and labels
files = {
    'level-2': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-2_taxa_abundance_depression_001.csv.csv',
    'level-3': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-3_taxa_abundance_depression_001.csv',
    'level-4': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-4_taxa_abundance_depression_001.csv',
    'level-5': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-5_taxa_abundance_depression_001.csv',
    'level-6': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-6_taxa_abundance_depression_001.csv'
}

# Loop through each file and create the plot
for level, filepath in files.items():
    # Read the CSV file
    df = pd.read_csv(filepath)

    # Set the index
    df.set_index('index', inplace=True)

    # Select columns that start with 'k__'
    k_cols = [col for col in df.columns if col.startswith('k__')]
    df_clean = df[k_cols]

    # Calculate the row sums
    row_sums = df_clean.sum(axis=1)

    # Calculate the relative abundance
    df_relative = df_clean.div(row_sums, axis=0)

    # Join the 'Cohort' column back
    df_relative = df_relative.join(df['Cohort'])

    # Group by 'Cohort' and calculate the mean relative abundance for each taxon
    cohort_means = df_relative.groupby('Cohort').mean()

    # Plotting
    ax = cohort_means.plot(kind='bar', stacked=True, figsize=(13, 7), colormap='tab20')

    # Customize the plot
    ax.set_xlabel('Cohort')
    ax.set_ylabel('Average Relative Abundance')
    ax.set_title(f'Average Relative Abundance by Cohort ({level})')
    ax.set_xticks(range(len(cohort_means.index)))
    ax.set_xticklabels(cohort_means.index, rotation=0)
    plt.legend(title='Taxa', bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside of plot
    plt.tight_layout()  # Adjust layout to make room for legend

    # Save the plot
    plt.savefig(f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_average_abundance.png')

    # Clear the figure for the next plot
    plt.clf()