from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
 
df = pd.read_csv(r'C:\Users\Sorok\Downloads\hhru_backfront3.csv')


 
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True 
all_cont = df['employer_name'].unique()

SIDESTYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#8C82BC",
}


CONTSTYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([    
        html.H2("Раздел", className="display-4", style={'color': 'white'}),
            html.Hr(style={'color': 'white'}),
            dbc.Nav([
                    dbc.NavLink("Общие показатели", href="/page1", active="exact"),
                ],
                vertical=True,pills=True),
        ],
        style=SIDESTYLE,
    ),
    html.Div(id="page-content", children=[], style=CONTSTYLE)
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def pagecontent(pathname):
    if pathname == "/page1":
        return [
   
        html.Div([
            html.H1("Показатели вакансий и зарплат по профессии бэкенд и фронтэнд разработчик"),


            html.P(
                "Анализ основных показателей за 2021 и 2022"
                " Используйте фильтры, чтобы увидеть результат."
            )
        ], style = {
            'backgroundColor': 'rgb(140, 130, 188)',
            'padding': '10px 5px'
        }),




        html.Div([
            html.Div([
                html.Label('Организации'),
                dcc.Dropdown(
                    id = 'crossfilter-cont',
                    options = [{'label': i, 'value': i} for i in all_cont],
                    # значение компании, выбранное по умолчанию
                    value = ['Софтлекс'],
                    # возможность множественного выбора
                    multi = True
                )
            ],
            style = {'width': '48%', 'display': 'inline-block'}),
       
            html.Div([
                html.Label('Основные показатели'),
                dcc.RadioItems(
                options = [
                    {'label':'Средняя зарплата по вакансиям', 'value': 'name'},
                    {'label':'Средняя зарплата по территории', 'value': 'area_name'},
                ],
                id = 'crossfilter-ind',
                value = 'Средняя зарплата',
                labelStyle={'display': 'inline-block'}
                )
            ],
            style = {'width': '48%',  'float': 'right', 'display': 'inline-block'}),
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),


        html.Div(
            dcc.RangeSlider(
                id = 'crossfilter-year',
                min = df['Дата создания'].min(),
                max = df['Дата создания'].max(),
                value = [df['Дата создания'].min(),df['Дата создания'].max()],
                step = None,
                marks = {str(year):
                    str(year) for year in df['Дата создания'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),


        html.Div(
            dcc.Graph(id = 'bar'),
            style = {'width': '49%', 'display': 'inline-block'}
        ),
       
        html.Div(
            dcc.Graph(id = 'sunburst'),
            style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Graph(id = 'line'),
            # style = {'width': '70%', 'float': 'right', 'display': 'inline-block'}
        ),
        ]

 
@callback(
    Output('bar', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(continent, indication, year):
    filtered_data = df[(df['Дата создания'] >= year[0]) &
        (df['Дата создания'] <= year[1]) &
        (df['employer_name'].isin(continent))]
    figure = px.bar(
        filtered_data,
        x = indication,
        y = 'Средняя зарплата',
        color = 'name',
        title = "Значения средней зарплаты по странам"
        )
    return figure

 
@callback(
    Output('line', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Дата создания'] >= year[0]) &
        (df['Дата создания'] <= year[1]) &
        (df['employer_name'].isin(continent))]
    figure = px.line(
        filtered_data,
        x = "Средняя зарплата",
        y = indication,
        color = "name",
        title = "Значения показателя по странам",
        markers = True,
    )
    return figure

@callback(
    Output('sunburst', 'figure'),
    [Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_pie(indication, year):
    filtered_data = df[(df['Дата создания'] == year[1])]
    figure = px.pie(
        filtered_data,
        values = 'Средняя зарплата',
        names = 'name',
        title = f"Показатели по странам за {year[1]} год"
    )
    figure.update_traces(textposition='inside')
    return figure
 
 
if __name__ == '__main__':
    app.run_server(debug=True)