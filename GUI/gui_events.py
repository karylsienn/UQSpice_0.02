import locale

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np; np.random.seed(1)
import tkinter as tk
from tkinter import filedialog as fd
import ntpath
import component_sketcher as comp
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
import customtkinter

BACKGROUND_COLOUR = '#F0F0F0'
Mode = 'dark'
all_component_parameters = []
entering_parameters_window = None


# Replacing the oval function of tkinter with a simpler function for circles
def _create_circle(self, x_coordinate, y_coordinate, r, **kwargs):
    return self.create_oval(x_coordinate - r, y_coordinate - r, x_coordinate + r, y_coordinate + r, **kwargs)


tk.Canvas.create_circle = _create_circle


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Functions for Root starting window ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def open_asc_file(root, schematic_analysis):
    root.withdraw()
    schematic_analysis_width = 1100  # width for the Tk schematic_analysis
    schematic_analysis_height = 750  # height for the Tk schematic_analysis
    # Find the location of the main schematic analysis window
    screen_width = root.winfo_screenwidth()  # width of the screen
    screen_height = root.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk schematic_analysis window
    analysis_x = (screen_width / 2) - (schematic_analysis_width / 2) - (schematic_analysis_width / 5)
    analysis_y = (screen_height / 2) - (schematic_analysis_height / 2) - (schematic_analysis_height / 5)

    # set the dimensions of schematic analysis window and its position
    schematic_analysis.geometry('%dx%d+%d+%d' % (schematic_analysis_width,
                                                 schematic_analysis_height,
                                                 analysis_x,
                                                 analysis_y))

    # make the entering parameters window on top of the main schematic analysis window
    schematic_analysis.wm_transient(root)
    schematic_analysis.deiconify()


def open_raw_file():
    print('Open raw File')


def exit_application(root):
    root.destroy()


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Functions for schematic analysis --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Function for sketching graphs on tab 2 ----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def sketch_graphs(data, frame_to_display):
    figure = plt.Figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)
    x = np.sort(np.random.rand(15))
    y = np.sort(np.random.rand(15))
    names = np.array(list("ABCDEFGHIJKLMNO"))

    line, = ax.plot(x, y)

    chart_type = FigureCanvasTkAgg(figure, master=frame_to_display)
    chart_type.get_tk_widget().pack(side='top', fill='both')
    ax.set_title('Example Plot')
    ax.grid('on')
    names = np.array(list("ABCDEFGHIJKLMNO"))
    annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        graph_x, graph_y = line.get_data()
        annot.xy = (graph_x[ind["ind"][0]], graph_y[ind["ind"][0]])
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

    toolbar = NavigationToolbar2Tk(chart_type, frame_to_display, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for quiting the program --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def exit_program(frame_to_close):
    frame_to_close.destroy()


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- Component Filtering ------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def filter_components(components, adjustment):
    # Store all components coordinates in a list on the same line
    components = components.split('\n')
    # Split each element into its list of coordinates
    components = [comp for component in components for comp in component.split(' ')]
    # Remove anything containing R at the end
    components = [x for x in components if "R" not in x]
    # Remove last element which is empty
    components.pop()
    # convert all stored strings into integer values
    components = [int(component) for component in components]
    # add a small adjustment to all coordinates, so it appears on centre of screen
    modified_components = [modification + adjustment for modification in components]
    return modified_components


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Functions for hovering over components --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def on_enter(e, element_to_change, canvas):
    canvas.itemconfig(element_to_change, fill='green')


def on_leave(e, element_to_change, canvas):
    canvas.itemconfig(element_to_change, fill=BACKGROUND_COLOUR)


def on_resistor_press(event, arg, components):
    print(components)
    print(components[arg])
    print(arg)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------- Function for opening an LTSpice schematic ----------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for opening a ltspice schematic file
def get_file_path(component_parameters_frame,
                  all_component_parameters,
                  canvas,
                  schematic_analysis,
                  enter_parameters_button,
                  entering_parameters_window):
    """
    Obtains the file path selected from a dialog box.
    Event function for the Open a schematic button

    """
    # Open and return file path
    file_path = fd.askopenfilenames(
        title="Select a Schematic",

        filetypes=(
            ("Schematic", "*.asc"),
            ("All files", "*.*")
        )

    )

    too_many_files_selected = tk.Label(canvas,
                                       text='Please Select Two files,'
                                            ' an LTSpice schematic and an image of the schematic'
                                       )
    while len(file_path) > 2:
        file_path = fd.askopenfilenames(
            title="Select a Schematic",

            filetypes=(
                ("Schematic", "*.asc"),
                ("All files", "*.*")
            )

        )

    # Image Implementation - not yet working
    # svg_schematic = svg2rlg('C:/Users/moaik/OneDrive - The University of Nottingham/NSERP/LTspice to latex/Delete.svg')
    # renderPM.drawToFile(svg_schematic, "temp_schematic.png", fmt="PNG")
    # img = Image.open('temp_schematic.png')
    # pimg = ImageTk.PhotoImage(img)
    # global delete_image
    # delete_image = ImageTk.PhotoImage(img)
    # size = img.size
    # canvas.create_image(96 + 150, 224 + 150, image=pimg)
    # #canvas.create_line(96-13+150, 224+150, 128 + 13 + 150, 224+150)

    fpath = file_path[0]
    file_name = ntpath.basename(fpath)
    folder_location = fpath.removesuffix(file_name)
    file_name_no_extension = file_name.replace('.asc', '.txt')
    new_schematic_file = folder_location + file_name_no_extension

    with open(fpath, 'rb') as ltspiceascfile:
        first_line = ltspiceascfile.read(4)
        if first_line.decode('utf-8') == "Vers":
            encoding = 'utf-8'
        elif first_line.decode('utf-16 le') == 'Ve':
            encoding = 'utf-16 le'
        else:
            raise ValueError("Unknown encoding.")
    ltspiceascfile.close()

    read_encoding = locale.getpreferredencoding()

    # Open and store all file data
    with open(fpath, mode='r', encoding=read_encoding) as file:
        schematic_data = file.read()
    file.close()

    # Remove all 'µ' and replace them with 'u'
    with open(new_schematic_file, mode='w', encoding=encoding) as clean_schematic_file:
        clean_schematic_file.write(schematic_data.replace('µ', 'u'))
    clean_schematic_file.close()

    # Read clean file
    with open(new_schematic_file, mode='r', encoding=encoding) as ltspiceascfile:
        schematic = ltspiceascfile.readlines()
    ltspiceascfile.close()

    sketch_schematic_asc(schematic,
                         component_parameters_frame,
                         all_component_parameters,
                         canvas,
                         schematic_analysis,
                         enter_parameters_button,
                         entering_parameters_window)

    # Display file path at the bottom of the window
    # l1 = Label(schematic_analysis, text="File path: " + file_path).pack()


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- Function for Drawing Schematic -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function to sketch the schematic which has been opened
def sketch_schematic_asc(schematic,
                         component_parameters_frame,
                         all_component_parameters,
                         canvas,
                         schematic_analysis,
                         enter_parameters_button,
                         entering_parameters_window):
    """
    Sketches the LTSpice schematic provided from a given file path.

    Parameters
        ----------
        schematic : file path obtained from file dialog box with extension (.asc)
        component_parameters_frame: frame in which the component parameters are placed after selection
        all_component_parameters: List for storing parameters of all components
        canvas: Canvas to draw the components inside
        schematic_analysis: Window in which component parameters frame is placed inside
        enter_parameters_button: button to open a new window for entering parameters
        entering_parameters_window: Window displayed when button is clicked to enter parameters

    """

    # Remove all previous schematic drawings
    canvas.delete('all')
    # Clear all previous labels in schematic_analysis window of component parameters
    for labels in component_parameters_frame.winfo_children():
        labels.destroy()
    # Clear all previous component parameters
    all_component_parameters.clear()

    # Clear all previous drawn wires, components, power flags, voltage sources, etc.
    wires = ''
    canvas_size = ''
    voltage_sources = ''
    components = ''
    component_name_and_values = ''
    comp_values_list = []
    power_flags = ''
    resistors = ''
    capacitors = ''
    inductors = ''
    diodes = ''
    npn_transistor = ''
    comp_index = 0
    # finds the connection wires in the circuit
    for lines in schematic:

        # Store all connection wires
        if "WIRE" in lines:
            wires += lines.replace("WIRE ", '')
        if "SHEET" in lines:
            canvas_size += lines.replace("SHEET 1 ", '')

        # Store all components
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
        if "SYMBOL npn " in lines:
            npn_transistor += lines.replace("SYMBOL npn ", '')

        # Store all power flags used in the circuit
        if "FLAG" in lines:
            power_flags += lines.replace("FLAG ", '')

        # Store all component names and values
        if "SYMATTR InstName" in lines:
            components += lines.replace("SYMATTR InstName ", '')
            component_name_and_values += lines.replace("SYMATTR InstName ", '')
            comp_index = comp_index + 1
        if "SYMATTR Value" in lines:
            component_name_and_values += lines.replace("SYMATTR Value ", '')
            # print(comp_index - 1, end='')
            # print(':' + component_constant_values)

    # ------------------------------------------Cleaning and filtering of elements--------------------------------------
    # Find canvas size to center image
    # TODO: USE CANVAS SIZE FROM LTSPICE SCHEMATIC
    # canvas_size = canvas_size.split(" ")
    # canvas_size = [int(size) for size in canvas_size]
    # print(canvas_size)
    # canvas.configure(scrollregion=(-canvas_size[0]//4, -canvas_size[1]//4, canvas_size[0]//4, canvas_size[1]//4))

    # Store all component names and values
    component_name_and_values = component_name_and_values.split('\n')
    component_name_and_values.pop()
    component_details_dictionary = {}

    print(component_name_and_values)
    # for comps in range(0, len(component_name_and_values) + 1, 2):
    #     if (comps + 1) >= len(component_name_and_values):
    #         component_details_dictionary[component_name_and_values[comps]] = component_name_and_values[comps + 1]
    #         break
    #     else:
    #         component_details_dictionary[component_name_and_values[comps]] = component_name_and_values[comps + 1]

    print(component_details_dictionary)
    # Store all component names in a list after removing new lines
    components = components.split('\n')
    # Remove last element which is empty
    components.pop()

    enter_parameters_button.configure(command=lambda: open_new_window(components,
                                                                      schematic_analysis,
                                                                      component_parameters_frame,
                                                                      entering_parameters_window))

    adjustment = 150
    # ------------------------------------ Separating npn transistors --------------------------------------------------
    modified_npn_transistor = filter_components(npn_transistor, adjustment)

    # ------------------------------------------ Separating Resistors --------------------------------------------------
    modified_resistors = filter_components(resistors, adjustment)

    # ------------------------------------------ Separating Capacitors -------------------------------------------------
    modified_capacitors = filter_components(capacitors, adjustment)

    # ------------------------------------------ Separating Inductors --------------------------------------------------
    modified_inductors = filter_components(inductors, adjustment)

    # ------------------------------------------ Separating Diodes -----------------------------------------------------
    modified_diodes = filter_components(diodes, adjustment)

    # ------------------------------------------ Separating voltage sources --------------------------------------------
    modified_voltage_sources = filter_components(voltage_sources, adjustment)

    # -------------------------------------------- Separating Wires ----------------------------------------------------
    modified_coordinates = filter_components(wires, adjustment)

    # ------------------------------------------- Separating Power Flags -----------------------------------------------
    ground_flags = []
    other_power_flags = []
    power_flags = power_flags.split('\n')
    power_flags = [flag for pwr_flag in power_flags for flag in pwr_flag.split(' ')]
    power_flags.pop()

    for flag_coordinates in range(2, len(power_flags), 3):
        # Store all ground power flags
        if power_flags[flag_coordinates] == '0':
            ground_flags.append(power_flags[flag_coordinates - 2])
            ground_flags.append(power_flags[flag_coordinates - 1])
        # Store all other power flags
        elif power_flags[flag_coordinates] != '0':
            other_power_flags.append(power_flags[flag_coordinates - 2])
            other_power_flags.append(power_flags[flag_coordinates - 1])

    ground_flags = [int(coordinate) for coordinate in ground_flags]
    other_power_flags = [int(coordinate) for coordinate in other_power_flags]
    print(other_power_flags)
    modified_ground_flags = [modification + adjustment for modification in ground_flags]

    # -------------------------------------- Power flags other than ground ---------------------------------------------
    # TODO: Implement remaining power flags
    modified_other_power_flags = [modification + adjustment for modification in other_power_flags]

    # ------------------------------------------------ Drawing resistors -----------------------------------------------
    drawn_resistors = len(modified_resistors) * [None]

    drawing_components = comp.ComponentSketcher(canvas)
    drawing_components.sketch_components(modified_resistors, drawn_resistors, drawing_components.draw_resistor)

    # ------------------------------------------------ Drawing Capacitors ----------------------------------------------
    drawn_capacitors = len(modified_capacitors) * [None]
    drawing_components.sketch_components(modified_capacitors, drawn_capacitors, drawing_components.draw_capacitor)

    # ------------------------------------------------ Drawing Inductors -----------------------------------------------
    drawn_inductors = len(modified_inductors) * [None]
    drawing_components.sketch_components(modified_inductors, drawn_inductors, drawing_components.draw_inductor)

    # ------------------------------------------------ Drawing Diodes --------------------------------------------------
    drawn_diodes = len(modified_diodes) * [None]
    drawing_components.sketch_components(modified_diodes, drawn_diodes, drawing_components.draw_diode)

    # -------------------------------------------- Drawing Grounds -----------------------------------------------------
    drawn_ground_flags = len(ground_flags) * [None]
    drawing_components.sketch_components(modified_ground_flags,
                                         drawn_ground_flags,
                                         drawing_components.draw_ground_flags)

    # --------------------------------------------- Drawing npn transistors --------------------------------------------
    drawn_npn_transistors = len(modified_npn_transistor) * [None]
    drawing_components.sketch_components(modified_npn_transistor,
                                         drawn_npn_transistors,
                                         drawing_components.draw_npn_transistor)

    # ----------------------------------------------- Drawing voltage sources ------------------------------------------
    drawn_voltage_sources = len(modified_voltage_sources) * [None]
    for vol_sources in range(0, len(modified_voltage_sources), 2):
        drawn_voltage_sources[vol_sources] = canvas.create_circle(modified_voltage_sources[vol_sources],
                                                                  modified_voltage_sources[vol_sources + 1] + 56,
                                                                  40,
                                                                  tags='schematic')

    while None in drawn_voltage_sources:
        drawn_voltage_sources.remove(None)

    # ---------------------------------------------- Drawing Wires -----------------------------------------------------
    for coordinate in range(0, len(modified_coordinates), 4):

        canvas.create_line(modified_coordinates[coordinate],
                           modified_coordinates[coordinate + 1],
                           modified_coordinates[coordinate + 2],
                           modified_coordinates[coordinate + 3],
                           tags='schematic')

    # ------------------------------------ Binding events to drawn shapes ----------------------------------------------

    # --------------------------- Making voltage sources change colour when hovered over -------------------------------
    for vol_elements in drawn_voltage_sources:
        canvas.tag_bind(vol_elements, '<Enter>', lambda event, arg=vol_elements: on_enter(event, arg, canvas))
        canvas.tag_bind(vol_elements, '<Leave>', lambda event, arg=vol_elements: on_leave(event, arg, canvas))

    # # --------------------------- Making resistors open new window when hovered over ---------------------------------
    # for resistor_elements in drawn_resistors:
    #     canvas.tag_bind(resistor_elements, '<ButtonPress-1>',
    #                     lambda event,
    #                     arg=resistor_elements: on_resistor_press(event, arg))


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


# Function when the selected component has been changed from dropdown list
def change_component_index(component_selected,
                           value_selected,
                           distribution_type,
                           component_distribution_array,
                           component_param1_label_array,
                           component_param2_label_array,
                           component_param1_array,
                           component_param2_array,
                           components
                           ):
    global component_index
    for comp_index in range(len(components)):
        if component_selected.get() == components[comp_index]:
            component_index = comp_index

    component_param1_array[component_index].grid_remove()
    component_param2_array[component_index].grid_remove()
    component_distribution_array[component_index].delete('1.0', tk.END)

    # Check which distribution has been selected and change the parameters accordingly
    if distribution_type.get() == 'Gamma Distribution':
        component_distribution_array[component_index].insert(tk.INSERT, 'Gamma')
        component_param1_label_array[component_index]['text'] = 'Shape (k)'
        component_param2_label_array[component_index]['text'] = 'Scale (θ)'

    if distribution_type.get() == 'Beta Distribution':
        component_distribution_array[component_index].insert(tk.INSERT, 'Beta')
        component_param1_label_array[component_index]['text'] = 'Alpha (α)'
        component_param2_label_array[component_index]['text'] = 'Beta (β)'

    if distribution_type.get() == 'Normal Distribution':
        component_distribution_array[component_index].insert(tk.INSERT, 'Normal')
        component_param1_label_array[component_index]['text'] = 'Mean (μ)'
        component_param2_label_array[component_index]['text'] = 'Standard deviation (σ)'

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
    component_distribution[index_of_selected_component].delete('1.0', tk.END)
    if distribution_type.get() == 'Gamma Distribution':
        component_distribution[index_of_selected_component].insert(tk.INSERT, 'Gamma')
        parameter1_label[index_of_selected_component]['text'] = 'Shape (k)'
        parameter2_label[index_of_selected_component]['text'] = 'Scale (θ)'

    if distribution_type.get() == 'Beta Distribution':
        component_distribution[index_of_selected_component].insert(tk.INSERT, 'Beta')
        parameter1_label[index_of_selected_component]['text'] = 'Alpha (α)'
        parameter2_label[index_of_selected_component]['text'] = 'Beta (β)'

    if distribution_type.get() == 'Normal Distribution':
        component_distribution[index_of_selected_component].insert(tk.INSERT, 'Normal')
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
# -------------------------------------- Function for enter all parameters button --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for entering parameters
def open_new_window(components, schematic_analysis, component_parameters_frame, parameters_window):
    # Creating a new window for entering parameters
    # Check if entering parameters window is already open:
    # if TRUE: lift it on top of schematic analysis window
    global entering_parameters_window
    if entering_parameters_window is not None and entering_parameters_window.winfo_exists():
        entering_parameters_window.lift(schematic_analysis)
        entering_parameters_window.wm_transient(schematic_analysis)
    # if FALSE: Create a new enter parameters window
    else:
        entering_parameters_window = customtkinter.CTkToplevel(schematic_analysis)

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

        # Find the location of the main schematic analysis window
        schematic_x = schematic_analysis.winfo_x()
        schematic_y = schematic_analysis.winfo_y()
        # set the size and location of the new window created for entering parameters
        entering_parameters_window.geometry("460x210+%d+%d" % (schematic_x + 40, schematic_y + 100))
        # make the entering parameters window on top of the main schematic analysis window
        entering_parameters_window.wm_transient(schematic_analysis)

        component_name_array = [None] * len(components)
        component_distribution_array = [None] * len(components)
        component_param1_entry_box = [None] * len(components)
        component_value_array = ['Constant'] * len(components)
        component_param1_label_array = [None] * len(components)
        component_param2_label_array = [None] * len(components)
        component_param1_array = [None] * len(components)
        component_param2_array = [None] * len(components)
        name_label_array = [None] * len(components)
        component_full_information_array = [None] * len(components)
        delete_button = [None] * len(components)
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
        component_value_label = tk.Label(entering_parameters_window,
                                         height=1,
                                         width=10,
                                         text='Value:',
                                         background=label_background,
                                         foreground=text_colour,
                                         highlightbackground=label_background)

        component_name_array_label = tk.Label(entering_parameters_window,
                                              height=1,
                                              width=20,
                                              text='Component Name:',
                                              background=label_background,
                                              foreground=text_colour,
                                              highlightbackground=label_background
                                              )

        component_distribution_label = tk.Label(entering_parameters_window,
                                                height=1,
                                                width=20,
                                                text='Distribution',
                                                background=label_background,
                                                foreground=text_colour,
                                                highlightbackground=label_background
                                                )

        for circuit_component in range(len(components)):
            component_name_array[circuit_component] = tk.Label(entering_parameters_window,
                                                               height=1,
                                                               width=20,
                                                               text=components[circuit_component],
                                                               background=label_background,
                                                               foreground=text_colour
                                                               )

            component_distribution_array[circuit_component] = tk.Text(entering_parameters_window,
                                                                      height=1,
                                                                      width=20,
                                                                      bg="white"
                                                                      )

            component_param1_label_array[circuit_component] = tk.Label(entering_parameters_window,
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

            component_param2_label_array[circuit_component] = tk.Label(entering_parameters_window,
                                                                       height=1,
                                                                       width=20,
                                                                       text='',
                                                                       background=label_background,
                                                                       foreground=text_colour
                                                                       )

            component_param1_array[circuit_component] = tk.Text(entering_parameters_window,
                                                                height=1,
                                                                width=20,
                                                                bg="white")

            component_param2_array[circuit_component] = tk.Text(entering_parameters_window,
                                                                height=1,
                                                                width=20,
                                                                bg="white")

            name_label_array[circuit_component] = tk.Label(component_parameters_frame,
                                                           text='',
                                                           width=25,
                                                           height=5,
                                                           highlightcolor='black',
                                                           highlightthickness=2,
                                                           borderwidth=1,
                                                           justify='center',
                                                           relief='solid'
                                                           )

            delete_button[circuit_component] = tk.Button(name_label_array[circuit_component],
                                                         text='',
                                                         background=BACKGROUND_COLOUR,
                                                         activebackground='red',
                                                         relief='flat',
                                                         # image=delete_image,
                                                         command=delete_label
                                                         )

            # component_full_information_array[circuit_component] = tk.Entry(component_parameters_frame)

            # Default parameters which are:
            # distribution: Normal
            # Mean = 1
            # Standard Deviation = 2
            component_distribution_array[circuit_component].insert(tk.INSERT, 'Normal')
            component_param1_label_array[circuit_component]['text'] = 'Mean (μ)'
            component_param2_label_array[circuit_component]['text'] = 'Standard deviation (σ)'
            component_param1_array[circuit_component].insert(tk.INSERT, '1')
            component_param2_array[circuit_component].insert(tk.INSERT, '2')

        component_selected = tk.StringVar(entering_parameters_window)
        component_selected.set(components[0])
        distributions = ['Normal Distribution', 'Gamma Distribution', 'Beta Distribution']
        distribution_selected = tk.StringVar(entering_parameters_window)
        distribution_selected.set(distributions[0])
        comp_values = ['Constant', 'Random']
        values_selected = tk.StringVar(entering_parameters_window)
        values_selected.set(comp_values[0])
        max_distribution_width = len(max(distributions, key=len))

        global component_index
        component_index = 0

        # Drop down list for selecting which component to enter parameters for
        component_drop_down_list = \
            customtkinter.CTkOptionMenu(master=entering_parameters_window,
                                        variable=component_selected,
                                        values=components,
                                        width=max_distribution_width,
                                        command=lambda _: change_component_index(component_selected,
                                                                                 values_selected,
                                                                                 distribution_selected,
                                                                                 component_distribution_array,
                                                                                 component_param1_label_array,
                                                                                 component_param2_label_array,
                                                                                 component_param1_array,
                                                                                 component_param2_array,
                                                                                 components
                                                                                 ))

        # Drop down list for selecting the type of distribution for random components
        distribution_drop_down_list = \
            customtkinter.CTkOptionMenu(master=entering_parameters_window,
                                        variable=distribution_selected,
                                        values=distributions,
                                        width=max_distribution_width,
                                        command=lambda _:
                                        select_distribution_type(distribution_selected,
                                                                 component_index,
                                                                 component_distribution_array,
                                                                 component_param1_label_array,
                                                                 component_param2_label_array,
                                                                 component_param1_array,
                                                                 component_param2_array
                                                                 ))
        # Drop down list for selecting if component value is random or constant
        # component_value_drop_down_list = \
        #     customtkinter.CTkOptionMenu(master=entering_parameters_window,
        #                                 variable=values_selected,
        #                                 values=comp_values,
        #                                 width=max_distribution_width,
        #                                 command=lambda _: random_or_constant(values_selected,
        #                                                                      component_distribution_label,
        #                                                                      distribution_drop_down_list,
        #                                                                      component_param1_label_array,
        #                                                                      component_param2_label_array,
        #                                                                      component_param1_array,
        #                                                                      component_param2_array
        #                                                                      ))

        # Button for saving individual parameters
        save_parameters_button = customtkinter.CTkButton(
            entering_parameters_window,
            text='Save Parameters',
            command=lambda:
            save_entered_parameters(entering_parameters_window,
                                    values_selected,
                                    component_selected.get(),
                                    distribution_selected.get(),
                                    component_distribution_array[component_index].get('1.0', tk.END).strip('\n'),
                                    component_param1_label_array[component_index]['text'],
                                    component_param2_label_array[component_index]['text'],
                                    component_param1_array[component_index].get('1.0', tk.END).strip('\n'),
                                    component_param2_array[component_index].get('1.0', tk.END).strip('\n'),
                                    component_index,
                                    name_label_array,
                                    delete_button,
                                    component_value_array)
        )

        # Button for saving all parameters
        save_all_parameters_button = customtkinter.CTkButton(
            entering_parameters_window,
            text='Save All Parameters',
            command=lambda: save_all_entered_parameters(components,
                                                        values_selected,
                                                        component_distribution_array,
                                                        component_param1_label_array,
                                                        component_param2_label_array,
                                                        component_param1_array,
                                                        component_param2_array,
                                                        name_label_array,
                                                        component_value_array,
                                                        component_parameters_frame)
        )

        component_name_row = 3
        distribution_row = 4
        button_row = 10

        # Button for closing window
        cancel_button = customtkinter.CTkButton(entering_parameters_window,
                                                text='Cancel',
                                                command=lambda: close_window(entering_parameters_window))

        # Component drop down list and component name label
        component_name_array_label.grid(row=component_name_row, column=5, sticky='news')
        component_drop_down_list.grid(row=component_name_row, column=6)

        # Placing label and dropdown for distributions
        component_distribution_label.grid(row=distribution_row, column=5, sticky='news')
        distribution_drop_down_list.grid(row=distribution_row, column=6)

        # Closing parameters window
        cancel_button.grid(row=button_row, column=5)

        # Saving Parameters button location in new window
        save_parameters_button.grid(row=button_row, column=6)

        # Saving All Parameters button location in new window
        save_all_parameters_button.grid(row=button_row, column=7)

        # Ensuring all widgets inside enter parameters window are resizable
        entering_parameters_window.grid_rowconfigure(tuple(range(button_row)), weight=1)
        entering_parameters_window.grid_columnconfigure(tuple(range(button_row)), weight=1)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for deleting entered parameters ------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def delete_label():
    print('Deleting label')


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for saving a single parameter --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for closing new windows using a  button
def save_entered_parameters(entering_parameters_window,
                            component_value,
                            component_name,
                            selected_distribution,
                            component_distribution,
                            component_param1_label,
                            component_param2_label,
                            component_param1,
                            component_param2,
                            index,
                            full_name_labels,
                            delete_label_button,
                            component_value_array):
    global all_component_parameters
    global component_index

    if component_value.get() == 'Random':
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
        # --------------------------------- Displaying entered parameters on schematic_analysis window -----------------
        print(component_index)

        full_name_labels[index].config(text='')
        full_name_labels[index].config(width=25)
        full_name_labels[index].config(height=5)

        full_name_labels[index].config(text=component_name +
                                            '\nDistribution: ' + component_distribution +
                                            '\n' + component_param1_label + '=' + component_param1 +
                                            '\n' + component_param2_label + '=' + component_param2)

    # If value is constant just display the label only.
    elif component_value.get() == 'Constant':
        full_name_labels[index].config(text='')
        full_name_labels[index].config(width=25)
        full_name_labels[index].config(height=5)

        # Store that component as a constant
        component_value_array[index] = 'Constant'

        full_name_labels[index].config(text=component_name +
                                       '\nDistribution: ' + component_distribution +
                                       '\n' + component_param1_label + '=' + component_param1 +
                                       '\n' + component_param2_label + '=' + component_param2)

    # for comp in range(len(components)):
    #     delete_label_button[comp] = Button(full_name_labels[comp],
    #                                         text='',
    #                                         background=BACKGROUND_COLOUR,
    #                                         activebackground='red',
    #                                         relief='flat',
    #                                         image=delete_image,
    #                                         command=delete_label
    #                                         )
    #     delete_label_button[comp].pack(side=LEFT, anchor=NW, expand=False)

    full_name_labels[component_index].grid(row=component_index, column=1, sticky='nsew')
    # delete_label_button[component_index].pack(side=LEFT, anchor=NW, expand=False)


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
                                component_value_array,
                                component_parameters_frame
                                ):
    global all_component_parameters
    all_component_parameters.clear()

    component_param1_dictionary_input = [None] * len(component_param1_label_array)
    component_param2_dictionary_input = [None] * len(component_param2_label_array)

    for distributions in range(len(component_distribution_array)):
        if component_distribution_array[distributions].get('1.0', tk.END).strip('\n') == 'Normal':
            component_param1_dictionary_input[distributions] = 'mean'
            component_param2_dictionary_input[distributions] = 'standard deviation'
        elif component_distribution_array[distributions].get('1.0', tk.END).strip('\n') == 'Gamma':
            component_param1_dictionary_input[distributions] = 'shape'
            component_param2_dictionary_input[distributions] = 'theta'
        elif component_distribution_array[distributions].get('1.0', tk.END).strip('\n') == 'Beta':
            component_param1_dictionary_input[distributions] = 'alpha'
            component_param2_dictionary_input[distributions] = 'beta'

    # If value is Random, display label and store in dictionary
    for circuit_component in range(len(component_name)):
        if component_value_array[circuit_component] == 'Random':
            print(component_name)
            # clearing the name label of all parameters
            full_name_labels[circuit_component].config(text='')
            full_name_labels[circuit_component].config(borderwidth=0)
            full_name_labels[circuit_component].config(relief='flat')

            # Storing the name label of all parameters
            full_name_labels[circuit_component] = \
                tk.Label(component_parameters_frame,
                         text=component_name[circuit_component]
                         + '\nDistribution: ' +
                         component_distribution_array[circuit_component].get('1.0', tk.END).strip('\n')
                         + '\n' + component_param1_label_array[circuit_component]['text'] + '='
                         + component_param1_array[circuit_component].get('1.0', tk.END).strip('\n')
                         + '\n' + component_param2_label_array[circuit_component]['text'] +
                         '=' + component_param2_array[circuit_component].get('1.0', tk.END).strip('\n'),
                         highlightcolor='black',
                         highlightthickness=2,
                         borderwidth=1,
                         relief='solid',
                         justify='center',
                         height=5,
                         width=25
                         )

            # Placing the name label of all parameters on the schematic_analysis window
            full_name_labels[circuit_component].grid(row=circuit_component, column=1)

            # Storing all components with their parameters in a dictionary
            all_component_parameters.append(
                {component_name[circuit_component]:
                     {'distribution': component_distribution_array[circuit_component].get('1.0', tk.END).strip('\n'),

                      'parameters': {  # Parameter 1 label and user entered number
                          component_param1_dictionary_input[circuit_component]:
                              component_param1_array[circuit_component].get('1.0', tk.END).strip('\n'),
                          # Parameter 2 label and user entered number
                          component_param2_dictionary_input[circuit_component]:
                              component_param2_array[circuit_component].get('1.0', tk.END).strip('\n')}
                      }
                 }
            )

        # If value is Constant, display label only. DO NOT store in dictionary
        elif component_value_array[circuit_component] == 'Constant':

            full_name_labels[circuit_component].config(text='')
            full_name_labels[circuit_component].config(borderwidth=0)
            full_name_labels[circuit_component].config(relief='flat')

            # Storing the name label of all parameters
            full_name_labels[circuit_component] = \
                tk.Label(component_parameters_frame,
                         text=component_name[circuit_component] + '\nValue: ' + '5',
                         highlightcolor='black',
                         highlightthickness=2,
                         borderwidth=1,
                         relief='solid',
                         justify='center',
                         height=5,
                         width=25
                         )

            # Placing the name label of all parameters on the schematic_analysis window
            full_name_labels[circuit_component].grid(row=circuit_component, column=1)

    print(all_component_parameters)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Function for closing parameters window -------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def close_window(window_to_close):
    window_to_close.destroy()


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Function when no schematic selected ----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def error_select_schematic(canvas):
    canvas.create_window(400, 300,
                         window=tk.Label(canvas,
                                         text="Please select a schematic",
                                         width=40,
                                         font=("Times New Roman", 20),
                                         height=40),
                         tags='Error if schematic not entered')


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Function for entering component parameters ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Entering Component Parameters for all elements
def component_parameters(components,
                         canvas,
                         schematic_analysis,
                         component_parameters_frame,
                         entering_parameters_window):
    global all_component_parameters

    if len(components) != 0:
        open_new_window(components, schematic_analysis, component_parameters_frame, entering_parameters_window)
    else:
        error_for_not_entering_schematic = \
            canvas.create_window(400, 300,
                                 window=tk.Label(canvas,
                                                 text="Please select a schematic with components",
                                                 width=40,
                                                 font=("Times New Roman", 20),
                                                 height=40),
                                 tags='Error if schematic has no components')