from web3 import Web3
import streamlit as st

# API using Infura Node to obtain blockchain data
infura_url = 'https://mainnet.infura.io/v3/15bf55ae87d142d8b5f0b2c3ba87d1cb'

# Creates w3 instance
w3 = Web3(Web3.HTTPProvider(infura_url))


# Text box to input any Ethereum address and return the Ether balance
def check_latest_block(w3):
    if st.button("Latest Block Number"):
        latest = w3.eth.blockNumber
        st.write(latest)


def check_balance(w3):
    address = st.text_input("Input the address you would like to see the balance of")
    if st.button("Check Ether Balance"):
    # Get balance of address in Wei
        wei_balance = w3.eth.get_balance(address)
    # Convert Wei value to ether
        ether = w3.fromWei(wei_balance, "ether")
    # Return the value in ether
        st.write(ether)

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
    st.bar_chart(list)




