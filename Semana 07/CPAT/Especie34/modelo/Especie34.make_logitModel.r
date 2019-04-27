data <- read.table(file="./CPAT/Especie34/modelo/Especie34.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie34/modelo/Especie34.logit.RData")
