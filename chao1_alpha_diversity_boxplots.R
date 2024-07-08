library(ggplot2)
library(plyr)
library(agricolae)
setwd('/Users/madelaineleitman/Downloads/DongLab/Depression/chao1_alpha_diversity/')
data_box_plot<-read.table('alpha-diversity.tsv',sep ='\t', header = TRUE)

mapping <- read.csv2('/Users/madelaineleitman/Downloads/DongLab/Depression/mapping_depression.csv', sep = ',', header = TRUE)

mapping <- cbind(mapping$Sample.ID, mapping$Cohort)


combined <- merge(data_box_plot, mapping, by.x = "X", by.y = "V1")

combined$V2<-factor(combined$V2, levels =c("WT","SERT KO"))

names(combined)[names(combined) == "V2"] <- "Group"
names(combined)[names(combined) == "X"] <- "Sample"

p<-ggplot(combined, aes(y=chao1, x=Group, color=Group))

p + theme_bw() + geom_boxplot() + 
  theme(plot.background=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.text.x=element_text(color="black"),axis.text.y=element_text(color="black")) + 
  scale_color_manual(values=c("green3","red","blue")) + 
  geom_jitter(position=position_jitter(0.1))

#ANOVA

res.aov<-aov(chao1 ~ Group, data=combined)
summary(res.aov)
