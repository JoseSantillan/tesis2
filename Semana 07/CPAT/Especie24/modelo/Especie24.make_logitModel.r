data <- read.table(file="./CPAT/Especie24/modelo/Especie24.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie24/modelo/Especie24.logit.RData")
