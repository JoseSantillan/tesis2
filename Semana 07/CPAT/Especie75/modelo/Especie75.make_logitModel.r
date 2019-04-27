data <- read.table(file="./CPAT/Especie75/modelo/Especie75.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie75/modelo/Especie75.logit.RData")
