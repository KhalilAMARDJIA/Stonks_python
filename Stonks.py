import time
import datetime
import pandas as pd
import finplot as fplt


################### API request ##############################
api_key = "c08l5dn48v6vku8uk8p0"
basic_url = 'https://finnhub.io/api/v1/stock/'
data_type = "candle"
resolution = "D" # 1, 5, 15, 30, 60, D, W, M
symbol = "BTC-EUR"

from_date = "01/01/2000"
from_date = int(time.mktime(datetime.datetime.strptime(from_date, "%d/%m/%Y").timetuple())) # api accepts only UNIX time

to_date = int(time.time()) # api accepts only UNIX time

url = f'{basic_url}{data_type}?symbol={symbol}&resolution={resolution}&from={from_date}&to={to_date}&token={api_key}&format=csv'

################# Convert url to dataframe ####################


df = pd.read_csv(url)
df['t'] = pd.to_datetime(df['t'], unit='s')
df = df.rename(columns={'t':'time', 'o':'open', 'c':'close', 'h':'high', 'l':'low', 'v':'volume'})


####################### Ploting ##############################

ax,ax2 = fplt.create_plot(symbol, rows=2)

# plot candle sticks
candles = df[['time','open','close','high','low']]
fplt.candlestick_ochl(candles, ax=ax)

# overlay volume on the top plot
volumes = df[['time','open','close','volume']]
fplt.volume_ocv(volumes, ax=ax.overlay())

# put an MA on the close price
fplt.plot(df['time'], df['close'].rolling(25).mean(), ax=ax, legend='ma-25')

# place some dumb markers on low wicks
lo_wicks = df[['open','close']].T.min() - df['low']
df.loc[(lo_wicks>lo_wicks.quantile(0.99)), 'marker'] = df['low']
fplt.plot(df['time'], df['marker'], ax=ax, color='#4a5', style='^', legend='dumb mark')

# draw some random crap on our second plot
fplt.plot(df['time'], np.random.normal(size=len(df)), ax=ax2, color='#927', legend='stuff')
fplt.set_y_range(-1.4, +3.7, ax=ax2) # hard-code y-axis range limitation

# restore view (X-position and zoom) if we ever run this example again
fplt.autoviewrestore()

# we're done
fplt.show()


