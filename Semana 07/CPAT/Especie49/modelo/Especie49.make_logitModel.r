data <- read.table(file="./CPAT/Especie49/modelo/Especie49.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie49/modelo/Especie49.logit.RData")
