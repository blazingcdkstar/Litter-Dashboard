'''
Overall Process

Step 1: Import packages and create base columns variable.
Step 2: Import and formate data
Step 3: Create dataframe named litter_base with id vars
Step 4: Reshape data from wide to long, so that a unique record is the combination of the id and the item. 
        1 id is tied to 1 photo, and a photo can include more than 1 litter.

        a. Create data frame to capture the custom tag items. 
            - the custom tag columns contain column headers, not values, so this has to be reshaped 
              separately, and then added back to the dataframe at the end. I only do this for custom_tag_1. The dataframe
              will have columns: 'id', 'main_category', 'sub_category', and 'value'.
        
        b. Identify the column headers that are in all upper case. These are dummy columns to identify the main categorization
           of the litter item, they contain no data. Create a new dataframe for each main category with columns: 'id', 'main_category', 
           'sub_category', and 'value'. 
           The main categories are:  'alcohol', 'coffee', 'food', 'industrial', 'other', 'sanitary', 'softdrinks'

           

Step 5: Reshape address column. The address column is 1 long string with address components separated by commas. 
        I split out each component of the address field into separate columns. There are some irregularities with this data. For example,
        some records have place names rather than the street address, or some have a neighborhood designation and others do not. To facilitate
        litter by street block aggregation, I replace the place names with the street address. I remove the neighborhood designations so 
        that all addresses have the same number of components. After these steps there are addresses with 5 or 6 components. For those with 
        5 components are missing a house number. I add the column and fill with 0. This data is brought back together and then joined
        with the base data.

Exclusions:
I exclude the columns for brand and material identification. I have not done this identification with my data.

Variance:
There is a small variance between the sum of the total column in the raw data and the sum total in my final output.
This is because there is not a value in the total column in the raw data for items that are categorized in the custom_tag_1 column,
and because there are a handful of items where there is a flag for the item and for the material, and these
are getting double counted in the total column in the raw data, but they are counted once in my output.

Variance Examples:
ID 449030 is counted twice, as a straw and as plastic in the raw source data.
ID 459532 is custom tagged as a hair net, and has no value in the total column in the raw source data.

'''
#%%
#######################################################                             ############################################################
####################################################### < Step 1: Import Packages > ############################################################
#######################################################                             ############################################################

#%% Import Packages

# Data packages
import pandas as pd
import numpy as np
import gc

# graphing packages
import plotly.express as px
import matplotlib.pyplot as plt

# create list of main base columns in dataset
base_columns = ['id', 'verification','phone', 'date_taken', 'date_taken_date', 'date_taken_yrmth',
                'date_uploaded', 'lat', 'lon', 'picked up', 'address']

#%%
######################################################                         #################################################################
###################################################### < Step 2: Import Data > #################################################################
######################################################                         #################################################################

#%% Import Data
litter = pd.read_csv('Data\OpenLitterMap.csv')


#%% make dates date data type
litter['date_taken'] = pd.to_datetime(litter['date_taken'])
litter['date_uploaded'] = pd.to_datetime(litter['date_uploaded'])

litter['date_taken_date'] = litter['date_taken'].dt.floor('d')
litter['date_taken_yrmth'] = litter['date_taken_date'].apply(lambda x: x.strftime('%Y-%m'))

#%% clean up addresses

"""
The address field is not consistent. For example, some addresses have a street address, some have a place name, some have a neighborhood designation along with the address. The next few steps go through and 
replace the placenames with street addresses, and remove additional data points like the neighborhood name that are not relevant for this analysis and are not consistently part of the data.

The process then counts the number of commas in the address field. If there are 6 commas, then there is a address number, street, city, country, state, zip, and country included in the address. If there are 5 columns then the 
address number is missing. These are handled separately, and then for those that are missing the address number, the field is added with empty values and the 2 data sets are merged back together.

The addresses will be grouped by block to show litter density by block.

"""

# make copy of address column, then replace the place names with street address as shown below.
litter['addressx'] = litter['address']

# replace placenames with street addresss
litter['address'] = litter['address'].str.replace('L&M Mighty Shop, South Van Buren Street, ', '504, E Burlington Street, ')
litter['address'] = litter['address'].str.replace('La Petite Academy, ', '1504, ')
litter['address'] = litter['address'].str.replace('Elizabeth Tate Alternative High School, ', '1528, ')
litter['address'] = litter['address'].str.replace('Four Seasons Car Wash, ', '1455, ')
litter['address'] = litter['address'].str.replace('Periodontal Associates, ', '1517, ')
litter['address'] = litter['address'].str.replace('Mergen Orthodontics, ', '1570, ')
litter['address'] = litter['address'].str.replace('Lower Muscatine @ Mall Dr, ', '1800, ')
litter['address'] = litter['address'].str.replace('Lower Muscatine Ave @ Iowa City Maketplace, ', '1600, ')
litter['address'] = litter['address'].str.replace('Kirkwood Community College - Iowa City Campus, ', '1816, ')
litter['address'] = litter['address'].str.replace('Sports Column, ', '12 S, ')
litter['address'] = litter['address'].str.replace('Assembly of God Church, ', '800, ')
litter['address'] = litter['address'].str.replace('Deli Mart, ', '1700, ')
litter['address'] = litter['address'].str.replace('First Christian Church, ', '200, ')
litter['address'] = litter['address'].str.replace('Iowa City Public Library, ', '123, ')
litter['address'] = litter['address'].str.replace("Jimmy Jack's Rib Shack, ", '1940, ')
litter['address'] = litter['address'].str.replace("JOANN Fabrics and Crafts, ", '1676, ')
litter['address'] = litter['address'].str.replace("McDonald's, ", '1861, ')
litter['address'] = litter['address'].str.replace("Bradley's Cleaners, ", '19030, ')
litter['address'] = litter['address'].str.replace("Oyama Sushi, ", '1853, ')
litter['address'] = litter['address'].str.replace("Select Physical Therapy, ", '1555, ')
litter['address'] = litter['address'].str.replace("Southeast Junior High School, ", '2501, ')
litter['address'] = litter['address'].str.replace("Spenler Tire, ", '1455, ')
litter['address'] = litter['address'].str.replace("Sycamore Mall, ", '1660, ')
litter['address'] = litter['address'].str.replace("The Record Collector, ", '116, ')
litter['address'] = litter['address'].str.replace("Wells Fargo, ", '103, ')


# remove neighborhoods and placenames
# create list of placenames to remove
str_orig = ['Plum Grove Acres, ','Kirkwood Place, ','Sunnyside, ', 'AMC DINE-IN Coral Ridge 10, ', 'Continuing Education Center, ', 'Formosa Sushi Bar, ', 'Plaza Centre One, ', 'Procter & Gamble Oral Care, ', "Sueppel's Flowers, ", 'Taco Loco, ', 'US-IA, ', 'Nodo Coffee, Carry-Out & Catering, ']

# replace with empty string
input_char = ''

# loop through placenames and replace them with the empty string
for i in range(len(str_orig)):
    litter['address'] = litter['address'].str.replace(str_orig[i],input_char)


#%%
######################################################                                           ###############################################
###################################################### < Step 3: Create Base or Main DataFrame > ###############################################
######################################################                                           ###############################################

# %% create base df
litter_base = litter[[c for c in litter.columns if c in base_columns]]


#%%
######################################################                                          #################################################
###################################################### < Step 4a: Create Custom Tag DataFrame > #################################################
######################################################                                          #################################################

#%% Organize the data for custom tags


litter_customtag = litter[['id', 'custom_tag_1']].dropna()
litter_customtag = litter_customtag.loc[litter_customtag['custom_tag_1'] != 'category:fastfood']
litter_customtag['main_category'] = 'custom_litter_type'
litter_customtag['value'] = 1.0

litter_customtag = litter_customtag.rename(columns={'custom_tag_1':'sub_category'})

litter_customtag = litter_customtag[['id', 'main_category', 'sub_category', 'value']]

litter_customtag['sub_category'] = litter_customtag['sub_category'].str.lower()

# remove the custom tag columns from the main dataset
litter = litter.loc[:,~litter.columns.str.startswith('custom_tag')]
litter = litter.loc[~litter['id'].isin(litter_customtag['id'])]


#%%
###################################################### < Step 4b: Find Main Category Cols         > ####################################################
###################################################### < Create function clean_subset             > ####################################################
###################################################### < Create dataframes for each main category > ####################################################
###################################################### < and combine back with main base data set > ####################################################

# %% find the columns where the name is all caps. These are the main category columns.

col_names = pd.DataFrame(litter.columns.tolist())
col_names = col_names.rename(columns = {0: 'col_name'})
col_names['isupper'] = col_names.loc[col_names['col_name'].str.isupper(), :]
col_names_all = col_names
col_names = col_names.dropna()
col_names_index = col_names.index.tolist()

# %%
#litter_base = litter.loc[:, base_columns]



#%% Create function to clean susbsetted data for each of the main categories.

# prefix is the main category name
def clean_subset(df_name,prefix):
    prefix = prefix + '_'
    df_name = df_name.rename(columns = lambda s: prefix + s)
    df_name = pd.concat([litter['id'], df_name], axis=1)
    df_name = df_name.melt(id_vars = 'id',
                           var_name = 'sub_category').dropna(subset=['value'])
    
    
    
    df_name['main_category'] = [x.split('_')[0] for x in df_name['sub_category']]
    df_name['sub_category'] = df_name['sub_category'].str.replace(prefix, '')

    df_name = df_name[['id', 'main_category', 'sub_category', 'value']]

    return(df_name)


#%% Create dataframes for each main category

litter_smoking = litter.iloc[:,col_names_index[0]:col_names_index[1]]
litter_smoking = clean_subset(litter_smoking, 'smoking')

litter_food = litter.iloc[:,col_names_index[1]:col_names_index[2]]
litter_food = clean_subset(litter_food, 'food')

litter_coffee = litter.iloc[:,col_names_index[2]:col_names_index[3]]
litter_coffee = clean_subset(litter_coffee, 'coffee')

litter_alcohol = litter.iloc[:,col_names_index[3]:col_names_index[4]]
litter_alcohol = clean_subset(litter_alcohol, 'alcohol')


litter_softdrinks = litter.iloc[:,col_names_index[4]:col_names_index[5]]
litter_softdrinks = clean_subset(litter_softdrinks, 'softdrinks')

litter_sanitary = litter.iloc[:,col_names_index[5]:col_names_index[6]]
litter_sanitary = clean_subset(litter_sanitary, 'sanitary')

litter_coastal = litter.iloc[:,col_names_index[6]:col_names_index[7]]
litter_coastal = clean_subset(litter_coastal, 'coastal')


litter_dumping = litter.iloc[:,col_names_index[7]:col_names_index[8]]
litter_dumping = clean_subset(litter_dumping, 'dumping')


litter_industrial = litter.iloc[:,col_names_index[8]:col_names_index[9]]
litter_industrial = clean_subset(litter_industrial, 'industrial')


# litter_brands = litter.iloc[:,col_names_index[9]:col_names_index[10]]
# litter_brands = clean_subset(litter_brands, 'brands')


litter_dogshit = litter.iloc[:,col_names_index[10]:col_names_index[11]]
litter_dogshit = clean_subset(litter_dogshit, 'dogshit')

litter_other = litter.iloc[:,col_names_index[13]:289]
litter_other = clean_subset(litter_other, 'other')


#%% Combine data subsets into one data frame
litter_categories = pd.concat([litter_smoking, litter_food, litter_coffee, litter_alcohol,
                               litter_softdrinks, litter_sanitary, litter_coastal, litter_dumping,
                               litter_industrial, litter_dogshit, litter_other, litter_customtag], axis= 0)
# %% Delete all the data frames and clear memory

del [[litter_smoking, litter_food, litter_coffee, litter_alcohol, litter_softdrinks,
      litter_sanitary, litter_coastal, litter_dumping, litter_industrial, litter_dogshit, 
      litter_other, litter_customtag]]

gc.collect()

# %% Combine the litter categories to the base litter data frame.

litter = litter_base.merge(litter_categories, how='right', on='id')
litter=litter.rename(columns = {'value': 'litter_count'})
litter['main_category'] = litter['main_category'].str.title()
litter['sub_category'] = litter['sub_category'].str.title()

#%%
###################################################### < Step 5: Clean and split Address          > ####################################################
###################################################### < Replace place names with add number      > ####################################################
###################################################### < Test address component count != 5 or 6   > ####################################################
###################################################### < Create a subset for 5 and 6 components   > ####################################################
###################################################### < Create a subset for 5 and 6 components   > ####################################################



#%% Identify number of commas, or components in the address
litter_base['comma_count'] = litter_base['address'].str.count(',')

# test for the number of components in the address. If it something other than 5 or 6, it will not work with this code.

test_comma_counts = pd.DataFrame(litter_base.groupby('comma_count').size()).reset_index()

# create list of expected values 5 and 6.

expected_vals = [5,6]

actual_vals = test_comma_counts['comma_count'].tolist()

test_list = []
for val in actual_vals:
    if(val in expected_vals):
        test_list.append(0)
    else:
        test_list.append(1)

test_list_sum = sum(test_list)

# Create exception

class NewCommaCountException(Exception):
    'Raised when there is an address that does not have 5 or 6 commas.'
    pass

# if test_list_sum is greater than 0, then throw an error and pring the comma counts

try:
    if test_list_sum > 0:
        raise NewCommaCountException
except NewCommaCountException:
    print('Check for addresses with comma count not equal to 5 or 6.')
    print(test_comma_counts)

# %% Create subset fo 5 components

litter_add_5 = litter_base.loc[litter_base['comma_count'] == 5]
litter_add_5 = litter_add_5[['id', 'address']]

litter_add_5[['add_street', 'add_city', 'add_county', 'add_state', 'add_zip', 'add_country']] = litter_add_5['address'].str.split(',',expand= True)

litter_add_5['add_num'] = np.nan

litter_add_5 = litter_add_5[['id', 'address', 'add_num', 'add_street', 'add_city', 'add_county', 'add_state', 'add_zip', 'add_country']]





# %% Create subset fo 6 components

litter_add_6 = litter_base.loc[litter_base['comma_count'] == 6]
litter_add_6 = litter_add_6[['id', 'address']]

litter_add_6[['add_num', 'add_street', 'add_city', 'add_county', 'add_state', 'add_zip', 'add_country']] = litter_add_6['address'].str.split(',',expand=True)

litter_add_6 = litter_add_6[['id', 'address', 'add_num', 'add_street', 'add_city', 'add_county', 'add_state', 'add_zip', 'add_country']]

# %% combine data sets back to 1 data set

litter_add_final = pd.concat([litter_add_5, litter_add_6])

# sort by row index value
litter_add_final = litter_add_final.sort_index() 

litter_add_final['add_street'] = litter_add_final['add_street'].apply(lambda x: x.strip())


# %% Aggregate by block number

# create new df named 'add_num' to identify if the value in the 'add_num' field is a number or text. 
# If it is a number, put in column 'add_is_num', if it is text put it in column 'add_is_text'.
add_num = litter_add_final['add_num'].str.extract('(?P<add_is_num>\d+)?(?P<add_is_text>\D+)?').fillna('')
# format column 'add_is_num' as an integer. 
add_num['add_is_num'] = pd.to_numeric(add_num['add_is_num'], errors = 'coerce', downcast = 'integer', )
# create new column, 'add_block_num' by rounding the address number.
add_num['add_block_num'] = round(add_num['add_is_num']/100,0)*100
# for column 'add_block_num', fill na's with the 'add_is_text' field
add_num['add_block_num'] = add_num['add_block_num'].fillna(add_num['add_is_text']) 
# remove .0 from the number
add_num['add_block_num'] = add_num['add_block_num'].astype(str).apply(lambda x: x.replace('.0',''))


# %%
litter_add_final = pd.concat([litter_add_final, add_num], axis=1)
litter_add_final['add_blocknum_street'] = litter_add_final['add_block_num'].astype(str) + ' ' + litter_add_final['add_street']

litter_add_final = litter_add_final[['id', 'add_num', 'add_street', 'add_city', 'add_county', 'add_state', 'add_zip', 'add_country', 'add_block_num', 'add_blocknum_street']]

litter = pd.merge(litter, litter_add_final, on = 'id', how = 'left')


# %%
# create new dataframe, 'df_latlon' to get the minimum latitude and minimum longitude by block
df_latlon = litter[['add_blocknum_street', 'lat', 'lon']]
df_latlon = df_latlon.groupby('add_blocknum_street')[['lat', 'lon']].min().reset_index()
df_latlon = df_latlon.rename(columns = {'lat': 'min_lat', 'lon': 'min_lon'})

litter = pd.merge(litter, df_latlon, on = 'add_blocknum_street', how = 'left')


# %%
# create pivot table 'st_count' to show the number of times litter was picked up on that block
st_count = pd.DataFrame(litter.groupby(['add_blocknum_street'])['date_taken_date'].nunique()).reset_index()
st_count = st_count.rename(columns = {'date_taken_date': 'total_count_pickup_dates'})
# %%
# create pivot table 'litter_sum' to show the total litter picked up at each block
litter_sum = pd.DataFrame(litter.groupby(['add_blocknum_street'])['litter_count'].sum()).reset_index()
litter_sum = litter_sum.rename(columns = {'litter_count':'total_litter_pickedup'})

# %%
# join 'st_count' to 'litter_sum' using left join on 'add_blocknum_street'
litter_sum = pd.merge(litter_sum, st_count, on = 'add_blocknum_street', how = 'left')
# calculate the average total litter picked up at each block per date
litter_sum['avg_litter_pickedup'] = round((litter_sum['total_litter_pickedup']) / (litter_sum['total_count_pickup_dates']),1)


# join the 'df_latlon' to 'litter_sum' to facilitate litter density on a street map
litter_sum = pd.merge(litter_sum, df_latlon, on = 'add_blocknum_street', how = 'left')


#%% clean up environment

del actual_vals, add_num, base_columns, col_names, col_names_all, col_names_index, df_latlon,expected_vals, i, input_char, litter_add_5, litter_add_6, litter_add_final, litter_base, litter_categories, st_count, str_orig, test_comma_counts, test_list, test_list_sum, val

litter=litter.rename(columns = {'value': 'litter_count'})
# %%
