data <- read.table(file="prueba/modelos_referenciales/clase_1/folds/fold_clase_ff985b10013a354a5b9fbffb8cba33fc8b2ca80aebd22c8e9ff678d9/cpat/fold.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("prueba/modelos_referenciales/clase_1/folds/fold_clase_ff985b10013a354a5b9fbffb8cba33fc8b2ca80aebd22c8e9ff678d9/cpat/fold.logit.RData")
