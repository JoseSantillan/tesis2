data <- read.table(file="./CPAT/Especie73/modelo/Especie73.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie73/modelo/Especie73.logit.RData")
