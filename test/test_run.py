from src import utils as u


def func_arb(rates):
    # create fx_rates and their inverse pairs
    fx = u.ArbFinder('initial_test', fx_rates=rates)

    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    # print the results. True if arbitrage exists else False
    fx.get_results()
    if fx.prob.objective.value() > 1:
        return True
    else:
        return False


# 1
def test_simple_with_arbitrage():

    rates = dict()
    rates["USDEUR"] = 1.1486
    rates["USDGBP"] = 0.7003
    rates["USDJPY"] = 133.33
    rates["EURJPY"] = 116.14
    rates["EURGBP"] = 0.6097
    rates["JPYGBP"] = 0.00525

    assert func_arb(rates)


# 2
def test_simple_without_arbitrage():

    rates = dict()
    rates["USDEUR"] = 1
    rates["USDGBP"] = 1
    rates["USDJPY"] = 1
    rates["EURJPY"] = 1
    rates["EURGBP"] = 1
    rates["JPYGBP"] = 1

    assert not func_arb(rates)


# 3
def test_with_less_elements_without_arbitrage():

    rates = dict()
    rates["USDNOK"] = 9.8
    rates["EURUSD"] = 1.06
    rates["EURNOK"] = rates["EURUSD"] * rates["USDNOK"]

    assert not func_arb(rates)


# 4
def test_with_less_elements_with_arbitrage():

    rates = dict()
    rates["USDNOK"] = 9.8
    rates["EURUSD"] = 1.06
    rates["EURNOK"] = rates["EURUSD"] / rates["USDNOK"]

    assert func_arb(rates)


# 5
def test_update_function_with_arbitrage():

    rates = dict()
    rates["USDNOK"] = 9.8
    rates["USDEUR"] = 1.06
    rates["EURNOK"] = 1

    fx = u.ArbFinder('initial_test', fx_rates=rates)
    fx.update('EURNOK', fx.pairs['USDNOK'] / fx.pairs['EURUSD'])
    # Create the model
    fx.create_arb_model('USD', fx.pairs, 10000)

    fx.get_results()

    assert fx.prob.objective.value()
