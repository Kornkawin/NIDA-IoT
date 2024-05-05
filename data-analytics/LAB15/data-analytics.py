import numpy as np
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(25)
num_rows = 1440
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2023, 1, 2)
temperature_mean = 80
temperature_stddev = 10
pressure_mean = 30000
pressure_stddev = 5000
wind_speed_mean = 10
wind_speed_stddev = 5
rpm_mean = 1500
rpm_stddev = 250
energy_output_mean = 50
energy_output_stddev = 10
timestamps = np.arange(start_date, end_date, dtype='datetime64[m]')

# simulate the data
temperature = np.random.normal(temperature_mean, temperature_stddev, num_rows)
pressure = np.random.normal(pressure_mean, pressure_stddev, num_rows) / 100     # Scale pressure by a factor of 100
wind_speed = np.random.normal(wind_speed_mean, wind_speed_stddev, num_rows)
rpm = rpm_mean + 0.5*(wind_speed - wind_speed_mean) + np.random.normal(0, rpm_stddev, num_rows)
energy_output = energy_output_mean + 0.3 * (rpm - rpm_mean) + np.random.normal(0, energy_output_stddev, num_rows)

turbine_data = {
    'timestamps': timestamps,
    'temperature': temperature,
    'pressure': pressure,
    'wind_speed': wind_speed,
    'rpm': rpm,
    'energy_output': energy_output
}

df = pd.DataFrame(turbine_data)
print(df)

# export the data to a csv file
df.to_csv('turbine_data.csv', sep=',', index=False, encoding='utf-8')

# Plot the data using seaborn
sns.pairplot(df)
plt.show()

# Plot the data using matplotlib
df = df.set_index('timestamps')
df[-100:].plot()
plt.title('Turbine Data')
plt.show()
