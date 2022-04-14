<h1 align="center">
  <br>
  <a><img src="Media/Logo.png" alt="Markdownify" width="200"></a>
  <br>
  Blockchain System
  <br>
</h1>

<h3 align="center">Blockchain, Smart Contract, Cryptocurrency System & RSI trading bot.</h3>

Contents
========

1. [General](#general)
    - [Background](#background)
    - [File Structure](#file-structure)
    - [Technologies Used](#technologies-used)
    - [Demo](#demo)
2. [Architecture](#architecture)
    - [Blockchain](#blockchain)
    - [Smart Contract](#smart-contract)
    - [Adonis Cryptocurrency](#adonis-cryptocurrency)
    - [Trading Bot](#trading-bot)
3. [Installation](#installation)
    - [How To Use](#how-to-use)
    - [Dependencies](#dependencies)
4. [Documentation](#documentation)
    - [Libraries used](#libraries-used)

## General

### Background
As part of the final year of the university, we are required to choose a topic that interests us, research it and develop it.

In the recent years I have found a lot of interest in the whole world of trading, and especially in the world of virtual currencies. Therefore, I decided that I would choose a project that incldes this issue.

As part of my project, I chose to realize 4 cornerstones in everything related to the world of virtual currencies:
1. Blockchain system
2. System of smart contracts
3. Virtual currency
4. Trading Algorithm (Bot)

### File Structure
    .
    ├── Blockchain
    │   ├── Blockchain.py       # Creation, Mining and Decentralizing the Blockchain
    │   ├── Constants.py        # Helper
    ├── Demo
    │   ├── Demo.mp4            # Demo of the blockchain system including coin's transfer
    │   ├── Pre-Demo.mp4        # Preparations required for the benefit of the demo
    │   ├── Demo- Explain.pdf   # Explanation of the demo
    ├── Documentation
    │   ├── Architecture.pdf    # Architecture of the system
    │   ├── Test Plan.pdf       # Test Plan of the system
    ├── Media 
    │   ├── Logo.png     
    ├── Smart Contract 
    │   ├── adonis_ico.sol      # Creation of the "Adonis" cryptocurrency    
    ├── Trading Bot             
    │   ├── RSIbot.py           # Define and build the cryptocurrency bot
    │   ├── config.py           # Helper
    └── README                  # README.md file

### Technologies Used
- [Postman][Postman]
- IDE used: [Anaconda][Anaconda]
- Python version: 3.6 or above
- Python development environment: Spyder (built in the Anaconda IDE)

### Demo
You can find a demo of the blockchain system and transferring funds under the Demo tab.

## Architecture

### Blockchain
Building a Blockchain system that enables the execution of secure business activities, while adjusting business transactions between different parties without the need for a central management entity, when the management is replaced by encrypted blocks of information generated through P2P sharing.

During the project, I implemented an end-to-end blockchain system that allows transactions to be made, when the relevant transactions in this case being `Adonis` currency transactions.

### Smart Contract
A smart contract is a digital contract distributed on a blockchain network, which is capable of receiving and exporting data and performing certain operations automatically. Its operations are reviewed and verified by the blockchain network.

### Adonis Cryptocurrency
Cryptocurrency is a digital means of transferring value for a variety of uses like payment.

Definition of a new Cryptocurrency called `Adonis`. </br>
The maximum number of coins for the sale of this coin is 1000000, with the initial price of the coin being 0.001 (i.e. $ 1 = 1000 Adonis coins).

### Trading Bot
The trading algorithm is based on the Relative Strength Index (RSI): a technical indicator used to analyze and review various markets. The indicator shows the price intensity by comparing up and down fluctuations in the closing prices of the given cryptocurrency.

The trading algorithm is designed for [Binance][Binance] trading arena, where the trader's personal API information is entered into the `config.py` file.
A link to binance's documentation can be found [here][BinanceDoc].

## Installation

### Dependencies
To run the application, you'll need to install the following :
- Flask: pip install Flask==0.12.2 (from Anaconda prompt: Assuming you are using Anaconda)
- Requests libary: pip install requests==2.18.4 (from Anaconda prompt: Assuming you are using Anaconda)
- Python version: 3.6 and above

### How To Use

To clone and run this application, you'll need [Git][GIT] and several more applications installed on your computer. </br>
After installing all the dependencies above, type from your command line (I describe from anaconda prompt):

```bash
# Clone this repository
$ git clone https://github.com/davidlevinwork/Blockchain

# Go into the repository
$ cd Blockchain

# Run the Blockchain System in the terminal
runcell(0, '...path-to-file.../Blockchain.py')
```

## Documentation
The documentation of the project is [available here][Documentation].

### Libraries Used:
Libary Name | Usage  
-----------|-----------
`Hashlib` | Will use to hash the blocks.
`From uuid import uuid4` | Generate a random UUID.
`Json` | Built-in package for working with JSON data.
`Datetime` | Each block will have his own timestamp of creation.
`From flask import jsonify` | Interact with the Blockchain and Postman.
`From flask import request` | Connect some nodes in the decentralized Blockchain network.
`From flask import flask` | We will create an object of flask which will be the web application.
`Requests` | Ensure that all the nodes in the decentralized Blockchain have indeed the same chain.
`From urlib.parse import urlparse` | Standard interface to break Uniform Resource Locator (URL).

<!--- Links --->
[GIT]: https://git-scm.com
[Binance]: https://www.binance.com/en
[Postman]: https://www.postman.com/downloads/
[Anaconda]: https://www.anaconda.com/products/individual
[Documentation]: https://github.com/davidlevinwork/Blockchain/tree/main/Documentation
[BinanceDoc]: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
