## Description:
A python project for finding potential arbitrage between asset prices using linear programming. It uses third-party module called pulp. More information about pulp-module can be found at https://coin-or.github.io/pulp/

Project is based on the ideas from https://bitbucket.org/nikkekin/glpk-arbitrage-finder/src/master/ (java project) and http://mattmcd.github.io/2013/03/30/FX-Arbitrage-CLP.html (c++ project).

## Long Description
In any tradable markets where one can exchange one asset to another arbitrage opportunity exists if there is a sequence of transactions from initial currency through other currencies and back to the initial currency resulting in more units of the initial currency than in the beginnig. These markets are typically Foreign Exchange (FX) and Crypto currency markets. Linear programming may be used to find these opportunities.

First, let's assume the following FX-prices.

USDNOK = 9.8
EURUSD = 1.06
EURNOK = 10.388

There are no arbitrage opportunities between these prices. However, if one of the prices changes while other pair(s) don't change, there might be an arbitrage opportunity. Let's demonstrate this by changing one of them, Specifically, EURNOK to 10.388 * 1.01 and calculate the cash flows. One could start converting 100,047.53 USD to 94,383.84 EUR, which further may be converted to 990,264 NOK and then finally back to 101,047.5 USD. Trading with these prices has created roughly 1,000 USD profit.

Mathematically, this may be presented as an optimization problem by maximizing a target currency USD, with cash flow constraints on all currencies and maximum profit max_amount:

- max USD
 - subject to:
    - USD + USDEUR + USDNOK - 1 / USDEUR * EURUSD - 1 / USDNOK * NOKUSD = 1
    - EURUSD + EURNOK - 1 / EURUSD * USDEUR - 1 / EURNOK * NOKEUR = 0
    - NOKEUR + NOKUSD - 1 / NOKUSD * USDNOK - 1 / NOKEUR * EURNOK = 0
    - USD <= max_amount
    - Notations to be corrected

Explained here why above...

## Setup:
One has to have python installed. The project has been tested on version 3.8. It's recommended to use virtual environments before running the following two steps to clone and run the tests locally:

Type below in command line in your desired directory:
  - git clone https://github.com/leikeri/arbitrage_finder.git
  - build_and_test.bat
