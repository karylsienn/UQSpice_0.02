# GUI controller containing all functions
import controller as control


def main():
    control.root.mainloop()


<<<<<<< HEAD
# Run main GUI application
if __name__ == '__main__':
    # Starting the GUI program
    main()
=======
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


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

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


# create the root window
root = Tk()
root.title('EMC Analysis')
root.geometry('1080x720+250+200')

tabControl = ttk.Notebook(root)

schematic_params = ttk.Frame(tabControl)
graphs = ttk.Frame(tabControl)

tabControl.add(schematic_params, text='Schematic and entering parameters')
tabControl.add(graphs, text='Graphs')

component_parameters_frame = Frame(schematic_params, width=200, height=100)
component_parameters_frame.pack(side='right', fill=Y, padx=40)

canvas = ResizingCanvas(schematic_params, width=700, height=500, highlightthickness=0)

all_component_parameters = []
name_label = Label(canvas, text='')


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Functions for hovering over components --------------------------------------
# ---------------------------------------------Not Implemented----------------------------------------------------------
def on_enter(e, element_to_change):
    canvas.itemconfig(element_to_change, fill='green')
    print("happening")


def on_leave(e, element_to_change):
    canvas.itemconfig(element_to_change, fill='white')


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Functions for distribution buttons ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def normal_distribution_params(component_distribution,
                               component_param1_label,
                               component_param2_label,
                               component_param1,
                               component_param2,
                               array_of_tabs,
                               tab_number
                               ):
    component_distribution.delete('1.0', END)
    component_distribution.insert(INSERT, 'Normal')
    component_param1_label['text'] = 'Mean (μ)'
    component_param2_label['text'] = 'Standard deviation (σ)'
    # component_param1.place(in_=array_of_tabs[tab_number], x=136, y=100)
    # component_param2.place(in_=array_of_tabs[tab_number], x=136, y=130)
    # component_param1_label.place(in_=array_of_tabs[tab_number], x=1, y=100)
    # component_param2_label.place(in_=array_of_tabs[tab_number], x=1, y=130)


def gamma_distribution_params(component_distribution,
                              component_param1_label,
                              component_param2_label,
                              component_param1,
                              component_param2,
                              array_of_tabs,
                              tab_number
                              ):
    component_distribution.delete('1.0', END)
    component_distribution.insert(INSERT, 'Gamma')
    component_param1_label['text'] = 'Shape (k)'
    component_param2_label['text'] = 'Scale (θ)'
    # component_param1.place(in_=array_of_tabs[tab_number], x=136, y=100)
    # component_param2.place(in_=array_of_tabs[tab_number], x=136, y=130)
    # component_param1_label.place(in_=array_of_tabs[tab_number], x=1, y=100)
    # component_param2_label.place(in_=array_of_tabs[tab_number], x=1, y=130)


def beta_distribution_params(component_distribution,
                             component_param1_label,
                             component_param2_label,
                             component_param1,
                             component_param2,
                             array_of_tabs,
                             tab_number
                             ):
    component_distribution.delete('1.0', END)
    component_distribution.insert(INSERT, 'Beta')
    component_param1_label['text'] = 'Alpha (α)'
    component_param2_label['text'] = 'Beta (β)'
    # component_param1.place(in_=array_of_tabs[tab_number], x=136, y=100)
    # component_param2.place(in_=array_of_tabs[tab_number], x=136, y=130)
    # component_param1_label.place(in_=array_of_tabs[tab_number], x=1, y=100)
    # component_param2_label.place(in_=array_of_tabs[tab_number], x=1, y=130)


def change_component_index(component_selected):
    global component_index
    for comp_index in range(len(circuit_components)):
        if component_selected.get() == circuit_components[comp_index]:
            component_index = comp_index


def select_distribution_type(distribution_type,
                             parameter1_label,
                             parameter2_label,
                             component_distribution):

    if distribution_type.get() == 'Gamma Distribution':
        component_distribution['text'] = 'Gamma'
        parameter1_label['text'] = 'Shape (k)'
        parameter2_label['text'] = 'Scale (θ)'

    if distribution_type.get() == 'Beta Distribution':
        component_distribution['text'] = 'Beta'
        parameter1_label['text'] = 'Alpha (α)'
        parameter2_label['text'] = 'Beta (β)'

    if distribution_type.get() == 'Normal Distribution':
        component_distribution['text'] = 'Normal'
        parameter1_label['text'] = 'Mean (μ)'
        parameter2_label['text'] = 'Standard deviation (σ)'
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

    data = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
            'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
            }
    data_frame_plot = DataFrame(data, columns=['Country', 'GDP_Per_Capita'])
    figure = plt.Figure(figsize=(10, 6), dpi=100)
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, graphs)
    chart_type.get_tk_widget().pack()
    data_frame_plot = data_frame_plot[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
    data_frame_plot.plot(kind='line', legend=True, ax=ax)
    ax.set_title('Example Plot')


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Function for enter all parameters button --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for entering parameters
def open_new_window(component, index):
    global name_label
    # Toplevel object which will
    # be treated as a new window
    entering_parameters_window = Toplevel(root)

    # sets the title of the new window created for entering parameters
    entering_parameters_window.title("Enter Component Parameters")

    # sets the size of the new window created for entering parameters
    # entering_parameters_window.geometry("500x300")

    # # Add a grid
    # mainframe = Frame(entering_parameters_window)
    # mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    # mainframe.columnconfigure(0, weight=1)
    # mainframe.rowconfigure(0, weight=1)



    component_tabs = ttk.Notebook(entering_parameters_window)

    component_tabs_array = [None] * len(circuit_components)
    component_name_array = [None] * len(circuit_components)
    component_distribution_array = [None] * len(circuit_components)
    component_param1_label_array = [None] * len(circuit_components)
    component_param2_label_array = [None] * len(circuit_components)
    component_param1_array = [None] * len(circuit_components)
    component_param2_array = [None] * len(circuit_components)
    name_label_array = [None] * len(circuit_components)

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
    component_name_array_label = Label(entering_parameters_window,
                                       text='Component Name:',
                                       width=20)

    component_distribution_label = Label(entering_parameters_window,
                                         text='Distribution',
                                         width=20)

    distribution_for_component_label = Label(entering_parameters_window,
                                       text='',
                                       width=20)

    component_param1_label = Label(entering_parameters_window,
                              text='',
                              width=20)

    component_param2_label = Label(entering_parameters_window,
                                   text='',
                                   width=20)

    component_selected = StringVar(root)
    component_selected.set(circuit_components[0])
    distributions = ['Normal Distribution', 'Gamma Distribution', 'Beta Distribution']
    distribution_selected = StringVar(root)
    distribution_selected.set(distributions[0])

    global component_index
    component_index = 0
    component_drop_down_list = OptionMenu(entering_parameters_window,
                                          component_selected,
                                          *circuit_components,
                                          command=lambda _: change_component_index(component_selected))
    distribution_drop_down_list = OptionMenu(entering_parameters_window,
                                             distribution_selected,
                                             *distributions,
                                             command=lambda _: select_distribution_type(distribution_selected,
                                                                                        component_param1_label,
                                                                                        component_param2_label,
                                                                                        distribution_for_component_label))

    for circuit_component in range(len(circuit_components)):

        component_tabs_array[circuit_component] = ttk.Frame(component_tabs)
        component_tabs.add(component_tabs_array[circuit_component], text=circuit_components[circuit_component])
        component_name_array[circuit_component] = Label(entering_parameters_window,
                                                                text=circuit_components[circuit_component],
                                                                width=10)
        # Parameters entered by the user
        #component_name_array[circuit_component].place(in_=component_tabs_array[circuit_component], x=180, y=17)
        component_distribution_array[circuit_component] = Text(entering_parameters_window,
                                                               height=1,
                                                               width=12,
                                                               bg="white")

        component_param1_label_array[circuit_component] = Label(entering_parameters_window,
                                                                        text='',
                                                                        width=20)

        component_param2_label_array[circuit_component] = Label(entering_parameters_window,
                                                                        text='',
                                                                        width=20)

        component_param1_array[circuit_component] = Text(entering_parameters_window,
                                                         height=1,
                                                         width=6,
                                                         bg="white")

        component_param2_array[circuit_component] = Text(entering_parameters_window,
                                                         height=1,
                                                         width=6,
                                                         bg="white")

        name_label_array[circuit_component] = Label(canvas,
                                                    text='')



        # Default parameters which are:
        # distribution: Normal
        # Mean = 1
        # Standard Deviation = 2
        component_distribution_array[circuit_component].insert(INSERT, 'Normal')
        component_param1_label_array[circuit_component]['text'] = 'Mean (μ)'
        component_param2_label_array[circuit_component]['text'] = 'Standard Deviation (σ)'
        component_param1_array[circuit_component].insert(INSERT, '1')
        component_param2_array[circuit_component].insert(INSERT, '2')


    #component_tabs.pack(expand=True, fill=BOTH)
    distribution_for_component_label['text'] = 'Normal'
    component_param1_label['text'] = 'Mean (μ)'
    component_param2_label['text'] = 'Standard Deviation (σ)'


    print(distribution_for_component_label['text'])
    # Button for saving parameters
    save_parameters_button = ttk.Button(
        entering_parameters_window,
        text='Save Parameters',
        command=lambda: save_entered_parameters(entering_parameters_window,
                                                component_selected.get(),
                                                distribution_for_component_label['text'],
                                                component_param1_label['text'],
                                                component_param2_label['text'],
                                                component_param1_array[
                                                    component_tabs.index(component_tabs.select())].get(
                                                    '1.0', END).strip('\n'),
                                                component_param2_array[
                                                    component_tabs.index(component_tabs.select())].get(
                                                    '1.0', END).strip('\n'),
                                                component_index,
                                                name_label_array)
    )

    # Button for saving parameters
    save_all_parameters_button = ttk.Button(
        entering_parameters_window,
        text='Save All Parameters',
        command=lambda: save_all_entered_parameters(component,
                                                    component_distribution_array,
                                                    component_param1_label_array,
                                                    component_param2_label_array,
                                                    component_param1_array,
                                                    component_param2_array,
                                                    name_label_array)
    )

    # Component drop down list and component name label
    component_name_array_label.grid(row=3, column=5)
    component_drop_down_list.grid(row=3, column=6)

    # Placing Distribution Label
    component_distribution_label.grid(row=4, column=5)
    distribution_drop_down_list.grid(row=4, column=6)

    component_param1_label.grid(row=5, column=5)
    component_param2_label.grid(row=6, column=5)
    component_param1_array[0].grid(row=5, column=6)
    component_param2_array[0].grid(row=6, column=6)

    # Saving Parameters button location in new window
    save_parameters_button.grid(row=8, column=7)
    save_parameters_button.grid_rowconfigure(8, weight=1)
    save_parameters_button.grid_columnconfigure(6, weight=1)

    # Saving All Parameters button location in new window
    save_all_parameters_button.grid(row=8, column=8)
    save_all_parameters_button.grid_rowconfigure(8, weight=1)
    save_all_parameters_button.grid_columnconfigure(7, weight=1)

    component_name_array_label.grid_rowconfigure(3, weight=1)
    component_name_array_label.grid_columnconfigure(5, weight=1)
    component_drop_down_list.grid_rowconfigure(3, weight=1)
    component_drop_down_list.grid_columnconfigure(6, weight=1)
    entering_parameters_window.resizable(False, False)
    enter_parameters_button.wait_window(entering_parameters_window)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for saving a single parameter --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Function for closing new windows using a  button
def save_entered_parameters(entering_parameters_window,
                            component_name,
                            component_distribution,
                            component_param1_label,
                            component_param2_label,
                            component_param1,
                            component_param2,
                            index,
                            full_name_labels):
    global all_component_parameters
    global component_index

    if len(all_component_parameters) == 0:
        all_component_parameters.append({component_name:
                                             {'distribution': component_distribution,
                                              'parameters': {component_param1_label: component_param1,
                                                             component_param2_label: component_param2}
                                              }
                                         }
                                        )

    # -------------------------- removing duplicates and storing in a list of dictionaries -----------------------------
    appending_flag = 0
    for parameters in range(len(all_component_parameters)):
        if component_name == list(all_component_parameters[parameters].keys())[-1]:
            # If the last entered component is similar to the previously entered one then,
            # replace the old parameters with the new ones
            all_component_parameters[parameters] = ({component_name:
                                                         {'distribution': component_distribution,
                                                          'parameters': {component_param1_label: component_param1,
                                                                         component_param2_label: component_param2}
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
                                              'parameters': {component_param1_label: component_param1,
                                                             component_param2_label: component_param2}
                                              }
                                         }

                                        )
        appending_flag = 0

    print(all_component_parameters)
    # --------------------------------- Displaying entered parameters on root window -----------------------------------
    global name_label
    print(component_index)
    full_name_labels[index].config(text='')
    full_name_labels[index] = Label(component_parameters_frame,
                                    text=component_name +
                                         '\nDistribution: ' + component_distribution +
                                         '\n' + component_param1_label + '=' + component_param1 +
                                         '\n' + component_param2_label + '=' + component_param2)

    full_name_labels[component_index].grid(row=component_index, column=1)


    # frame_window = canvas.create_window(800,
    #                                     (100 * index) + 100, anchor=E,
    #                                     window=canvas_frame,
    #                                     tags='schematic')


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- Function for saving all parameters ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def save_all_entered_parameters(component_name,
                                component_distribution_array,
                                component_param1_label_array,
                                component_param2_label_array,
                                component_param1_array,
                                component_param2_array,
                                full_name_labels):
    global name_label
    global all_component_parameters
    all_component_parameters.clear()

    print(component_name)
    for circuit_component in range(len(circuit_components)):
        # clearing the name label of all parameters
        full_name_labels[circuit_component].config(text='')

        # Storing the name label of all parameters
        full_name_labels[circuit_component] = \
            Label(canvas,
                  text=component_name[circuit_component] +

                       '\nDistribution: ' + component_distribution_array[circuit_component].get('1.0', END).strip(
                      '\n') +

                       '\n' + component_param1_label_array[circuit_component]['text']
                       + '=' + component_param1_array[circuit_component].get('1.0', END).strip('\n') +

                       '\n' + component_param2_label_array[circuit_component]['text']
                       + '=' + component_param2_array[circuit_component].get('1.0', END).strip('\n'))

        # Placing the name label of all parameters on the root window
        name_label_window = canvas.create_window(800, (100 * circuit_component) + 100, anchor=E,
                                                 window=full_name_labels[circuit_component],
                                                 tags='schematic')

        # Storing all components with their parameters in a dictionary
        all_component_parameters.append(
            {component_name[circuit_component]:
                 {'distribution': component_distribution_array[circuit_component].get('1.0', END).strip('\n'),
                  'parameters': {component_param1_label_array[circuit_component]['text']:
                                     component_param1_array[circuit_component].get('1.0', END).strip('\n'),

                                 component_param2_label_array[circuit_component]['text']:
                                     component_param2_array[circuit_component].get('1.0', END).strip('\n')}
                  }
             }
        )

    print(all_component_parameters)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Function for entering component parameters ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Entering Component Parameters for all elements
def component_parameters():
    global all_component_parameters
    global circuit_components
    print(type(all_component_parameters))
    if len(circuit_components) != 0:
        open_new_window(circuit_components, 0)
    else:
        error_for_not_entering_schematic = \
            canvas.create_window(500, 300,
                                 window=Label(canvas,
                                              text="Please select a schematic first",
                                              width=40,
                                              font=("Courier", 20),
                                              height=40),
                                 tags='Error if schematic not entered')


# Replacing the oval function of tkinter with a simpler function for circles
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


# Function for opening a file
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
                                    text='Please Select Two files, an LTSpice schematic and and image of the schematic'
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
    # canvas.create_image(20, 20, anchor=NW, image=pimg, tags='schematic')

    # TODO: Guess the encoding
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
        # TODO: read the remainder with readlines(encoding=encoding)
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
    global name_label
    # Clear all previous component parameters
    all_component_parameters.clear()

    # Clear all previous drawn wires, components, power flags, voltage sources, etc.
    wires = ''
    canvas_size = ''
    voltage_sources = ''
    components = ''
    power_flags = ''
    # finds the connection wires in the circuit
    for lines in schematic:
        if "WIRE" in lines:
            wires += lines.replace("WIRE ", '')
        if "SHEET" in lines:
            canvas_size += lines.replace("SHEET 1 ", '')
        if "SYMBOL voltage " in lines:
            voltage_sources += lines.replace("SYMBOL voltage ", '')
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
    global circuit_components
    circuit_components = components
    # for component_number in range(len(components)):

    adjustment = 150
    # Draw voltage source/s
    voltage_sources = voltage_sources.split('\n')
    voltage_sources = [voltage for source in voltage_sources for voltage in source.split(' ')]
    # removing anything which has 'R'
    voltage_sources = [x for x in voltage_sources if "R" not in x]
    voltage_sources.pop()
    voltage_sources = [int(sources) for sources in voltage_sources]
    modified_voltage_sources = [modification + adjustment for modification in voltage_sources]

    # Separating Wires
    coordinates_one_line = wires.split('\n')
    coordinates_one_line.remove('')
    single_coordinates = [coordinate for singleCoord in coordinates_one_line for coordinate in singleCoord.split(' ')]
    single_coordinates = [int(coordinate) for coordinate in single_coordinates]
    modified_coordinates = [modification + adjustment for modification in single_coordinates]

    # Separating Power Flags
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

    # -------------------------------------------------Drawing voltage sources------------------------------------------
    drawn_voltage_sources = len(modified_voltage_sources) * [None]
    for vol_sources in range(0, len(modified_voltage_sources), 2):
        if (vol_sources + 1) >= len(modified_voltage_sources):
            drawn_voltage_sources[vol_sources] = canvas.create_circle(modified_voltage_sources[vol_sources - 2],
                                                                      modified_voltage_sources[vol_sources - 1] + 56,
                                                                      40,
                                                                      tags='schematic')
            break
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
    for flag_coordinates in range(0, len(ground_flags), 2):
        canvas.create_polygon(modified_ground_flags[flag_coordinates] - 25, modified_ground_flags[flag_coordinates + 1],
                              modified_ground_flags[flag_coordinates] + 25, modified_ground_flags[flag_coordinates + 1],
                              modified_ground_flags[flag_coordinates], modified_ground_flags[flag_coordinates + 1] + 25,
                              tags='schematic')

    # enter_parameters_window = canvas.create_window(150, 650, anchor=NW, window=enter_parameters_button)

    # --------------------------------------------Binding events--------------------------------------------------------

    # --------------------------------- Making voltage sources change colour when hovered over -------------------------
    ############################# Not yet implemented ##################################################################
    # for vol_elements in drawn_voltage_sources:
    #     canvas.tag_bind(vol_elements, '<Enter>', on_enter)
    #     canvas.tag_bind(vol_elements, '<Leave>', on_leave)


# Select a schematic using a button
openfile_button = ttk.Button(
    root,
    text='Open a Schematic',
    command=get_file_path
)

# Button for entering the parameters of the circuit
enter_parameters_button = ttk.Button(
    root,
    text='Enter All Parameters',
    command=component_parameters
)

value = 0
sketch_graphs(value)
# open file button, tab control and canvas location in root window
openfile_button_window = canvas.create_window(20, 650, anchor=NW, window=openfile_button)
enter_parameters_button.pack(padx=0, pady=10, side=BOTTOM)
openfile_button.pack(padx=0, pady=2, side=BOTTOM)
tabControl.pack(expand=True, fill=BOTH)
canvas.pack(fill=BOTH, expand=True)
# run the application
root.mainloop()
>>>>>>> 7798878 (Made Distribution and components into drop down lists)
