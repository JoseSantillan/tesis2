data <- read.table(file="prueba/modelos_referenciales/clase_2/folds/fold_clase_47d800247683ac6d254a40958ec5c9bd45dc79edcfcd88b71b2c91ce/cpat/fold.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("prueba/modelos_referenciales/clase_2/folds/fold_clase_47d800247683ac6d254a40958ec5c9bd45dc79edcfcd88b71b2c91ce/cpat/fold.logit.RData")
