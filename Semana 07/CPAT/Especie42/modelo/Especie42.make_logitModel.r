data <- read.table(file="./CPAT/Especie42/modelo/Especie42.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie42/modelo/Especie42.logit.RData")
