# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 18:05:11 2022

@author: dtket
"""

# import needed libraries
import warnings
warnings.simplefilter(action='ignore')
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data as web
#import seaborn as sns
from scipy.stats import norm
from scipy import stats
import scipy
# Make function for calls to Yahoo Finance
def get_adj_close(ticker, start, end):
    '''
    A function that takes ticker symbols, starting period, ending period
    as arguments and returns with a Pandas DataFrame of the Adjusted Close Prices
    for the tickers from Yahoo Finance
    '''
    num_tries = 0
    start = start
    end = end
    while (num_tries<=5):
        try:
            num_tries=num_tries+1
            info = web.DataReader(ticker, data_source='yahoo', start=start, end=end, retry_count= 10)['Adj Close']
            return pd.DataFrame(info)
        except:
            print("ERROR #", str(num_tries)," ", ticker)
        
        
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def calc_beta(df,market):
#    df.values.reshape(2,-1)
    np_array = df.values
#    market.values.reshape(1,-1)
    np_array2 = market.values
    m = np_array[:] # market returns are column zero from numpy array
    s = np_array2[:,0] # stock returns are column one from numpy array
    if (m.size==s.size):
        1
    elif (m.size<s.size):
        s = s[:m.size]
    else:
        m = m[:s.size]
    covariance = np.cov(s,m) # Calculate covariance between stock and market
    beta = covariance[0,1]/covariance[1,1]
    return beta
def calc_rsi(close):
    delta = close.diff()     
# Get rid of the first row, which is NaN since it did not have a previous 
# row to calculate the differences
    delta = delta[1:]   
        # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.clip(lower=0), delta.clip(upper=0)
        # Calculate the EWMA
    roll_up = up.ewm(span=window_length).mean()
    roll_down = down.abs().ewm(span=window_length).mean()
        # Calculate the RSI based on EWMA
    RS = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + RS))    
    return rsi



num_stocks = 1 #how many to graph
num_years = 1 #how long analysis
num_days_ago=0
num_months_ago= 0

for i in range(4):
    tic = time.perf_counter()
    print('i = '+str(i))
    d = datetime.timedelta(days = i)
    now = datetime.datetime.now()
    now = now - d
    start  =str(now.day)+ '/'+str(now.month)+'/'+  str(now.year-num_years)
    #start_ =str(now.day)+ '_'+str(now.month)+'_'+  str(now.year-num_years)
    end = str(now.day)+ '/'+str(now.month)+'/'+  str(now.year)
    #end_ = str(now.day-num_days_ago)+ '_'+str(now.month-num_months_ago)+'_'+  str(now.year)
    end_ = str(now.year)+ '_'+str(now.month)+'_'+  str(now.day)
    #just bc yahoo finance formats it  DDMMYYYY doesnt mean i cant change it  in my own file formats
    
    
    #############################################
    s_p500 = ['GOOGL','MMM','ABT',	'ABBV',	'ABMD',	'ACN',	'ATVI',	'ADBE',	'AMD',	'AAP',	'AES',	'AFL',	'A',	'APD',	'AKAM',	'ALK',	'ALB',	'ARE',	'ALGN',	'ALLE',	'LNT',	'ALL',	'GOOG',	'MO',	'AMZN',	'AMCR',	'AEE',	'AAL',	'AEP',	'AXP',	'AIG',	'AMT',	'AWK',	'AMP',	'ABC',	'AME',	'AMGN',	'APH',	'ADI',	'ANSS',	'ANTM',	'AON',	'AOS',	'APA',	'AAPL',	'AMAT',	'APTV',	'ADM',	'ANET',	'AJG',	'AIZ',	'T',	'ATO',	'ADSK',	'ADP',	'AZO',	'AVB',	'AVY',	'BKR',	'BLL',	'BAC',	'BBWI',	'BAX',	'BDX',	'BBY',	'BIO',	'BIIB',	'BLK',	'BK',	'BA',	'BKNG',	'BWA',	'BXP',	'BSX',	'BMY',	'AVGO',	'BR',	'CHRW',	'CDNS',	'CZR',	'CPB',	'COF',	'CAH',	'KMX',	'CCL',	'CARR',	'CTLT',	'CAT',	'CBOE',	'CBRE',	'CDW',	'CE',	'CNC',	'CNP',	'CERN',	'CF',	'CRL',	'SCHW',	'CHTR',	'CVX',	'CMG',	'CB',	'CHD',	'CI',	'CINF',	'CTAS',	'CSCO',	'C',	'CFG',	'CTXS',	'CLX',	'CME',	'CMS',	'KO',	'CTSH',	'CL',	'CMCSA',	'CMA',	'CAG',	'COP',	'ED',	'STZ',	'COO',	'CPRT',	'GLW',	'CTVA',	'COST',	'CCI',	'CSX',	'CMI',	'CVS',	'DHI',	'DHR',	'DRI',	'DVA',	'DE',	'DAL',	'XRAY',	'DVN',	'DXCM',	'FANG',	'DLR',	'DFS',	'DISCA',	'DISCK',	'DISH',	'DG',	'DLTR',	'D',	'DPZ',	'DOV',	'DOW',	'DTE',	'DUK',	'DRE',	'DD',	'DXC',	'EMN',	'ETN',	'EBAY',	'ECL',	'EIX',	'EW',	'EA',	'EMR',	'ENPH',	'ETR',	'EOG',	'EFX',	'EQIX',	'EQR',	'ESS',	'EL',	'ETSY',	'EVRG',	'ES',	'RE',	'EXC',	'EXPE',	'EXPD',	'EXR',	'XOM',	'FFIV',	'FB',	'FAST',	'FRT',	'FDX',	'FIS',	'FITB',	'FE',	'FRC',	'FISV',	'FLT',	'FMC',	'F',	'FTNT',	'FTV',	'FBHS',	'FOXA',	'FOX',	'BEN',	'FCX',	'GPS',	'GRMN',	'IT',	'GNRC',	'GD',	'GE',	'GIS',	'GM',	'GPC',	'GILD',	'GL',	'GPN',	'GS',	'GWW',	'HAL',	'HBI',	'HIG',	'HAS',	'HCA',	'PEAK',	'HSIC',	'HSY',	'HES',	'HPE',	'HLT',	'HOLX',	'HD',	'HON',	'HRL',	'HST',	'HWM',	'HPQ',	'HUM',	'HBAN',	'HII',	'IEX',	'IDXX',	'INFO',	'ITW',	'ILMN',	'INCY',	'IR',	'INTC',	'ICE',	'IBM',	'IP',	'IPG',	'IFF',	'INTU',	'ISRG',	'IVZ',	'IPGP',	'IQV',	'IRM',	'JKHY',	'J',	'JBHT',	'SJM',	'JNJ',	'JCI',	'JPM',	'JNPR',	'K',	'KEY',	'KEYS',	'KMB',	'KIM',	'KMI',	'KLAC',	'KHC',	'KR',	'LHX',	'LH',	'LRCX',	'LW',	'LVS',	'LEG',	'LDOS',	'LEN',	'LLY',	'LNC',	'LIN',	'LYV',	'LKQ',	'LMT',	'L',	'LOW',	'LUMN',	'LYB',	'MTB',	'MRO',	'MPC',	'MKTX',	'MAR',	'MMC',	'MLM',	'MAS',	'MA',	'MKC',	'MCD',	'MCK',	'MDT',	'MRK',	'MET',	'MTD',	'MGM',	'MCHP',	'MU',	'MSFT',	'MAA',	'MRNA',	'MHK',	'TAP',	'MDLZ',	'MPWR',	'MNST',	'MCO',	'MS',	'MOS',	'MSI',	'MSCI',	'NDAQ',	'NTAP',	'NFLX',	'NWL',	'NEM',	'NWSA',	'NWS',	'NEE',	'NLSN',	'NKE',	'NI',	'NSC',	'NTRS',	'NOC',	'NLOK',	'NCLH',	'NOV',	'NRG',	'NUE',	'NVDA',	'NVR',	'NXPI',	'ORLY',	'OXY',	'ODFL',	'OMC',	'OKE',	'ORCL',	'OGN',	'OTIS',	'PCAR',	'PKG',	'PH',	'PAYX',	'PAYC',	'PYPL',	'PENN',	'PNR',	'PBCT',	'PEP',	'PKI',	'PRGO',	'PFE',	'PM',	'PSX',	'PNW',	'PXD',	'PNC',	'POOL',	'PPG',	'PPL',	'PFG',	'PG',	'PGR',	'PLD',	'PRU',	'PTC',	'PEG',	'PSA',	'PHM',	'PVH',	'QRVO',	'PWR',	'QCOM',	'DGX',	'RL',	'RJF',	'RTX',	'O',	'REG',	'REGN',	'RF',	'RSG',	'RMD',	'RHI',	'ROK',	'ROL',	'ROP',	'ROST',	'RCL',	'SPGI',	'CRM',	'SBAC',	'SLB',	'STX',	'SEE',	'SRE',	'NOW',	'SHW',	'SPG',	'SWKS',	'SNA',	'SO',	'LUV',	'SWK',	'SBUX',	'STT',	'STE',	'SYK',	'SIVB',	'SYF',	'SNPS',	'SYY',	'TMUS',	'TROW',	'TTWO',	'TPR',	'TGT',	'TEL',	'TDY',	'TFX',	'TER',	'TSLA',	'TXN',	'TXT',	'TMO',	'TJX',	'TSCO',	'TT',	'TDG',	'TRV',	'TRMB',	'TFC',	'TWTR',	'TYL',	'TSN',	'UDR',	'ULTA',	'USB',	'UAA',	'UA',	'UNP',	'UAL',	'UNH',	'UPS',	'URI',	'UHS',	'UNM',	'VLO',	'VTR',	'VRSN',	'VRSK',	'VZ',	'VRTX',	'VFC',	'VIAC',	'VTRS',	'V',	'VNO',	'VMC',	'WRB',	'WAB',	'WMT',	'WBA',	'DIS',	'WM',	'WAT',	'WEC',	'WFC',	'WELL',	'WST',	'WDC',	'WU',	'WRK',	'WY',	'WHR',	'WMB',	'WLTW',	'WYNN',	'XEL',	'XLNX',	'XYL',	'YUM',	'ZBRA',	'ZBH',	'ZION',	'ZTS']
    ###################less code and neater but significantly increased runtime
    window_length = 14
    index=0
    
    adj_list=[None] * len(s_p500)
    bol_list = [None]* len(s_p500)
    rsi_list = [None]* len(s_p500)
    xcel_list = pd.DataFrame(np.zeros([len(s_p500),7]) ,index=s_p500, columns=['Stock','Current','Expected','Variance','Bollinger','RSI','Beta'])
    xcel_list['Stock'] = xcel_list['Stock'].astype(str)
    SPY=get_adj_close("SPY",start,end)      

    for name in s_p500:
#            print(name)
            adj_list = get_adj_close(name,start,end)
            adj_list['30 Day MA']   = adj_list['Adj Close'].rolling(window=30).mean()
            adj_list['30 Day STD']  = adj_list['Adj Close'].rolling(window=30).std()
            
#            adj_list['Upper Band'] = adj_list['30 Day MA'] + (adj_list['30 Day STD'] * 2)
#            adj_list['Lower Band'] = adj_list['30 Day MA'] - (adj_list['30 Day STD'] * 2)
#            adj_list['Upper Band2'] = adj_list['30 Day MA'] + (adj_list['30 Day STD'] * 3)
#            adj_list['Lower Band2'] = adj_list['30 Day MA'] - (adj_list['30 Day STD'] * 3)
#            adj_list['Upper Band3'] = adj_list['30 Day MA'] + (adj_list['30 Day STD'] * 1)
#            adj_list['Lower Band3'] = adj_list['30 Day MA'] - (adj_list['30 Day STD'] * 1)
            
            adj_list['Bollinger'] =(adj_list['Adj Close'] - adj_list['30 Day MA'] ) / (adj_list['30 Day STD'] * 1)    
            close = adj_list['Adj Close']
            adj_list['RSI'] = calc_rsi(close)
        #    item['daily returns']=close.pct_change()
            adj_list['Beta'] = calc_beta(close,SPY)
            
            
            timerange=7
            log_returns = np.log(1+close.pct_change())
            u = log_returns.mean()
            var = log_returns.var()
            drift = u - (0.5*var)
            stddev = log_returns.std()
            daily_returns = np.exp(drift + stddev * norm.ppf(np.random.rand(timerange,10000)))
            S0 = close.iloc[-1]
            
            price_list = np.zeros_like(daily_returns)
            price_list.shape
            price_list[0] = S0
            
            for t in range(1,timerange):
                price_list[t] = price_list[t-1]*daily_returns[t]
        
            data = pd.DataFrame(price_list).iloc[-1]
        #    kde = stats.gaussian_kde(data)
        #    x = np.linspace(data.min(), data.max(), 100)
        #    p = kde(x);
        ##    plt.plot(p)
        #    dx = x[1]-x[0]
        #    x_2 = x*x
        #    total= sum(p*dx)
        #    mean_x = sum(x*p*dx)
            mean2_x= np.mean(data)
        #    var_x = sum((x-mean_x)*(x-mean_x)*p*dx)
            var2_x = np.var(data)/mean2_x
            xcel_list['Stock'][index]=s_p500[index]
            xcel_list['Current'][index]=S0
            xcel_list['Expected'][index]=mean2_x
            xcel_list['Variance'][index]=var2_x
            xcel_list['Bollinger'][index]= adj_list['Bollinger'][-1]
            xcel_list['RSI'][index]=adj_list['RSI'][-1]
            xcel_list['Beta'][index]=adj_list['Beta'][-1]
        #    print(s_p500[index] + " expected value: " + str(mean_x) + " current value: " + str(S0))
            index = index+1
            toc = time.perf_counter()
            print(index)
            print(str((toc-tic)/index))
                
    writer = pd.ExcelWriter(end_+'.xlsx')
    
    xcel_list.to_excel(writer, sheet_name = end_, index = False)
    writer.save()    
