library(ggplot2)
library(vegan)
library(RColorBrewer)

setwd('/Users/madelaineleitman/Downloads/DongLab/Depression/')
data_pcoa<-read.csv(file = 'pcoa_cleaned_2pc.csv', header = TRUE)
rownames(data_pcoa) <- data_pcoa$X

metadata <- read.csv(file='mapping_depression.csv', sep = ',', header = TRUE)

metadata$Cohort<-factor(metadata$Cohort, levels =c("WT","SERT KO"))

merged_data = merge(data_pcoa, metadata, by.x = 'X', by.y = 'Sample.ID')

# Plot the PCoA with cohort as color
ggplot(merged_data, aes(x = PC1, y = PC2, color = Cohort)) +
  geom_point(size = 3) +
  labs(title = "PCoA Plot", x = "PC1", y = "PC2") +
  theme_minimal()


#With Elipses
# Ensure unique colors for each group
colorCount <- length(unique(merged_data$Cohort))
getPalette <- colorRampPalette(brewer.pal(9, "Set1"))

# Plot the PCoA with ellipses
ggplot(merged_data, aes(x = PC1, y = PC2, color = Cohort)) +
  geom_point(size = 2) +
  stat_ellipse(type = "norm", level = 0.95) +  # Add 95% CI ellipses
  scale_color_manual(values = getPalette(colorCount)) +
  labs(title = "Genus PCoA with 95% CI Ellipses", x = "PC1", y = "PC2") +
  theme_bw() +
  theme(aspect.ratio = 1/1.12,
        plot.background = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank())
