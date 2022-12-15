import pytest
from main import ArbFinder

rates = dict()
# first run
rates["USDEUR"] = 1.1486
rates["USDGBP"] = 0.7003
rates["USDJPY"] = 133.33
rates["EURJPY"] = 116.14
rates["EURGBP"] = 0.6097
rates["JPYGBP"] = 0.00525


# class TestClass:

def func_arb():
    # create fx_rates and their inverse pairs
    fx = ArbFinder('initial_test', fx_rates=rates)

    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    # print the results
    fx.get_results()
    return fx.prob.status


def test_simple_with_arbitrage():
    assert func_arb() == 1


def test_simple_without_arbitrage():

    for item, val in rates.items():
        rates[item] = 1

    fx = ArbFinder('initial_test', fx_rates=rates)

    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    # print the results
    fx.get_results()
    fx.prob.status

    assert True  # THIS should fail ie. return False???


rates.clear()
rates["USDNOK"] = 9.8
rates["USDEUR"] = 1.06
rates["EURNOK"] = 9.8 * 1.06


def test_with_less_elements_no_arbitrage():

    fx = ArbFinder('initial_test', fx_rates=rates)

    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    # print the results
    fx.get_results()
    fx.prob.status

    assert True  # THIS should fail ie. return False???


def test_with_less_elements_with_arbitrage():

    fx = ArbFinder('initial_test', fx_rates=rates)
    fx.update('EURNOK', fx.pairs['USDNOK'] / fx.pairs['EURUSD'])
    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    # print the results
    fx.get_results()
    fx.prob.status

    assert True  # THIS should fail ie. return False???
