data <- read.table(file="./CPAT/Especie23/modelo/Especie23.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie23/modelo/Especie23.logit.RData")
