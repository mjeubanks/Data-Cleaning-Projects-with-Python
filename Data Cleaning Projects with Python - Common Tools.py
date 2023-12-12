#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning Projects with Python

# Foreword:
# 
# It is important to explore the data before cleaning it. You should have done a quick review of the data so that you have a general idea of the correlation between features, distribution of values and fully understand what the values signify.
# 
# There are three examples of data cleaning; each with different degrees of complexity. The goal of this notebook is to present these examples and demonstrate the common functions/tools/revisions in the data cleaning process.

# In[243]:


import pandas as pd
import numpy as np


# ## EXAMPLE 1 - Sales Contacts
# 
# The goal of this data cleaning is to provide the Sales Team a table containing a list of customers to call to follow up on our new product that was recently released.
# 
# Comments on the below table:
# - There are typos in last names. They contain unwarranted characters.
# - Phone numbers does not have a unified format.
# - Addresses contain different levels on information.
# - Some entries are duplicates
# - There is a column with irrelevant information.
# - Some rows have missing values.

# In[153]:


df = pd.read_excel("Customer Call List.xlsx") #Enter your path
df


# ### DROP DUPLICATE ENTRIES
# 
# `df.drop_duplicates()` 

# In[154]:


df = df.drop_duplicates()
df


# ### DROP NOT USEFUL COLUMNS
# 
# `df.drop(columns = "COLUMNNAME")`

# In[155]:


df = df.drop(columns = "Not_Useful_Column")
df


# ### FIX TYPOS IN LAST NAME
# 
# The below method will remove undesireable characters from string values:
# - df['Last_Name'].str.lstrip("""...""") removes the first value from the left
# - df['Last_Name'].str.rstrip("""...""") removes the last value from the right
# - df['Last_Name'].str.strip("""/._""") removes first and last values. This example removes all values '/', '.', and '_'.

# In[156]:


df['Last_Name'] = df['Last_Name'].str.strip("/._") #NOTE: Strip must NOT be in list format!
df


# ### FORMAT PHONE NUMBERS - REMOVE NON-DIGIT CHARACTERS
# 
# `df['COLUMNNAME'].str.replace(regex, replacementvalue)`
# 
# regex - regex value
# 
# replacementvalue - value to replace the regex value

# In[157]:


#Phone numbers aren't considered strings so it so the strip method doesn't work.
df['Phone_Number'] = df['Phone_Number'].str.replace('[\W]','')
df['Phone_Number'].str.replace('[^a-zA-z0-9]','') #alternative (inefficient) method
df


# ### FORMAT PHONE NUMBERS - UNIFY THE PHONE NUMBER FORMAT
# 
# `df.apply()` - Apply a function to the DataFrame.
# 
# 
# `df.apply(lambda x: x+3)` - lambda are equivalent to single expression functions
# 
# ![image.png](attachment:image.png)

# In[158]:


df['Phone_Number'] = df['Phone_Number'].apply(lambda x: str(x))
df['Phone_Number'] = df['Phone_Number'].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
df


# ### FORMAT PHONE NUMBERS - REMOVE NULL VALUES
# 
# 

# In[159]:


df['Phone_Number'] = df['Phone_Number'].str.replace('nan--', '')
df['Phone_Number'] = df['Phone_Number'].str.replace('Na--', '')
df


# Formatting the Address
# 
# `df.str.split` (separator, #columns, expand=True)
# 
# __separator__ - the separated value which is usually a comma but can also be a '|', '/' or even a space
# 
# __#columns__ - the number of desired columns. There will be one column for every sequential separator
# 
# __expand=True__ - required to make each separation a column

# In[160]:


df[['Street_Address', 'State', 'Zip_Code']] = df['Address'].str.split(',', 2, expand=True)
df = df.drop(columns = 'Address') # The current 'Address' column is now obsolete
df


# ### REFORMAT CUSTOMERS AND CONTACT APPROVAL

# In[162]:


df['Paying Customer'] = df['Paying Customer'].str.replace('Yes', 'Y')
df['Paying Customer'] = df['Paying Customer'].str.replace('No', 'N')
df['Do_Not_Contact'] = df['Do_Not_Contact'].str.replace('Yes', 'Y')
df['Do_Not_Contact'] = df['Do_Not_Contact'].str.replace('No', 'N')
df


# ### REMOVE THE NaN VALUES.
# 
# NOTE: NaN is not actually a value so df.replace will not work.
# 
# `df.fillna()` - fills na values with desired value

# In[163]:


df = df.replace('N/a', '')
df = df.replace('NaN', '')
df = df.fillna('')
df


# ### REMOVE 'DO NOT CALL' CUSTOMERS'
# 
# We only want to have a table which we would like to call.

# In[164]:


for i in df.index:
    if df.loc[i, "Do_Not_Contact"] == 'Y':
        df.drop(i, inplace=True)

df


# Removes empty fields:

# In[165]:


for i in df.index:
    if df.loc[i, "Phone_Number"] == '':
        df.drop(i, inplace=True)

df

#df = df.dropna(subset='Phone_Number', inplace=True) Alternative Method


# ### RESET INDEX

# In[166]:


df = df.reset_index(drop=True)
df


# ### FINAL PRODUCT

# In[167]:


df


# ### CONCLUSION
# 
# At this point, the dataset has been cleaned. There is missing data but thats inevitable and arugably irrelavent because the Sales people can get retrieve that contact information once they have a phone conversation. 

# ## EXAMPLE 2 - New York City Trees

# In this example, assume you've already explored the data and the table below is an output of that exploration.

# In[282]:


tree_census = pd.read_csv(r"2015_Street_Tree_Census_-_Tree_Data.csv")
pd.set_option('display.max_columns', None)
tree_census_subset = tree_census[['tree_id','tree_dbh', 'stump_diam',
       'curb_loc', 'status', 'health', 'spc_latin', 'steward',
       'sidewalk','problems', 'root_stone',
       'root_grate', 'root_other', 'trunk_wire', 'trnk_light', 'trnk_other',
       'brch_light', 'brch_shoe', 'brch_other']]
tree_census_subset.head(3)


# ### MODIFY THE THE FEATURE  (NULL) VALUES
# 
# 

# Logically, if the health of a tree is either a stump or dead then the health, square square, steward, sidewalk and problems features are 'Not Applicable' as opposed to 'Not Available'. Let's do the conversion:

# In[283]:


mask = ((tree_census_subset['status'] == 'Stump') | (tree_census_subset['status'] == 'Dead'))


# In[284]:


tree_census_subset.loc[mask] = tree_census_subset.loc[mask].fillna('Not Applicable')


# In[285]:


tree_census_subset[tree_census_subset['status'] == 'Stump']


# Filling in the Null, Na, NaN values

# In[286]:


tree_census_subset.isna().sum()


# For some odd reason - health, spc_latin, sidewalk and problems still have an NA. value. This is why it's always good to double check that fillna() has filled all of the empty values.

# Let's look at all the individual rows to see happens.

# In[287]:


tree_census_subset[tree_census_subset['health'].isna()]


# Side walk still has an NaN value and so do the rest of the remaining features that stated were still NaN.

# In[288]:


tree_census_subset[tree_census_subset['sidewalk'].isna()]


# In[289]:


tree_census_subset[tree_census_subset['spc_latin'].isna()]


# In[290]:


tree_census_subset[tree_census_subset['problems'].isna()].head(3)


# There is a mix of None and Nan Values. Often, these act like viruses that cannot be treated. You can see that even `.replace()` isn't updating it.

# In[188]:


tree_census_subset = tree_census_subset.replace('None', 'Not Applicable')
tree_census_subset = tree_census_subset.replace('NaN', 'Not Applicable')


# In[222]:


tree_census_subset.isna().sum()


# In the code lines below, you can see that `fillna()` isn't working because technically they are not null values
# 
# The boolean does not consider the value as a string NaN, None or np.nan. This is why none of the functions are filling the values:

# In[291]:


tree_census_subset[tree_census_subset.index == 120289]['problems']


# In[292]:


tree_census_subset[tree_census_subset.index == 120289]['problems'] == None


# In[293]:


tree_census_subset[tree_census_subset.index == 120289]['problems'] == np.nan


# In[294]:


tree_census_subset[tree_census_subset.index == 120289]['problems'] == 'NaN'


# We will have to manually fill null values. First let's get the index values all 'health', 'spc_latin', 'sidewalk', 'problems' that are still NaN:

# In[295]:


tree_census_subset[tree_census_subset['health'].isna()].index


# In[296]:


tree_census_subset[tree_census_subset['spc_latin'].isna()].index


# In[297]:


tree_census_subset[tree_census_subset['sidewalk'].isna()].index


# In[298]:


tree_census_subset[tree_census_subset['problems'].isna()].index


# Now let's do a for statement to fill all the values with 'Not Applicable'.
# 
# NOTE: All of the codes below could be consolidated in one 'for statement' but it is separated to show how the code is working.

# In[299]:


healthnan = [32889]

for i in problemsnan:
    tree_census_subset.loc[healthnan, 'health'] = 'Not Applicable'


# In[300]:


spc_latinnan = [356613, 427541, 431417, 608632, 656960]

for i in spc_latinnan:
    tree_census_subset.loc[spc_latinnan, 'spc_latin'] = 'Not Applicable'


# In[301]:


sidewalknan = [346299]

for i in sidewalknan:
    tree_census_subset.loc[sidewalknan, 'sidewalk'] = 'Not Applicable'


# In[302]:


problemsnan = [120289, 121488, 121685, 133470, 133812, 134820, 144137, 145324,
            145337, 146314, 146378, 146430, 146630, 146662, 263577, 263578,
            263795, 274280, 327575, 356663, 360398, 427541, 469486, 472398,
            472451, 472574, 473973, 473976, 474508, 474527, 474555, 475095,
            475326, 475368, 475661, 479859, 483223, 484013, 484247, 485096,
            489204, 489292, 491710, 491826, 492433, 492434, 496366, 496835,
            500888]

for i in problemsnan:
    tree_census_subset.loc[problemsnan, 'problems'] = 'Not Applicable'


# Congrats! There are no more null values!

# In[303]:


tree_census_subset.isna().sum()


# ### REMOVE OUTLIERS
# 
# Tree depth and Stump diameter are fortunately (or unfortunately?) the only to features with numerical values. There are over 60k rows of values so it is easy to see outliers using a scatterplot.

# In[309]:


tree_census_subset.plot(kind='scatter', figsize=(20,10), x = 'tree_id', y = 'tree_dbh')


# You can see the frequency of the scatter plot is usually less than 60. Statistically, this is also confirmed by the box plot:

# In[323]:


tree_census_subset['tree_dbh'].plot(kind='box', figsize=(20,10))


# Offically, an outlier is considered Q3 * 1.5IQR. This leads to value 16.75.

# In[329]:


tree_census_subset['tree_dbh'].quantile([0.25, 0.75])


# In[331]:


16 + ((0.75 - 0.25) * 1.5)


# In theory we can remove all values greater than 16.76 but we will be deleted a substantial quanitty of data based on looking at the scatter plot. Maybe there is something missing, It's possible that the trees with a high tree depth are part of a certain class of trees. Let's look at the type of trees:

# In[337]:


tree_census_subset.loc[tree_census_subset['tree_dbh'] > 60]['spc_latin'].value_counts()


# Based on the value counts, it doesn't look like the huge tree depths are part of specific class.
# 
# Let's remove the outliers based on our eyeball estimate from the scatterplot and filter the dataset to have a tree depth less than 60. Let's repeat the exercise with stump diameter. Coincidentally, we can also filter this feature by values less than 60.

# In[310]:


tree_census_subset.plot(kind='scatter', figsize=(20,10), x = 'tree_id', y = 'stump_diam')


# In[341]:


tree_census_subset = tree_census_subset[(tree_census_subset['tree_dbh']<= 60) & (tree_census_subset['stump_diam']<= 60)]
tree_census_subset


# We're going to do separate analysis for Alive and Dead trees:

# In[343]:


tree_census_subset_alive = tree_census_subset[tree_census_subset['status'] == 'Alive']
tree_census_subset_dead_or_stump = tree_census_subset[(tree_census_subset['status'] == 'Dead') | (tree_census_subset['status'] == 'Stump')]


# In[346]:


tree_census_subset_alive.groupby('spc_latin')['tree_dbh'].describe()


# Strangely, the minimum value is 0 which is unrealistic. We may want to consider removing data below the 25 and above the 75 quantiles.

# In[350]:


stats = tree_census_subset_alive.groupby('spc_latin')['tree_dbh'].describe().reset_index()[['spc_latin', '25%', '75%']]


# In[353]:


tree_census_subset_alive = tree_census_subset_alive.merge(stats, on='spc_latin', how='left')
tree_census_subset_alive


# ### CONCLUSION
# 
# At this point, you are technically finished with cleaning. You can remove outliers or delete values under a certain quantile but I would recommend to consult with the persons who generated the data so that you can get their opinion before you proceed.
# 
# You should get more feedback on the purpose of this dataset and subject matter experts should provide questions that can be answered with the current data.
# 
# Sometimes there is no point to proceeding with more advanced analysis such as statistics and Machine Learning unless there is a clear goal in mind.

# ## EXAMPLE 3 - FIFA 21

# In[358]:


data = pd.read_csv(r"fifa21 raw data v2.csv")
pd.set_option('display.max_columns', None)
data.head(10)


# ### QUICK EXPLORATION

# There are 19,000 rows and 77 features:

# In[360]:


data.shape


# We used `df.isna().sum()` in the previous example but this dataset has a lot of features and isn't displaying all the values.

# In[370]:


data.isna().sum()


# Below is a workaround using `df.info()`. The shape states that there was a little under 19,000 rows. You can see that 'Loan Date End' and 'Hits' have some missing values. `df.info()` is also valuable for datasets with a lot of features because you can get a summary of which columns are catagorical or numeric.

# In[361]:


data.info()


# In[367]:


data.isna().sum()


# ### CREATE NEW DATA SET
# 
# There are many times when you want to work on a copy of the dataset as opposed to the actual extracted dataset. Such occurances are do to the dataset being an output of multiple joins or it can be something as simple as you expect to make a lot of changes so you want to periodically reference the original dataset.

# In[373]:


fifa = data.copy()
fifa.head(3)


# use `df.dtype` to confirm the type of feature values.

# ### CLEAN INDIVIDUAL COLUMNS (FEATURE VALUES)
# 
# There are a lot of features so it's not feasible to look at a summary of the table and get an immediate idea of what to modify. We'll need to look at each feature in detail.

# #### Club

# In[374]:


fifa['Club'].dtype


# df.unique() shows all the unique values.
# 
# Note that the values contain a lot of leading spaces which will eventually have to get stripped.

# In[376]:


fifa['Club'].unique()


# Notice that `df.str.strip()` contains no values in the function as opposed to previous examples. By default, this function strips any whitespaces.

# In[379]:


fifa['Club'] = fifa['Club'].str.strip()
fifa['Club'].unique()


# #### Contract 

# In[524]:


"""NOTE: this was already seen when .info() was used"""

fifa['Contract'].dtype


# We immediately notice that the nomeclature of values aren't unified. There are three formats:
# 
# - '2004 ~ 2021'
# - 'Jun 30, 2021 On Loan'
# - 'Free'

# In[383]:


fifa['Contract'].unique()


# A for loop was used to see the formatting for this columns. Suprisingly to our luck - although there are three different formats, the formatting is consistent.

# In[385]:


for index, row in fifa.iterrows():
    if 'On Loan' in row['Contract'] or 'Free' in row['Contract']:
        print(row['Contract'])


# We're going to create a function to extract contract dates. There's a lot going on in this function so play close attention to each line.
# 
# NOTE: Pay close attention to '''On Loan' in contract' - 'On Loan' is only a portion of the value hence why we use 'in' instead of '=='

# In[412]:


'''Free' is an actual value, while 'On Loan' is only a portion of a value. For this
# reason, we must use 'in' instead of '==''''
def extract_contract_info(contract):
    if contract == 'Free' or 'On Loan' in contract:
        start_date = np.nan #Players are not under contract so that value is 0
        end_date = np.nan
        contract_length = 0
    else:
        start_date, end_date = contract.split(' ~ ') #There are spaces in between the ~ value
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        contract_length = end_year - start_year
    return start_date, end_date, contract_length

'''Use a lambda function to creat a new data set that will have the contract dates reformatted'''
new_cols = ['Contract Start', 'Contract End', 'Contract Length(years)']
new_data = fifa['Contract'].apply(lambda x: pd.Series(extract_contract_info(x)))

for i in range(len(new_cols)):
    fifa.insert(loc=fifa.columns.get_loc('Contract')+1+i, column=new_cols[i], value=new_data[i])


# In[408]:


'''I will look into if this will save on lines of code.'''
#fifa['Contract'].str.split(' ~ ', 2, expand=True)


# Confirm the new columns have been properly inserted:

# In[419]:


fifa.head(3)


# In[427]:


fifa[['Contract','Contract Start', 'Contract End', 'Contract Length(years)']][203:207]


# Let's create new catagorical columns to represent three types of players: On contract, free or on loan.

# In[436]:


def catagorize_contract_status(contract):
    if contract == 'Free':
        return 'Free'
    elif 'On Loan' in contract:
        return 'On Loan'
    else:
        return 'Contract'
    
fifa.insert(fifa.columns.get_loc('Contract Length(years)')+1, 'Contract Status', fifa['Contract'].apply(catagorize_contract_status))


# In[439]:


fifa[['Contract','Contract Start', 'Contract End', 'Contract Length(years)', 'Contract Status']][203:207]


# ### Height

# Height should be an integer as the value is in CM but the type is an object.

# In[441]:


fifa['Height'].dtype


# The formatting is not consistent as some values are in cm and others in ft/in.

# In[443]:


fifa['Height'].unique()


# In[498]:


def convert_height(height):
    if "cm" in height:
        return int(height.strip("cm"))
    else:
        feet, inches = height.split("'") #This refers to the ' in 6'2".
        total_inches = int(feet)*12 + int(inches.strip('"')) #This refers to the " in 6'2"
        return round(total_inches * 2.54) #convert to cm
    
#Apply function to height column
#fifa['Height'] = fifa['Height'].apply(convert_height) #<----This also works
fifa['Height'] = fifa['Height'].apply(lambda x: pd.Series(convert_height(x)))


# In[509]:


fifa['Height'].unique()


# Update the column to state that the units.

# In[510]:


fifa = fifa.rename(columns={'Height': 'Height (cm)'})


# In[511]:


fifa.head(1)


# ### Weight

# In[512]:


fifa['Weight'].dtype


# Same situation as 'Height'. We expected the values to be an integer since weight is a numerical value but the dtype is an object.

# In[513]:


fifa['Weight'].unique()


# In[520]:


def convert_weight(weight):
    if "kg" in weight: 
        return int(weight.strip("kg"))
    else:
        pounds = int(weight.strip("lbs"))
        return round(pounds/2.205) #converts lbs to kg

#Apply funciton to weight column
fifa['Weight'] = fifa['Weight'].apply(convert_weight)
fifa['Weight'].unique()


# In[521]:


fifa = fifa.rename(columns={'Weight': 'Weight (kg)'})


# In[522]:


fifa.head(1)


# ### Loan Date End

# In[523]:


fifa['Loan Date End'].dtype


# We lucked out! The values are in correct formatting.

# In[525]:


fifa['Loan Date End'].unique()


# Let's see if the data makes sense: the date the player was on loan should not conflict with when the loan date ended.
# 
# It's also important to note that we now know why there are only 1000 rows of this feature - only a small quanitty of players were ever on loan.

# In[527]:


on_loan = fifa[fifa['Contract Status'] == 'On Loan']
on_loan[['Contract', 'Contract Status', 'Loan Date End']]


# ### W/F
# 
# Player's week foot rating (out of 5) - A 5 star rating means the player has equal performance accuracy and power of shooting and passing, and tackling with either foot.

# In[528]:


fifa['W/F'].dtype


# We expected this value to be an integer but it's an object. This case has a special character in the value.
# 
# You may or may not want to change this value to an integer. Arguably this can be considered a catagorical feature.
# 
# We're going to strip the stars just in case we want to do a calculation in the future that we are currently unaware of.

# In[529]:


fifa['W/F'].unique()


# There are two methods to remove the ★

# In[530]:


fifa['W/F'].str.replace('★', "")


# In[536]:


fifa['W/F'].str.strip('★')


# In[537]:


fifa['W/F'] = fifa['W/F'].str.replace('★', "")
fifa['W/F'].unique()


# ### SM
# 
# Repeat the exact same line of codes as 'W/F'

# ### HITS
# 
# Number of times the player has been searched for in the FIFA database.

# In[738]:


fifa['Hits'] = data['Hits']


# In[739]:


fifa['Hits'].dtype


# We can see that there are values that state '1.6K' instead of 1600 which is why this feature is considered an object. 
# 
# Note that since the value states 1.6K. It is impossible to know the exact value.
# 
# This dataset is also tricky because there are some values that act as strings, others as float and there is a nan

# In[740]:


print(fifa['Hits'].shape)
fifa['Hits'].unique()


# Before we can use the above function, we have to remove the nan value because this will raise an error if we try to apply a function.

# In[741]:


fifa['Hits'] = fifa['Hits'].fillna(0)
print(fifa['Hits'].shape)
fifa['Hits'].unique()


# In[742]:


"""
This original version of the function was still returning string values with '.0'

def convert_hits(hits):
    string = (str(hits))
    string = string.strip('.0')
    if "K" in string:
        return str(float(string.strip('K')) * 1000)
    else:
        return string.strip('.0')"""


"""The mixture of strings and floats is causing a bug in the data. Float values are
labeled as objects but are acting as floats which makes string to unify the nomeclature
for this feature complicated.

Pay attention to the logic of this fuction:"""
def convert_hits(hits):
    string = (str(hits))
    string = string.strip('.0') #This is to ensure all values such as '6.0' are stripped.
    if "K" in string:
        stringfloat = str(float(string.strip('K')) * 1000) #converts float from '1.6' to '1600.0'
        return str(stringfloat.strip('.0')) #string value still has '.0' due to calculation
    else:
        return string.strip('.0')
    
fifa['Hits'] = fifa['Hits'].apply(convert_hits)
print(fifa['Hits'].shape)
fifa['Hits'].unique()


# ### CONCLUSION
# 
# At this point in this example, all the remaining features in this dataset are acceptable or the required updates use the identical lines of codes that were already mentioned. Congrats! At this point the data cleaning as been complete.
# 
# The fun part begins - there is a lot of data to perform statistcs and run some Machine Learning Algorithims. That would be covered in a different notebook.
# 
# Imagine you're working for a European footbal club such as Real Madrid and you want to better understand your competition. This data can be used to understand who's overpaid (Player Salary vs Player stats), if younger players perform better than older players and which nationalities have the highest paid players. The possibilities are endless.
