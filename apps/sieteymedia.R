
repeat({

numero <-c(1:7,"sota","caballo","rey")
palo   <- c("espadas","bastos","copas","oros")
#cartas<-outer(numero,palo,FUN=paste)
#dim(cartas)<- c(length(cartas),1)

df_cartas = merge(numero,palo)
colnames(df_cartas)<-c("numero","palo")
df_cartas$valor<-as.numeric(as.character(df_cartas$numero))
df_cartas$valor[is.na(df_cartas$valor)]<-0.5
#cartas <- paste(df_cartas$x,df_cartas$y)


saca_carta <- function(cartas, num_cartas=1){
    id_carta <- sample(1:nrow(df_cartas),num_cartas)
    cartas_seleccionada <- cartas[id_carta,]
    cartas_restantes<- cartas[-id_carta,]
    list(seleccion=cartas_seleccionada, resto=cartas_restantes)
}
MAX_VALOR <- 7.5
s_n="S"
total_valor=0
while(s_n!="N") {  
  if (s_n=="S"){
    ret <- saca_carta(df_cartas)
    carta<-ret$seleccion
    df_cartas<-ret$resto
    print(paste("La carta es: ",carta$numero,"de", carta$palo))
    total_valor=total_valor+carta$valor
    if (total_valor>MAX_VALOR){
       print(paste("Lo sentimos, has perdido. Tu puntuación era",total_valor))
       break;       
    }
  }else{
    print("Por favor, responde S/N")	  
  }
  s_n <- readline("¿Deseas una nueva carta? (S/N)")
}
if (s_n=="N"){
    print(paste("Tu puntuación es:",total_valor))
    ret <- saca_carta(df_cartas)
    carta<-ret$seleccion
    
    print(paste0("La BANCA saca la carta: ",carta$numero," de ", carta$palo))
    puntuacion_banca<-total_valor+carta$valor
    print(paste0("Tu puntuación es:",total_valor," la puntuación de la BANCA ",puntuacion_banca))
    if (puntuacion_banca>MAX_VALOR){
    	print("Has ganado!")
    }else{
    	print("Gana la BANCA, es el mercado amigo!")
    }
}

s_n <- readline("¿Deseas volver a jugar? (S/N)")
if (s_n=="N"){
  break;
}


})