from alpha_vantage.timeseries import TimeSeries
import urllib.request # throws errors if you don't import this
import matplotlib.pyplot as plt

ts = TimeSeries(key='SM7GE35DSMNWSBPD', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AMD', interval='1min', outputsize='full')


data['4. close'].plot()
plt.title('Intraday Time Series for MSFT stock (1min)')
plt.show()
