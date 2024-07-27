### do this for L2 to L6
library(Maaslin2)
library(dplyr)
library(plyr)

for (level in 2:6) {
  input_data <- read.csv(paste0("/Users/madelaineleitman/Downloads/DongLab/Depression/exported_data_L", level, "/feature-table.csv"), sep=",", header=TRUE, row.names=1)
  df_input_data <- as.data.frame(input_data)
  
  input_metadata <- read.csv("/Users/madelaineleitman/Downloads/DongLab/Depression/mapping_depression.csv", header=TRUE)
  df_input_metadata <- input_metadata
  df_input_metadata <- df_input_metadata[match(colnames(df_input_data), df_input_metadata$Sample.ID),]
  rownames(df_input_metadata) <- df_input_metadata$Sample.ID
  
  df_input_metadata$Cohort <- factor(df_input_metadata$Cohort)
  df_input_metadata$Sex <- factor(df_input_metadata$Sex)
  df_input_metadata$Litter <- factor(df_input_metadata$Litter)
  
  fit_data <- Maaslin2(
    input_data = df_input_data, 
    input_metadata = df_input_metadata, 
    output = paste0("/Users/madelaineleitman/Downloads/DongLab/Depression/maaslin2_filtered_L", level), 
    fixed_effects = c("Sex", "Litter", "Cohort"), 
    normalization = "clr", 
    transform = "none", 
    plot_heatmap = FALSE, 
    plot_scatter = FALSE
  )
}
