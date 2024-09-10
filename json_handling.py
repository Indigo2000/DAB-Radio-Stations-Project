import json
import config
import ast


# Load json files upon program launch if available, otherwise load csvs
def load_current_state_at_launch():
    print("Loading data...")
    config.json_string = import_json('CurrentState.json')
    if config.json_string == []:
        return False
    else:
        return True


# Load json files upon program launch if available, otherwise load csvs
def load_ant_at_launch():

    print("Loading data...")
    config.ant_json_string = import_json('TxAntennaDAB.json')
    if config.ant_json_string == []:
        return False
    else:
        return True


# Load json files upon program launch if available, otherwise load csvs
def load_par_at_launch():

    print("Loading data...")
    config.par_json_string = import_json('TxParamsDAB.json')
    if config.par_json_string == []:
        return False
    else:
        return True


# For converting csv data to client required data
def import_data(ant_data_in, par_data_in):

    # Setup json strings in required format
    config.json_string = '{'
    for line in config.desired_multiplexes:
        # Add the data to be grouped with NGR values
        config.json_string = config.json_string + '\"' + line + '\": ['
        config.json_string = config.json_string + (group_data(ant_data_in, par_data_in, line,
                                                   config.desired_grp_ant_fields, config.desired_grp_par_fields))
        config.json_string = config.json_string + '],\n'
        # Add the data for correlation
        config.json_string = config.json_string + '\"' + line + '_correlation_data\": ['
        config.json_string = config.json_string + (group_data(ant_data_in, par_data_in, line,
                                                   config.desired_cor_ant_fields, config.desired_cor_par_fields))
        config.json_string = config.json_string + '],\n'
    # remove final comma and add newline and bracket
    config.json_string = config.json_string[:len(config.json_string) - 2] + '\n}'
    # Write to file
    json_to_file('CurrentState.json', config.json_string)


# Groups data into format required by client and returns a string in json format
def group_data(ant_data_in, par_data_in, EID_in, desired_grp_ant_fields_in, desired_grp_par_fields_in):
    string = '\n'
    print("\nGrouping data for", EID_in)
    for par_line in par_data_in:
        # Look for required EID
        if (par_line.get('EID') == EID_in):
            # Use 'id' to find corresponding entry from ant_data_in
            current_id = par_line.get('id')
            # Find the corresponding entry in ant_data_in
            for ant_line in ant_data_in:
                # Find the matching id
                if ant_line.get('id') == current_id:
                    # Check if we can disregard this due to NGR value
                    write_field = True
                    for NGR_line in config.ignore_NGR_fields:
                        if ant_line.get('NGR') == NGR_line:
                            print("Skipping NGR value", (ant_line.get('NGR')), "for EID", EID_in, "- not required.")
                            write_field = False
                    # Write the data for this field if we're not skipping due to NGR field
                    if write_field:
                        # All checks complete, assemble the string
                        string = string + '{\n '
                        # Put the data together from par_data
                        for grp_par_line in desired_grp_par_fields_in:
                            string = string + '\"' + grp_par_line + '\": \"' + par_line.get(grp_par_line) + '\",\n'
                        # Put the data together for ant_data, renaming the required fields
                        for grp_ant_line in desired_grp_ant_fields_in:
                            if grp_ant_line == 'In-Use Ae Ht':
                                string = string + '\"Aerial height (m)\": \"' + ant_line.get(grp_ant_line) + '\",\n'
                            elif grp_ant_line == 'In-Use ERP Total':
                                string = string + '\"Power (kW)\": \"' + ant_line.get(grp_ant_line) + '\",\n'
                            else:
                                string = string + '\"' + grp_ant_line + '\": \"' + ant_line.get(grp_ant_line) + '\",\n'
                        # remove final comma and add newline
                        string = string[:len(string) - 2] + '\n'
                        string = string + '},\n'
                    # Once matching ant_line id found, no need to check the rest
                    break
    # remove final comma and add newline
    string = string[:len(string) - 2] + '\n'
    return string


# Imports a json file
def import_json(file_name):
    print("Opening file", file_name, end="...")
    try:
        file = open(file_name)
        list_data = json.load(file)
        print("...done")
        file.close()
        return json.dumps(list_data, sort_keys=True, indent=2)
    except FileNotFoundError:
        list_data = []
        print("Error reading", file_name)
    return list_data


# Writes a string in json format to file
def json_to_file(file_name, data_in):
    print("Writing to file", file_name, end="...")
    file = open(file_name, 'w', encoding='utf-8')
    print(f"{data_in}", file=file)
    file.close()
    print("...done")


# Convert json string into Python readable dictionary
def convert_to_dict():
    return json.loads(config.json_string)


# Returns a list of lists client required variable for editing
# Format is list one: Fields, list two: Current value
def get_for_edit(id_in, df_in, ant_or_par):
    # Initialise list of 2 lists for returning data
    entry_list = []
    list_1 = []
    list_2 = []
    entry_list.append(list_1)
    entry_list.append(list_2)

    # Check either ints or strings
    try:
        df_id = df_in.set_index('id').index.get_loc(id_in)
    except KeyError:
        df_id = df_in.set_index('id').index.get_loc(int(id_in))

    # Check if it's ant or par data needed
    if ant_or_par == 'ant':
        for item in config.editable_ant_fields:
            entry_list[0].append(item)
            entry_list[1].append(df_in.at[df_id, item])
    else:
        for item in config.editable_par_fields:
            entry_list[0].append(item)
            entry_list[1].append(df_in.at[df_id, item])
    return entry_list


# Takes a list of values edited by the user and returns ALL the data as a dictionary ready to write to file
def change_entry(id_in, change_list, df_in, edits_in):
    # Convert the id to the entry in the dataframe

    new_frame = df_in.copy()
    # Find the dataframe's row number for this id
    # Check either ints or strings
    try:
        df_id = new_frame.set_index('id').index.get_loc(id_in)
    except KeyError:
        df_id = new_frame.set_index('id').index.get_loc(int(id_in))
    # Replace this row in the dataframe with the values user edited
    count = 0
    for item in change_list[0]:
        # Don't change id fields
        if item == 'id':
            pass
        else:
            for entry in edits_in:
                if item == entry:
                    new_frame.at[df_id, item] = change_list[1][count]
        count = count + 1
    # Put the datframe into a dictionary ready to import back into program and write to file.
    return new_frame.to_dict(orient="list")