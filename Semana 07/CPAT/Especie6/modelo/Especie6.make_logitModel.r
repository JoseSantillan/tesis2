data <- read.table(file="./CPAT/Especie6/modelo/Especie6.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie6/modelo/Especie6.logit.RData")
