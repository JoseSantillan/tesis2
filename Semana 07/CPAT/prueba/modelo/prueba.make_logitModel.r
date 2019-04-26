data <- read.table(file="./CPAT/prueba/modelo/prueba.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/prueba/modelo/prueba.logit.RData")
