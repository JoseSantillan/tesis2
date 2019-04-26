data <- read.table(file="./CPAT/Especie5/modelo/Especie5.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie5/modelo/Especie5.logit.RData")
