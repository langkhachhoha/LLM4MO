from eoh import eoh
from eoh.utils.getParas import Paras

# Parameter initilization #
paras = Paras() 

# Set your LLM API key here
with open("secret.txt", "r") as f:
    secret = f
    llm_api_key = secret.readline().strip()


# Set parameters #
paras.set_paras(method = "eoh",    # ['ael','eoh']
                problem = "tri_tsp_construct", #['tsp_construct','bp_online', 'bi_tsp_construct']
                llm_api_endpoint = 'api.openai.com', # set your LLM endpoint
                llm_api_key = llm_api_key,   # set your key
                llm_model = "gpt-3.5-turbo",
                ec_pop_size = 10, # number of samples in each population
                ec_n_pop = 4,  # number of populations
                exp_n_proc = 4,  # multi-core parallel
                ec_m = 2, # number of parents
                exp_debug_mode = False)

# initilization
evolution = eoh.EVOL(paras)

# run 
evolution.run()