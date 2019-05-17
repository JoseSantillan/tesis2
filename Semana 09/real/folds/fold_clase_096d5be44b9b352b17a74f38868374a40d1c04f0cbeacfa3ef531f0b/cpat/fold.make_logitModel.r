data <- read.table(file="./real/folds/fold_clase_096d5be44b9b352b17a74f38868374a40d1c04f0cbeacfa3ef531f0b/cpat/fold.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./real/folds/fold_clase_096d5be44b9b352b17a74f38868374a40d1c04f0cbeacfa3ef531f0b/cpat/fold.logit.RData")
