data <- read.table(file="./CPAT/Especie80/modelo/Especie80.feature.xls",sep="\t",header=T)
attach(data)
mylogit <- glm(Label ~ mRNA + ORF + Fickett + Hexamer, family=binomial(link="logit"), na.action=na.pass)
save.image("./CPAT/Especie80/modelo/Especie80.logit.RData")
