data <- read.table(file="./modelo_regresion_logistica/Amborella_trichopoda.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./modelo_regresion_logistica/Amborella_trichopoda.logit.RData")
