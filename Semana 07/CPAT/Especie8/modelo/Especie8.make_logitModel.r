data <- read.table(file="./CPAT/Especie8/modelo/Especie8.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie8/modelo/Especie8.logit.RData")
