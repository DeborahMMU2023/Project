from dash import Dash, html, dcc, Output, Input
import pandas as pd
import dash_daq as daq 
import plotly.express as px

app = Dash(__name__)
server = app.server

# Read your CSV data
data_url = "https://raw.githubusercontent.com/DeborahMMU2023/DataVisualization/spotifydata/data.csv"
dataSpotify = pd.read_csv(data_url)

# Define a function to create the boxplot using Plotly Express
def create_boxplot(data):
    fig = px.box(data, y='acousticness')
    fig.update_layout(title='Acousticness')
    
    return fig

# Create a Slider component
slider = daq.Slider(
    id='acousticness-slider',
    min=0,
    max=1,
    step=0.1,
    value=0.5,
    marks={0: '0', 1: '1'},  # Add marks for the slider
)

# Define a callback to update the boxplot based on the slider value
@app.callback(Output('boxplot', 'figure'), Input('acousticness-slider', 'value'))
def update_boxplot(acousticness_value):
    filtered_data = dataSpotify[dataSpotify['acousticness'] <= acousticness_value]
    fig = create_boxplot(filtered_data)
    return fig


# Define a function to create the bar chart using Plotly Express
def create_bar_chart(data, num_songs=10):
    popular_songs = data['song_title'].value_counts().sort_values(ascending=False)[:num_songs]
    popular_songs = pd.DataFrame(popular_songs).reset_index()
    popular_songs = popular_songs.rename(columns={"index": "Songs", "song_title": "Count"})
    
    fig = px.bar(popular_songs, x='Songs', y='Count', title=f"{num_songs} Songs")
    fig.update_yaxes(title_text='Listeners per million')
    
    return fig

# Define a function to create the pie chart using Plotly Express
def create_pie_chart(data, num_artists=10):
    popular_artists = data['artist'].value_counts().sort_values(ascending=False)[:num_artists]
    popular_artists = pd.DataFrame(popular_artists).reset_index()
    popular_artists = popular_artists.rename(columns={"index": "Artist", "artist": "Count"})
    
    fig = px.pie(popular_artists, values="Count", names="Artist", 
                 title=f"{num_artists} Artists")
    
    return fig 

# Default number of top artists
default_num_artists = 10
pie_chart_figure = create_pie_chart(dataSpotify, num_artists=default_num_artists)

# Create a RadioItems component for selecting the number of top artists
radio_items = dcc.RadioItems(
    id='num-artists-radio',
    options=[
        {'label': '5 Artists', 'value': 5},
        {'label': '10 Artists', 'value': 10},
        {'label': '15 Artists', 'value': 15}
        # Add more options as needed
    ],
    value=default_num_artists  # Default value
)



# Define a callback to update the pie chart based on the radio button value
@app.callback(Output('pie-chart', 'figure'), Input('num-artists-radio', 'value'))
def update_pie_chart(num_artists):
    fig = create_pie_chart(dataSpotify, num_artists=num_artists)
    return fig

# Call the create_boxplot function to generate the Plotly Express boxplot
boxplot_figure = create_boxplot(dataSpotify)
#pie_chart_figure = create_pie_chart(dataSpotify)

# Default number of top songs
default_num_songs = 10
bar_chart_figure = create_bar_chart(dataSpotify, num_songs=default_num_songs)
# Create a Dropdown component for selecting the number of top songs
dropdown = dcc.Dropdown(
    id='num-songs-dropdown',
    options=[
        {'label': '5 Songs', 'value': 5},
        {'label': '10 Songs', 'value': 10},
        {'label': '15 Songs', 'value': 15},
        # Add more options as needed
    ],
    value=default_num_songs  # Default value
)

# Define a callback to update the bar chart based on the dropdown value
@app.callback(Output('bar-chart', 'figure'), Input('num-songs-dropdown', 'value'))
def update_bar_chart(num_songs):
    fig = create_bar_chart(dataSpotify, num_songs=num_songs)
    return fig

app.layout = html.Div(
    [
        html.H1("Data Visualization Project Debbie"),
        html.H2("Dashboard showing graphs"), html.Br(),
        html.H3("1. Filter the acousticness"),
        slider,  # Add the slider to the layout
        dcc.Graph(id='boxplot', figure=boxplot_figure),
        html.Br(),
        html.H3("2. Top Songs from Mr. X Spotify Data"),
        dropdown,
        dcc.Graph(id='bar-chart', figure=bar_chart_figure),  # Use a bar chart
        html.Br(),
        html.H3("3. Top Artists from Mr. X Spotify Data"),
        radio_items,
        dcc.Graph(id='pie-chart', figure=pie_chart_figure)  # Use a pie chart


    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)