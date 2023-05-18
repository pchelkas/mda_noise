# Import Packages
import os
import pandas as pd
from pandasgui import show
import numpy as np
from fancyimpute import IterativeImputer
from datetime import datetime

# <1> Function to process "raw" noise data of 12 months in a folder. 
    # <1> Example => 
    # concatenate_files(r'D:\KUL2022\SS2022\Modern Data Analysis\Project\Data\Sound in Street\All sites original')
def generate_new_file(file_path):
    import os
    import pandas as pd
    from datetime import datetime
    file_list = []
    for file in os.listdir(file_path):
        file_list.append(os.path.join(file_path, file))
    print(file_list)
    for file in file_list:
        # Read Files.
        df = pd.read_csv(file, delimiter=';')

        # Convert 'result_timestamp' column to datetime format
        df['result_timestamp'] = pd.to_datetime(df['result_timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

        # create new columns for year, month, day, hour, minute and weekday
        # df['description'] = df['description']
        # df['result_timestamp'] =  df['result_timestamp']
        df['year']  = df['result_timestamp'].dt.year
        df['month'] = df['result_timestamp'].dt.month
        df['day'] = df['result_timestamp'].dt.day
        df['hour'] = df['result_timestamp'].dt.hour
        df['minute'] = df['result_timestamp'].dt.minute
        df['10min'] = df['minute'].apply(lambda x: int(x/10)*10)
        df['weekday'] = df['result_timestamp'].dt.weekday

        # Create columns by taking the means of every 10 minutes
        new_df = df.groupby([
            df['description'],
            df['year'],
            df['month'],        
            df['day'],
            df['hour'],
            df['weekday'],
            df['10min']])[['lamax','laeq','lceq', 'lcpeak']].mean().reset_index()
    
        # Rename the columns
        new_df.columns = ['description', 'year', 'month', 'day', 'hour', 'weekday', '10min','mean_lamax', 'mean_laeq', 'mean_lceq', 'mean_lcpeak']
        new_file_path = file[:-4]+'_new.csv'
        new_df.to_csv(new_file_path, index=False)


# <2> Function to cancatenate the files in a folder into one file
    # <2> Example => 
    # concatenate_files(r'C:\Users\LIE\MDA Project\Sound in Street\All sites 10min\vrijthof')
def concatenate_files(file_path):
    import os
    # Create a list of all the files in the directory
    file_list = []
    for file in os.listdir(file_path):
        file_list.append(os.path.join(file_path, file))
    #return file_list
    # Read Files.
    import pandas as pd
    merged_df = pd.DataFrame()
    for file in file_list:    
        df = pd.read_csv(file)
        merged_df = pd.concat([merged_df, df])
    # Export merged_df
    new_file_path = file_path+'\Cancatenated_File.csv'
    merged_df.to_csv(new_file_path, index=False)




# <3> Function to create a timestamp column to the concatenated file, then export
    # <3> Example => 
    # create_timestamp('2022-01-01 00:00', '2023-01-01 00:00', r'C:\Users\LIE\MDA Project\Sound in Street\All sites 10min')
    # PS: the following line may raise an error message because I tried to assign multiple values to a single column
    #df['datetime'] = df.apply(lambda x: datetime(x['year'], x['month'], x['day'], x['hour'], int(x['10min']-10)), axis=1)
def  create_timestamp(min_time, max_time, file_path):
    import pandas as pd
    from datetime import datetime
    import os
    # Define min and max time
    min_time = pd.to_datetime(min_time)
    max_time = pd.to_datetime(max_time)
    # Create a new dataframe with all possible combinations of time variables
    time_df = pd.DataFrame({'datetime': pd.date_range(min_time, max_time, freq='10min')})

    # Create a list of all the files in the directory
    file_list = []
    for file in os.listdir(file_path):
        file_list.append(os.path.join(file_path, file))
    # Read Files and merge the files with TimeFrame dataframe.
    for file in file_list:    
        df = pd.read_csv(file+'\Cancatenated_File.csv')
        df['datetime'] = df.apply(lambda x: datetime(x['year'], x['month'], x['day'], x['hour'], int(x['10min'])), axis=1)
        merged_df = pd.merge(time_df, df, how='outer', on='datetime')
        new_file_path = file+'\Cancatenated_File_Timestamp.csv'        
        merged_df.to_csv(new_file_path, index=False)


# <3-1> Function to add new time variables from timestamp (I used it after merging the averaged noise data with the 10 minute timestamp of 2022 )
    # Results from this step can be found in <8_Sites of noise for imputation>, just in case we don't want to do imputation
def generate_new_file(file_path):
    import os
    import pandas as pd
    from datetime import datetime
    file_list = []
    for file in os.listdir(file_path):
        file_list.append(os.path.join(file_path, file))
    print(file_list)

    # Read Files.
    for file in file_list:
        df = pd.read_csv(file)

        # Convert 'result_timestamp' column to datetime format
        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
        df['year']  = df['datetime'].dt.year
        df['month'] = df['datetime'].dt.month
        df['day'] = df['datetime'].dt.day
        df['hour'] = df['datetime'].dt.hour
        df['10min'] = df['datetime'].dt.minute
        df['weekday'] = df['datetime'].dt.weekday
    
        # Export files
        new_file_path = file[:-4]+'_new.csv'
        df.to_csv(new_file_path, index=False)


# <4> Function to apply Multivariate Imputation by Chained Equations Algorithm (MICE) to impute noise data
    # Impute the noise data with also the values from weather variables after merging with the meteo dataset.
    # The results from this step can be found in <8_Sites of noise imputed with weather ref>
    
# Example to run this function =>
# file_path = r'C:\Users\LIE\MDA Project\Sound in Street\8_Sites of noise for imputation'
# weatherFile = r'C:\Users\LIE\MDA Project\Weather\lc_2022_avgbyid_timecoverted.csv'
# impute_2files(file_path, weatherFile)

# A function to read 2 csv, join them, and do imputation
def impute_2files(file_path, weatherFile):
    import os
    import pandas as pd
    from datetime import datetime
    from fancyimpute import IterativeImputer

    df_weather = pd.read_csv(weatherFile)
    # Rename the column in df_weather to match the column name in df
    df_weather = df_weather.rename(columns={'DATE_BRU': 'datetime'})
    df_weather['datetime'] = df_weather['datetime'].str[:-6]
    file_list = []
    for file in os.listdir(file_path):
        file_list.append(os.path.join(file_path, file))
    print(file_list)
    for file in file_list:
        df = pd.read_csv(file)
        # Filter DataFrame based on 'year' and 'month'
        merged_df = pd.merge(df, df_weather, on='datetime', how='inner')
        
        # Create a copy of the data
        df_imputer_mice = merged_df.copy(deep=True)
        
        # Check the missing value counts before imputation
        print(df_imputer_mice.isnull().sum())
        
        # Specify the numerical columns to be imputed: use also weather featurers
        numerical_cols = ['mean_lamax', 'mean_laeq', 'mean_lceq', 'mean_lcpeak', 'LC_HUMIDITY', 'LC_DWPTEMP']

        # Create an object of IterativeImputer
        imputer_mice = IterativeImputer(max_iter=10)

        # Fit the imputer object to the data
        imputer_mice.fit(df_imputer_mice[numerical_cols])

        # Impute the missing values in the specified numerical columns
        df_imputer_mice.loc[:, numerical_cols] = pd.DataFrame(imputer_mice.transform(df_imputer_mice[numerical_cols]), columns=numerical_cols)
    
        # Check the missing value counts of imputed dataframe
        print(df_imputer_mice.isnull().sum())
        
        #Export file
        new_file_path = file[:-4]+'_weather_imputed.csv'
        df_imputer_mice.to_csv(new_file_path, index=False)


