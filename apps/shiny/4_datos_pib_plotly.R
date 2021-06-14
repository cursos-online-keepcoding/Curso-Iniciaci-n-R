# Ejemplo Shiny:
#
# Añadimos grafica plotly

library(shiny)
library(dslabs)
library(plotly)
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
      textOutput(outputId = "txt_out"),
      # Output: Gráfico que dibujamos
      plotlyOutput(outputId = "pibPlot")
      
    )
  )
)

# Función que controla el código. Cada vez que cambia alguna entrada, 
# es decir, cualquier valor de `input`, se ejecuta esta función.
# También ocurre al inicio de la aplicación.
server <- function(input, output) {
  
  min_y <- min(gapminder$life_expectancy)
  max_y <- max(gapminder$life_expectancy)
  gdp_pc <- with(gapminder,
       gdp_pc[!is.infinite(gdp_pc) & !is.na(gdp_pc) ])
  min_x <- min(gdp_pc)
  max_x <- max(gdp_pc)
  
  # Guardamos en el objeto `output` el gráfico deseado en el atributo "pibPlot"
  output$pibPlot <- renderPlotly({
    print(input)
    
    gapminder_year<-gapminder[gapminder$year == input$years,]
    
    fig <- plot_ly(gapminder_year, x=~gdp_pc, y = ~life_expectancy, color = ~continent, size=~population, 
                   text=~country, type = "scatter", 
                   hovertemplate = '<b>Pais:</b>%{text}<br><b>PIBpc:</b>$%{x:.0f}<br><b>Esperanza de vida:</b>%{y:.1f}<br><b>Poblacion:</b>%{marker.size}'
                   )
    fig %>% layout(xaxis=list(title='PIB per capita', range = c(min_x,max_x)),
                   yaxis=list(title='Esperanza de vida', range = c(min_y,max_y)))
    
    
  })
  
  output$txt_out<-renderText({
    paste("Datos para el año",input$years)
  })
  
}

shinyApp(ui = ui, server = server)
