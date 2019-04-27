data <- read.table(file="./CPAT/Especie10/modelo/Especie10.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie10/modelo/Especie10.logit.RData")
