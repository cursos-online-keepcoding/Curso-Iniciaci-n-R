# Ejemplo Shiny:
#
# Añadimos sidebarPanel que permite seleccionar el año


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
      "Gráfica PIB per capita frente esperanza de vida",
      sliderInput(
        inputId = "years", label = "Año de estudio:",
        min = min(gapminder$year), value = 2011 , max = max(gapminder$year), step=1, sep=''
      )
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
  
  min_y <- min(gapminder$life_expectancy)
  max_y <- max(gapminder$life_expectancy)
  min_x <- min(gapminder$gdp_pc)
  max_x <- max(gapminder$gdp_pc)
  
  # Guardamos en el objeto `output` el gráfico deseado en el atributo "pibPlot"
  output$pibPlot <- renderPlot({
    print(input)
    
    gapminder_year<-gapminder[gapminder$year==input$years,]
    
    g<-ggplot(gapminder_year,aes(x=gdp_pc,y=life_expectancy,size=population,color=continent))+
      geom_point()+
      xlab("PIB per capita")+
      ylab("Esperanza de vida")+labs(size = "Poblacion",color="Continente")+
      xlim(min_x,max_x)+ylim(min_y,max_y)
    return(g)
  })
  
}

shinyApp(ui = ui, server = server)
