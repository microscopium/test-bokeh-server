"""Test bokeh server for debugging / feature development."""
import click
import numpy as np

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models.widgets import Button


def image_array():
    N = 500
    x = np.linspace(0, 10, N)
    y = np.linspace(0, 10, N)
    xx, yy = np.meshgrid(x, y)
    img = np.sin(xx)*np.cos(yy)
    return img


def make_makedoc():
    """Make the makedoc function required by Bokeh Server."""

    def makedoc(doc):
        img = image_array()
        p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
        p.x_range.range_padding = p.y_range.range_padding = 0
        # must give a vector of image data for image parameter
        p.image(image=[img], x=0, y=0, dw=10, dh=10, palette="Spectral11")
        controls = [Button(label="button 1", button_type="success"),
                    Button(label="button 1", button_type="success")]

        page_content = layout([
            [p],
            controls,
            ], sizing_mode="scale_width")
        doc.title = 'Test bokeh app'
        doc.add_root(page_content)
    print('ready!')
    return makedoc


@click.command()
@click.option('-c', '--config', default=None)
@click.option('-p', '--path', default='/')
@click.option('-P', '--port', type=int, default=5000)
def run_server_cmd(config=None, path='/', port=5000):
    run_server(config=config, path=path, port=port)


def run_server(config=None, path='/', port=5000):
    """Run the bokeh server."""
    makedoc = make_makedoc()
    apps = {path: Application(FunctionHandler(makedoc))}

    server = Server(apps, port=port, allow_websocket_origin=['*'])
    server.run_until_shutdown()


if __name__ == '__main__':
    run_server_cmd()
