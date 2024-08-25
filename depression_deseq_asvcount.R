library("phyloseq")
library("ggplot2")
library("DESeq2")
library("qvalue")
library("data.table")


setwd('/Users/madelaineleitman/Downloads/DongLab/Depression/')


count_dir <- "count_folders"
mapping_file <- 'mapping_depression.csv'

level_dirs <- list.files(count_dir, full.names = TRUE)


for (dir in level_dirs) {
  # Print current directory for debugging
  print(paste("Processing directory:", dir))

  count_file <- file.path(dir, "feature-table.csv")
  metadata_file <- file.path(mapping_file)
  

  if (!file.exists(count_file)) {
    stop(paste("Count file not found:", count_file))
  }
  if (!file.exists(metadata_file)) {
    stop(paste("Metadata file not found:", metadata_file))
  }

  count_data <- read.csv(count_file, row.names = 1)
  meta_data <- read.csv(metadata_file, row.names = 1)
  rownames(meta_data) <- meta_data$Sample.ID

  sample_ids <- rownames(meta_data)  # Sample IDs from the metadata
  count_data <- count_data[, sample_ids, drop = FALSE]  # Reorder count_data columns to match metadata rows
  
  if (!all(rownames(meta_data) == colnames(count_data))) {
    stop("Sample names in count matrix and metadata do not match.")
  }
  
  meta_data$Cohort <- factor(meta_data$Cohort)
  meta_data$Sex <- factor(meta_data$Sex)
  meta_data$Litter <- factor(meta_data$Litter)
  
  OTU <- otu_table(as.matrix(count_data), taxa_are_rows = TRUE)
  sample_data <- sample_data(meta_data)
  physeq <- phyloseq(OTU, sample_data)
  

  dds <- phyloseq_to_deseq2(physeq, ~ Sex + Litter + Cohort)

  dds <- DESeq(dds)
  
  WTvsSERTKO <- results(dds, contrast = c("Cohort", "WT", "SERT KO"))

  WTvsSERTKO <- WTvsSERTKO[order(WTvsSERTKO$padj, na.last = NA), ]
  
  WTvsSERTKOMatrix <- as.data.frame(WTvsSERTKO)
  
  result_file <- file.path(dir, "DESeq2_WTvsSERTKO.csv")
  write.csv(WTvsSERTKOMatrix, result_file)
  
  print(paste("Completed DESeq2 analysis for", basename(dir)))
}


