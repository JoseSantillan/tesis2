data <- read.table(file="./CPAT/Especie57/modelo/Especie57.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie57/modelo/Especie57.logit.RData")
