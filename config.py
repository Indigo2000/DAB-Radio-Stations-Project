# Global variables are created here
import pandas as pd

# Stings for storing data in json format
json_string = ''
ant_json_string = ''
par_json_string = ''

# DataFrames for ant, par and CurrentState data
cleaned_ant_data = pd.DataFrame()
cleaned_par_data = pd.DataFrame()

# DataFrames for correlation
mult1_vs_mult2_df = pd.DataFrame()
mult1_df = pd.DataFrame()
mult2_df = pd.DataFrame()

# These are the variables showing which fields the client has expressed interest in seeing
# Individual entries can be added to or removed.
# These are for the grouping with the NGR field
desired_grp_ant_fields = ('NGR', 'Site Height', 'In-Use Ae Ht', 'In-Use ERP Total')
desired_grp_par_fields = ('Site', 'Date')
# These are for the correlation analysis
desired_cor_par_fields = ('Site', 'Freq.', 'Block', 'Serv Label1 ', 'Serv Label2 ', 'Serv Label3 ', 'Serv Label4 ',
                          'Serv Label10 ')
desired_cor_ant_fields = ()
# This is for the multiplexes requested
desired_multiplexes = ['C18A', 'C18F', 'C188']

editable_ant_fields = ('id', 'NGR', 'Site Height', 'In-Use Ae Ht', 'In-Use ERP Total')
editable_par_fields = ('id', 'Site', 'Freq.', 'Block', 'Serv Label1 ', 'Serv Label2 ', 'Serv Label3 ', 'Serv Label4 ',
                       'Serv Label10 ')

# These are the NGR fields to ignore
ignore_NGR_fields = ('NZ02553847', 'SE213515', 'NT05399374', 'NT25265908')

display_value = 0

