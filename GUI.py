import json
import Plot
import tkinter as tk
import json_handling
from tkinter import filedialog
import csv_handling
import config
import Calculations
import pandas as pd
from tkinter import ttk


# Gets the user to select the TxAntennaDAB.csv file
def get_ant_csv():
    data = []
    print("Asking user for TxAntennaDAB.csv file")
    test = False
    while test == False:
        message_box("Select TxAntennaDAB.csv file")
        ant_file = filedialog.askopenfilename(initialdir=".", title="Select TxAntennaDAB.csv file",
                                              filetypes=(("csv files",
                                                          "*.csv*"),
                                                         ("all files",
                                                          "*.*")))
        data = csv_handling.import_csv(ant_file)
        # Abort if no file was found - cancel button was pressed
        if data == 'CANCEL':
            print("User cancelled.")
            test = True
        else:
            test = csv_handling.csv_check(data, 'NGR')
            if test == False:
                print("Informed user that data is not in correct format. Prompting for file again")
    return data


# Asks user to select TxParamsDAB.csv file
def get_par_csv():
    data = []
    print("Asking user for TxParamsDAB.csv file")
    test = False
    while test == False:
        message_box("Select TxParamsDAB.csv file")
        par_file = filedialog.askopenfilename(initialdir=".", title="Select TxParamsDAB.csv file",
                                              filetypes=(("csv files",
                                                          "*.csv*"),
                                                         ("all files",
                                                          "*.*")))

        data = csv_handling.import_csv(par_file)
        # Abort if no file was found - cancel button was pressed
        if data == 'CANCEL':
            test = True
            print("User cancelled.")
        else:
            test = csv_handling.csv_check(data, 'Date')
            if test == False:
                print("Informed user that data is not in correct format. Prompting for file again")
    return data


# Gets csv files and converts to json
def load_csvs_gui(self):
    # Get the data for TxAntennaDAB
    ant_data = get_ant_csv()
    # If retrieval of TxAntennaDAB gets cancelled, don't get the other file
    if ant_data != 'CANCEL':
        # Get the data for TxParamsDAB
        par_data = get_par_csv()
        # If TxParamsDAB doesn't get cancelled...
        if par_data != 'CANCEL':
            # Make a progress bar
            progressbar = ttk.Progressbar(self, mode="indeterminate")
            progressbar.grid(column=0, row=0)
            progressbar.start(5)
            self.update()
            # Export full, clean backup to TxAntennaDAB.json, TxParamsDAB.json and CurrentState.json
            csv_handling.export_jsons(ant_data, par_data)
            # Get rid of the progress bar
            progressbar.destroy()
            message_box("Data imported successfully.")

    self.destroy()
    main_win()


# Message box, click OK to close
def message_box(text_in):
    # Create a message box
    message_win = tk.Tk()
    message_win.title("Message")

    # Display the message box
    message_win.geometry("400x100")
    message_win.label = tk.Label(message_win, text=text_in + "\n", font="Helvetica 10", wraplength=300, justify="left")
    message_win.label.pack()
    message_win.button = tk.Button(message_win, text="OK", command=message_win.quit)
    message_win.button.pack()
    message_win.mainloop()
    message_win.destroy()


# Displays a splash screen on launch
def splash():
    #global progressbar
    # Create splash screen object
    splash_screen = tk.Tk()

    # Adjust size
    splash_screen.geometry("200x200")
    splash_screen.overrideredirect(True)
    # Set Label
    splash_label = tk.Label(splash_screen, text="Splash Screen", font=18)
    splash_label.pack()
    # Run loading files info
    splash_message = tk.Message(splash_screen, text="Loading data...", font=10)
    splash_message.pack()
    progressbar = ttk.Progressbar(splash_screen, mode="indeterminate")
    progressbar.start(10)
    progressbar.pack()

    splash_screen.update()

    print("Splash Screen on display")
    # Check for current State file
    if json_handling.load_current_state_at_launch() == False:
        message_box("Unable to load CurrentState.json from backup, please import data using the import function.")
        progressbar.stop()
        splash_screen.destroy()
    # Check for full backup TxAntennaDAB.json file
    elif json_handling.load_ant_at_launch() == False:
        message_box("Unable to load TxAntennaDAB.jsom from backup, please import data using the import function.")
        progressbar.stop()
        splash_screen.destroy()
    # Check for full backup TxAntennaDAB.json file
    elif json_handling.load_par_at_launch() == False:
        message_box("Unable to load TxParamsDAB.json from backup, please import data using the import function.")
        progressbar.stop()
        splash_screen.destroy()
    else:
        # Write to data frames for cleaned_ant_data, and cleaned_par_data
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        config.cleaned_ant_data = pd.read_json(config.ant_json_string)
        config.cleaned_par_data = pd.read_json(config.par_json_string, convert_dates=False)
        # Load the stored view:
        json_dict = json.loads(config.json_string)
        try:
            config.display_value = json_dict["View"][0]["Current View"]
        except KeyError:
            print("Unable to load last stored view. Default view will be displayed.")
            message_box("Unable to load last stored view. Default view will be displayed.")
        print("Load at launch worked, destroying the splash")
        progressbar.stop()
        # Destroy the splash screen
        splash_screen.destroy()
    splash_screen.mainloop()
    main_win()


# Informs user this will be implemented in the future
def future_implementation():
    print("This could be implemented in the future.")
    message_box("This could be implemented in the future.")


# Prompt user for id of info they want to change
def prompt_for_id():
    id_send = ''
    test = False

    # Check to see if the id is in the ant DataFrame (will also be in par)
    def test_id(id_in):
        is_in = False
        # Check for both ints and string values of id_in
        if int(id_in) in config.cleaned_ant_data['id'].unique():
            is_in = True
        elif id_in in config.cleaned_ant_data['id'].unique():
            is_in = True
        return is_in

    # Get the text from the field and close the message box
    def get_text():
        nonlocal id_send
        nonlocal test
        id_send = text.get()
        if test_id(id_send) == False:
            message_box("Invalid ID! Please try again.")
        else:
            test = True
            prompt_win.quit()

    while test == False:
        # Create a message box
        prompt_win = tk.Tk()
        prompt_win.title("Prompt for ID")

        # Display the message box
        prompt_win.geometry("400x100")
        prompt_win.label = tk.Label(prompt_win, text="Enter ID for which to change values: " + "\n", font="Helvetica 10",
                                    wraplength=300, justify="left")
        prompt_win.label.pack()

        # Set up entry field
        text = tk.Entry(prompt_win, bd=3)
        text.pack()

        # Create Done button
        prompt_win.button = tk.Button(prompt_win, text="Done", command=get_text)
        prompt_win.button.pack()

        # Run the window
        prompt_win.mainloop()
        prompt_win.destroy()



    return id_send


# creates dictionaries of ant data and par data to use for csvhandling export jsons
# It uses json string to know which info to look at from each of cleaned_ant data and cleaned_par data
def user_edit():
    # Set up lists for handling the data
    ant_change_list = []
    par_change_list = []
    ant_change_data = []
    par_change_data = []

    # Set up list of 2 lists for ant_change_data and par_change_data
    temp_list_1 = []
    temp_list_2 = []
    ant_change_data.append(temp_list_1)
    ant_change_data.append(temp_list_2)
    par_change_data.append(temp_list_1)
    par_change_data.append(temp_list_2)

    # Prompt user for id of entry they wish to change
    id_for_change = prompt_for_id()
    # Get the data for that site
    ant_for_change = json_handling.get_for_edit(id_for_change, config.cleaned_ant_data, 'ant')
    par_for_change = json_handling.get_for_edit(id_for_change, config.cleaned_par_data, 'par')

    #Create the edit window
    edit_win = tk.Tk()
    edit_win.title("Edit window")
    edit_win.geometry("300x400")  # set starting size of window
    edit_win.maxsize(300, 400)  # width x height
    edit_win.config(bg="lightgrey")

    # Set up tabs
    tab_control = ttk.Notebook(edit_win)
    # One for TxAntennaDab, one for TxParamsDAB
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='TxAntennaDAB')
    tab_control.add(tab2, text='TxParamsDAB')
    tab_control.pack(expand=1, fill="both")

   # Create a 'Done' button
    edit_win.button = tk.Button(edit_win, text="Done", command=edit_win.quit)
    edit_win.button.pack()

    # Add a canvas in both tabs
    canvas1 = tk.Canvas(tab1, bg="lightgrey")
    canvas1.grid(row=0, column=0, sticky="news")
    canvas2 = tk.Canvas(tab2, bg="lightgrey")
    canvas2.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to each canvas
    vsb1 = tk.Scrollbar(tab1, orient="vertical", command=canvas1.yview)
    vsb1.grid(row=0, column=2, sticky='ns')
    canvas1.configure(yscrollcommand=vsb1.set)
    vsb2 = tk.Scrollbar(tab2, orient="vertical", command=canvas2.yview)
    vsb2.grid(row=0, column=2, sticky='ns')
    canvas2.configure(yscrollcommand=vsb2.set)
    # Create titles for each tab
    enter_ant = tk.Label(canvas1, text="Please enter information for entry with id: " + str(ant_for_change[1][0]),
                          bg="lightgrey")
    enter_ant.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

    enter_par = tk.Label(canvas2, text="Please enter information for entry with id: " + str(par_for_change[1][0]),
                          bg="lightgrey")
    enter_par.grid(row=0, column=1, columnspan=4, padx=5, pady=5)
    # create entry fields, variables and labels for ant_data
    count = 0
    # Create an empty line for spacing
    tk.Label(canvas1, text='', bg="lightgrey").grid(row=count + 1, column=1, padx=5, pady=5, sticky='E')
    for item in ant_for_change[0]:
        # Don't create an entry for id
        if item != 'id':
            # Change for Aerial height
            if item == 'In-Use Ae Ht':
                tk.Label(canvas1, text='Aerial height(m)', bg="lightgrey").grid(row=count + 2, column=1, padx=5,
                                                                                pady=5, sticky='E')
            # Change for Power
            elif item == 'In-Use ERP Total':
                tk.Label(canvas1, text='Power(kW)', bg="lightgrey").grid(row=count + 2, column=1, padx=5, pady=5,
                                                                         sticky='E')
            else:
                tk.Label(canvas1, text=item, bg="lightgrey").grid(row=count + 2, column=1, padx=5, pady=5, sticky='E')
            # If we have a -1 entry, switch it to blank
            if ant_for_change[1][count] == -1:
                value = ''
            else:
                value = ant_for_change[1][count]
            # Set up entry field
            entry = tk.Entry(canvas1, bd=3)
            entry.grid(row=count + 2, column=2, padx=5, pady=5)
            entry.insert(0, value)
            ant_change_list.append(entry)
        else:
            # Create a placeholder for id entry but don't display it
            entry = tk.Entry(canvas1, bd=3)
            entry.insert(0, ant_for_change[1][count])
            ant_change_list.append(entry)
        count = count + 1

    # create entry fields, variables and labels for par_data
    count = 0
    # Create an empty line for spacing
    tk.Label(canvas2, text='', bg="lightgrey").grid(row=count + 1, column=1, padx=5, pady=5, sticky='E')
    for item in par_for_change[0]:
        # Don't create an entry for id
        if item != 'id':
            # Display label
            tk.Label(canvas2, text=item, bg="lightgrey").grid(row=count + 2, column=1, padx=5, pady=5, sticky='E')
            # If we have a -1 entry, switch it to blank
            if par_for_change[1][count] == -1:
                value = ''
            else:
                value = par_for_change[1][count]
            # Set up entry field
            entry = tk.Entry(canvas2, bd=3)
            entry.grid(row=count + 2, column=2, padx=5, pady=5)
            entry.insert(0, value)
            par_change_list.append(entry)
        else:
            # Create a placeholder for id entry but don't display it
            entry = tk.Entry(canvas2, bd=3)
            entry.insert(0, par_for_change[1][count])
            par_change_list.append(entry)
        count = count + 1

    # Run the edit window
    edit_win.mainloop()

    # Get the values entered by the user
    for field, entry in zip(ant_for_change[0], ant_change_list):
        ant_change_data[0].append(field)
        ant_change_data[1].append(entry.get())

    # Get the values entered by the user
    for field, entry in zip(par_for_change[0], par_change_list):
        par_change_data[0].append(field)
        par_change_data[1].append(entry.get())

    # Get rid of the window
    edit_win.destroy()
    #print(ant_change_data)
    # Reassemble dictionaries for ant and par and re-write all data via json_handling.import_data
    ant_data = json_handling.change_entry(id_for_change, ant_change_data, config.cleaned_ant_data,
                                          config.editable_ant_fields)
    print("Done Ant")
    par_data = json_handling.change_entry(id_for_change, par_change_data, config.cleaned_par_data,
                                          config.editable_par_fields)
    csv_handling.export_jsons(ant_data, par_data)


# Class for the main window
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # List to store all labels in left column
        self.l_column_label = []

        # Initialise a blank subtitle
        self.subtitle = tk.Label(self, text='',
                                 font=('Helvetica', 18), fg="red", anchor="center")

        # Create the menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Variable for determining radiobutton selection in display menu
        disp_var = tk.StringVar()

        self.title("Main Window")
        # Calculate screen width for padding purposes
        screen_width = self.winfo_screenwidth()
        # Set to fill the screen
        self.state('zoomed')

        # Functions for performing operations when the buttons are pressed:
        # import from csvs response
        def import_csvs():
            load_csvs_gui(self)

        # Heatmap 1 button response
        def heat_1():
            # Change main title
            self.subtitle.destroy()
            self.subtitle = tk.Label(self, text='Heatmap showing the correlation for service labels on the '
                                     'selected multiplexes', font=('Helvetica', 18), fg="red", anchor="center")
            self.subtitle.grid(row=0, column=0, columnspan=3, padx=screen_width / 100)
            Plot.plot_heat_1(self)
            # Update the display menu radio buttons
            disp_var.set('1')
            menubar.update()
            # Update the key
            display_heatmap_ledger(config.desired_multiplexes[0], config.desired_multiplexes[1])
            # Update stored display value
            config.display_value = 1

        # Heatmap 2 button response
        def heat_2():

            # Change main title
            self.subtitle.destroy()
            self.subtitle = tk.Label(self, text='Heatmap showing the correlation for service labels on the '
                                     'selected multiplexes', font=('Helvetica', 18), fg="red", anchor="center")
            self.subtitle.grid(row=0, column=0, columnspan=3, padx=screen_width / 100)
            Plot.plot_heat_2(self)
            # Update the display menu radio buttons
            disp_var.set('2')
            menubar.update()
            # Update the key
            display_heatmap_ledger(config.desired_multiplexes[0], config.desired_multiplexes[2])
            # Update stored display value
            config.display_value = 2

        # Heatmap 2 button response
        def heat_3():
            # Change main title
            self.subtitle.destroy()
            self.subtitle = tk.Label(self, text='Heatmap showing the correlation for service labels on the '
                                     'selected multiplexes', font=('Helvetica', 18), fg="red", anchor="center")
            self.subtitle.grid(row=0, column=0, columnspan=3, padx=screen_width / 100)
            Plot.plot_heat_3(self)
            # Update the display menu radio buttons
            disp_var.set('3')
            menubar.update()
            # Update the key
            display_heatmap_ledger(config.desired_multiplexes[1], config.desired_multiplexes[2])
            # Update stored display value
            config.display_value = 3

        # Display all data response
        def scatter():
            # Change main title
            self.subtitle.destroy()
            self.subtitle = tk.Label(self, text='Chart showing service labels and sites for different multiplexes',
                                     font=('Helvetica', 18), fg="red", anchor="center")
            self.subtitle.grid(row=0, column=0, columnspan=3, padx=screen_width / 100)
            # Show the graph
            Plot.plot_scatter(self)

            # Destroy old info in left column
            clear_left_column()
            # Display the averages
            self.l_column_label.append(tk.Label(self, text="Averages for power\nfor chosen multiplexes",
                                       font=('Helvetica', 10), fg="red", justify='left'))
            self.l_column_label[0].grid(row=1, column=0, padx=screen_width / 40)

            # Gather data to collate averages
            data = []
            for item in config.desired_multiplexes:
                data.extend(json_handling.convert_to_dict()[item])

            # Display the average for height
            self.l_column_label.append(tk.Label(self, text="Sites above 75m\n(in Kw to 2 decimal places):",
                                                font=('Helvetica', 10), fg="red", justify='left'))
            self.l_column_label[1].grid(row=2, column=0, padx=screen_width / 40)
            display_averages(data, 3, 'Height')

            # Display the average for date
            self.l_column_label.append(tk.Label(self, text="Dates 2001 onwards\n(in Kw to 2 decimal places):",
                                                font=('Helvetica', 10), fg="red", justify='left'))
            self.l_column_label[3].grid(row=4, column=0, padx=screen_width / 40)
            display_averages(data, 5, 'Date')

            # Update the display menu radio buttons
            disp_var.set('0')
            menubar.update()
            # Update stored display value
            config.display_value = 0

        # Function to display and calculate averages
        def display_averages(data_in, row_in, criteria):
            # Get the averages and write them as a label
            self.l_column_label.append(tk.Label(self, text=Calculations.averages_get(data_in, criteria), justify='left'))
            self.l_column_label[row_in-1].grid(row=row_in, column=0)

        # Function to display and calculate averages
        def display_heatmap_ledger(mult_in_1, mult_in_2):
            # Clear the left column ready for the new data
            clear_left_column()

            # Create header for mult_1 service labels
            self.l_column_label.append(tk.Label(self, text="Service label information\nfor " + mult_in_1 + ":",
                                       font=('Helvetica', 10), fg="red", justify='left'))
            self.l_column_label[0].grid(row=1, column=0, padx=screen_width / 40)

            def is_missing(data_in):
                if data_in == '-1':
                    return 'MISSING LABEL'
                else:
                    return data_in

            # Create text for mult_in_1 label
            mult_1_text = "SL1   -  " + config.mult1_df.iloc[0]['Serv Label1 ']
            mult_1_text = mult_1_text + "\nSL2   -  " + is_missing(config.mult1_df.iloc[0]['Serv Label2 '])
            mult_1_text = mult_1_text + "\nSL3   -  " + is_missing(config.mult1_df.iloc[0]['Serv Label3 '])
            mult_1_text = mult_1_text + "\nSL4   -  " + is_missing(config.mult1_df.iloc[0]['Serv Label4 '])
            mult_1_text = mult_1_text + "\nSL10 -  " + is_missing(config.mult1_df.iloc[0]['Serv Label10 '])
            # Display the label
            self.l_column_label.append(tk.Label(self, text=mult_1_text, font=('Helvetica', 10),
                                                justify='left'))
            self.l_column_label[1].grid(row=2, column=0, padx=screen_width / 40)

            # Create header for mult_2 service labels
            self.l_column_label.append(tk.Label(self, text="Service label information\nfor " + mult_in_2 + ":",
                                                font=('Helvetica', 10), fg="red", justify='left'))
            self.l_column_label[2].grid(row=3, column=0, padx=screen_width / 40)

            # Create text for mult_in_2 label
            mult_2_text = "SL1   - " + is_missing(config.mult2_df.iloc[0]['Serv Label1 '])
            mult_2_text = mult_2_text +  "\nSL2   - " + is_missing(config.mult2_df.iloc[0]['Serv Label2 '])
            mult_2_text = mult_2_text +  "\nSL3   - " + is_missing(config.mult2_df.iloc[0]['Serv Label3 '])
            mult_2_text = mult_2_text +  "\nSL4   - " + is_missing(config.mult2_df.iloc[0]['Serv Label4 '])
            mult_2_text = mult_2_text +  "\nSL10 - " + is_missing(config.mult2_df.iloc[0]['Serv Label10 '])
            # Display the label
            self.l_column_label.append(tk.Label(self, text=mult_2_text, font=('Helvetica', 10),
                                                justify='left'))
            self.l_column_label[3].grid(row=4, column=0, padx=screen_width / 40)

        def clear_left_column():
            for item in self.l_column_label:
                item.destroy()
            # Now clear the list
            self.l_column_label.clear()

        def load_csvs():
            load_csvs_gui(self)

        def user_edit_launch():
            # Get the changes
            user_edit()
            # Re-draw graph
            select_graph(config.display_value)

        def select_graph(graph_in):
            # This code has been re-written below as match is only supported in python 3.10
            #            match graph:
            #                case 0: scatter()
            #                case 1: heat_1()
            #                case 2: heat_2()
            #                case 3: heat_3()
            #                case _: message_box('Error loading graph! Try importing from csv.')
            if graph_in == 0:
                scatter()
            elif graph == 1:
                heat_1()
            elif graph == 2:
                heat_2()
            elif graph == 3:
                heat_3()
            else:
                message_box('Error loading graph! Try importing from csv.')

        # Button creation
        buttons_header = tk.Label(self, text="Control buttons",
                                  font=('Helvetica', 10), fg="red", justify='left')
        buttons_header.grid(row=1, column=2, padx=screen_width / 40)

        # Import csvs button
        import_button = tk.Button(self, text="Import Data from csv", command=import_csvs)
        import_button.grid(row=2, column=2, padx=screen_width / 100)

        # Display multiplex info button
        mult_button = tk.Button(self, text='All multiplex information', command=scatter)
        mult_button.grid(row=3, column=2, padx=screen_width / 100)

        # Create correlation button 1
        c_button_1_text = config.desired_multiplexes[0] + ' correlation with ' + config.desired_multiplexes[1]
        change_button_1 = tk.Button(self, text=c_button_1_text, command=heat_1)
        change_button_1.grid(row=4, column=2, padx=screen_width / 100)

        # Create correlation button 2
        c_button_2_text = config.desired_multiplexes[0] + ' correlation with ' + config.desired_multiplexes[2]
        change_button_2 = tk.Button(self, text=c_button_2_text, command=heat_2)
        change_button_2.grid(row=5, column=2, padx=screen_width / 100)

        # Create correlation button 3
        c_button_3_text = config.desired_multiplexes[1] + ' correlation with ' + config.desired_multiplexes[2]
        change_button_3 = tk.Button(self, text=c_button_3_text, command=heat_3)
        change_button_3.grid(row=6, column=2, padx=screen_width / 100)

        # Create modify data button
        modify_button = tk.Button(self, text="Change Data", command=user_edit_launch)
        modify_button.grid(row=7, column=2, padx=screen_width / 100)

        # If we have data to work with, display the averages and graphs
        if config.json_string != []:
            # Show the graph last viewed when program closed
            graph = config.display_value
            select_graph(graph)

        else:
            error_label = tk.Label(self, text='Unable to display data, please import from csv')
            error_label.grid(row=2, column=0)
            Plot.plot_blank(self)
            # Put the blank chart here*****************************************************************************************************

        # Configure the file menu *************************************************
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label='Change data',
            command=user_edit,
        )
        file_menu.add_command(
            label='Import data',
            command=load_csvs,
        )
        file_menu.add_command(
            label='Exit',
            command=self.destroy,
        )
        menubar.add_cascade(
            label="File",
            menu=file_menu,
            underline=0
        )

        # Configure the display menu **********************************************
        display_menu = tk.Menu(menubar, tearoff=0)

        # Change the display if a display menu item was selected
        def display_button_pressed():
            option = disp_var.get()
#       This code has been re-written below as it only works in python 3.10 and above
#            match option:
#                case '0':
#                    scatter()
#                case '1':
#                    heat_1()
#                    display_value = 1
#                case '2':
#                    heat_2()
#                    display_value = 2
#                case '3':
#                    heat_3()
#                    display_value = 3
#                case _:
#                    message_box('No such option exists!')

            if option == '0':
                scatter()
                # config.display_value is set to 0 in the scatter function
            elif option == '1':
                heat_1()
                config.display_value = 1
            elif option == '2':
                heat_2()
                config.display_value = 2
            elif option == '3':
                heat_3()
                config.display_value = 3
            else:
                message_box('No such option exists!')

        # Add radio buttons for each of the desired views to the display menu
        # Show all multiplex data
        display_menu.add_radiobutton(
            label='Show all multiplex data',
            command=display_button_pressed,
            variable=disp_var,
            value=0
        )

        # Create radio buttons for all combinations of multiplexes to view correlations
        counter_a = 0
        for line in config.desired_multiplexes:
            for counter_b in range (1, len(config.desired_multiplexes)):
                if line != config.desired_multiplexes[counter_b]:
                    if counter_b > counter_a:
                        display_menu.add_radiobutton(
                            label=line + ' correlation with ' + config.desired_multiplexes[counter_b],
                            command=display_button_pressed,
                            variable=disp_var,
                            value=str(counter_a+counter_b)
                        )
            counter_a = counter_a + 1
        disp_var.set(str(config.display_value))
        menubar.add_cascade(
            label="Display",
            menu=display_menu,
            underline=0
        )

        # Configure the help menu *************************************************
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label='Tips',
            command=user_edit,
        )
        help_menu.add_command(
            label='About',
            command=future_implementation,
        )
        menubar.add_cascade(
            label="Help",
            menu=help_menu,
            underline=0
        )


# Function to launch the main window
def main_win():
    app = App()
    print("Main window on display")
    app.mainloop()


