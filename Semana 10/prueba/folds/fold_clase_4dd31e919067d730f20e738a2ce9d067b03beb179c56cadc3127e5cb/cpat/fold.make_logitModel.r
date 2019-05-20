data <- read.table(file="prueba/folds/fold_clase_4dd31e919067d730f20e738a2ce9d067b03beb179c56cadc3127e5cb/cpat/fold.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("prueba/folds/fold_clase_4dd31e919067d730f20e738a2ce9d067b03beb179c56cadc3127e5cb/cpat/fold.logit.RData")
