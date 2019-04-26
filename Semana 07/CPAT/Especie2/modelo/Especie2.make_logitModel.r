data <- read.table(file="./CPAT/Especie2/modelo/Especie2.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie2/modelo/Especie2.logit.RData")
