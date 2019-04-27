load("./CPAT/Especie63/modelo/Especie63.logit.RData")
test <- read.table(file="./CPAT/Especie63/modelo/Especie63.dat",sep="\t",col.names=c("ID","mRNA","ORF","Fickett","Hexamer"))
test$prob <- predict(mylogit,newdata=test,type="response")
attach(test)
output <- cbind("mRNA_size"=mRNA,"ORF_size"=ORF,"Fickett_score"=Fickett,"Hexamer_score"=Hexamer,"coding_prob"=test$prob)
write.table(output,file="./CPAT/Especie63/modelo/Especie63",quote=F,sep="\t",row.names=ID)
