# Ejemplo Shiny:
#
# Añadimos gráfica con ggplot

library(shiny)
library(dslabs)
library(ggplot2)
data("gapminder")
gapminder$gdp_pc<-gapminder$gdp/gapminder$population

# Definimos el objeto UI. 
# La función fluidPage() crea una estructura HTML que automáticamente se ajusta 
# a las dimensiones del navegador. Dentro de esta función se definen los elementos
# que se mostrarán en la web.
ui <- fluidPage(
  
  # Título de la aplicación:
  titlePanel("Datos gapminder"),
  
  # Crea un diseño con una barra lateral (sidebarPanel) y un panel principal (mainPanel)
  sidebarLayout(
    
    # Barra lateral con texto:
    sidebarPanel(
      "Gráfica PIB per capita frente esperanza de vida"
    ),
    # Panel principal
    mainPanel(
      # Output: Gráfico que dibujamos
      plotOutput(outputId = "pibPlot")
      
    )
  )
)

# Función que controla el código. Cada vez que cambia alguna entrada, 
# es decir, cualquier valor de `input`, se ejecuta esta función.
# También ocurre al inicio de la aplicación.
server <- function(input, output) {
  
  # Guardamos en el objeto `output` el gráfico deseado en el atributo "pibPlot"
  output$pibPlot <- renderPlot({
    gapminder_2011<-gapminder[gapminder$year==2011,]
    
    ggplot(gapminder_2011,aes(x=gdp_pc,y=life_expectancy,size=population,color=continent))+
      geom_point()+
      xlab("PIB per capita")+ylab("Esperanza de vida")+
      labs(size = "Poblacion",color="Continente")
  })
  
}

shinyApp(ui = ui, server = server)
