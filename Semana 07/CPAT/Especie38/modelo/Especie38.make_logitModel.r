data <- read.table(file="./CPAT/Especie38/modelo/Especie38.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie38/modelo/Especie38.logit.RData")
