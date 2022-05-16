from web3 import Web3
import streamlit as st
import pandas as pd
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from ta.trend import MACD
from ta.momentum import RSIIndicator


# API using Infura Node to obtain blockchain data
infura_url = 'https://mainnet.infura.io/v3/15bf55ae87d142d8b5f0b2c3ba87d1cb'

# Creates w3 instance
w3 = Web3(Web3.HTTPProvider(infura_url))


# Text box to input any Ethereum address and return the Ether balance
def check_latest_block(w3):
    if st.button("Latest Block Number"):
        latest = w3.eth.blockNumber
        st.write(latest)

# function to get the balance in ether of an ethereum address
def check_balance(w3):
    address = st.text_input("Input the address you would like to see the balance of")
    if st.button("Check Ether Balance"):
    # Get balance of address in Wei
        wei_balance = w3.eth.get_balance(address)
    # Convert Wei value to ether
        ether = w3.fromWei(wei_balance, "ether")
    # Return the value in ether
        st.write(ether)

# function to get the details of a transaction hash
def get_transaction(w3):
    # allows user to input transactions hash and push button to obtain details
    txn_hash = st.text_input("Enter a transaction hash")
    if st.button("Get transaction details"):
        txn_details = w3.eth.get_transaction(txn_hash)
        st.write(txn_details)


# Creates empty list
list = []
# obtains latest block number
latest = w3.eth.blockNumber
# Function to obtain last 10 blocks of gas data
def check_gas(w3):
    with st.spinner('Obtaining Historical Block Data...'):
        for i in range(0, 10):
            list.append(w3.eth.getBlock(latest - i)['gasUsed'])
    st.text("Gas Used in Gwei Over Past 10 Blocks")
    # display as bar chat
    st.bar_chart(list)



# Trading Tab - Bollinger Bands Steps and Calculation
def BollBnd(token, moving_avg, std):
    "function to calculate Bollinger Band"

    #gathers price data for each token
    prices = cg.get_coin_market_chart_by_id(id= token, vs_currency='usd', days = 1080, interval='daily')['prices']
    prices_df = pd.DataFrame(prices)
    prices_df = prices_df[1]
    prices_df = pd.DataFrame({token:prices_df})

    #computes simple moving average given user selection
    sma = prices_df[token].rolling(moving_avg).mean()
    sma_df = pd.DataFrame({'moving average':sma})

    #computes upper and lower bollinger bands
    bb_up = sma + (std*sma.rolling(moving_avg).std())
    bb_up_df = pd.DataFrame({'upper band':bb_up})
    bb_lower = sma - (std*sma.rolling(moving_avg).std())
    bb_lower_df = pd.DataFrame({'lower band':bb_lower})

    #creates a dataframe to hold all data
    bollinger_bands = pd.concat([prices_df, sma_df,bb_up_df,bb_lower_df], axis=1)
    # display as line chart
    st.line_chart(bollinger_bands)


# Function to generate MACD and RSI charts using TA.trend and TA.momentum
def macd_rsi(token):
    # Gathers price data
    coin_data = cg.get_coin_market_chart_by_id(id= token, vs_currency='usd', days = 1080, interval='daily')['prices']
    coin_df = pd.DataFrame(coin_data)
    coin_df = coin_df[1]
    coin_df = pd.DataFrame({token:coin_df})
    # Computes MACD and RSI
    macd = MACD(coin_df[f'{token}']).macd()
    rsi = RSIIndicator(coin_df[f'{token}']).rsi()
    # displays as line chart in streamlit
    st.line_chart(macd)
    st.line_chart(rsi)



