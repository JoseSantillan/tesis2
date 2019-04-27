data <- read.table(file="./CPAT/Especie63/modelo/Especie63.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie63/modelo/Especie63.logit.RData")
