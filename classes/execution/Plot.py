__author__ = 'Erics'
import uuid
import plotly.plotly as py
import plotly.graph_objs
from plotly import tools


class Plot(object):

    def __init__(self):
        plotly.tools.set_credentials_file(username='shemer77', api_key='m034bapk2z', stream_ids=['0373v57h06', 'cjbitbcr9j'])

    # x=x values of line
    # y=y values of line
    def gen_line(self, x, y, name, width=2, dash='solid'):
        return {'x': x, 'y': y, 'name': name, 'line': plotly.graph_objs.Line(width=width, dash=dash)}

    # x=x value of point
    # y=y value of point
    def gen_point(self, x, y, name, size=12):
        return {'x': x, 'y': y, 'name': name, 'marker': plotly.graph_objs.Marker(size=size)}

    def get_graph(self, graph, out_file):
        figure = py.get_figure('shemer77', graph)
        py.image.save_as(figure, out_file)

    def make_traces(self, data):
        traces = []
        for item in data:
            traces.append(plotly.graph_objs.Scatter(item))

        return traces

    def create_plot(self, fig, title):
        # add auto_open=False arg to turn off opening the browser
        unique_url = ""
        try:
            unique_url = py.plot(fig, filename=title+str(uuid.uuid4()), auto_open=False)
        except Exception, e:
            print e

        #print unique_url
        return str(unique_url)

    def generate_subplots(self, title, plot_data):
        fig = tools.make_subplots(rows=4, cols=1, specs=[[{'rowspan': 3}],
                                                         [None],
                                                         [None],
                                                         [{}]])
        fig['layout'].update(height=600)

        traces = self.make_traces(plot_data[0])
        for t in traces:
            fig.append_trace(t, 1, 1)
        traces = self.make_traces(plot_data[1])
        for t in traces:
            fig.append_trace(t, 4, 1)

        return self.create_plot(fig, title)

    # items is a list of lines or points
    def generate_a_graph(self, title, items):
        traces = []
        data = []

        traces = self.make_traces(items)

        data = plotly.graph_objs.Data(traces)
        layout = plotly.graph_objs.Layout(
            title=title
        )
        fig = plotly.graph_objs.Figure(data=data, layout=layout)

        return self.create_plot(fig, title)