obtener_precio_cierre_ajustado<-function(ticker, fecha_inicio, fecha_fin=Sys.Date() ){
  xts_tick<-getSymbols(ticker, ticket = "yahoo", from = fecha_inicio, to=fecha_fin, auto.assign = F)
  precio_cierre_ajustado<-as.data.frame(xts_tick)[,6]
  precio_cierre_ajustado
}

calcula_maximos_dias_retorno_positivo<-function(precio_cierre_ajustado ){
  idx <- 2
  num_dias_consecutivos <- 0
  max_num_dias_consecutivos <- 0
  while(idx<=length(precio_cierre_ajustado)){
    diferencia_precio_cierre_ayer <- precio_cierre_ajustado[idx]-precio_cierre_ajustado[idx-1]
    if (diferencia_precio_cierre_ayer>0){
      #Hay subida del precio de la acción
      num_dias_consecutivos <- num_dias_consecutivos+1
    }else{
      #NO hay subida del precio de la acción
      max_num_dias_consecutivos <- max(c(num_dias_consecutivos, max_num_dias_consecutivos))
      num_dias_consecutivos <- 0
    }
    idx<-idx+1  
  }
  max_num_dias_consecutivos
}

calcula_maximos_dias_retorno_positivo_diff<-function(precio_cierre_ajustado ){
  diferencia_precio_cierre_ajustado <- diff(precio_cierre_ajustado)
  subida_precio_cierre_ajustado <- diferencia_precio_cierre_ajustado>0
  numero_dias_sin_subida <- cumsum(!subida_precio_cierre_ajustado)
  
  max(sapply(split(subida_precio_cierre_ajustado,numero_dias_sin_subida),sum))
}
