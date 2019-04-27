data <- read.table(file="./CPAT/Especie71/modelo/Especie71.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie71/modelo/Especie71.logit.RData")
