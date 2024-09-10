import json
import ast
import GUI
import csv
import json_handling
import pandas as pd
import config


# Prompt user for csv files
def csv_check(data_in, field_check):
    check = False
    data = data_in

    if data == []:
        GUI.message_box("No data found, please try again.")
    else:
        if data[0].get(field_check) == None:
            GUI.message_box("csv file not in correct format. Please try again.")
        else:
            check = True
    return check


# Converts data from csv file to a list
def data_to_list(data_in):
    all_data = []
    # Look through each line and put it into a list
    for line in data_in:
        all_data.append(line)
    return all_data


# Import csv files - returns a list of dictionaries, one for each entry
def import_csv(file_name):
    print("Opening file", file_name, end="...")
    try:
        with open(file_name, newline='') as file:
            data = csv.DictReader(file)
            list_data = data_to_list(data)
            print("...done")
            return list_data
    except FileNotFoundError:
        print("Error reading file")
        list_data = 'CANCEL'
    return list_data


# Exports all data and current state to json format files and creates variables for the data
def export_jsons(ant_data_in, par_data_in):
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # Write the ant_data to a DataFrame and to file
    ant_df = pd.DataFrame(ant_data_in)
    config.cleaned_ant_data = data_clean(ant_df.astype(str))
    print("Writing to file TxAntennaDAB.json...", end="")
    config.cleaned_ant_data.to_json(path_or_buf="TxAntennaDAB.json", orient="records")
    print("...done")

    # Write the par_data to a DataFrame and to file
    par_df = pd.DataFrame(par_data_in)
    config.cleaned_par_data = data_clean(par_df.astype(str))
    print("Writing to file TxParamsDAB.json...", end="")
    config.cleaned_par_data.to_json(path_or_buf="TxParamsDAB.json", orient="records")
    print("...done")

    # Convert the cleaned par and ant data back to lists and store as current state
    print("\nGrouping data as per client requirements and writing to CurrentState.json")
    ant_list = ast.literal_eval(config.cleaned_ant_data.to_json(orient="records"))
    par_list = ast.literal_eval(config.cleaned_par_data.to_json(orient="records"))
    json_handling.import_data(ant_list, par_list)


# Clean the data provided
def data_clean(data_in):
    print("Cleaning data...")
    # Fill any blank values with -1 so that negative values in calculations can be identified as having come
    # from missing data
    data_to_return = data_in.fillna(-1)
    # Replace empty strings with ("-1") for the same reasons as above
    data_to_return = data_to_return.replace("", "-1")
    # Truncate very long labels that would interfere with diagrams
    for column in data_to_return:
        data_to_return[column] = data_to_return[column].str.slice(stop=20)
    return data_to_return


