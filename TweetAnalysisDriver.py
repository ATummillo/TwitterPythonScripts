import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
# import logging

# logging.basicConfig(filename=Path("C:/Users/Anthony/Desktop/pythonArgs/python2.log"), filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# logging.warning("Script has begun")

intvl_map = {'3day':'3D', '1day':'D', '12hr':'12H', '6hr':'6H', '4hr':'4H', '3hr':'3H', '2hr':'2H', '1hr':'H'}

start = datetime.strptime(sys.argv[1], '%Y-%m-%dT%H:%M:%S')
end = datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%S')
intvl = intvl_map[sys.argv[3]]

#Configure filepath for data
data_folder = Path("Python/")
file_to_read = data_folder / "tweet_data.csv"

#Build and format data frame for data from desktopbrain
base_df = pd.read_csv(file_to_read)
# base_df = pd.read_csv(sys.stdin)

base_df['TweetTimestamp_ts'] = pd.to_datetime(base_df['TweetTimestamp'])
# del base_df['TweetTimestamp']
base_df['period'] = base_df['TweetTimestamp_ts'].dt.to_period('H')

#Get dataframe of tweet counts over entire interval
count_df = pd.DataFrame(base_df['period'].value_counts())
count_df.rename(columns={'period':'TweetCount'}, inplace=True)
count_df.index = count_df.index.to_timestamp()
count_df = count_df.reindex(pd.date_range(start=start, end=end, freq='H'), fill_value=0)
final_df = count_df.groupby(pd.Grouper(freq=intvl)).sum()
final_df['PercentChange'] = final_df['TweetCount'].pct_change()
final_df = final_df.replace('NaN', 0)

#Write dataframe as csv to file
file_to_write = data_folder / "final_data.csv"

f = open(file_to_write, "w+")
f.write("Index")
f.close()
final_df.to_csv(file_to_write, mode='a')

#Exit
sys.exit(0)