load("../Semana 05/tablas_hexamer/Amborella_trichopoda_logitModel.RData")
test <- read.table(file="../Semana 05/cpat_features/Amborella_trichopoda.PCT.dat",sep="\t",col.names=c("ID","mRNA","ORF","Fickett","Hexamer"))
test$prob <- predict(mylogit,newdata=test,type="response")
attach(test)
output <- cbind("mRNA_size"=mRNA,"ORF_size"=ORF,"Fickett_score"=Fickett,"Hexamer_score"=Hexamer,"coding_prob"=test$prob)
write.table(output,file="../Semana 05/cpat_features/Amborella_trichopoda.PCT",quote=F,sep="\t",row.names=ID)
