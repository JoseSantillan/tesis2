data <- read.table(file="./CPAT/Especie68/modelo/Especie68.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie68/modelo/Especie68.logit.RData")
