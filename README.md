
```markdown
<div align=center>
<h1 align="center">
MEoH
</h1>
<h3 align="center">
MSOLab: Large Language Model 4 Discrete Multi-Objectives 
</h3>
</div>

## Introduction

MEoH is a framework that leverages large language models (LLMs) for solving discrete multi-objective optimization problems.

## Requirements

Before running the project, make sure you have installed all the required dependencies. You can install them using the following command:

```sh
pip install -r requirements.txt
```

## Running the Project

To run the project, follow these steps:

1. Set your LLM API key in the secret.txt file.
2. Navigate to the directory of the problem you want to solve.
3. Run the `runMEoH.py` script.

### Example

For example, to run the `tri_tsp_construct` problem, use the following commands:

```sh
cd Problems/Multi-Objective/tri_tsp_construct
python runMEoH.py
```

## Available Problems

The following problems are available in the MEoH framework:

- `tri_tsp_construct`: Traveling Salesman Problem with three objectives.
- `bi_tsp_construct`: Traveling Salesman Problem with two objectives.
- `bp_online`: Bin Packing Problem.

Each problem has its own directory under Multi-Objective. You can navigate to the respective directory and run the `runMEoH.py` script to solve the problem.

## Configuration

You can configure the parameters for each problem by modifying the `set_paras` function in the `runMEoH.py` script. Here is an example configuration:

```python
paras.set_paras(
    method="eoh",  # ['ael','eoh']
    problem="tri_tsp_construct",  # ['tsp_construct','bp_online', 'bi_tsp_construct']
    llm_api_endpoint='api.openai.com',  # set your LLM endpoint
    llm_api_key=llm_api_key,  # set your key
    llm_model="gpt-3.5-turbo",
    ec_pop_size=10,  # number of samples in each population
    ec_n_pop=4,  # number of populations
    exp_n_proc=4,  # multi-core parallel
    ec_m=2,  # number of parents
    exp_debug_mode=False
)
```

Feel free to adjust the parameters according to your needs.

## Contact

For any questions or issues, please contact the project maintainers.
```


