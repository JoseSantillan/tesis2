data <- read.table(file="./CPAT/Especie43/modelo/Especie43.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie43/modelo/Especie43.logit.RData")
