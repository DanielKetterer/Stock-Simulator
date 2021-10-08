# import needed libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from pandas_datareader import data as web
#input("press enter to continue")
# Make function for calls to Yahoo Finance
def get_adj_close(ticker, start, end,adj_list,name_list):
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
            print(ticker)
            temp = pd.DataFrame(info)
            temp.fillna(0)
            adj_list.append(temp)
            name_list.append(ticker)
            return adj_list,name_list
        except:
            print("ERROR #", str(num_tries)," ", ticker)
            if (num_tries == 5):
                  return adj_list,name_list
                  
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def buy(index,price,budget,shares):
    if (price <= budget):
        shares[index]=shares[index]+1
#        print("buy")
        budget = budget - price
    return budget
def sell(index,price,budget,shares): 
    if (shares[index] >= 1):
        shares[index]=shares[index]-1
#        print("sell")
        budget = budget + price
    return budget

#############################################
s_p500 = ['MMM',	'ABT',	'ABBV',	'ABMD',	'ACN',	'ATVI',	'ADBE',	'AMD',	'AAP',	'AES',	'AFL',	'A',	'APD',	'AKAM',	'ALK',	'ALB',	'ARE',	'ALGN',	'ALLE',	'LNT',	'ALL',	'GOOGL',	'GOOG',	'MO',	'AMZN',	'AMCR',	'AEE',	'AAL',	'AEP',	'AXP',	'AIG',	'AMT',	'AWK',	'AMP',	'ABC',	'AME',	'AMGN',	'APH',	'ADI',	'ANSS',	'ANTM',	'AON',	'AOS',	'APA',	'AAPL',	'AMAT',	'APTV',	'ADM',	'ANET',	'AJG',	'AIZ',	'T',	'ATO',	'ADSK',	'ADP',	'AZO',	'AVB',	'AVY',	'BKR',	'BLL',	'BAC',	'BAX',	'BDX',	'BBY',	'BIO',	'BIIB',	'BLK',	'BK',	'BA',	'BKNG',	'BWA',	'BXP',	'BSX',	'BMY',	'AVGO',	'BR','CHRW',	'COG',	'CDNS',	'CZR',	'CPB',	'COF',	'CAH',	'KMX',	'CCL',	'CTLT',	'CAT',	'CBOE',	'CBRE',	'CDW',	'CE',	'CNC',	'CNP',	'CERN',	'CF',	'CRL',	'SCHW',	'CHTR',	'CVX',	'CMG',	'CB',	'CHD',	'CI',	'CINF',	'CTAS',	'CSCO',	'C',	'CFG',	'CTXS',	'CLX',	'CME',	'CMS',	'KO',	'CTSH',	'CL',	'CMCSA',	'CMA',	'CAG',	'COP',	'ED',	'STZ',	'COO',	'CPRT',	'GLW',	'CTVA',	'COST',	'CCI',	'CSX',	'CMI',	'CVS',	'DHI',	'DHR',	'DRI',	'DVA',	'DE',	'DAL',	'XRAY',	'DVN',	'DXCM',	'FANG',	'DLR',	'DFS',	'DISCA',	'DISCK',	'DISH',	'DG',	'DLTR',	'D',	'DPZ',	'DOV',	'DOW',	'DTE',	'DUK',	'DRE',	'DD',	'DXC',	'EMN',	'ETN',	'EBAY',	'ECL',	'EIX',	'EW',	'EA',	'EMR',	'ENPH',	'ETR',	'EOG',	'EFX',	'EQIX',	'EQR',	'ESS',	'EL',	'ETSY',	'EVRG',	'ES',	'RE',	'EXC',	'EXPE',	'EXPD',	'EXR',	'XOM',	'FFIV',	'FB',	'FAST',	'FRT',	'FDX',	'FIS',	'FITB',	'FE',	'FRC',	'FISV',	'FLT',	'FMC',	'F',	'FTNT',	'FTV',	'FBHS',	'FOXA',	'FOX',	'BEN',	'FCX',	'GPS',	'GRMN',	'IT',	'GNRC',	'GD',	'GE',	'GIS',	'GM',	'GPC',	'GILD',	'GL',	'GPN',	'GS',	'GWW',	'HAL',	'HBI',	'HIG',	'HAS',	'HCA',	'PEAK',	'HSIC',	'HSY',	'HES',	'HPE',	'HLT',	'HOLX',	'HD',	'HON',	'HRL',	'HST',	'HWM',	'HPQ',	'HUM',	'HBAN',	'HII',	'IEX',	'IDXX',	'INFO',	'ITW',	'ILMN',	'INCY',	'IR',	'INTC',	'ICE',	'IBM',	'IP',	'IPG',	'IFF',	'INTU',	'ISRG',	'IVZ',	'IPGP',	'IQV',	'IRM',	'JKHY',	'J',	'JBHT',	'SJM',	'JNJ',	'JCI',	'JPM',	'JNPR',	'KSU',	'K',	'KEY',	'KEYS',	'KMB',	'KIM',	'KMI',	'KLAC',	'KHC',	'KR',	'LHX',	'LH',	'LRCX',	'LW',	'LVS',	'LEG',	'LDOS',	'LEN',	'LLY',	'LNC',	'LIN',	'LYV',	'LKQ',	'LMT',	'L',	'LOW',	'LYB',	'MTB',	'MRO',	'MPC',	'MKTX',	'MAR',	'MMC',	'MLM',	'MAS',	'MA',	'MKC',	'MXIM',	'MCD',	'MCK',	'MDT',	'MRK',	'MET',	'MTD',	'MGM',	'MCHP',	'MU',	'MSFT',	'MAA',	'MRNA',	'MHK',	'TAP',	'MDLZ',	'MPWR',	'MNST',	'MCO',	'MS',	'MOS',	'MSI',	'MSCI',	'NDAQ',	'NTAP',	'NFLX',	'NWL',	'NEM',	'NWSA',	'NWS',	'NEE',	'NLSN',	'NKE',	'NI',	'NSC',	'NTRS',	'NOC',	'NLOK',	'NCLH',	'NOV',	'NRG',	'NUE',	'NVDA',	'NVR',	'NXPI',	'ORLY',	'OXY',	'ODFL',	'OMC',	'OKE',	'ORCL',	'PCAR',	'PKG',	'PH',	'PAYX',	'PAYC',	'PYPL',	'PENN',	'PNR',	'PBCT',	'PEP',	'PKI',	'PRGO',	'PFE',	'PM',	'PSX',	'PNW',	'PXD',	'PNC',	'POOL',	'PPG',	'PPL',	'PFG',	'PG',	'PGR',	'PLD',	'PRU',	'PTC',	'PEG',	'PSA',	'PHM',	'PVH',	'QRVO',	'PWR',	'QCOM',	'DGX',	'RL',	'RJF',	'RTX',	'O',	'REG',	'REGN',	'RF',	'RSG',	'RMD',	'RHI',	'ROK',	'ROL',	'ROP',	'ROST',	'RCL',	'SPGI',	'CRM',	'SBAC',	'SLB',	'STX',	'SEE',	'SRE',	'NOW',	'SHW',	'SPG',	'SWKS',	'SNA',	'SO',	'LUV',	'SWK',	'SBUX',	'STT',	'STE',	'SYK',	'SIVB',	'SYF',	'SNPS',	'SYY',	'TMUS',	'TROW',	'TTWO',	'TPR',	'TGT',	'TEL',	'TDY',	'TFX',	'TER',	'TSLA',	'TXN',	'TXT',	'TMO',	'TJX',	'TSCO',	'TT',	'TDG',	'TRV',	'TRMB',	'TFC',	'TWTR',	'TYL',	'TSN',	'UDR',	'ULTA',	'USB',	'UAA',	'UA',	'UNP',	'UAL',	'UNH',	'UPS',	'URI',	'UHS',	'UNM',	'VLO',	'VTR',	'VRSN',	'VRSK',	'VZ',	'VRTX',	'VFC',	'VIAC',	'VTRS',	'V',	'VNO',	'VMC',	'WRB',	'WAB',	'WMT',	'WBA',	'DIS',	'WM',	'WAT',	'WEC',	'WFC',	'WELL',	'WST',	'WDC',	'WU',	'WRK',	'WY',	'WHR',	'WMB',	'WLTW',	'WYNN',	'XEL',	'XLNX',	'XYL',	'YUM',	'ZBRA',	'ZBH',	'ZION',	'ZTS']
#
# s_p500 = ['SPY','GOOGL', 'AMZN','AAPL','MSFT','TSLA']    
####################less code and neater 
index=0
name_list=[]
#adj_list=[None] * len(s_p500)



adj_list = []

for name in s_p500:
    adj_list,name_list = get_adj_close(name,'10/08/2020','10/08/2021',adj_list,name_list)
       
print("done1")
for it in (adj_list):
#    print(namestr(item, globals()))
    it['30 Day MA']   = it['Adj Close'].rolling(window=30).mean()
    it['20 Day MA']  = it['Adj Close'].rolling(window=20).mean()
    it['30 Day STD']  = it['Adj Close'].rolling(window=30).std()
    it['Upper Band'] = it['30 Day MA'] + (it['30 Day STD'] * 2)
    it['Lower Band'] = it['30 Day MA'] - (it['30 Day STD'] * 2)
    it['Bollinger'] =(it['Adj Close']- it['30 Day MA'] ) / (it['30 Day STD'] * 1)
    close = it['Adj Close']
    delta = close.diff()
# Get rid of the first row, which is NaN since it did not have a previous 
# row to calculate the differences
    delta = delta[1:] 

# Make the positive gains (up) and negative gains (down) Series
    up, down = delta.clip(lower=0), delta.clip(upper=0)
# Calculate the EWMA
    roll_up = up.ewm(span=14).mean()
    roll_down = down.abs().ewm(span=14).mean()
# Calculate the RSI based on EWMA
    RS = roll_up / roll_down
    it['RSI'] = 100.0 - (100.0 / (1.0 + RS))



print("done2")
global budget_ma
budget_ma   = 1000000
budget_hold = 1000000
budget_bol  = 1000000
budget_rsi  = 1000000

bma = [0] * len(it)
bma = np.array(bma)
bho = [0] * len(it)
bho = np.array(bho)
bbo= [0] * len(it)
bbo = np.array(bbo)
brs= [0] * len(it)
brs = np.array(brs)

prices = [0] * len(adj_list)
prices = np.array(prices,dtype='float64')
prices2 = [0] * len(adj_list)
prices2 = np.array(prices2,dtype='float64')
prices3 = [0] * len(adj_list)
prices3 = np.array(prices3,dtype='float64')
prices4 = [0] * len(adj_list)
prices4 = np.array(prices4,dtype='float64')

shares = [0] * len(adj_list) 
shares2 = [0] * len(adj_list)
shares3 = [0] * len(adj_list)
shares4 = [0] * len(adj_list)



#  strategy 1 : moving average
index2=0
for time in range(len(it)):
    index = 0    
    for it in (adj_list):
        if (time < len(it)):
#       print(it['Adj Close'][time])
            price = it['Adj Close'][time]
            if(it['30 Day MA'][time] < it['20 Day MA'][time]):
               budget_ma = buy(index,price,budget_ma,shares)
            elif(it['30 Day MA'][time] >= it['20 Day MA'][time]):
               budget_ma = sell(index,price,budget_ma,shares)
            else:
               1
            prices[index] = price
            index=index+1
    if (index2 < len(it)):
        bma[index2] = budget_ma + np.dot(prices,shares) 
        index2 = index2 + 1
print("done3")

####################################################
# strategy 3 bollinger
index2=0
for time in range(len(it)):
    index = 0    
    for it in (adj_list):
        if (time < len(it)):
#       print(it['Adj Close'][time])
            price = it['Adj Close'][time]
            if(it['Bollinger'][time] < -2):
               budget_bol = buy(index,price,budget_bol,shares3)
            elif(it['Bollinger'][time] > 2):
               budget_bol = sell(index,price,budget_bol,shares3)
            else:
               1
            prices3[index] = price
            index=index+1
    if (index2 < len(it)):
        bbo[index2] = budget_bol + np.dot(prices3,shares3) 
        index2 = index2 + 1
print("done4")

################################################
#strategy 2 hold
index = 0         
for it in (adj_list):
#       print(it['Adj Close'][time])
#    print("index: ",index)
    if (index>=57):
        1
    initial_price = it['Adj Close'][0]
#    while (shares2[index] < shares[index]):
#        budget_hold = buy(index,initial_price,budget_hold,shares2)
    shares2[index]=shares[index]
    budget_hold = budget_hold - initial_price*shares[index]
#    print(shares2[index])
    index=index+1
print("done5")
###########################################################
#strategy4 rsi
index2=0
for time in range(len(it)):
    index = 0    
    for it in (adj_list):
        if (time < len(it)):
#       print(it['Adj Close'][time])
            price = it['Adj Close'][time]
            if(it['RSI'][time] < 30):
               budget_rsi = buy(index,price,budget_rsi,shares4)
            elif(it['RSI'][time] > 70):
               budget_rsi = sell(index,price,budget_rsi,shares4)
            else:
               1 # just hold
            prices4[index] = price
            index=index+1
    if (index2 < len(it)):
        brs[index2] = budget_rsi + np.dot(prices4,shares4) 
        index2 = index2 + 1
print("done6")



# to get the graph of the hold strategy   
##########################################
index2 = 0    
for time in range(len(it)):
    index = 0    
    for it in (adj_list):
        if (time < len(it)):
#       print(it['Adj Close'][time])
            price = it['Adj Close'][time]
            prices2[index] = price
            index=index+1
    if (index2 < len(it)):
        bho[index2] = budget_hold + np.dot(prices2,shares2) 
        index2 = index2 + 1




    
#########################################
print("done7")
# to compare end growth sell off all remaining assets
#######################################################################
index = 0         
for it in (adj_list):
#       print(it['Adj Close'][time])
    time = len(it)
    final_price = it['Adj Close'][time-1]
    while (shares[index] > 0):
        budget_ma = sell(index,final_price,budget_ma,shares)
    index=index+1           
print("done8")
index = 0
         
for it in (adj_list):
#       print(it['Adj Close'][time])
    time = len(it)
    final_price = it['Adj Close'][time-1]
    while (shares2[index] > 0):
        budget_hold = sell(index,final_price,budget_hold,shares2)
    index=index+1   

index = 0        
for it in (adj_list):
#       print(it['Adj Close'][time])
    time = len(it)
    final_price = it['Adj Close'][time-1]
    while (shares3[index] > 0):
        budget_bol = sell(index,final_price,budget_bol,shares3)
    index=index+1   

index = 0        
for it in (adj_list):
#       print(it['Adj Close'][time])
    time = len(it)
    final_price = it['Adj Close'][time-1]
    while (shares4[index] > 0):
        budget_rsi = sell(index,final_price,budget_rsi,shares4)
    index=index+1  
     
print("done")
plt.rcParams["figure.figsize"] = (20,20)
plt.plot(bma)    
plt.plot(bho)
plt.plot(bbo)
plt.plot(brs)
plt.legend(['Moving Average','Hold Strategy', 'Bollinger Band','RSI'])    
#    def selloff(budget,shares,time):
#    index = 0         
#    for it in (adj_list):
#    #       print(it['Adj Close'][time])
#        price = it['Adj Close'][time]
#        while (shares[index] > 0):
#            budget = sell(index,price,budget,shares)
#        index=index+1  
#    return budget