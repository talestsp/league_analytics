#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bokeh.plotting import figure, show
from bokeh.io import output_file, save
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.models import Legend
from bokeh.models import HoverTool

COLOR_PALLET = ["#063258", "#dd360c", "#68dd5e", "#27c0d6", "#93579f", "#000000", "#ff6666", "#ff0000"]

class PlotLine:

    def __init__(self, x, x_label, y, y_label, title):
        self.x_label = x_label
        self.x_values = x
        self.y_label = y_label
        self.y_values = y

        self.title = title

    def plot(self, fig_width=900, fig_height=500):
        tools = self.get_tools()

        fig = figure(title=self.title, x_axis_label=self.x_label, y_axis_label=self.y_label,
                     width=fig_width, height=fig_height, tools=tools)

        fig.line(self.x_values, self.y_values, line_width=1, alpha=1, color="magenta")

        output_file("/home/tales/temp.html")
        show(fig)
        
    def get_tools(self):
        return "xwheel_zoom,box_select,pan,save,help"


class PlotMultiLine:

    def __init__(self, x_list, x_label, y_list, y_label, title, line_legends, colors=COLOR_PALLET):
        self.x_label = x_label
        self.x_values_list = x_list
        self.y_label = y_label
        self.y_values_list = y_list

        self.title = title
        self.line_legends=line_legends
        self.colors=colors

        if len(colors) < len(x_list):
            raise Exception("Color length not enough to set total lines. Please add " + str(len(x_list) - len(colors)) + " colors!")

    def plot(self, max_x, max_y, fig_width=900, fig_height=500, plot=True):

        hover = HoverTool(
            tooltips=[
                ("Points", "@y{int}"),
                ("Match no.", "@x")
            ]
        )

        tools=[hover, "save"]

        fig = figure(title=self.title, x_axis_label=self.x_label, y_axis_label=self.y_label,
                     width=fig_width, height=fig_height, x_range=(-0.3, max_x) ,y_range=(-1, max_y),
                     tools=tools, toolbar_location="left")
        fig.background_fill_color = "beige"

        legends = []

        for i in range(len(self.x_values_list)):
            x_values = self.x_values_list[i]
            y_values = self.y_values_list[i]
            line_legend = self.line_legends[i]
            color = self.colors[i]

            line = fig.line(x_values, y_values, line_width=1, alpha=1, color=color)
            circle = fig.circle(x_values, y_values, size=5, alpha=1, color=color)

            legends.append( (self.line_legends[i], [line, circle]) )

        legend = Legend(legends=legends ,location=(0, -60))
        fig.add_layout(legend, 'right')

        output_file(self.title + ".html")
        if plot:
            show(fig)
        else:
            save(fig)
        
    def get_tools(self):
        return ["xwheel_zoom","save","hover","help"]


class PlotDataMultiLine(PlotMultiLine):

    def __init__(self, plot_data_list, x_label, y_label, title):
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

        x_values_list = []
        y_values_list = []
        line_legends = []
        
        for plot_data in plot_data_list:
            x_values_list.append(plot_data.x)
            y_values_list.append(plot_data.y)
            line_legends.append(plot_data.legend)

        super(PlotDataMultiLine, self).__init__(x_list=x_values_list, x_label=x_label, 
                                                y_list=y_values_list, y_label=y_label, 
                                                title=title, line_legends=line_legends)