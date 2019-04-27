data <- read.table(file="./CPAT/Especie70/modelo/Especie70.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie70/modelo/Especie70.logit.RData")
