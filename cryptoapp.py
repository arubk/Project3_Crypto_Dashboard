# imports
from web3 import Web3
import streamlit as st
from streamlit_option_menu import option_menu
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import pandas as pd
from etherscan import w3, check_latest_block, check_balance, check_gas


# Streamlit 
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


# Gathers price data for each of the coin sectors
# Used for HOME tab
layer_1_prices = cg.get_price(ids='ethereum,binancecoin,solana', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, vs_currencies='usd')
layer_1_prices_df = pd.DataFrame(layer_1_prices).T
layer_1_prices_df.columns =['Latest Price', 'Market Capitalization', '24H Volume', '24H % Change']
layer_1_prices_df.index = ['Binance Coin', 'Ethereum', 'Solana']

defi_prices = cg.get_price(ids='aave,uniswap,sushi', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, vs_currencies='usd')
defi_prices_df = pd.DataFrame(defi_prices).T
defi_prices_df.columns =['Latest Price', 'Market Capitalization', '24H Volume', '24H % Change']
defi_prices_df.index = ['Aave', 'Sushiswap', 'Uniswap']

meme_prices = cg.get_price(ids='apecoin,dogecoin,shiba-inu', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, vs_currencies='usd')
meme_prices_df = pd.DataFrame(meme_prices).T
meme_prices_df.columns =['Latest Price', 'Market Capitalization', '24H Volume', '24H % Change']
meme_prices_df.index = ['Ape-Coin', 'Dogecoin', 'Shiba-Inu']


# Gathers historical 30 day price information for each token
# Used for Price Trends tab
eth = cg.get_coin_market_chart_by_id(id= 'ethereum', vs_currency='usd', days = 360, interval='daily')['prices']
eth_df = pd.DataFrame(eth)
eth_df = eth_df[1]

bnb = cg.get_coin_market_chart_by_id(id= 'binancecoin', vs_currency='usd', days = 360, interval='daily')['prices']
bnb_df = pd.DataFrame(bnb)
bnb_df = bnb_df[1]

sol = cg.get_coin_market_chart_by_id(id= 'solana', vs_currency='usd', days = 360, interval='daily')['prices']
sol_df = pd.DataFrame(sol)
sol_df = sol_df[1]

aave = cg.get_coin_market_chart_by_id(id= 'aave', vs_currency='usd', days = 360, interval='daily')['prices']
aave_df = pd.DataFrame(aave)
aave_df = aave_df[1]

uni = cg.get_coin_market_chart_by_id(id= 'uniswap', vs_currency='usd', days = 360, interval='daily')['prices']
uni_df = pd.DataFrame(uni)
uni_df = uni_df[1]

sushi = cg.get_coin_market_chart_by_id(id= 'sushi', vs_currency='usd', days = 360, interval='daily')['prices']
sushi_df = pd.DataFrame(sushi)
sushi_df = sushi_df[1]

apecoin = cg.get_coin_market_chart_by_id(id= 'apecoin', vs_currency='usd', days = 360, interval='daily')['prices']
apecoin_df = pd.DataFrame(apecoin)
apecoin_df = apecoin_df[1]

dogecoin = cg.get_coin_market_chart_by_id(id= 'dogecoin', vs_currency='usd', days = 360, interval='daily')['prices']
dogecoin_df = pd.DataFrame(dogecoin)
dogecoin_df = dogecoin_df[1]

shib = cg.get_coin_market_chart_by_id(id= 'shiba-inu', vs_currency='usd', days = 360, interval='daily')['prices']
shib_df = pd.DataFrame(shib)
shib_df = shib_df[1]



# Conditional statement to determine which tokens to pull onto the Home screen
if selected == "Home" and selected2 == 'Layer 1 Tokens':
        st.dataframe(layer_1_prices_df)
        # Snowflakes if all 3 coins have 24 hour returns less than 2%
        if layer_1_prices_df['24H % Change'].apply(lambda x: 1 if x < -2 else 0).sum() == len(layer_1_prices_df):
                st.snow()
        # Balloons if all 3 coins have 24 hour returns greater than 2%
        elif layer_1_prices_df['24H % Change'].apply(lambda x: 1 if x > 2 else 0).sum() == len(layer_1_prices_df):
                st.balloons()
elif selected == "Home" and selected2 == 'DeFi Tokens':
        st.dataframe(defi_prices_df)
        # Snowflakes if all 3 coins have 24 hour returns less than 2%
        if defi_prices_df['24H % Change'].apply(lambda x: 1 if x < -2 else 0).sum() == len(defi_prices_df):
                st.snow()
        # Balloons if all 3 coins have 24 hour returns greater than 2%
        elif defi_prices_df['24H % Change'].apply(lambda x: 1 if x > 2 else 0).sum() == len(defi_prices_df):
                st.balloons()
elif selected =='Home' and selected2 == 'NFT / Memes':
        st.dataframe(meme_prices_df)
        # Snowflakes if all 3 coins have 24 hour returns less than 2%
        if meme_prices_df['24H % Change'].apply(lambda x: 1 if x < -2 else 0).sum() == len(meme_prices_df):
                st.snow()
        # Balloons if all 3 coins have 24 hour returns greater than 2%
        elif meme_prices_df['24H % Change'].apply(lambda x: 1 if x > 2 else 0).sum() == len(meme_prices_df):
                st.balloons()

# Conditional statement to determine which tokens to pull onto the Price Trends screen
elif selected == "Price Trends" and selected2 == 'Layer 1 Tokens':
        st.markdown('## Binance Coin')
        st.line_chart(bnb_df)
        st.markdown('## Ethereum')
        st.line_chart(eth_df)
        st.markdown('## Solana')
        st.line_chart(sol_df)
elif selected == "Price Trends" and selected2 == 'DeFi Tokens':
        st.markdown('## Aave')
        st.line_chart(aave_df)
        st.markdown('## Sushiswap')
        st.line_chart(sushi_df)
        st.markdown('## Uniswap')
        st.line_chart(uni_df)
elif selected == "Price Trends" and selected2 == 'NFT / Memes':
        st.markdown('## Ape-Coin')
        st.line_chart(apecoin_df)
        st.markdown('## Dogecoin')
        st.line_chart(dogecoin_df)
        st.markdown('## Shiba-Inu')
        st.line_chart(shib_df)







# Etherscan Tab. Pulls in functions from ethdashboard file
if selected == 'Etherscan':
        st.text("\n")
        check_latest_block(w3)
        st.text("\n")
        st.text("\n")
        check_balance(w3)
        st.text("\n")
        st.text("\n")
        check_gas(w3)
