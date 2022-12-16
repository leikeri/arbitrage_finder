from utils import ArbFinder
"""
    To be done:
    - Bid-offers should be used 
    - FX-rates defined manually. One should receive fx rates via a messaging protocol (kafka, aeron, zeromq) in a real application
"""

if __name__ == '__main__':

    fx = dict()
    fx["USDEUR"] = 1.1486
    fx["USDGBP"] = 0.7003
    fx["USDJPY"] = 133.33
    fx["EURJPY"] = 116.14
    fx["EURGBP"] = 0.6097
    fx["JPYGBP"] = 0.00525

    rates = dict()
    rates["USDNOK"] = 9.8
    rates["EURUSD"] = 1.06
    rates["EURNOK"] = 9.8 / 1.06  # rates["USDEUR"] * rates["USDNOK"]

    # create fx_rates and their inverse pairs
    fx = ArbFinder('initial_test', fx_rates=rates)

    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    # print the results
    fx.get_results()

    # update a fx-rate and rerun
    fx.update('USDEUR', 1.15)
    model = fx.create_arb_model('USD', fx.pairs, 10000)
    fx.get_results()
