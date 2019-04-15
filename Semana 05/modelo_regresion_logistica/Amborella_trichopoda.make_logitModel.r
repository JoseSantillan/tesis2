data <- read.table(file="../Semana 05/modelo_regresion_logistica/Amborella_trichopoda.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("../Semana 05/modelo_regresion_logistica/Amborella_trichopoda.logit.RData")
