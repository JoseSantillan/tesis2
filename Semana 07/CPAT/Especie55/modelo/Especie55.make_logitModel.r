data <- read.table(file="./CPAT/Especie55/modelo/Especie55.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie55/modelo/Especie55.logit.RData")
