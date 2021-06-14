#Ejemplo de plumber https://www.rplumber.io/

library(dslabs)
library(ggplot2)
data("gapminder")
gapminder$gdp_pc<-gapminder$gdp/gapminder$population

#* Imagen del PIB per capita 
#* @png(width = 800, height=600)
#* @param year
#* @get /pib_plot
function(year) {
  min_y <- min(gapminder$life_expectancy)
  max_y <- max(gapminder$life_expectancy)
  gdp_pc <- with(gapminder,
                 gdp_pc[!is.infinite(gdp_pc) & !is.na(gdp_pc) ])
  min_x <- min(gdp_pc)
  max_x <- max(gdp_pc)
  
  
  
  gapminder_year<-gapminder[gapminder$year==year,]
  g<-ggplot(gapminder_year,aes(x=gdp_pc,y=life_expectancy,size=population,color=continent))+
      geom_point()+xlab("PIB per capita")+ylab("Esperanza de vida")+labs(size = "Poblacion",color="Continente")+
      xlim(min_x,max_x)+ylim(min_y,max_y)
  
#  file <- "pib_plot.png"
#  ggsave(file, g)
#  readBin(file, "raw", n = file.info(file)$size)
  print(g)
}

#*@assets . /files
list()


#library(plumber)
#plumb('3_datos_pib_interactivo.R') %>% pr_run(port=8080)
# Cargar en navegador: http://127.0.0.1:8080/files/3_datos_pib_interactivo.html