library(mixOmics)
library(ggplot2)
library(randomForest)
library(caret)
library(caTools)


x <- read.csv('/Users/madelaineleitman/Downloads/DongLab/Depression/samples_asv_aug26.csv', row.names = 'X')
y <- read.csv('/Users/madelaineleitman/Downloads/DongLab/Depression/cohort_classification_aug26.csv', row.names = 'Sample.ID')

y <- as.factor(y$Cohort)

# Perform sPLS-DA with 2 components and keepX to select top 5 features
splsda_model <- splsda(x, y, ncomp = 2, keepX = c(5, 5)) # Adjust keepX for more or fewer features

# Assuming you have already run sPLS-DA
# splsda_model <- splsda(X, Y, ncomp = 2, keepX = c(5, 5)) 

# Extract the loadings for the selected features
selected_vars <- splsda_model$loadings$X

# Find the top 5 features based on their contribution to the first component
top_5_features <- rownames(selected_vars)[order(abs(selected_vars[, 1]), decreasing = TRUE)][1:5]

print("Top 5 features contributing to variance between the groups:")
print(top_5_features)


# Get the absolute loadings of these features (magnitude of contributions)
top_5_contributions <- abs(selected_vars[top_5_features, 1])


top_5_df <- data.frame(
  Feature = top_5_features,
  Contribution = top_5_contributions
)

ggplot(top_5_df, aes(x = reorder(Feature, -Contribution), y = Contribution)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Top 5 Features Contribution to Variance",
       x = "Feature",
       y = "Absolute Contribution") +
  theme_minimal()

write.csv(x=top_5_df, '/Users/madelaineleitman/Downloads/DongLab/Depression/top_5_bacteria.csv')


