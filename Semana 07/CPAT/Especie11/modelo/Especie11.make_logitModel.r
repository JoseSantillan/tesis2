data <- read.table(file="./CPAT/Especie11/modelo/Especie11.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie11/modelo/Especie11.logit.RData")
