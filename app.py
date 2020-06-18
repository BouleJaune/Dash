import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import flask
import time
import os
from tasks import hello
# import eventlet
# eventlet.monkey_patch()

server = flask.Flask('app')
server.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6382/0'
server.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6382/0'

app = dash.Dash('app', server=server)

image_directory  = "assets/"
list_of_images = [p for p in os.listdir(image_directory)]
static_image_route = "static/"
app.layout = html.Div([
    html.H1('Imaged'),
    dcc.Dropdown(
        id='img_dropdown',
        options=[{'label': i, 'value': i} for i in list_of_images],
        value=list_of_images[0]
    ),
    html.Img(id='image')
], className="container")


@app.callback(Output('image', 'src'),
              [Input('img_dropdown', 'value')])
def update_graph(selected_dropdown_value):
    hello.delay()
    return static_image_route + selected_dropdown_value

@app.server.route(f'/{static_image_route}<image_path>.png')
def serve_image(image_path):
    image_name = f'{image_path}.png'
    if image_name not in list_of_images:
        raise Exception(f'"{image_path}" is excluded from the allowed static files')
    return flask.send_from_directory(image_directory, image_name)


if __name__ == '__main__':
    app.run_server(debug=True)
