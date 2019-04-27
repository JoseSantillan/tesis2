data <- read.table(file="./CPAT/Especie62/modelo/Especie62.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie62/modelo/Especie62.logit.RData")
