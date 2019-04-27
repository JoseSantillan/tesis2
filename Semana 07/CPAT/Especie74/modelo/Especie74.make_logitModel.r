data <- read.table(file="./CPAT/Especie74/modelo/Especie74.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie74/modelo/Especie74.logit.RData")
