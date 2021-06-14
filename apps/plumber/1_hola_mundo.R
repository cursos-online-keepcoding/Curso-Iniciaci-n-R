#Ejemplo de plumber https://www.rplumber.io/


#* Mensaje de entrada
#* @get /hola_mundo
function() {
  list(msg = "Hola mundo!")
}

#* Suma de dos números
#* @param a El primer número
#* @param b El segundo número
#* @get /sum
function(a,b){
  as.numeric(a)+as.numeric(b)
}

#library(plumber)
plumb('1_hola_mundo.R') %>% pr_run(port=8080)