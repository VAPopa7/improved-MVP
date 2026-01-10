import yfinance as yf
import os
import pandas as pd

# Function that normalizes the ticker
def normalize_ticker(ticker):
    if ticker.endswith("Q") or ticker.endswith("*"):
        ticker = ticker[:-1]
    ticker = ticker.replace("/", "-").replace(".", "-").strip()
    return ticker

# Continuing entity after rebrand, rename, acquisitions and mergers
continuing_entities = {"FB": "META", "GOOG": "GOOGL", "VIAB": "PARA", "CBS": "PARA", "ANTM": "ELV", "WLP": "ELV",
                        "UTX": "RTX", "RTN": "RTX", "TWX": "DIS", "YHOO":"", "AABA":"", "SYMC": "GEN",
                        "INFO": "SPGI", "LIFE": "ILMN", "UA": "UAA", "DISCA": "WBD", "DISCK": "WBD", "TWC": "CHTR",
                        "NYX": "ICE", "PX": "LIN", "GENZ": "SNY", "BRKB":"BRK-B"}

# Index artificats; non-tradeable
index_artificats = {"", "-", "0R01", "8686", "A60", "AG4", "GGQ7", "MIL-", "PA9", "QCI", "RN7", "T3W1",
                    "UUM", "USX1", "VX1", "MX4A", "SYF-W", "KMIWS", "OXYWSWI", "NSM-2", "GAS-2", "THC1", 
                    "RTN1", "UAC-C", "DC7", "4XS", "6COP", "3EC"}

# Delisted / bankrupt; no usable price history
delisted_bankrupt = {"ANRZQ", "CITGQ", "OSHWQ", "OSHSQ", "SHLDQ", "RSHCQ", "NEBLQ", "MNKKQ", "CPPRQ", "EKDKQ",
                    "DOFSQ", "MTLQQ", "BBBY", "FTR", "WIN", "EVHC", "WCG", "SIVB", "SBNY", "FRC", 
                    "LVLT", "ENDP", "CHK", "WFT", "RIG", "GGP", "MNK", "OSHSQ", "EKDK", "UTX", "GE"}

# Others; no price data found (possibly delisted)
others = {'BHI', 'WFR', 'HSP', 'MWV', 'COH', 'JNS', 'NDA', 'ACAS', 'KORS', 
          'CFN', 'SIAL', 'SNI', 'MFE', 'SLBA', 'BXLT', 'LLTC', 'ALD', 'MHFI', 'MWW', 'COV', 'LUK', 'SPLS', 'BNI', 'APOL', 'CSC', 'PCP', 'LXK', 'HNZ', 'TYC', 'CBG', 'NOVL', 'DPS', 'KFT', 'ARG', 'GMCR', 'MJN', 'MWZ', 'GAS', 'WFM', 'BDK', 'NVLS', 'CMCSK', 'HCBK', 'HCN', 'LTD', 'CVH', 'WAG', 'WYE', 'SWY', 'XTO', 'PGN', 'MOT', 'SRCL', 'ACS', 'JOY', 'ZMH', 'RAI', 'BCR', 'ACE', 'TSO', 'CVC', 'KRFT', 'JNY', 'AYE', 'STJ', 'LO', 'CEPH', 'PETM', 'BRCM', 'CTX', 'FDO', 'CPGX', 'SCN', 'BJS', 'ROH', 'WYN','DO', 'PXD', 'CDAY', 'HES', 'LSI', 'RHT', 'AKS', 'PKI', 'CELG', 'DEN', 'TMUSR', 'WLTW', 'PARA', 'BLL', 'JNPR', 'RDC', 'ALTR', 'MDP', 'DISHR', 'COG', 'DTV', 'NBL', 'XL', 'ARNC', 'HCP', 'ESV', 'ADS', 'FRX', 'DF', 'AEC1', 'FLT', 'RE', 'TWTR', 'OSHS', 'FLIR', 'MNKK', 'JEC', 'CITG', 'PDCO', 'ANRZ', 'NEBL', 'HFC', 'XEC', 'CERN', 'BFB', 'BIG', 'AVP', 'CTXS', 'STR', 'BHGE', 'PBCT', 'VISA', 'PEAK', 'OSHW', 'CPPR', 'HRS', 'ANSS', 'UNS1', 'QEP', 'LK', 'CXO', 'LM', 'DRE', 'VAR', 'TIF', 'GPS', 'SWN', 'ALXN', 'NLSN', 'MXIM', 'OXY WS WI', 'NLOK', 'WPX', 'WBA', 'DWDP', 'MRO', 'DISH', 'IGT', 'ABC', 'DLPH', 'ABMD', 'MON', 'JWN', 'BLD WI', 'ETFC', 'GEC', 'WYND', 'RSHC', 'CC WI', 'APC', 'MTLQ', 'X', 'ATVI', 'KMI WS', 'LLL', 'KSU', 'PLL', 'WPG', 'MYL', 'TMK', 'WRK', 'XLNX', 'TSS', 'AGN', 'DFS', 'VIAC', 'DOFS', 'RRD', 'FL', 'CTLT', 'DNR', 'FBHS', 'HAWKB', 'CTL', 'DNB', 'PCS', 'CAM', 'SNDK', 'PCL', 'POM', 'PCLN'}

all_files = os.listdir("assets")
all_tickers = set()

# Save all tickers from monthly constituents
for file in all_files:
    constituents = pd.read_csv("assets\\" + file)
    cur_tickers = constituents['ticker'].apply(normalize_ticker)
    cur_tickers = cur_tickers.replace(continuing_entities)
    cur_tickers = cur_tickers.dropna()
    cur_tickers = list(cur_tickers)
    all_tickers.update(cur_tickers)

# Only keep tickers with price data    
excluded = index_artificats | delisted_bankrupt | others
all_tickers = all_tickers - excluded

# Download price data and save to .csv file
prices = yf.download(tickers=sorted(all_tickers), start="2006-01-30", end="2024-10-30")["Close"]
prices.to_csv('historical_data.csv')