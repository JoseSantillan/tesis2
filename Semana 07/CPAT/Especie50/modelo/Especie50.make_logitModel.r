data <- read.table(file="./CPAT/Especie50/modelo/Especie50.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie50/modelo/Especie50.logit.RData")
