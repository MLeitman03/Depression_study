library("phyloseq")
library("ggplot2")
library("DESeq2")
library("qvalue")
library("data.table")

# Set the working directory
setwd('/Users/madelaineleitman/Downloads/DongLab/Depression/')

# Define the base directory containing all your level directories
count_dir <- "count_folders"
mapping_file <- 'mapping_depression.csv'

# List all level directories (L1 to L7)
level_dirs <- list.files(count_dir, full.names = TRUE)

# Loop through each directory and perform DESeq2 analysis
for (dir in level_dirs) {
  # Print current directory for debugging
  print(paste("Processing directory:", dir))
  
  # Set the file paths for the count matrix and metadata
  count_file <- file.path(dir, "feature-table.csv")
  metadata_file <- file.path(mapping_file)
  
  # Check if the files exist before proceeding
  if (!file.exists(count_file)) {
    stop(paste("Count file not found:", count_file))
  }
  if (!file.exists(metadata_file)) {
    stop(paste("Metadata file not found:", metadata_file))
  }
  
  # Read the count matrix and metadata
  count_data <- read.csv(count_file, row.names = 1)
  meta_data <- read.csv(metadata_file, row.names = 1)
  rownames(meta_data) <- meta_data$Sample.ID
  
  # Ensure that sample IDs match and reorder columns
  sample_ids <- rownames(meta_data)  # Sample IDs from the metadata
  count_data <- count_data[, sample_ids, drop = FALSE]  # Reorder count_data columns to match metadata rows
  
  # Check if sample names match between metadata and count matrix
  if (!all(rownames(meta_data) == colnames(count_data))) {
    stop("Sample names in count matrix and metadata do not match.")
  }
  
  # Convert relevant columns to factors
  meta_data$Cohort <- factor(meta_data$Cohort)
  meta_data$Sex <- factor(meta_data$Sex)
  meta_data$Litter <- factor(meta_data$Litter)
  
  # Create a phyloseq object
  OTU <- otu_table(as.matrix(count_data), taxa_are_rows = TRUE)
  sample_data <- sample_data(meta_data)
  physeq <- phyloseq(OTU, sample_data)
  
  # Convert phyloseq object to DESeq2 object
  dds <- phyloseq_to_deseq2(physeq, ~ Sex + Litter + Cohort)
  
  # Run the DESeq2 analysis
  dds <- DESeq(dds)
  
  # Perform the contrast for WT vs SERT KO
  WTvsSERTKO <- results(dds, contrast = c("Cohort", "WT", "SERT KO"))
  
  # Order results by adjusted p-value
  WTvsSERTKO <- WTvsSERTKO[order(WTvsSERTKO$padj, na.last = NA), ]
  
  # Convert results to data frame and add q-values
  WTvsSERTKOMatrix <- as.data.frame(WTvsSERTKO)
  
  # Save results to CSV
  result_file <- file.path(dir, "DESeq2_WTvsSERTKO.csv")
  write.csv(WTvsSERTKOMatrix, result_file)
  
  # Optionally print status
  print(paste("Completed DESeq2 analysis for", basename(dir)))
}


