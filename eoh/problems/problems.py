# from machinelearning import *
# from mathematics import *
# from optimization import *
# from physics import *
class Probs():
    def __init__(self,paras):

        if not isinstance(paras.problem, str):
            self.prob = paras.problem
            print("- Prob local loaded ")
        elif paras.problem == "bi_tsp_construct":
            from .optimization.bi_tsp_greedy import run
            self.prob = run.BITSPCONST()
            print("- Prob "+paras.problem+" loaded ")
        elif paras.problem == "tri_tsp_construct":
            from .optimization.tri_tsp_greedy import run
            self.prob = run.TRITSPCONST()
            print("- Prob "+paras.problem+" loaded ")
        else:
            print("problem "+paras.problem+" not found!")


    def get_problem(self):

        return self.prob
