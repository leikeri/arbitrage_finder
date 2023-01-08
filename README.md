## Description:
A python project for finding potential arbitrage between asset prices using linear programming. It uses third-party module called pulp. More information about pulp-module can be found at https://coin-or.github.io/pulp/

Project is based on the ideas from https://bitbucket.org/nikkekin/glpk-arbitrage-finder/src/master/ (java project) and http://mattmcd.github.io/2013/03/30/FX-Arbitrage-CLP.html (c++ project).

## Long Description
In any tradable markets where one can exchange one asset to another arbitrage opportunity exists if there is a sequence of transactions from initial asset through other assets and back to the initial asset resulting in more units of the initial asset than in the beginnig. These markets are typically Foreign Exchange (FX) and Crypto currency markets. Linear programming may be used to find these opportunities.

First, let's assume the following FX-prices.

USDNOK = 9.8, EURUSD = 1.06, EURNOK = 10.388

There are no arbitrage opportunities between these prices. However, if one of the prices changes while other pair(s) don't change, there might be an arbitrage opportunity. Let's demonstrate this by changing one of them, specifically, EURNOK to 10.388 * 1.01. One could start converting 100,047.53 USD to 94,383.84 EUR, which further may be converted to 990,264 NOK and then finally back to 101,047.5 USD. Trading with these prices would create roughly 1,000 USD profit.

Mathematically, this may be presented as an optimization problem by maximizing a target currency D with cash flow constraints and maximum profit amount max_amount:

- max D
 - subject to:
    - D + DE + DN - EURUSD * ED - NOKUSD * ND = 1
    - ED + EN - USDEUR * DE - NOKEUR * NE = 0
    - NE + ND - USDNOK * DN - EURNOK * EN = 0
    - D <= max_amount,

where DE describes the amount of USD to be converted to EUR, DN dollar amount to be converted to NOK and so on. All the FX-pairs are the current market prices. Also, note that EURUSD = USDEUR^-1. The constrains represent cash flows in and out of each currency. For all non-target currencies they should net to zero as one is not aiming for accumulation of those currencies. For example, second row describes EUR cash flows from EURs to other currencies (ED + EN) which should equal all the cash flows to EURs. Only difference to the target currency D (USD) cash flows is that it has an addtional term for the 1 USD initially available and final USD arbitrage amount D. One should limit amount of target profits as well with the max_amount constraint.

Please find python-file main.py as an example run. One need to define FX-rates in a dictionary and pass it on  to ArbFinder class.

```
    rates = dict()
    rates["USDNOK"] = 9.8
    rates["EURUSD"] = 1.06
    rates["EURNOK"] = 10.388
```

It initializes FX-rates and their inverse values in a dictionary. Next step is to define the linear programming model in which the optimization task is being created with three input parameters: Target ccy, FX-pairs class and maximum target amount.

```
    # Create the model
    fx.create_arb_model('USD', fx.pairs, 1000)
```

Finally, one can solve the model by running

```
    # print the results
    fx.get_results()
```
giving no arbitrage opportunities.

When new FX-prices get updated from your desired data feed, one should update relevant values and rerun the solver. The following illustrates that with prices as in the description above generating an arbitrage opportunity.

```
    # update a fx-rate and rerun
    fx.update('EURNOK', 10.388 * 1.01)
    model = fx.create_arb_model('USD', fx.pairs, 1000)
    fx.get_results()
```

Resulting in the following output:

EURNOK and its inverse updated.

```
Results:
status: 1, Optimal
objective: 1000.0
EURNOK: 94383.839
NOKUSD: 990263.91
USD: 1000.0
USDEUR: 100047.53
It took 0.011001 seconds using solver <pulp.apis.coin_api.PULP_CBC_CMD object at 0x0000018F9D0C2A30>.
```

There are several aspects to consider for a production application such as latency and liquidity issues, transaction costs, usage of bid-offer prices and so on. The project is merely describing what is the problem setup and how it can be solved using optimization methods.

## Setup:
One has to have python installed. The project has been tested on version 3.8. It's recommended to use virtual environments before running the following two steps to clone and run the tests locally:

Type below in command line in your desired directory:
  - git clone https://github.com/leikeri/arbitrage_finder.git
  - build_and_test.bat
