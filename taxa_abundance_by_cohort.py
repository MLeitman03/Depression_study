# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from mlxtend.evaluate import permutation_test
from scipy.stats import mannwhitneyu

# %%
# File paths and labels
files = {
    'level-2': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-2_taxa_abundance_depression_001.csv.csv',
    'level-3': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-3_taxa_abundance_depression_001.csv',
    'level-4': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-4_taxa_abundance_depression_001.csv',
    'level-5': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-5_taxa_abundance_depression_001.csv',
    'level-6': '/Users/madelaineleitman/Downloads/DongLab/Depression/level-6_taxa_abundance_depression_001.csv'
}

#%%

palette = {'SERT KO': 'skyblue', 'WT': 'salmon'}


for level, filepath in files.items():

    df = pd.read_csv(filepath)

    df.set_index('index', inplace=True)

    # Select columns that start with 'k__'
    k_cols = [col for col in df.columns if col.startswith('k__')]
    df_clean = df[k_cols]

    # Calculate the row sums
    row_sums = df_clean.sum(axis=1)

    # Calculate the relative abundance
    df_relative = df_clean.div(row_sums, axis=0)
    df_relative = df_relative.join(df['Cohort'])

    # Group by 'Cohort' and calculate the mean relative abundance for each taxon
    cohort_means = df_relative.groupby('Cohort').mean()

    plt.figure(figsize=(13, 7))
    ax = cohort_means.plot(kind='bar', stacked=True, figsize=(13, 7))

    ax.set_xlabel('Cohort')
    ax.set_ylabel('Average Relative Abundance')
    ax.set_title(f'Average Relative Abundance by Cohort ({level})')
    ax.set_xticks(range(len(cohort_means.index)))
    ax.set_xticklabels(cohort_means.index, rotation=0)
    plt.legend(title='Taxa', bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside of plot
    plt.tight_layout()  # Adjust layout to make room for legend

    plt.savefig(f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_average_abundance.png')
    plt.clf()

    # Perform t-tests
    results = {'Taxa': [], 'p-value': [], 'mean_SERT_KO': [], 'mean_WT': []}

    for col in k_cols:
        group1 = df[df['Cohort'] == 'SERT KO'][col]
        group2 = df[df['Cohort'] == 'WT'][col]

        t_stat, p_val = ttest_ind(group1, group2, nan_policy='omit')

        results['Taxa'].append(col)
        results['p-value'].append(p_val)
        results['mean_SERT_KO'].append(group1.mean())
        results['mean_WT'].append(group2.mean())

        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Cohort', y=col, data=df, palette=palette)
        sns.stripplot(x='Cohort', y=col, data=df, jitter=True, color='black', alpha=0.5)
        plt.title(f'Comparison of {col} by Cohort ({level})')
        plt.ylabel('Relative Abundance')
        plt.xlabel('Cohort')
        plt.tight_layout()
        plt.savefig(f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_{col}_jitter_plot.png')
        plt.clf()

    results_df = pd.DataFrame(results)

    results_df.to_csv(f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_t_test_results.csv', index=False)

#%%

for level, filepath in files.items():

    df = pd.read_csv(filepath)

    df.set_index('index', inplace=True)

    # Select columns that start with 'k__'
    k_cols = [col for col in df.columns if col.startswith('k__')]
    df_clean = df[k_cols]

    # Calculate the row sums
    row_sums = df_clean.sum(axis=1)

    # Calculate the relative abundance
    df_relative = df_clean.div(row_sums, axis=0)
    df_relative = df_relative.join(df['Cohort'])

    # Group by 'Cohort' and calculate the mean relative abundance for each taxon
    cohort_means = df_relative.groupby('Cohort').mean()

    # Perform permutation tests
    results = {'Taxa': [], 'p-value': [], 'mean_SERT_KO': [], 'mean_WT': []}

    for col in k_cols:
        group1 = df[df['Cohort'] == 'SERT KO'][col]
        group2 = df[df['Cohort'] == 'WT'][col]

        p_val = permutation_test(group1, group2, method='approximate', num_rounds=10000, seed=42)

        results['Taxa'].append(col)
        results['p-value'].append(p_val)
        results['mean_SERT_KO'].append(group1.mean())
        results['mean_WT'].append(group2.mean())


    results_df = pd.DataFrame(results)

    results_df.to_csv(f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_permutation_test_results.csv', index=False)

#%%
# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# %%

def bootstrap_mean_diff(group1, group2, num_bootstrap=10000):
    # Compute the observed difference in means
    observed_diff = np.mean(group1) - np.mean(group2)

    # Combine the groups for bootstrapping
    combined = np.concatenate([group1, group2])

    # Generate bootstrap samples and compute mean differences
    bootstrap_diffs = []
    for _ in range(num_bootstrap):
        np.random.shuffle(combined)
        new_group1 = combined[:len(group1)]
        new_group2 = combined[len(group1):]
        bootstrap_diffs.append(np.mean(new_group1) - np.mean(new_group2))

    # Calculate the p-value
    p_val = np.mean(np.abs(bootstrap_diffs) >= np.abs(observed_diff))

    return p_val, observed_diff


for level, filepath in files.items():

    df = pd.read_csv(filepath)

    df.set_index('index', inplace=True)

    # Select columns that start with 'k__'
    k_cols = [col for col in df.columns if col.startswith('k__')]
    df_clean = df[k_cols]

    # Calculate the row sums
    row_sums = df_clean.sum(axis=1)

    # Calculate the relative abundance
    df_relative = df_clean.div(row_sums, axis=0)
    df_relative = df_relative.join(df['Cohort'])

    # Group by 'Cohort' and calculate the mean relative abundance for each taxon
    cohort_means = df_relative.groupby('Cohort').mean()

    # Perform bootstrapping
    results = {'Taxa': [], 'p-value': [], 'mean_SERT_KO': [], 'mean_WT': [], 'observed_diff': []}

    for col in k_cols:
        group1 = df[df['Cohort'] == 'SERT KO'][col]
        group2 = df[df['Cohort'] == 'WT'][col]

        p_val, observed_diff = bootstrap_mean_diff(group1.values, group2.values)

        results['Taxa'].append(col)
        results['p-value'].append(p_val)
        results['mean_SERT_KO'].append(group1.mean())
        results['mean_WT'].append(group2.mean())
        results['observed_diff'].append(observed_diff)

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_bootstrap_test_results.csv', index=False)


# %%

for level, filepath in files.items():

    df = pd.read_csv(filepath)

    df.set_index('index', inplace=True)

    # Select columns that start with 'k__'
    k_cols = [col for col in df.columns if col.startswith('k__')]
    df_clean = df[k_cols]

    # Calculate the row sums
    row_sums = df_clean.sum(axis=1)

    # Calculate the relative abundance
    df_relative = df_clean.div(row_sums, axis=0)
    df_relative = df_relative.join(df['Cohort'])

    # Group by 'Cohort' and calculate the mean relative abundance for each taxon
    cohort_means = df_relative.groupby('Cohort').mean()

    # Perform Mann-Whitney U tests
    results = {'Taxa': [], 'p-value': [], 'mean_SERT_KO': [], 'mean_WT': []}

    for col in k_cols:
        group1 = df[df['Cohort'] == 'SERT KO'][col]
        group2 = df[df['Cohort'] == 'WT'][col]

        u_stat, p_val = mannwhitneyu(group1, group2, alternative='two-sided')

        results['Taxa'].append(col)
        results['p-value'].append(p_val)
        results['mean_SERT_KO'].append(group1.mean())
        results['mean_WT'].append(group2.mean())

    results_df = pd.DataFrame(results)

    results_df.to_csv(f'/Users/madelaineleitman/Downloads/DongLab/Depression/outputs/{level}_mannwhitneyu_test_results.csv', index=False)