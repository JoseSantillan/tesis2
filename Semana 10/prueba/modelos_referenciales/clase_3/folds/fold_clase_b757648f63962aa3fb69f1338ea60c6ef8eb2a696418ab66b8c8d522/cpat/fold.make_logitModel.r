data <- read.table(file="prueba/modelos_referenciales/clase_3/folds/fold_clase_b757648f63962aa3fb69f1338ea60c6ef8eb2a696418ab66b8c8d522/cpat/fold.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("prueba/modelos_referenciales/clase_3/folds/fold_clase_b757648f63962aa3fb69f1338ea60c6ef8eb2a696418ab66b8c8d522/cpat/fold.logit.RData")
