from pulp import *


class ArbFinder:

    def __init__(self, name, fx_rates):
        self.pairs = dict()
        self.ccys = list()
        self.name = name
        self.prob = LpProblem(name=name, sense=LpMaximize)
        self.x = dict()
        for pair, vals in fx_rates.items():

            self.pairs[pair] = vals  # below roundings based on the fx-market conventions
            if pair[0:3] == 'JPY':
                self.pairs[pair[-3:] + pair[:3]] = round(vals ** -1, 2)
            elif pair[-3:] == 'JPY':
                self.pairs[pair[-3:] + pair[:3]] = round(vals ** -1, 5)
            else:
                self.pairs[pair[-3:] + pair[:3]] = int(vals ** -1 * 10000) / 10000  # round(vals ** -1, 4) This is not precise, but replicates the article

    def __add__(self, pair):  # allows adding several pairs in a dictionary
        for ccy_key, val in pair.items():
            if ccy_key not in self.pairs.keys():  # don't add if already exists
                self.pairs[ccy_key] = val
                if ccy_key[0:3] == 'JPY':
                    self.pairs[ccy_key[-3:] + ccy_key[:3]] = round(val ** -1, 2)
                elif ccy_key[-3:] == 'JPY':
                    self.pairs[ccy_key[-3:] + ccy_key[:3]] = round(val ** -1, 5)
                else:
                    self.pairs[ccy_key[-3:] + ccy_key[:3]] = int(val ** -1 * 10000) / 10000  # round(vals ** -1, 4) This is not precise, but replicates the article

    def delete_pair(self, pair):
        """
        one can't delete only one pair. All the pairs should be deleted for one of the CCYs.
        Input should be only one CCY. Update to remove all the elements of that CCY
        """
        if pair not in self.pairs.keys():
            print('Pair is not present in the FX-pairs')
        else:
            self.pairs.pop(pair)
            self.pairs.pop(pair[-3:] + pair[:3])
            print(pair + ' and its inverse deleted')

    def update(self, pair, value):
        if pair not in self.pairs.keys():
            print('Pair is not present in the FX-pairs')
        else:
            self.pairs[pair] = value
            self.pairs[pair[-3:] + pair[:3]] = round(value ** -1, 4)  # missing convention/nr of decimals check
            print(pair + ' and its inverse updated')

            # delete constraints --> create_arb_model need to be rerun. Can't rerun solver without redefining the "prob"
            self.prob.constraints.clear()  # , self.x.clear()
            self.prob = LpProblem(name=self.name, sense=LpMaximize)

    def create_arb_model(self, base_ccy, fx_pairs, profit_cap):
        self.ccys = list()
        for pair, val in fx_pairs.items():
            # print(str(pair) + ': ' + str(val))
            if pair not in self.ccys:  # creating list of CCYs
                self.ccys.append(pair[:3])
                self.ccys.append(pair[-3:])
        self.ccys = list(set(self.ccys))  # unique list

        # create variables
        for name, val in fx_pairs.items():
            self.x[name] = LpVariable(name=name, lowBound=0)
            self.x[name[-3:] + name[:3]] = LpVariable(name=name[-3:] + name[:3], lowBound=0)

        self.x[base_ccy] = LpVariable(name=str(base_ccy), lowBound=0)

        # creating target CCYs constraint string
        str_1 = str()
        str_2 = str()
        for ccy in self.ccys:  # target CCY constraint string
            if ccy != base_ccy:
                str_2 += " - fx_pairs[\"" + str(ccy) + str(base_ccy) + "\"] * " + "self.x[\"" + str(ccy) + base_ccy + "\"]"
                str_1 += "+ " + "self.x[\"" + base_ccy + str(ccy) + "\"]"
        # add target CCY constraint
        self.prob += (eval("self.x[\"" + base_ccy + "\"]" + str_1 + str_2 + ' == 1'), "from_target_ccy_and_back")

        # rest of CCY constraint strings
        for ccy in self.ccys:
            if ccy != base_ccy:
                self.prob.addConstraint(lpSum(self.x[ccy + i] - fx_pairs[i + ccy] * self.x[i + ccy] for i in self.ccys if ccy != i) == 0)

        # max profit constraint
        self.prob.addConstraint(self.x[base_ccy] <= profit_cap)

        # Objective function to the model
        self.prob.objective = self.x[base_ccy]

    def get_results(self):
        """
        could be written to file or directed to a publisher
        """
        self.prob.solve()
        # print(list_solvers(onlyAvailable=True))  # list available solvers
        print('Results:')
        # print(value(x))
        if self.prob.objective.value() > 1:  # check that target returns profits
            print(f"status: {self.prob.status}, {LpStatus[self.prob.status]}")
            print(f"objective: {self.prob.objective.value()}")
            for var in self.prob.variables():
                if var.value() > 0:
                    print(f"{var.name}: {var.value()}")
        else:
            print('No arbitrage found')
        print(f"solved using solver {self.prob.solver}\n\n")
