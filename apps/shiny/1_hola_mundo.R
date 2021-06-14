library(shiny)

ui <- fluidPage(
  titlePanel("Hola mundo!"),
)
server <- function(input, output, session) {}
shinyApp(ui = ui, server = server)
