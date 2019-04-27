data <- read.table(file="./CPAT/Especie69/modelo/Especie69.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie69/modelo/Especie69.logit.RData")
