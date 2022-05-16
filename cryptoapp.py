# imports

from web3 import Web3
import streamlit as st
from streamlit_option_menu import option_menu
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import pandas as pd
from functions import w3, check_latest_block, check_balance, check_gas, get_transaction, BollBnd, macd_rsi
from ta.trend import MACD
from ta.momentum import RSIIndicator

# Streamlit - allows ability to refresh app to see code changes
st.cache(allow_output_mutation=True)

# Sets layout of menu items
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide",
    initial_sidebar_state="auto",)

# Title of page
st.markdown("<h1 style='text-align: center; color: Black;'>Crypto Dashboard</h1>", unsafe_allow_html=True)

# Creates horizontal menu items
selected = option_menu(None, ["Home", "Price Trends", "Trading", 'Etherscan'], 
    icons=['house', 'bar-chart', "activity", 'broadcast'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

# Creates side bar menu items
with st.sidebar:
        selected2 = option_menu(None, ["Layer 1 Tokens", "DeFi Tokens", "NFT / Memes"], 
                icons=['box', 'cash-coin', "emoji-laughing"], 
                menu_icon="cast", default_index=0, orientation="vertical")



# Conditional statement to determine which tokens to pull onto the Home screen
if selected == "Home" and selected2 == 'Layer 1 Tokens':
        # Gathers price data using coingecko api
        layer_1_prices = cg.get_price(ids='ethereum,binancecoin,solana', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, vs_currencies='usd')
        layer_1_prices_df = pd.DataFrame(layer_1_prices).T
        layer_1_prices_df.columns =['Latest Price', 'Market Capitalization', '24H Volume', '24H % Change']
        layer_1_prices_df.index = ['Binance Coin', 'Ethereum', 'Solana']

        # Creates visual of dataframe in st.metric format
        col1, col2, col3 = st.columns(3)
        col1.metric("BNB Price", layer_1_prices_df.loc['Binance Coin', 'Latest Price'], layer_1_prices_df.loc['Binance Coin', '24H % Change'].round(2))
        col2.metric("Eth Price", layer_1_prices_df.loc['Ethereum', 'Latest Price'], layer_1_prices_df.loc['Ethereum', '24H % Change'].round(2))
        col3.metric("Solana Price", layer_1_prices_df.loc['Solana', 'Latest Price'], layer_1_prices_df.loc['Solana', '24H % Change'].round(2))

        col4, col5, col6 = st.columns(3)
        col4.metric("BNB Market Capitalization", layer_1_prices_df.loc['Binance Coin', 'Market Capitalization'].round(2), '')
        col5.metric("Eth Market Capitalization", layer_1_prices_df.loc['Ethereum', 'Market Capitalization'].round(2), '')
        col6.metric("Solana Market Capitalization", layer_1_prices_df.loc['Solana', 'Market Capitalization'].round(2), '')

        col7, col8, col9 = st.columns(3)
        col7.metric("BNB 24H Volume", layer_1_prices_df.loc['Binance Coin', '24H Volume'].round(2), '')
        col8.metric("Eth 24H Volume", layer_1_prices_df.loc['Ethereum', '24H Volume'].round(2), '')
        col9.metric("Solana 24H Volume", layer_1_prices_df.loc['Solana', '24H Volume'].round(2), '')

        # Snowflakes if all 3 coins have 24 hour returns less than 2%
        if layer_1_prices_df['24H % Change'].apply(lambda x: 1 if x < -2 else 0).sum() == len(layer_1_prices_df):
                st.snow()
        # Balloons if all 3 coins have 24 hour returns greater than 2%
        elif layer_1_prices_df['24H % Change'].apply(lambda x: 1 if x > 2 else 0).sum() == len(layer_1_prices_df):
                st.balloons()

# Conditional statement to determine which tokens to pull onto the Home screen
elif selected == "Home" and selected2 == 'DeFi Tokens':
        # Gathers price data using coingecko api
        defi_prices = cg.get_price(ids='aave,uniswap,sushi', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, vs_currencies='usd')
        defi_prices_df = pd.DataFrame(defi_prices).T
        defi_prices_df.columns =['Latest Price', 'Market Capitalization', '24H Volume', '24H % Change']
        defi_prices_df.index = ['Aave', 'Sushiswap', 'Uniswap']

        # Creates visual of dataframe in st.metric format
        col1, col2, col3 = st.columns(3)
        col1.metric("Aave Price", defi_prices_df.loc['Aave', 'Latest Price'], defi_prices_df.loc['Aave', '24H % Change'].round(2))
        col2.metric("Sushiswap Price", defi_prices_df.loc['Sushiswap', 'Latest Price'], defi_prices_df.loc['Sushiswap', '24H % Change'].round(2))
        col3.metric("Uniswap Price", defi_prices_df.loc['Uniswap', 'Latest Price'], defi_prices_df.loc['Uniswap', '24H % Change'].round(2))

        col4, col5, col6 = st.columns(3)
        col4.metric("Aave Market Capitalization", defi_prices_df.loc['Aave', 'Market Capitalization'].round(2), '')
        col5.metric("Sushiswap Market Capitalization", defi_prices_df.loc['Sushiswap', 'Market Capitalization'].round(2), '')
        col6.metric("Uniswap Market Capitalization", defi_prices_df.loc['Uniswap', 'Market Capitalization'].round(2), '')

        col7, col8, col9 = st.columns(3)
        col7.metric("Aave 24H Volume", defi_prices_df.loc['Aave', '24H Volume'].round(2), '')
        col8.metric("Sushiswap 24H Volume", defi_prices_df.loc['Sushiswap', '24H Volume'].round(2), '')
        col9.metric("Uniswap 24H Volume", defi_prices_df.loc['Uniswap', '24H Volume'].round(2), '')

        # Snowflakes if all 3 coins have 24 hour returns less than 2%
        if defi_prices_df['24H % Change'].apply(lambda x: 1 if x < -2 else 0).sum() == len(defi_prices_df):
                st.snow()
        # Balloons if all 3 coins have 24 hour returns greater than 2%
        elif defi_prices_df['24H % Change'].apply(lambda x: 1 if x > 2 else 0).sum() == len(defi_prices_df):
                st.balloons()

# Conditional statement to determine which tokens to pull onto the Home screen
elif selected =='Home' and selected2 == 'NFT / Memes':
        # Gathers price data using coingecko api
        meme_prices = cg.get_price(ids='apecoin,dogecoin,shiba-inu', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, vs_currencies='usd')
        meme_prices_df = pd.DataFrame(meme_prices).T
        meme_prices_df.columns =['Latest Price', 'Market Capitalization', '24H Volume', '24H % Change']
        meme_prices_df.index = ['Ape-Coin', 'Dogecoin', 'Shiba-Inu']

        # Creates visual of dataframe in st.metric format
        col1, col2, col3 = st.columns(3)
        col1.metric("Ape-Coin Price", meme_prices_df.loc['Ape-Coin', 'Latest Price'], meme_prices_df.loc['Ape-Coin', '24H % Change'].round(2))
        col2.metric("Dogecoin Price", meme_prices_df.loc['Dogecoin', 'Latest Price'], meme_prices_df.loc['Dogecoin', '24H % Change'].round(2))
        col3.metric("Shiba-Inu Price", meme_prices_df.loc['Shiba-Inu', 'Latest Price'], meme_prices_df.loc['Shiba-Inu', '24H % Change'].round(2))

        col4, col5, col6 = st.columns(3)
        col4.metric("Ape-Coin Market Capitalization", meme_prices_df.loc['Ape-Coin', 'Market Capitalization'].round(2), '')
        col5.metric("Dogecoin Market Capitalization", meme_prices_df.loc['Dogecoin', 'Market Capitalization'].round(2), '')
        col6.metric("Shiba-Inu Market Capitalization", meme_prices_df.loc['Shiba-Inu', 'Market Capitalization'].round(2), '')

        col7, col8, col9 = st.columns(3)
        col7.metric("Ape-Coin 24H Volume", meme_prices_df.loc['Ape-Coin', '24H Volume'].round(2), '')
        col8.metric("Dogecoin 24H Volume", meme_prices_df.loc['Dogecoin', '24H Volume'].round(2), '')
        col9.metric("Shiba-Inu 24H Volume", meme_prices_df.loc['Shiba-Inu', '24H Volume'].round(2), '')

        # Snowflakes if all 3 coins have 24 hour returns less than 2%
        if meme_prices_df['24H % Change'].apply(lambda x: 1 if x < -2 else 0).sum() == len(meme_prices_df):
                st.snow()
        # Balloons if all 3 coins have 24 hour returns greater than 2%
        elif meme_prices_df['24H % Change'].apply(lambda x: 1 if x > 2 else 0).sum() == len(meme_prices_df):
                st.balloons()

# Conditional statement to determine which tokens to pull onto the Price Trends screen
elif selected == "Price Trends" and selected2 == 'Layer 1 Tokens':
        # Gathers historical 360 day price information for each token
        eth = cg.get_coin_market_chart_by_id(id= 'ethereum', vs_currency='usd', days = 360, interval='daily')['prices']
        eth_df = pd.DataFrame(eth)
        eth_df = eth_df[1]
        eth_df = pd.DataFrame({'eth':eth_df})

        bnb = cg.get_coin_market_chart_by_id(id= 'binancecoin', vs_currency='usd', days = 360, interval='daily')['prices']
        bnb_df = pd.DataFrame(bnb)
        bnb_df = bnb_df[1]
        bnb_df = pd.DataFrame({'bnb':bnb_df})

        sol = cg.get_coin_market_chart_by_id(id= 'solana', vs_currency='usd', days = 360, interval='daily')['prices']
        sol_df = pd.DataFrame(sol)
        sol_df = sol_df[1]
        sol_df = pd.DataFrame({'sol':sol_df})

        # Creates multi select bar for price growth overlay
        options = st.multiselect(
            'Select tokens price comparison',
           ['binancecoin', 'ethereum', 'solana']
           )

        if len(options)>0:
                st.markdown('## 90 Day Growth Comparison')
        coin_df_combined = pd.DataFrame()
        # for loop to gather 90 day price data for each coin that the user selects in the multiselect feature
        for coin in options:
                coin_data = cg.get_coin_market_chart_by_id(id= coin, vs_currency='usd', days = 90, interval='daily')['prices']
                coin_df = pd.DataFrame(coin_data)
                coin_df = coin_df[1]
                coin_df = pd.DataFrame({coin:coin_df})
                # takes price data and normalizes by a base of 1.0 to compare coins with different price scales
                coin_df_pct = 1 + coin_df.pct_change()
                coin_df_cum = coin_df_pct.cumprod()
                coin_df_combined = pd.concat([coin_df_combined, coin_df_cum], axis=1)
        #display output as a line chart
        st.line_chart(coin_df_combined)

        # Display the trailing 1 year price graph of each coin individually
        st.markdown('## Binance Coin')
        st.line_chart(bnb_df)
        st.markdown('## Ethereum')
        st.line_chart(eth_df)
        st.markdown('## Solana')
        st.line_chart(sol_df)

# Conditional statement to determine which tokens to pull onto the Price Trends screen
elif selected == "Price Trends" and selected2 == 'DeFi Tokens':
        # Gathers historical 360 day price information for each token

        aave = cg.get_coin_market_chart_by_id(id= 'aave', vs_currency='usd', days = 360, interval='daily')['prices']
        aave_df = pd.DataFrame(aave)
        aave_df = aave_df[1]
        aave_df = pd.DataFrame({'aave':aave_df})

        uni = cg.get_coin_market_chart_by_id(id= 'uniswap', vs_currency='usd', days = 360, interval='daily')['prices']
        uni_df = pd.DataFrame(uni)
        uni_df = uni_df[1]
        uni_df = pd.DataFrame({'uni':uni_df})

        sushi = cg.get_coin_market_chart_by_id(id= 'sushi', vs_currency='usd', days = 360, interval='daily')['prices']
        sushi_df = pd.DataFrame(sushi)
        sushi_df = sushi_df[1]
        sushi_df = pd.DataFrame({'sushi':sushi_df})

        # Creates multi select bar for price growth overlay
        options = st.multiselect(
           'Select tokens for price comparison',
           ['aave', 'uniswap', 'sushi']
           )

        if len(options)>0:
                st.markdown('## 90 Day Growth Comparison')
        coin_df_combined = pd.DataFrame()
        # for loop to gather 90 day price data for each coin that the user selects in the multiselect feature
        for coin in options:
                coin_data = cg.get_coin_market_chart_by_id(id= coin, vs_currency='usd', days = 90, interval='daily')['prices']
                coin_df = pd.DataFrame(coin_data)
                coin_df = coin_df[1]
                coin_df = pd.DataFrame({coin:coin_df})
                # takes price data and normalizes by a base of 1.0 to compare coins with different price scales
                coin_df_pct = 1 + coin_df.pct_change()
                coin_df_cum = coin_df_pct.cumprod()
                coin_df_combined = pd.concat([coin_df_combined, coin_df_cum], axis=1)
        #display output as a line chart
        st.line_chart(coin_df_combined)

        # Display the trailing 1 year price graph of each coin individually
        st.markdown('## Aave')
        st.line_chart(aave_df)
        st.markdown('## Sushiswap')
        st.line_chart(sushi_df)
        st.markdown('## Uniswap')
        st.line_chart(uni_df)


# Conditional statement to determine which tokens to pull onto the Price Trends screen
elif selected == "Price Trends" and selected2 == 'NFT / Memes':
        # Gathers historical 360 day price information for each token
        apecoin = cg.get_coin_market_chart_by_id(id= 'apecoin', vs_currency='usd', days = 360, interval='daily')['prices']
        apecoin_df = pd.DataFrame(apecoin)
        apecoin_df = apecoin_df[1]
        apecoin_df = pd.DataFrame({'apecoin':apecoin_df})

        dogecoin = cg.get_coin_market_chart_by_id(id= 'dogecoin', vs_currency='usd', days = 360, interval='daily')['prices']
        dogecoin_df = pd.DataFrame(dogecoin)
        dogecoin_df = dogecoin_df[1]
        dogecoin_df = pd.DataFrame({'dogecoin':dogecoin_df})

        shib = cg.get_coin_market_chart_by_id(id= 'shiba-inu', vs_currency='usd', days = 360, interval='daily')['prices']
        shib_df = pd.DataFrame(shib)
        shib_df = shib_df[1]
        shib_df = pd.DataFrame({'shiba-inu':shib_df})

        # Creates multi select bar for price growth overlay
        options = st.multiselect(
            'Select tokens for price comparison',
           ['apecoin', 'dogecoin', 'shiba-inu']
           )

        if len(options)>0:
                st.markdown('## 50 Day Growth Comparison')
        coin_df_combined = pd.DataFrame()
        # for loop to gather 90 day price data for each coin that the user selects in the multiselect feature
        for coin in options:
                coin_data = cg.get_coin_market_chart_by_id(id= coin, vs_currency='usd', days = 50, interval='daily')['prices']
                coin_df = pd.DataFrame(coin_data)
                coin_df = coin_df[1]
                coin_df = pd.DataFrame({coin:coin_df})
                # takes price data and normalizes by a base of 1.0 to compare coins with different price scales
                coin_df_pct = 1 + coin_df.pct_change()
                coin_df_cum = coin_df_pct.cumprod()
                coin_df_combined = pd.concat([coin_df_combined, coin_df_cum], axis=1)
        #display output as a line chart
        st.line_chart(coin_df_combined)

        # Display the trailing 1 year price graph of each coin individually
        st.markdown('## Ape-Coin')
        st.line_chart(apecoin_df)
        st.markdown('## Dogecoin')
        st.line_chart(dogecoin_df)
        st.markdown('## Shiba-Inu')
        st.line_chart(shib_df)


# Trading Tab selections below
elif selected == 'Trading' and selected2 == 'Layer 1 Tokens':
        # Creates a select box to pick a token, a moving average interval and a number of standard deviations to calculate bollinger bands
        token = st.selectbox('Select a Token:', ('binancecoin', 'ethereum', 'solana'))
        moving_avg = int(st.selectbox('Select a Moving Average to Compute Bollinger Bands', (10,20,30,40,50)))
        std = int(st.selectbox('Select Number of Standard Deviations for the Upper and Lower Bollinger Bands', (1,2,3)))
        # Button to compute bollinger bands - uses import function from functions file
        if st.button("Compute Bollinger Bands, MACD and RSI"):
                BollBnd(token, moving_avg, std)
                macd_rsi(token)

elif selected == 'Trading' and selected2 == 'DeFi Tokens':
        # Creates a select box to pick a token, a moving average interval and a number of standard deviations to calculate bollinger bands 
        token = st.selectbox('Select a Token:', ('aave', 'uniswap', 'sushi'))
        moving_avg = int(st.selectbox('Select a Moving Average to Compute Bollinger Bands', (10,20,30,40,50)))
        std = int(st.selectbox('Select Number of Standard Deviations for the Upper and Lower Bands', (1,2,3)))
        # Button to compute bollinger bands - uses import function from functions file
        if st.button("Compute Bollinger Bands, MACD and RSI"):
                BollBnd(token, moving_avg, std)
                macd_rsi(token)

elif selected == 'Trading' and selected2 == 'NFT / Memes':
        # Creates a select box to pick a token, a moving average interval and a number of standard deviations to calculate bollinger bands 
        token = st.selectbox('Select a Token:', ('apecoin', 'dogecoin', 'shiba-inu'))
        moving_avg = int(st.selectbox('Select a Moving Average to Compute Bollinger Bands', (10,20,30,40,50)))
        std = int(st.selectbox('Select Number of Standard Deviations for the Upper and Lower Bands', (1,2,3)))
        # Button to compute bollinger bands - uses import function from functions file
        if st.button("Compute Bollinger Bands, MACD and RSI"):
                BollBnd(token, moving_avg, std)
                macd_rsi(token)


# Etherscan Tab. Pulls in functions from ethdashboard file
elif selected == 'Etherscan':
        st.text("\n")
        check_latest_block(w3)
        st.text("\n")
        st.text("\n")
        check_balance(w3)
        st.text("\n")
        st.text("\n")
        get_transaction(w3)
        st.text("\n")
        st.text("\n")
        check_gas(w3)

