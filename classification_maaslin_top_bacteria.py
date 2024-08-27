#%%
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt


#data processing
asv = pd.read_csv('/Users/madelaineleitman/Downloads/DongLab/Depression/count_folders/L7_collapsed_table_filtered_001_exported_data/feature-table.csv')
meta = pd.read_csv('/Users/madelaineleitman/Downloads/DongLab/Depression/mapping_depression.csv')

asv.set_index('#OTU ID', inplace=True)
asv = asv.T

y = meta.iloc[:,[3,15]]
y.set_index('Sample ID', inplace=True)

x = asv.reindex(sorted(asv.index, key=lambda x: int(x.replace('Sample', ''))))


top_5_features = ['k__Bacteria;p__Firmicutes;c__Clostridia;o__Eubacteriales;f__Clostridiaceae;g__Clostridium;s__Clostridium sp. MD294', 'k__Bacteria.p__Firmicutes.c__Clostridia.o__Eubacteriales.f__Lachnospiraceae.g__Acetatifactor.s__Acetatifactor MGBC165152', 'k__Bacteria.p__Proteobacteria.c__Deltaproteobacteria.o__Desulfovibrionales.f__Desulfovibrionaceae.g__Desulfovibrio.s__Desulfovibrio MGBC129232', 'k__Bacteria.p__Firmicutes.c__Clostridia.o__Eubacteriales.f__Oscillospiraceae.g__Oscillibacter.s__Oscillibacter MGBC161747','k__Bacteria.p__Firmicutes.c__Clostridia.o__Eubacteriales.f__Lachnospiraceae.g__Schaedlerella.s__Schaedlerella MGBC000001']


top_5_features = [top_5_features[0]] + [i.replace('.', ';') for i in top_5_features[1:]]



x = x.loc[:,top_5_features]


#x.to_csv('/Users/madelaineleitman/Downloads/DongLab/Depression/top_5_bacteria_cleaned.csv')


lb = LabelBinarizer()
y = lb.fit_transform(y)

# If y is a binary classification, LabelBinarizer will produce a 2D array, so you need to flatten it
y = np.squeeze(y)

x.reset_index(drop=True,inplace=True)
x.columns = range(x.shape[1])

#%%

param_grids = {
    'MLPClassifier': {
        'hidden_layer_sizes': [(50,), (100,), (100, 50)],
        'activation': ['relu', 'tanh'],
        'solver': ['adam', 'sgd'],
        'alpha': [0.0001, 0.001],
        'learning_rate': ['constant', 'adaptive'],
        'max_iter': [200, 300]
    },
    'RandomForestClassifier': {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'bootstrap': [True, False]
    },
    'LogisticRegression': {
        'penalty': ['l1', 'l2', 'elasticnet', 'none'],
        'C': [0.1, 1, 10],
        'solver': ['lbfgs', 'saga', 'liblinear']
    }
}

classifiers = {
    'MLPClassifier': MLPClassifier(random_state=1),
    'RandomForestClassifier': RandomForestClassifier(random_state=1),
    'LogisticRegression': LogisticRegression(random_state=1, max_iter=200)
}


kf = KFold(n_splits=5, shuffle=True, random_state=1)


best_models = {}
accuracy_scores = {}
for clf_name, clf in classifiers.items():
    print(f"Processing {clf_name}...")
    grid_search = GridSearchCV(clf, param_grids[clf_name], cv=kf, scoring='accuracy')
    grid_search.fit(x, y)  # Use the entire dataset; grid_search handles CV

    best_models[clf_name] = grid_search.best_estimator_

    print(f"Best parameters found for {clf_name}: {grid_search.best_params_}")


    cv_results = cross_val_score(best_models[clf_name], x, y, cv=kf, scoring='accuracy')
    accuracy_scores[clf_name] = np.mean(cv_results)

    print(f'Cross-validated Accuracy for {clf_name}: {accuracy_scores[clf_name]}')

# Plotting the accuracies
plt.figure(figsize=(10, 6))
plt.bar(accuracy_scores.keys(), accuracy_scores.values(), color='skyblue')
plt.xlabel('Classifier')
plt.ylabel('Cross-validated Accuracy')
plt.title('Cross-validated Accuracy Comparison of Different Classifiers')
plt.ylim([0, 1])  # Set y-axis limits from 0 to 1 for better visualization
plt.savefig('/Users/madelaineleitman/Downloads/DongLab/Depression/maaslin_top_bacteria_plot.png')
