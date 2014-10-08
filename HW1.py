__author__ = 'MMxs3d'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

print "QSTK Imported"

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
print "Third Party Libs Imported\n"

ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
t=ls_symbols, "Hey"
print "Tuple tested"

#Setting up timestamps for 2011

dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

#Preparing Data Access From Yahoo
c_dataobj = da.DataAccess('Yahoo')

#Keys for the required data
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

#Getting required data from Yahoo
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

#Setting up a dictionary to easily access the values
d_data = dict(zip(ls_keys, ldf_data))

na_price=d_data['close'].values
na_normalized_price=na_price/na_price[0, :]
na_rets=na_normalized_price.copy()
na_rets=tsu.returnize0(na_rets)

print na_normalized_price



