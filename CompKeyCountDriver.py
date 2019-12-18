import pandas as pd

tweets_df = pd.read_csv(r"C:\#####\#####\#####.csv")
count_df = pd.DataFrame(tweets_df['CompKey'].value_counts())
print(count_df.head())
count_df.to_csv(r"C:\#####\#####\#####.csv")