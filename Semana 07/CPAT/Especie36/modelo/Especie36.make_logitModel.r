data <- read.table(file="./CPAT/Especie36/modelo/Especie36.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie36/modelo/Especie36.logit.RData")