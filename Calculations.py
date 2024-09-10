import statistics
import json
import config
import datetime as dt
import numpy as np


# Removes all commas from a string
def remove_comma(string_in):
    return string_in.replace(",", "")


# Function to finds the values needed in the data for multiplexes over 75m and 2001 onwards
def find_values(data_in, criteria_in):
    entry = []
#   This code is re-written below as it only works in Python 3.10 and above
#    match criteria_in:
#        case 'Height':
#            for item in data_in:
#                # If the Aerial height is more than 75m, we'll look at this one
#                if int(item['Site Height']) > 75:
#                    # Remove the comma that's in the power field
#                    string = remove_comma(item['Power (kW)'])
#                    entry.append(float(string))
#
#        case 'Date':
#            # Set the date for which to look afterwards
#            test_date = dt.datetime(2000, 12, 31)
#            # Note the format of the dates we're receiving
#            date_format = "%d/%m/%Y"
#            for item in data_in:
#                # Convert the date to a format for comparison
#                date_in = dt.datetime.strptime(item['Date'], date_format)
#                # If the date is after 31/12/2000, we'll get the power value
#                if date_in > test_date:
#                    # Remove the comma that's in the power field
#                    string = remove_comma(item['Power (kW)'])
#                    entry.append(float(string))

    if criteria_in == 'Height':
        for item in data_in:
            # If the Site height is more than 75m, we'll look at this one
            if int(item['Site Height']) > 75:
                # Remove the comma that's in the power field
                string = remove_comma(item['Power (kW)'])
                entry.append(float(string))
    else:
        # Set the date for which to look afterwards
        test_date = dt.datetime(2000, 12, 31)
        # Note the format of the dates we're receiving
        date_format = "%d/%m/%Y"
        for item in data_in:
            # Convert the date to a format for comparison
            date_in = dt.datetime.strptime(item['Date'], date_format)
            # If the date is after 31/12/2000, we'll get the power value
            if date_in > test_date:
                # Remove the comma that's in the power field
                string = remove_comma(item['Power (kW)'])
                entry.append(float(string))

    return entry


# Function to get the 3 averages from the data given (criteria is height above 75m or date 2001 onwards)
def averages_get(data_in, criteria_in):
    data = find_values(data_in, criteria_in)
    string_out = "Mean: " + str(round(mean(data), 2))
    string_out = string_out + "\nMedian: " + str(round(median(data), 2))
    string_out = string_out + "\nMode: " + str(round(mode(data), 2))
    return string_out


# Returns the mean of the required values from the data
def mean(data_in):
    return np.mean(data_in)


# Returns the median of the required values from the data
def median(data_in):
    return np.median(data_in)


# Returns the mode of the required values from the data
def mode(data_in):
    return statistics.mode(data_in)


# Returns the site data for client specified multiplexes
# Returns five lots of each site in a list to match up with the 5 Serv Labels that get_station_data will return
def get_site_data(multiplex_in):
    site_list = []
    json_dict = json.loads(config.json_string)

    def site_multiplier(multiplex_in_2):
        nonlocal site_list
        nonlocal json_dict
        for site in json_dict[multiplex_in_2]:
            count = 0
            # Put 5 copies of this site in the list
            while count < 5:
                # If '-1' found, give the label as 'MISSING LABEL'
                if(site['Site']) == '-1':
                    site_list.append('MISSING LABEL')
                else:
                    site_list.append(site['Site'])
                count = count + 1

    site_multiplier(multiplex_in)
    return site_list


# Returns the Station data for the client specified multiplexes
def get_station_data(multiplex_in):
    stations_list = []
    serv_labels = ['Serv Label1 ', 'Serv Label2 ', 'Serv Label3 ', 'Serv Label4 ', 'Serv Label10 ']
    json_dict = json.loads(config.json_string)

    # For each site in the given multiplex...
    for station in json_dict[make_correlation_data_string(multiplex_in)]:
        # ...add the service labels to stations_list
        for label in serv_labels:
            # If '-1' found, give the label as 'MISSING LABEL'
            if(station[label]) == '-1':
                stations_list.append('MISSING LABEL')
            else:
                stations_list.append(station[label])

    return stations_list


# Creates a label for multiplex, frequency and block
def get_labels(multiplex_in):
    json_dict = json.loads(config.json_string)
    freq = json_dict[make_correlation_data_string(multiplex_in)][0]['Freq.']
    # If there was a blank entry denoted by the '-1' change freq to 'MISSING'
    if freq == '-1':
        freq = 'MISSING'
    block = json_dict[make_correlation_data_string(multiplex_in)][0]['Block']
    if block == '-1':
        block = 'MISSING'
    send_string = 'Multiplex: ' + multiplex_in + \
                  ' - Frequency: ' + freq + \
                  'Hz - Block:' + block
    return send_string


# Makes a string to access correlation data from the stored data for the given multiplex
def make_correlation_data_string(multiplex_in):
    return multiplex_in + '_correlation_data'

