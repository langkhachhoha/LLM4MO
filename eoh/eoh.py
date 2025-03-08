
import random

from .utils import createFolders
from .methods import methods
from .problems import problems

# main class for AEL
class EVOL:

    # initilization
    def __init__(self, paras, prob=None, **kwargs):

        print("----------------------------------------- ")
        print("---              Start EoH            ---")
        print("-----------------------------------------")
        # Create folder #
        createFolders.create_folders(paras.exp_output_path)
        print("- output folder created -")

        self.paras = paras

        print("-  parameters loaded -")

        self.prob = prob

        # Set a random seed
        random.seed(2024)

        
    # run methods
    def run(self):

        problemGenerator = problems.Probs(self.paras) 

        problem = problemGenerator.get_problem() # from .optimization.tsp_greedy import run... problem = run.TSPCONST()

        methodGenerator = methods.Methods(self.paras,problem) 

        method = methodGenerator.get_method() # from .eoh.eoh import EOH... method = EOH(self.paras,self.problem,self.select,self.manage)

        method.run()

        print("> End of Evolution! ")
        print("----------------------------------------- ")
        print("---     EoH successfully finished !   ---")
        print("-----------------------------------------")
