import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# read the data from the json file
with open('wind_turbine_with_issues.json') as f:
    data = json.load(f)

# clean the data
df = pd.DataFrame.from_dict(data['data'])
df[['temperature', 'pressure', 'wind_speed', 'rpm', 'energy_output']].apply(pd.to_numeric)
df.drop_duplicates(keep='first')
df.fillna(value=np.nan)
cleaned_values = df['energy_output'].str.split(',').str[0]
df['energy_output'] = pd.to_numeric(cleaned_values, errors='coerce')
mean_energy_output = df['energy_output'].mean()
df['energy_output'] = df['energy_output'].fillna(value=mean_energy_output)
df['timestamps'] = df['timestamps'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df = df.sort_values(by='timestamps', ascending=True, ignore_index=True)
print(df)

# export the data to a csv file
df.to_csv('wind_turbine_with_issue_cleansing data.csv', sep=',', index=False, encoding='utf-8')

# Plot the data using seaborn
sns.pairplot(df)
plt.show()

# Plot the data using matplotlib
df = df.set_index('timestamps')
df[500:].plot()
plt.title('Turbine Data')
plt.show()
