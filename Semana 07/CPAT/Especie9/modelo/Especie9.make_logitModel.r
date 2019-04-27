data <- read.table(file="./CPAT/Especie9/modelo/Especie9.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie9/modelo/Especie9.logit.RData")