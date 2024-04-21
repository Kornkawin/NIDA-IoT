import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as md
from temperature_db import *

print("Running temperature_analytics.py ...")
DATABASE = 'temperature_sensor.sqlite3'
cnx = create_connection(DATABASE)
TemperatureSensor.setup(cnx)
# for displaying the plot
plt.rcParams["font.size"] = 10
TIME_INTERVAL = 10      # unit in minutes


if __name__ == '__main__':
    # Load the data from sqlite3 database
    # Convert the data to a pandas DataFrame
    df = pandas.DataFrame([vars(item) for item in TemperatureSensor.objects])
    df['timestamp'] = pandas.to_datetime(df['timestamp'])

    # Display the data types
    print('Data types: ')
    print(df.dtypes)
    # Display the data description
    set_devices = df['device_name'].unique()
    print('All Devices: ', set_devices, '\n')

    # Display description of simulation data
    print('===========================================================')
    print('Device Name: temperature_sim')
    print('===========================================================')
    sim_data = df[df['device_name'] == 'temperature_sim']
    if sim_data.empty:
        print('No simulation data available')
    else:
        print(sim_data['temperature'].describe(), '\n')
        print(sim_data, '\n')
        # Plot the simulation data
        # get latest 10 minutes data
        sim_data = sim_data.sort_values('timestamp')
        sim_data = sim_data[sim_data['timestamp'] > sim_data['timestamp'].max() - pandas.Timedelta(minutes=TIME_INTERVAL)]
        sim_data.set_index('timestamp', inplace=True, drop=True)
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.autofmt_xdate()
        plt.title('Simulated Temperature Data')
        plt.ylabel('Temperature')
        plt.xticks(rotation=45)
        xfmt = md.DateFormatter('%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot('temperature', data=sim_data, label='temperature_sim')
        plt.show()

    # Display description of real data
    print('===========================================================')
    print('Device Name: temperature_real')
    print('===========================================================')
    real_data = df[df['device_name'] == 'temperature_real']
    if real_data.empty:
        print('No real data available')
    else:
        print(real_data['temperature'].describe(), '\n')
        print(real_data, '\n')
        plt.plot(real_data['temperature'])
        # Plot the real data
        # get latest 10 minutes data
        real_data = real_data.sort_values('timestamp')
        real_data = real_data[real_data['timestamp'] > real_data['timestamp'].max() - pandas.Timedelta(minutes=TIME_INTERVAL)]
        real_data.set_index('timestamp', inplace=True, drop=True)
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.autofmt_xdate()
        plt.title('Real Temperature Data')
        plt.ylabel('Temperature')
        plt.xticks(rotation=45)
        xfmt = md.DateFormatter('%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot('temperature', data=real_data, label='temperature_real')
        plt.show()
