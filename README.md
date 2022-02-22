<h1 align="center">
  <br>
  <a><img src="Media/Logo.png" alt="Markdownify" width="200"></a>
  <br>
  Blockchain System
  <br>
</h1>

<h4 align="center">Blockchain, Smart Contract & Cryptocurrency System</h4>

Contents
========

 * [Description](#Description)
 * [Installation](#installation)
 * [How To Use](#How-To-Use)
 * [Architecture](#Architecture)
 * [Documentation](#Documentation)

## Description

## Technologies Used
- [Postman][Postman]
- IDE used: [Anaconda][Anaconda]
- Python version: 3.6 and above
- Python development environment: Spyder (built in the Anaconda IDE)

## Installation (including demo ?)
To run the application, you'll need to install the following :
- Flask: pip install Flask==0.12.2 (from Anaconda prompt: Assuming you are using Anaconda)
- Requests libary: pip install requests==2.18.4 (from Anaconda prompt: Assuming you are using Anaconda)
- Python version: 3.6 and above

## How To Use

To clone and run this application, you'll need [Git][GIT] and several more applications installed on your computer. </br>
After installing all the above, type from your command line:

```bash
# Clone this repository
$ git clone https://github.com/davidlevinwork/Blockchain

# Go into the repository
$ cd Blockchain

# Install dependencies
$ npm install

# Run the app
$ npm start
```

## Architecture

## Documentation
The documentation of the project is [available here][Documentation].

## Complexity

## Libraries used:
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
[Postman]: https://www.postman.com/downloads/
[Anaconda]: https://www.anaconda.com/products/individual
[Documentation]: https://github.com/davidlevinwork/Blockchain/tree/main/Documentation
