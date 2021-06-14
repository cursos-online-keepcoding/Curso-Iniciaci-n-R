# Ejemplo Shiny:
#
# Añadimos selectInput que permite seleccionar los ejes

library(shiny)
library(dslabs)
library(plotly)
data("gapminder")
gapminder$gdp_pc<-gapminder$gdp/gapminder$population
gapminder_columns <- list("Mortalidad infantil" = 'infant_mortality', 
                          "Esperanza de vida" = 'life_expectancy', 'Fertilidad'='fertility',
                          'Poblacion'='population','PIB'='gdp','PIB per capita'='gdp_pc')

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
      h3("Gráfica PIB per capita frente esperanza de vida"),
      #Select box para seleccionar el eje X: https://shiny.rstudio.com/gallery/select-box.html
      selectInput(inputId = "select_axis_x", label = "Eje X", 
                  choices = gapminder_columns, 
                  selected = 'gdp_pc'),
      selectInput(inputId = "select_axis_y", label = "Eje Y", 
                  choices = gapminder_columns, 
                  selected = 'life_expectancy'),
      #Slider para seleccionar el Año
      sliderInput(
        "years", label = "Año de estudio:",
        min = min(gapminder$year), value = 2011 , max = max(gapminder$year), step=1, sep=''
      )
    ),
    # Panel principal
    mainPanel(
      textOutput("txt_out"),
      # Output: Gráfico que dibujamos
      plotlyOutput(outputId = "pibPlot")
      
    )
  )
)

# Función que controla el código. Cada vez que cambia alguna entrada, 
# es decir, cualquier valor de `input`, se ejecuta esta función.
# También ocurre al inicio de la aplicación.
server <- function(input, output) {
  
  get_min_max_variable<-function(v){
    v <- v[!is.infinite(v) & !is.na(v) ]
    c(min(v), max(v))
  }
  
  # Guardamos en el objeto `output` el gráfico deseado en el atributo "pibPlot"
  output$pibPlot <- renderPlotly({
    
    gapminder$x=gapminder[,input$select_axis_x]
    gapminder$y=gapminder[,input$select_axis_y]
    gapminder_year<-gapminder[gapminder$year==input$years,]
    gapminder_year<-na.omit(gapminder_year[,c("x","y","continent","population","country")])
    
    axis_x_name <- names(gapminder_columns[gapminder_columns==input$select_axis_x])
    axis_y_name <- names(gapminder_columns[gapminder_columns==input$select_axis_y])
    
    fig <- plot_ly(gapminder_year, x = ~x, y = ~y, color = ~continent, 
                   text=~country, type = "scatter", mode   = 'markers',
                   size=~population ,
                   hovertemplate = paste0('<b>Pais:</b>%{text}<br><b>',axis_x_name,':</b>$%{x:.0f}<br><b>',
                                          axis_y_name,':</b>%{y:.1f}<br>')
                    )
    fig %>% layout(xaxis=list(title=axis_x_name, range = get_min_max_variable(gapminder$x)),
                   yaxis=list(title=axis_y_name, range = get_min_max_variable(gapminder$y)))
    
    
  })
  
  output$txt_out<-renderText({
    paste("Datos para el año",input$years)
  })
  
}

shinyApp(ui = ui, server = server)
