﻿from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pandas import DataFrame
import mplcursors
# import plotly.graph_objects as go
import numpy as np; np.random.seed(1)
# from matplotlib.figure import Figure
# from matplotlib.widgets import Slider
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF, renderPM
# from PIL import Image, ImageTk


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------GUI Program beta v0.1------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
circuit_components = []


class IndexTracker(object):
    def __init__(self, ax, X, smax):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')
        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2
        self.im = ax.imshow(self.X[:, :, self.ind], cmap='gray')
        self.smax = smax
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def contrast(self, event):
        print('Changing contrast')
        print(self.smax.val)
        self.im.set_clim([0, self.smax.val])
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------ Functions for zooming in and out of canvas --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def do_zoom(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canvas.scale(ALL, x, y, factor, factor)


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.bind("<MouseWheel>", do_zoom)
        self.bind('<ButtonPress-1>', lambda event: self.scan_mark(event.x, event.y))
        self.bind("<B1-Motion>", lambda event: self.scan_dragto(event.x, event.y, gain=1))
        # # code for linux not yet implemented
        # self.bind('<Button-5>', self.__wheel)  # zoom for Linux, wheel scroll down
        # self.bind('<Button-4>', self.__wheel)  # zoom for Linux, wheel scroll up

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        width_scale = float(event.width) / self.width
        height_scale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, width_scale, height_scale)


# Set the colour of the background
Mode = 'dark'
theme_colour = ''
if Mode == 'light':
    theme_colour = 'green'
if Mode == 'dark':
    theme_colour = 'blue'

customtkinter.set_appearance_mode(Mode)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(theme_colour)  # Themes: blue (default), dark-blue, green

# create the root window
root = customtkinter.CTk()
root.title('EMC Analysis')
root.geometry('1100x750+250+200')
root.minsize(root.winfo_width(), root.winfo_height())

tabControl = ttk.Notebook(root)

schematic_params = ttk.Frame(tabControl)
graphs = ttk.Frame(tabControl)

tabControl.add(schematic_params, text='Schematic and entering parameters')
tabControl.add(graphs, text='Graphs')

component_parameters_frame = Frame(schematic_params, width=280, height=100, background='white')

canvas_frame = Frame(schematic_params, width=700, height=500, background='white')
canvas = ResizingCanvas(canvas_frame, width=1000, height=600, highlightthickness=0)

all_component_parameters = []
entering_parameters_window = None


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Functions for hovering over components --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def on_enter(e, element_to_change):
    canvas.itemconfig(element_to_change, fill='green')


def on_leave(e, element_to_change):
    canvas.itemconfig(element_to_change, fill='#F0F0F0')


def on_resistor_press(event, arg):
    print(circuit_components)
    print(circuit_components[arg])
    print(arg)


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------- Component Drawings ------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def draw_capacitor(start_coordinate_x, start_coordinate_y, canvas_to_draw_in):

    y_adjustment = 25
    canvas_to_draw_in.create_line(start_coordinate_x + 16,
                                  start_coordinate_y,
                                  start_coordinate_x + 16,
                                  start_coordinate_y + y_adjustment)

    canvas_to_draw_in.create_line(start_coordinate_x + 16,
                                  start_coordinate_y + y_adjustment + 12 + 5,
                                  start_coordinate_x + 16,
                                  start_coordinate_y + y_adjustment + y_adjustment + 12 + 5)

    canvas_to_draw_in.create_rectangle(start_coordinate_x - 10,
                                       start_coordinate_y + y_adjustment,
                                       start_coordinate_x + 40,
                                       start_coordinate_y + y_adjustment + 5)

    canvas_to_draw_in.create_rectangle(start_coordinate_x - 10,
                                       start_coordinate_y + y_adjustment + 12,
                                       start_coordinate_x + 40,
                                       start_coordinate_y + y_adjustment + 12 + 5)


def draw_inductor(start_coordinate_x, start_coordinate_y, canvas_to_draw_in):
    radius = 12
    x_adjustment = 16
    y_adjustment = 30
    canvas_to_draw_in.create_line(start_coordinate_x + x_adjustment,
                                  start_coordinate_y + y_adjustment - 20,
                                  start_coordinate_x + x_adjustment,
                                  start_coordinate_y + y_adjustment - 20 + 8)

    canvas_to_draw_in.create_line(start_coordinate_x + x_adjustment,
                                  start_coordinate_y + 5 * radius + y_adjustment,
                                  start_coordinate_x + x_adjustment,
                                  start_coordinate_y + 5 * radius + y_adjustment + 8)

    canvas_to_draw_in.create_circle(start_coordinate_x + x_adjustment,
                                    start_coordinate_y + y_adjustment,
                                    radius,
                                    tags='Inductor')

    canvas_to_draw_in.create_circle(start_coordinate_x + x_adjustment,
                                    start_coordinate_y + 2 * radius + y_adjustment,
                                    radius,
                                    tags='Inductor')

    canvas_to_draw_in.create_circle(start_coordinate_x + x_adjustment,
                                    start_coordinate_y + 4 * radius + y_adjustment,
                                    radius,
                                    tags='Inductor')

    canvas_to_draw_in.create_rectangle(start_coordinate_x - radius + x_adjustment - 0.2,
                                       start_coordinate_y - radius + y_adjustment,
                                       start_coordinate_x + x_adjustment - 0.2,
                                       start_coordinate_y + 5 * radius + y_adjustment + 1,
                                       fill='#F0F0F0',
                                       outline='#F0F0F0',
                                       activefill='#F0F0F0',
                                       tags='Inductor'
                                       )
    # # Highlighting shape still not working
    # canvas_to_draw_in.create_rectangle(start_coordinate_x - radius/2 + x_adjustment,
    #                                    start_coordinate_y - radius + y_adjustment,
    #                                    start_coordinate_x + radius + radius/2 + x_adjustment,
    #                                    start_coordinate_y + 5 * radius + y_adjustment,
    #                                    outline='#F0F0F0',
    #                                    disabledfill='#F0F0F0',
    #                                    tags='Inductor Highlight',
    #                                    activefill='green',
    #                                    )


def draw_diode(start_coordinate_x, start_coordinate_y, canvas_to_draw_in):
    ground_line = 10
    x_adjustment = 16

    # wire before diode
    canvas_to_draw_in.create_line(start_coordinate_x + x_adjustment,
                                  start_coordinate_y,
                                  start_coordinate_x + x_adjustment,
                                  start_coordinate_y + ground_line)

    # wire after diode
    canvas_to_draw_in.create_line(start_coordinate_x + x_adjustment,
                                  start_coordinate_y + 35 + ground_line,
                                  start_coordinate_x + x_adjustment,
                                  start_coordinate_y + 35 + ground_line + 20)

    # triangle shape of diode
    canvas_to_draw_in.create_polygon(start_coordinate_x - 25 + x_adjustment,
                                     start_coordinate_y + ground_line,
                                     start_coordinate_x + 25 + x_adjustment,
                                     start_coordinate_y + ground_line,
                                     start_coordinate_x + x_adjustment,
                                     start_coordinate_y + 35 + ground_line,
                                     fill='',
                                     outline='black',
                                     tags='schematic')

    # Diode line in front of triangle shape
    canvas_to_draw_in.create_line(start_coordinate_x - 25 + x_adjustment,
                                  start_coordinate_y + 35 + ground_line,
                                  start_coordinate_x + 25 + x_adjustment,
                                  start_coordinate_y + 35 + ground_line)


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- Functions for drop down lists --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def random_or_constant(value_selected,
                       distribution_label,
                       distribution_dropdown,
                       component_param1_label_array,
                       component_param2_label_array,
                       component_param1_array,
                       component_param2_array
                       ):
    # Placing Label and dropdown list for distribution
    if value_selected.get() == 'Random':
        distribution_label.grid(row=5, column=5)
        distribution_dropdown.grid(row=5, column=6)
    elif value_selected.get() == 'Constant':
        distribution_label.grid_remove()
        distribution_dropdown.grid_remove()

        # Remove all labels and text boxes
        for labels in range(len(component_param1_label_array)):
            component_param1_label_array[labels].grid_remove()
            component_param2_label_array[labels].grid_remove()
            component_param1_array[labels].grid_remove()
            component_param2_array[labels].grid_remove()

    print(value_selected.get())


# Function when the selected component has been changed from dropdown list
def change_component_index(component_selected,
                           value_selected,
                           distribution_type,
                           component_distribution_array,
                           component_param1_label_array,
                           component_param2_label_array,
                           component_param1_array,
                           component_param2_array
                           ):
    global component_index
    for comp_index in range(len(circuit_components)):
        if component_selected.get() == circuit_components[comp_index]:
            component_index = comp_index

    component_param1_array[component_index].grid_remove()
    component_param2_array[component_index].grid_remove()
    component_distribution_array[component_index].delete('1.0', END)

    # Check which distribution has been selected and change the parameters accordingly
    if distribution_type.get() == 'Gamma Distribution':
        component_distribution_array[component_index].insert(INSERT, 'Gamma')
        component_param1_label_array[component_index]['text'] = 'Shape (k)'
        component_param2_label_array[component_index]['text'] = 'Scale (θ)'

    if distribution_type.get() == 'Beta Distribution':
        component_distribution_array[component_index].insert(INSERT, 'Beta')
        component_param1_label_array[component_index]['text'] = 'Alpha (α)'
        component_param2_label_array[component_index]['text'] = 'Beta (β)'

    if distribution_type.get() == 'Normal Distribution':
        component_distribution_array[component_index].insert(INSERT, 'Normal')
        component_param1_label_array[component_index]['text'] = 'Mean (μ)'
        component_param2_label_array[component_index]['text'] = 'Standard deviation (σ)'

    if value_selected == 'Random':
        # Remove all labels for parameters, except the user selected component label
        for labels in range(len(component_param1_label_array)):
            if labels == component_index:
                component_param1_label_array[labels].grid(row=6, column=5)
                component_param2_label_array[labels].grid(row=7, column=5)
                component_param1_array[labels].grid(row=6, column=6)
                component_param2_array[labels].grid(row=7, column=6)
            else:
                component_param1_label_array[labels].grid_remove()
                component_param2_label_array[labels].grid_remove()
                component_param1_array[labels].grid_remove()
                component_param2_array[labels].grid_remove()

    elif value_selected == 'Constant':
        print('constant value')


# Function when the selected distribution for the component has been changed from dropdown list
def select_distribution_type(distribution_type,
                             index_of_selected_component,
                             component_distribution,
                             parameter1_label,
                             parameter2_label,
                             param1_array,
                             param2_array
                             ):

    # Check which distribution has been selected and change the parameters accordingly
    component_distribution[index_of_selected_component].delete('1.0', END)
    if distribution_type.get() == 'Gamma Distribution':
        component_distribution[index_of_selected_component].insert(INSERT, 'Gamma')
        parameter1_label[index_of_selected_component]['text'] = 'Shape (k)'
        parameter2_label[index_of_selected_component]['text'] = 'Scale (θ)'

    if distribution_type.get() == 'Beta Distribution':
        component_distribution[index_of_selected_component].insert(INSERT, 'Beta')
        parameter1_label[index_of_selected_component]['text'] = 'Alpha (α)'
        parameter2_label[index_of_selected_component]['text'] = 'Beta (β)'

    if distribution_type.get() == 'Normal Distribution':
        component_distribution[index_of_selected_component].insert(INSERT, 'Normal')
        parameter1_label[index_of_selected_component]['text'] = 'Mean (μ)'
        parameter2_label[index_of_selected_component]['text'] = 'Standard deviation (σ)'

    # Remove all labels for parameters, except the user selected component label
    for labels in range(len(param1_array)):
        if labels == index_of_selected_component:
            parameter1_label[labels].grid(row=6, column=5)
            parameter2_label[labels].grid(row=7, column=5)
            param1_array[labels].grid(row=6, column=6)
            param2_array[labels].grid(row=7, column=6)
        else:
            parameter1_label[labels].grid_remove()
            parameter2_label[labels].grid_remove()
            param1_array[labels].grid_remove()
            param2_array[labels].grid_remove()

    print(distribution_type.get())


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for sketching graphs on tab 2 --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def sketch_graphs(data):
    # im = np.array(np.random.rand(10, 10, 10))
    # graph = Figure()
    # canvas = FigureCanvasTkAgg(graph, root)
    # canvas.get_tk_widget().pack(fill="both", expand=True)
    #
    # im = np.array(np.random.rand(10, 10, 10))
    #
    # ax = graph.subplots(1, 1)
    #
    # axmax = graph.add_axes([0.25, 0.01, 0.65, 0.03])
    # smax = Slider(axmax, 'Max', 0, np.max(im), valinit=50)
    # tracker = IndexTracker(ax, im)
    # canvas.mpl_connect('scroll_event', tracker.onscroll)
    # canvas.mpl_connect('button_release_event', tracker.contrast)  # add this for contrast change

    # data = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
    #         'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
    #         }
    # data_frame_plot = DataFrame(data, columns=['Country', 'GDP_Per_Capita'])
    figure = plt.Figure(figsize=(10, 6), dpi=100)
    ax = figure.add_subplot(111)
    x = np.sort(np.random.rand(15))
    y = np.sort(np.random.rand(15))
    names = np.array(list("ABCDEFGHIJKLMNO"))

    line, = ax.plot(x, y)

    chart_type= FigureCanvasTkAgg(figure,master=graphs)
    chart_type.get_tk_widget().pack(side='top', fill='both', expand=1)
    # chart_type = FigureCanvasTkAgg(figure, graphs)
    # chart_type.get_tk_widget().pack(pady=0, fill=BOTH)
    # data_frame_plot = data_frame_plot[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
    # data_frame_plot.plot(kind='line', legend=True, ax=ax)
    ax.set_title('Example Plot')
    ax.grid('on')
    names = np.array(list("ABCDEFGHIJKLMNO"))
    annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        x, y = line.get_data()
        annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
        text = "{}, {}".format(" ".join(list(map(str, ind["ind"]))),
                               " ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = line.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                chart_type.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    chart_type.draw_idle()

    chart_type.mpl_connect("motion_notify_event", hover)

    toolbar = NavigationToolbar2Tk(chart_type, graphs, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=BOTTOM, fill=BOTH)

    # fig = go.Figure(
    #     data=[go.Bar(y=[2, 1, 3])],
    #     layout_title_text="A Figure Displayed with fig.show()"
    # )
    # fig.show()


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Function for enter all parameters button --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for entering parameters
def open_new_window(component):
    # Creating a new window for entering parameters
    global entering_parameters_window

    if entering_parameters_window is not None and entering_parameters_window.winfo_exists():
        entering_parameters_window.lift()
    else:
        entering_parameters_window = customtkinter.CTkToplevel(root)

        label_background = ''
        text_colour = ''
        global Mode
        if Mode == 'dark':
            label_background = '#212325'
            outline = '#212325'
            text_colour = 'white'
        elif Mode == 'light':
            label_background = '#EBEBEB'
            outline = '#EBEBEB'
            text_colour = 'black'

        # sets the title of the new window created for entering parameters
        entering_parameters_window.title("Enter Component Parameters")

        # sets the size of the new window created for entering parameters
        entering_parameters_window.geometry("400x210")

        component_name_array = [None] * len(circuit_components)
        component_distribution_array = [None] * len(circuit_components)
        component_param1_entry_box = [None] * len(circuit_components)
        component_value_array = ['Constant'] * len(circuit_components)
        component_param1_label_array = [None] * len(circuit_components)
        component_param2_label_array = [None] * len(circuit_components)
        component_param1_array = [None] * len(circuit_components)
        component_param2_array = [None] * len(circuit_components)
        name_label_array = [None] * len(circuit_components)
        component_full_information_array = [None] * len(circuit_components)

        # Example Structure
        # name: L1
        # distribution: normal
        # parameters:
        # mu: 1    sd: 2

        # Display names of the parameters using labels
        # Which looks like the following:
        # Component Name:
        # Distribution:
        # param1=
        # param2=
        component_value_label = Label(entering_parameters_window,
                                      height=1,
                                      width=10,
                                      text='Value:',
                                      background=label_background,
                                      foreground=text_colour,
                                      highlightbackground=label_background)

        component_name_array_label = Label(entering_parameters_window,
                                           height=1,
                                           width=20,
                                           text='Component Name:',
                                           background=label_background,
                                           foreground=text_colour,
                                           highlightbackground=label_background
                                           )
        component_distribution_label = Label(entering_parameters_window,
                                             height=1,
                                             width=20,
                                             text='Distribution',
                                             background=label_background,
                                             foreground=text_colour,
                                             highlightbackground=label_background
                                             )

        for circuit_component in range(len(circuit_components)):
            component_name_array[circuit_component] = Label(entering_parameters_window,
                                                            height=1,
                                                            width=20,
                                                            text=circuit_components[circuit_component],
                                                            background=label_background,
                                                            foreground=text_colour
                                                            )

            component_distribution_array[circuit_component] = Text(entering_parameters_window,
                                                                   height=1,
                                                                   width=20,
                                                                   bg="white"
                                                                   )

            component_param1_label_array[circuit_component] = Label(entering_parameters_window,
                                                                    height=1,
                                                                    width=20,
                                                                    text='',
                                                                    background=label_background,
                                                                    foreground=text_colour
                                                                    )

            # component_param1_entry_box[circuit_component] = customtkinter.CTkEntry(entering_parameters_window,
            #                                                                        height=1,
            #                                                                        width=40,
            #                                                                        text='',
            #                                                                        validatecommand=vcmd
            #                                                                        )

            component_param2_label_array[circuit_component] = Label(entering_parameters_window,
                                                                    height=1,
                                                                    width=20,
                                                                    text='',
                                                                    background=label_background,
                                                                    foreground=text_colour
                                                                    )

            component_param1_array[circuit_component] = Text(entering_parameters_window,
                                                             height=1,
                                                             width=20,
                                                             bg="white")

            component_param2_array[circuit_component] = Text(entering_parameters_window,
                                                             height=1,
                                                             width=20,
                                                             bg="white")

            name_label_array[circuit_component] = Label(component_parameters_frame,
                                                        text='',
                                                        width=22,
                                                        height=4)

            component_full_information_array[circuit_component] = Entry(component_parameters_frame)

            # Default parameters which are:
            # distribution: Normal
            # Mean = 1
            # Standard Deviation = 2
            component_distribution_array[circuit_component].insert(INSERT, 'Normal')
            component_param1_label_array[circuit_component]['text'] = 'Mean (μ)'
            component_param2_label_array[circuit_component]['text'] = 'Standard deviation (σ)'
            component_param1_array[circuit_component].insert(INSERT, '1')
            component_param2_array[circuit_component].insert(INSERT, '2')

        component_selected = StringVar(root)
        component_selected.set(circuit_components[0])
        distributions = ['Normal Distribution', 'Gamma Distribution', 'Beta Distribution']
        distribution_selected = StringVar(root)
        distribution_selected.set(distributions[0])
        values = ['Constant', 'Random']
        values_selected = StringVar(root)
        values_selected.set(values[0])

        global component_index
        component_index = 0

        # Drop down list for selecting which component to enter parameters for
        component_drop_down_list = OptionMenu(entering_parameters_window,
                                              component_selected,
                                              *circuit_components,
                                              command=lambda _: change_component_index(component_selected,
                                                                                       values_selected,
                                                                                       distribution_selected,
                                                                                       component_distribution_array,
                                                                                       component_param1_label_array,
                                                                                       component_param2_label_array,
                                                                                       component_param1_array,
                                                                                       component_param2_array
                                                                                       ))

        component_drop_down_list.config(background=label_background,
                                        foreground=text_colour,
                                        activebackground=text_colour,
                                        activeforeground=label_background)

        component_drop_down_list["menu"].config(background=label_background,
                                                foreground=text_colour,
                                                activebackground=text_colour,
                                                activeforeground=label_background
                                                )

        # Drop down list for selecting the type of distribution for random components
        distribution_drop_down_list = OptionMenu(entering_parameters_window,
                                                 distribution_selected,
                                                 *distributions,
                                                 command=lambda _: select_distribution_type(distribution_selected,
                                                                                            component_index,
                                                                                            component_distribution_array,
                                                                                            component_param1_label_array,
                                                                                            component_param2_label_array,
                                                                                            component_param1_array,
                                                                                            component_param2_array
                                                                                            ))

        distribution_drop_down_list.config(background=label_background,
                                           foreground=text_colour,
                                           activebackground=text_colour,
                                           activeforeground=label_background
                                           )
        distribution_drop_down_list["menu"].config(background=label_background,
                                                   foreground=text_colour,
                                                   activebackground=text_colour,
                                                   activeforeground=label_background
                                                   )

        # Drop down list for selecting if component value is random or constant
        component_value_drop_down_list = OptionMenu(entering_parameters_window,
                                                    values_selected,
                                                    *values,
                                                    command=lambda _: random_or_constant(values_selected,
                                                                                         component_distribution_label,
                                                                                         distribution_drop_down_list,
                                                                                         component_param1_label_array,
                                                                                         component_param2_label_array,
                                                                                         component_param1_array,
                                                                                         component_param2_array
                                                                                         ))

        component_value_drop_down_list.config(background=label_background,
                                              foreground=text_colour,
                                              activebackground=text_colour,
                                              activeforeground=label_background
                                              )

        component_value_drop_down_list["menu"].config(background=label_background,
                                                      foreground=text_colour,
                                                      activebackground=text_colour,
                                                      activeforeground=label_background
                                                      )


        # Button for saving parameters
        save_parameters_button = customtkinter.CTkButton(
            entering_parameters_window,
            text='Save Parameters',
            command=lambda: save_entered_parameters(entering_parameters_window,
                                                    values_selected,
                                                    component_selected.get(),
                                                    distribution_selected.get(),
                                                    component_distribution_array[component_index].get('1.0', END).strip(
                                                        '\n'),
                                                    component_param1_label_array[component_index]['text'],
                                                    component_param2_label_array[component_index]['text'],
                                                    component_param1_array[component_index].get('1.0', END).strip('\n'),
                                                    component_param2_array[component_index].get('1.0', END).strip('\n'),
                                                    component_index,
                                                    name_label_array,
                                                    component_value_array)
        )

        # Button for saving parameters
        save_all_parameters_button = customtkinter.CTkButton(
            entering_parameters_window,
            text='Save All Parameters',
            command=lambda: save_all_entered_parameters(component,
                                                        values_selected,
                                                        component_distribution_array,
                                                        component_param1_label_array,
                                                        component_param2_label_array,
                                                        component_param1_array,
                                                        component_param2_array,
                                                        name_label_array,
                                                        component_value_array)
        )

        # Component drop down list and component name label
        component_name_array_label.grid(row=3, column=5, sticky='news')
        component_drop_down_list.grid(row=3, column=6)

        # Placing label and dropdown for component value
        component_value_label.grid(row=4, column=5, sticky='news')
        component_value_drop_down_list.grid(row=4, column=6)

        # Saving Parameters button location in new window
        save_parameters_button.grid(row=10, column=6)

        # Saving All Parameters button location in new window
        save_all_parameters_button.grid(row=10, column=7)

        entering_parameters_window.grid_rowconfigure(tuple(range(10)), weight=1)
        entering_parameters_window.grid_columnconfigure(tuple(range(10)), weight=1)
        #entering_parameters_window.resizable(False, False)
        enter_parameters_button.wait_window(entering_parameters_window)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for saving a single parameter --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for closing new windows using a  button
def save_entered_parameters(entering_parameters_window,
                            value,
                            component_name,
                            selected_distribution,
                            component_distribution,
                            component_param1_label,
                            component_param2_label,
                            component_param1,
                            component_param2,
                            index,
                            full_name_labels,
                            component_value_array):
    global all_component_parameters
    global component_index

    if value.get() == 'Random':
        if component_distribution == 'Normal':
            component_param1_dictionary_input = 'mean'
            component_param2_dictionary_input = 'standard deviation'
        elif component_distribution == 'Gamma':
            component_param1_dictionary_input = 'shape'
            component_param2_dictionary_input = 'theta'
        elif component_distribution == 'Beta':
            component_param1_dictionary_input = 'alpha'
            component_param2_dictionary_input = 'beta'

        component_value_array[index] = 'Random'

        if len(all_component_parameters) == 0:
            all_component_parameters.append({component_name:
                                            {'distribution': component_distribution,
                                             'parameters': {component_param1_dictionary_input: component_param1,
                                                            component_param2_dictionary_input: component_param2}
                                             }
                                             }
                                            )

        # -------------------------- removing duplicates and storing in a list of dictionaries -------------------------
        appending_flag = 0
        for parameters in range(len(all_component_parameters)):
            if component_name == list(all_component_parameters[parameters].keys())[-1]:
                # If the last entered component is similar to the previously entered one then,
                # replace the old parameters with the new ones
                all_component_parameters[parameters] = ({component_name:
                                                        {'distribution': component_distribution,
                                                         'parameters': {
                                                                  component_param1_dictionary_input: component_param1,
                                                                  component_param2_dictionary_input: component_param2}
                                                              }
                                                         }

                )
                # Ensures no appending takes place
                appending_flag = 0
                break
            else:
                # If the last entered component is NOT similar to the previously entered one then,
                # ensure to add the component to the end of the list
                appending_flag = 1

        if appending_flag == 1:
            all_component_parameters.append({component_name:
                                            {'distribution': component_distribution,
                                             'parameters': {component_param1_dictionary_input: component_param1,
                                                            component_param2_dictionary_input: component_param2}
                                                  }
                                             }

                                            )
            appending_flag = 0

        print(all_component_parameters)
        # --------------------------------- Displaying entered parameters on root window -------------------------------
        print(component_index)
        full_name_labels[index].config(text='')
        full_name_labels[index].config(borderwidth=0)
        full_name_labels[index].config(relief='flat')
        full_name_labels[index] = Label(component_parameters_frame,
                                        text=component_name +
                                        '\nDistribution: ' + component_distribution +
                                        '\n' + component_param1_label + '=' + component_param1 +
                                        '\n' + component_param2_label + '=' + component_param2,
                                        highlightcolor='black',
                                        highlightthickness=2,
                                        borderwidth=1,
                                        relief='solid',
                                        height=4,
                                        width=22
                                        )
    elif value.get() == 'Constant':
        if len(all_component_parameters) == 0:
            all_component_parameters.append({component_name: {'Value': 'Constant'}})

        # -------------------------- removing duplicates and storing in a list of dictionaries -------------------------
        appending_flag = 0
        for parameters in range(len(all_component_parameters)):
            if component_name == list(all_component_parameters[parameters].keys())[-1]:
                # If the last entered component is similar to the previously entered one then,
                # replace the old parameters with the new ones
                all_component_parameters[parameters] = ({component_name: {'Value': 'Constant'}}

                )
                # Ensures no appending takes place
                appending_flag = 0
                break
            else:
                # If the last entered component is NOT similar to the previously entered one then,
                # ensure to add the component to the end of the list
                appending_flag = 1

        if appending_flag == 1:
            all_component_parameters.append({component_name: {'Value': 'Constant'}})
            appending_flag = 0
        full_name_labels[index].config(text='')
        full_name_labels[index].config(borderwidth=0)
        full_name_labels[index].config(relief='flat')

        full_name_labels[index] = Label(component_parameters_frame,
                                        text=component_name +
                                        '\nValue: ' + '5',
                                        highlightcolor='black',
                                        highlightthickness=2,
                                        borderwidth=1,
                                        relief='solid',
                                        height=4,
                                        width=22)

    full_name_labels[component_index].grid(row=component_index, column=1, sticky='nsew')


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for saving all parameters ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def save_all_entered_parameters(component_name,
                                value,
                                component_distribution_array,
                                component_param1_label_array,
                                component_param2_label_array,
                                component_param1_array,
                                component_param2_array,
                                full_name_labels,
                                component_value_array):
    global all_component_parameters
    all_component_parameters.clear()

    component_param1_dictionary_input = [None] * len(component_param1_label_array)
    component_param2_dictionary_input = [None] * len(component_param2_label_array)

    for distributions in range(len(component_distribution_array)):
        if component_distribution_array[distributions].get('1.0', END).strip('\n') == 'Normal':
            component_param1_dictionary_input[distributions] = 'mean'
            component_param2_dictionary_input[distributions] = 'standard deviation'
        elif component_distribution_array[distributions].get('1.0', END).strip('\n') == 'Gamma':
            component_param1_dictionary_input[distributions] = 'shape'
            component_param2_dictionary_input[distributions] = 'theta'
        elif component_distribution_array[distributions].get('1.0', END).strip('\n') == 'Beta':
            component_param1_dictionary_input[distributions] = 'alpha'
            component_param2_dictionary_input[distributions] = 'beta'

    for circuit_component in range(len(circuit_components)):
        if component_value_array[circuit_component] == 'Random':
            print(component_name)
            # clearing the name label of all parameters
            full_name_labels[circuit_component].config(text='')
            full_name_labels[circuit_component].config(borderwidth=0)
            full_name_labels[circuit_component].config(relief='flat')

            # Storing the name label of all parameters
            full_name_labels[circuit_component] = \
                Label(component_parameters_frame,
                      text=component_name[circuit_component] +
                           '\nDistribution: ' + component_distribution_array[circuit_component].get('1.0',
                                                                                                    END).strip(
                          '\n') +
                           '\n' + component_param1_label_array[circuit_component]['text'] +
                           '=' + component_param1_array[circuit_component].get('1.0', END).strip('\n') +
                           '\n' + component_param2_label_array[circuit_component]['text'] +
                           '=' + component_param2_array[circuit_component].get('1.0', END).strip('\n'),
                      highlightcolor='black',
                      highlightthickness=2,
                      borderwidth=1,
                      relief='solid',
                      height=4,
                      width=22
                      )

            # Placing the name label of all parameters on the root window
            full_name_labels[circuit_component].grid(row=circuit_component, column=1)

            # Storing all components with their parameters in a dictionary
            all_component_parameters.append(
                {component_name[circuit_component]:
                     {'distribution': component_distribution_array[circuit_component].get('1.0', END).strip('\n'),

                      'parameters': {  # Parameter 1 label and user entered number
                          component_param1_dictionary_input[circuit_component]:
                              component_param1_array[circuit_component].get('1.0', END).strip('\n'),
                          # Parameter 2 label and user entered number
                          component_param2_dictionary_input[circuit_component]:
                              component_param2_array[circuit_component].get('1.0', END).strip('\n')}
                      }
                 }
            )

        elif component_value_array[circuit_component] == 'Constant':
            # Storing all components with their parameters in a dictionary
            all_component_parameters.append(
                {component_name[circuit_component]: {'Value': '5'}}
            )

            full_name_labels[circuit_component].config(text='')
            full_name_labels[circuit_component].config(borderwidth=0)
            full_name_labels[circuit_component].config(relief='flat')

            # Storing the name label of all parameters
            full_name_labels[circuit_component] = \
                Label(component_parameters_frame,
                      text=component_name[circuit_component] + '\nValue: ' + '5',
                      highlightcolor='black',
                      highlightthickness=2,
                      borderwidth=1,
                      relief='solid',
                      height=4,
                      width=22
                      )

            # Placing the name label of all parameters on the root window
            full_name_labels[circuit_component].grid(row=circuit_component, column=1)

    print(all_component_parameters)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Function for entering component parameters ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Entering Component Parameters for all elements
def component_parameters():
    global all_component_parameters
    global circuit_components

    if len(circuit_components) != 0:
        open_new_window(circuit_components)
    else:
        error_for_not_entering_schematic = \
            canvas.create_window(400, 300,
                                 window=Label(canvas,
                                              text="Please select a schematic first",
                                              width=40,
                                              font=("Times New Roman", 20),
                                              height=40),
                                 tags='Error if schematic not entered')


# Replacing the oval function of tkinter with a simpler function for circles
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


# Function for opening a ltspice schematic file
def get_file_path():
    global file_path
    # Open and return file path
    file_path = fd.askopenfilenames(
        title="Select a Schematic",

        filetypes=(
            ("LTspice Schematic", "*.asc"),
            ("All files", "*.*")
        )

    )

    too_many_files_selected = Label(canvas,
                                    text='Please Select Two files, an LTSpice schematic and an image of the schematic'
                                    )
    while len(file_path) > 2:
        file_path = fd.askopenfilenames(
            title="Select a Schematic",

            filetypes=(
                ("LTspice Schematic", "*.asc"),
                ("All files", "*.*")
            )

        )

    # # Image Implementation - not yet working
    # svg_schematic = svg2rlg(file_path[1])
    # renderPM.drawToFile(svg_schematic, "temp_schematic.png", fmt="PNG")
    # img = Image.open('temp_schematic.png')
    # pimg = ImageTk.PhotoImage(img)
    # size = img.size
    # canvas.create_image(96 + 150, 224 + 150, image=pimg)
    #canvas.create_line(96-13+150, 224+150, 128 + 13 + 150, 224+150)

    # TODO: Make sure that micro gets replaced as it gives error to code
    fpath = file_path[0]
    with open(fpath, 'rb') as ltspiceascfile:
        first_line = ltspiceascfile.read(4)
        if first_line.decode('utf-8') == "Vers":
            encoding = 'utf-8'
        elif first_line.decode('utf-16 le') == 'Ve':
            encoding = 'utf-16 le'
        else:
            raise ValueError("Unknown encoding.")
    ltspiceascfile.close()

    with open(fpath, mode='r', encoding=encoding) as ltspiceascfile:
        schematic = ltspiceascfile.readlines()
    ltspiceascfile.close()

    sketch_schematic_asc(schematic)

    # Display file path at the bottom of the window
    # l1 = Label(root, text="File path: " + file_path).pack()


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- Function for Drawing Schematic -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function to sketch the schematic which has been opened
def sketch_schematic_asc(schematic):
    # Remove all previous schematic drawings
    canvas.delete('schematic')
    canvas.delete('all')
    # Clear all previous labels in root window of component parameters
    for labels in component_parameters_frame.winfo_children():
        labels.destroy()
    # Clear all previous component parameters
    all_component_parameters.clear()

    # Clear all previous drawn wires, components, power flags, voltage sources, etc.
    wires = ''
    canvas_size = ''
    voltage_sources = ''
    components = ''
    power_flags = ''
    resistors = ''
    capacitors = ''
    inductors = ''
    diodes = ''
    # finds the connection wires in the circuit
    for lines in schematic:
        if "WIRE" in lines:
            wires += lines.replace("WIRE ", '')
        if "SHEET" in lines:
            canvas_size += lines.replace("SHEET 1 ", '')
        if "SYMBOL voltage " in lines:
            voltage_sources += lines.replace("SYMBOL voltage ", '')
        if "SYMBOL res " in lines:
            resistors += lines.replace("SYMBOL res ", '')
        if "SYMBOL cap " in lines:
            capacitors += lines.replace("SYMBOL cap ", '')
        if "SYMBOL ind " in lines:
            inductors += lines.replace("SYMBOL ind ", '')
        if "SYMBOL diode " in lines:
            diodes += lines.replace("SYMBOL diode ", '')
        if "SYMATTR InstName" in lines:
            components += lines.replace("SYMATTR InstName ", '')
        if "FLAG" in lines:
            power_flags += lines.replace("FLAG ", '')

    # ------------------------------------------Cleaning and filtering of elements--------------------------------------
    # Find canvas size to center image
    ############################# Not yet implemented ##################################################################
    canvas_size = canvas_size.split(" ")
    canvas_size = [int(size) for size in canvas_size]
    # canvas.configure(scrollregion=(-canvas_size[0]//4, -canvas_size[1]//4, canvas_size[0]//4, canvas_size[1]//4))

    # Removing new lines from components
    components = components.split('\n')
    components.pop()
    print(components)
    global circuit_components
    circuit_components = components
    # for component_number in range(len(components)):

    adjustment = 150
    # ------------------------------------------ Separating Resistors --------------------------------------------------
    resistor_x_adjustment = 6
    resistor_y_adjustment = 16
    resistors = resistors.split('\n')
    resistors = [res for resistor in resistors for res in resistor.split(' ')]
    resistors = [x for x in resistors if "R" not in x]
    resistors.pop()
    resistors = [int(resistor) for resistor in resistors]
    modified_resistors = [modification + adjustment for modification in resistors]

    # adjusting the x and y coordinates of the resistors
    for resistor_start in range(1, len(modified_resistors), 2):
        modified_resistors[resistor_start] = modified_resistors[resistor_start] + resistor_y_adjustment

    for resistor_start in range(0, len(modified_resistors), 2):
        modified_resistors[resistor_start] = modified_resistors[resistor_start] + resistor_x_adjustment

    # ------------------------------------------ Separating Capacitors -------------------------------------------------
    capacitors = capacitors.split('\n')
    capacitors = [cap for capacitor in capacitors for cap in capacitor.split(' ')]
    capacitors = [x for x in capacitors if "R" not in x]
    capacitors.pop()
    capacitors = [int(capacitor) for capacitor in capacitors]
    modified_capacitors = [modification + adjustment for modification in capacitors]

    # ------------------------------------------ Separating Inductors --------------------------------------------------
    inductors = inductors.split('\n')
    inductors = [ind for inductor in inductors for ind in inductor.split(' ')]
    inductors = [x for x in inductors if "R" not in x]
    inductors.pop()
    inductors = [int(inductor) for inductor in inductors]
    modified_inductors = [modification + adjustment for modification in inductors]

    # ------------------------------------------ Separating Diodes --------------------------------------------------
    diodes = diodes.split('\n')
    diodes = [dio for diode in diodes for dio in diode.split(' ')]
    diodes = [x for x in diodes if "R" not in x]
    diodes.pop()
    diodes = [int(diode) for diode in diodes]
    modified_diodes = [modification + adjustment for modification in diodes]
    print(modified_diodes)

    # ------------------------------------------ Separating voltage sources --------------------------------------------
    voltage_sources = voltage_sources.split('\n')
    voltage_sources = [voltage for source in voltage_sources for voltage in source.split(' ')]
    # removing anything which has 'R'
    voltage_sources = [x for x in voltage_sources if "R" not in x]
    voltage_sources.pop()
    voltage_sources = [int(sources) for sources in voltage_sources]
    modified_voltage_sources = [modification + adjustment for modification in voltage_sources]

    # -------------------------------------------- Separating Wires ----------------------------------------------------
    coordinates_one_line = wires.split('\n')
    coordinates_one_line.remove('')
    single_coordinates = [coordinate for singleCoord in coordinates_one_line for coordinate in singleCoord.split(' ')]
    single_coordinates = [int(coordinate) for coordinate in single_coordinates]
    modified_coordinates = [modification + adjustment for modification in single_coordinates]

    # ------------------------------------------- Separating Power Flags -----------------------------------------------
    ground_flags = []
    other_power_flags = []
    power_flags = power_flags.split('\n')
    power_flags = [flag for pwr_flag in power_flags for flag in pwr_flag.split(' ')]
    power_flags.pop()

    for flag_coordinates in range(2, len(power_flags), 3):
        if power_flags[flag_coordinates] == '0':
            ground_flags.append(power_flags[flag_coordinates - 2])
            ground_flags.append(power_flags[flag_coordinates - 1])
        elif power_flags[flag_coordinates] != '0':
            other_power_flags.append(power_flags[flag_coordinates - 2])
            other_power_flags.append(power_flags[flag_coordinates - 1])

    ground_flags = [int(coordinate) for coordinate in ground_flags]
    other_power_flags = [int(coordinate) for coordinate in other_power_flags]
    modified_ground_flags = [modification + adjustment for modification in ground_flags]
    # ------------------------------Power flags other than ground, not yet implemented----------------------------------
    ############################# Not yet implemented ##################################################################
    modified_other_power_flags = [modification + adjustment for modification in other_power_flags]

    # -------------------------------------------------Drawing resistors------------------------------------------------
    drawn_resistors = len(modified_resistors) * [None]

    for resistor in range(0, len(modified_resistors), 2):
        if (resistor + 1) >= len(modified_resistors):
            drawn_resistors[resistor] = canvas.create_polygon(modified_resistors[resistor - 2],
                                                              modified_resistors[resistor - 1],
                                                              modified_resistors[resistor - 2] + 20,
                                                              modified_resistors[resistor - 1],
                                                              modified_resistors[resistor - 2] + 20,
                                                              modified_resistors[resistor - 1] + 80,
                                                              modified_resistors[resistor - 2],
                                                              modified_resistors[resistor - 1] + 80,
                                                              modified_resistors[resistor - 2],
                                                              modified_resistors[resistor - 1],
                                                              fill='',
                                                              activefill='green',
                                                              outline='black',
                                                              disabledfill='',
                                                              tags='schematic',
                                                              )
            break
        drawn_resistors[resistor] = canvas.create_polygon(modified_resistors[resistor],
                                                          modified_resistors[resistor + 1],
                                                          modified_resistors[resistor] + 20,
                                                          modified_resistors[resistor + 1],
                                                          modified_resistors[resistor] + 20,
                                                          modified_resistors[resistor + 1] + 80,
                                                          modified_resistors[resistor],
                                                          modified_resistors[resistor + 1] + 80,
                                                          modified_resistors[resistor],
                                                          modified_resistors[resistor + 1],
                                                          fill='',
                                                          outline='black',
                                                          activefill='green',
                                                          disabledfill='',
                                                          tags='schematic')

    # ------------------------------------------------ Drawing Capacitors ----------------------------------------------
    drawn_capacitors = len(modified_capacitors) * [None]
    for capacitor in range(0, len(modified_capacitors), 2):
        draw_capacitor(modified_capacitors[capacitor], modified_capacitors[capacitor + 1], canvas)

    # ------------------------------------------------ Drawing Inductors -----------------------------------------------
    drawn_inductors = len(modified_inductors) * [None]
    for inductor in range(0, len(modified_inductors), 2):
        draw_inductor(modified_inductors[inductor], modified_inductors[inductor + 1], canvas)

    # ------------------------------------------------ Drawing Diodes --------------------------------------------------
    drawn_inductors = len(modified_diodes) * [None]
    for diode in range(0, len(modified_diodes), 2):
        draw_diode(modified_diodes[diode], modified_diodes[diode + 1], canvas)

    # -------------------------------------------------Drawing voltage sources------------------------------------------
    drawn_voltage_sources = len(modified_voltage_sources) * [None]
    for vol_sources in range(0, len(modified_voltage_sources), 2):
        drawn_voltage_sources[vol_sources] = canvas.create_circle(modified_voltage_sources[vol_sources],
                                                                  modified_voltage_sources[vol_sources + 1] + 56,
                                                                  40,
                                                                  tags='schematic')

    while None in drawn_voltage_sources: drawn_voltage_sources.remove(None)

    # ---------------------------------------------- Drawing Wires -----------------------------------------------------
    for coordinate in range(0, len(modified_coordinates), 4):

        # in case of last wire to prevent exceeding loop size
        if (coordinate + 3) >= len(modified_coordinates):
            canvas.create_line(modified_coordinates[coordinate - 4],
                               modified_coordinates[coordinate - 3],
                               modified_coordinates[coordinate - 2],
                               modified_coordinates[coordinate - 1],
                               tags='schematic')
            break
        # drawing of all wires except last wire
        canvas.create_line(modified_coordinates[coordinate],
                           modified_coordinates[coordinate + 1],
                           modified_coordinates[coordinate + 2],
                           modified_coordinates[coordinate + 3],
                           tags='schematic')

    # -------------------------------------------- Drawing Grounds -----------------------------------------------------
    ground_line = 10
    for flag_coordinates in range(0, len(ground_flags), 2):
        canvas.create_line(modified_ground_flags[flag_coordinates],
                           modified_ground_flags[flag_coordinates + 1],
                           modified_ground_flags[flag_coordinates],
                           modified_ground_flags[flag_coordinates + 1] + ground_line)

        canvas.create_polygon(modified_ground_flags[flag_coordinates] - 25,
                              modified_ground_flags[flag_coordinates + 1] + ground_line,
                              modified_ground_flags[flag_coordinates] + 25,
                              modified_ground_flags[flag_coordinates + 1] + ground_line,
                              modified_ground_flags[flag_coordinates],
                              modified_ground_flags[flag_coordinates + 1] + 25 + ground_line,
                              fill='',
                              outline='black',
                              tags='schematic')

    # --------------------------------------------Binding events--------------------------------------------------------

    # --------------------------- Making voltage sources change colour when hovered over -------------------------------
    for vol_elements in drawn_voltage_sources:
        canvas.tag_bind(vol_elements, '<Enter>', lambda event, arg=vol_elements: on_enter(event, arg))
        canvas.tag_bind(vol_elements, '<Leave>', lambda event, arg=vol_elements: on_leave(event, arg))

    # # --------------------------- Making resistors change colour when hovered over -------------------------------
    # for resistor_elements in drawn_resistors:
    #     canvas.tag_bind(resistor_elements, '<ButtonPress-1>',
    #                     lambda event,
    #                     arg=resistor_elements: on_resistor_press(event, arg))


# Select a schematic using a button
openfile_button = customtkinter.CTkButton(root,
                                          text='Open a Schematic',
                                          command=get_file_path
                                          )

# Button for entering the parameters of the circuit
enter_parameters_button = customtkinter.CTkButton(root,
                                                  text='Enter All Parameters',
                                                  command=component_parameters
                                                  )

value = 0
sketch_graphs(value)
# open file button, tab control and canvas location in root window
enter_parameters_button.pack(padx=0, pady=10, side=BOTTOM)
openfile_button.pack(padx=0, pady=2, side=BOTTOM)
tabControl.pack(expand=True, fill=BOTH)
canvas_frame.pack(side='left', fill=BOTH)
canvas.pack(fill=BOTH, expand=True)
component_parameters_frame.pack(side='right', fill=BOTH)
component_parameters_frame.propagate(False)


# run the application
root.mainloop()
