library(ggplot2)
library(plyr)
library(agricolae)
setwd('/Users/madelaineleitman/Downloads/DongLab/Depression/shannon_alpha_diversty/')
data_box_plot<-read.table('alpha-diversity.tsv',sep ='\t', header = TRUE)

mapping <- read.csv2('/Users/madelaineleitman/Downloads/DongLab/Depression/mapping_depression.csv', sep = ',', header = TRUE)

mapping <- cbind(mapping$Sample.ID, mapping$Cohort)

colnames(mapping) <- c('Sample', 'Group')
colnames(data_box_plot)[1] <- ('Sample')

combined <- merge(data_box_plot, mapping, by= "Sample")

combined$Group<-factor(combined$Group, levels =c("WT","SERT KO"))

p<-ggplot(combined, aes(y=shannon_entropy, x=Group, color=Group))

p + theme_bw() + geom_boxplot() + 
  theme(plot.background=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.text.x=element_text(color="black"),axis.text.y=element_text(color="black")) + 
  scale_color_manual(values=c("green3","red","blue")) + 
  geom_jitter(position=position_jitter(0.1))

#ANOVA

res.aov<-aov(shannon_entropy ~ Group, data=combined)
summary(res.aov)
