__author__ = 'MMxs3d'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import numpy as np
from itertools import product


#INITIALIZATION
start=[1, 1, 2011]
end=[31, 12, 2011]
dt_start = dt.datetime(start[2], start[1], start[0])
dt_end = dt.datetime(end[2], end[1], end[0])
dt_timeofday = dt.timedelta(hours=16)
ls_symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
noVal=-100000000

#Preparing Data Access From Yahoo
c_dataobj = da.DataAccess('Yahoo')



def simulate(dt_start, dt_end, ls_symbols, attribution):

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    #Checking validity of attribution
    if sum(attribution)!=1:
        return {'avg': noVal, 'std': noVal, 'sharpe': noVal}

    #Getting required data from Yahoo
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    #Setting up a dictionary to easily access the values
    d_data = dict(zip(ls_keys, ldf_data))

    #Portfolio value and daily returns
    na_price=d_data['close'].values
    na_normalized_price=na_price/na_price[0, :]
    na_portfolio_price=np.dot(na_normalized_price,np.asmatrix(attribution).transpose())
    na_portfolio_rets=na_portfolio_price.copy()
    na_portfolio_rets=tsu.daily(na_portfolio_rets)

    #Computing Sharpe Ratio
    avg_daily_ret=np.average(na_portfolio_rets)
    std_daily_rets=np.std(na_portfolio_rets)
    sharpe_ratio=(avg_daily_ret/std_daily_rets)*np.sqrt(du.getNYSEdays(dt_start,dt_end, dt_timeofday).__len__())

    #Returning values
    return {'avg':avg_daily_ret, 'std':std_daily_rets, 'sharpe': sharpe_ratio}


def optimalAlloc(dt_start, dt_end, ls_symbols):
    posValues=np.arange(0, 1.1, 0.1)
    firstIteration = True

    for i in product(posValues, repeat=len(ls_symbols)):
        if firstIteration:
            retValOpt=simulate(dt_start, dt_end, ls_symbols, i)
            optimAlloc=i
            firstIteration = False
        else:
            retVal=simulate(dt_start, dt_end, ls_symbols, i)
            if (retVal['sharpe']>retValOpt['sharpe']):
                optimAlloc=i
                retValOpt=retVal

    return optimAlloc, retValOpt



def main():
    #Computing Optinal Values
    optimAll, optimVal=optimalAlloc(dt_start, dt_end, ls_symbols)

    #Printing Results
    print "Symbols: ", ls_symbols
    print "Start date: ", dt_start
    print "End date: ", dt_end
    print "Optimal Allocation: ", optimAll
    print "Optimal Values: ", optimVal


main()

