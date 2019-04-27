data <- read.table(file="./CPAT/Especie33/modelo/Especie33.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie33/modelo/Especie33.logit.RData")
