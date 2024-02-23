# BYTESIZED32
Byte-sized text games for code generation tasks on virtual environments.

## Quickstart
Clone the repository:
```bash
git clone git@github.com:cognitiveailab/BYTESIZED32.git
cd BYTESIZED32
```

Install Dependencies:
```bash
conda create --name bytesized32 python=3.10
conda activate bytesized32
pip install -e .
```

### API key
You will need an OpenAI API key to run the experiments. Set the environment variable `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY` to your key.

## Run Generation
We run three ablation experiments, namely *object*, *action*, *distractor*.

### Prompt Game Selection
First, we generate three csv files, one for each experiment. Those files contain information about which games to use as in-context example for the code generation.
```bash
python scripts/generate_experiment_file.py action
python scripts/generate_experiment_file.py distractor
python scripts/generate_experiment_file.py object
```
The above script makes use of train and test csv files found in the `data/` folder. They describe what actions/distractors/objects are found in each game. In `action_train.csv`, `distractor_train.csv`, `object_train.csv`, 1 refers to there exists such an action/distractor/object, and empty entries refers to there does not exist such an action/distractor/object. In `action_test.csv`, the second column is one action (human-generated) that we will find a similar prompt game with the same action. In `distractor_test.csv`, 1 means this test needs a distractor and 0 means it does not need a distractor. In `object_test.csv`, 2 means we will find a prompt with this object for similarity, 1 means this kind of object is also needed for this test and empty entries means this object may not be required.

Running the three commands above will give you `experiment_action.csv`, `experiment_distractor.csv`, and `experiment_object.csv`. Since sampling is used in `generate_experiment_file.py`, we offer our generated csv files to reproduce the results (they can be found in `data/`). The left column of the output csv file is the game name of a similar game (i.e. a prompt game that shares a same action/distractor/object with the test game) and the right column is the name of an unsimilar game.

### Code Generation
With the generated csv files, we can now run the code generation for each experiment.
```bash
python scripts/run_code_generation.py data/experiment_action.csv --output-folder results/run/
python scripts/run_code_generation.py data/experiment_distractor.csv --output-folder results/run/
python scripts/run_code_generation.py data/experiment_object.csv --output-folder results/run/
```
Each command will generate 32 games according to the experiment file. By default, the generated games along with the raw LLM prompts and responses are saved in `results/{datetime}/generated_games/` folder. See `run_code_generation.py --help` for all additional arguments.

### Perform Code Reflection
Some of the generated games may not be valid Python code. We use the following script to perform self-reflection and improve code according to technical validity.
```bash
python scripts/run_code_reflection.py --game-folder results/run/generated_games/ --revision-folder results/run/revised_games/
```

## Run Automatic Evaluation
The provided codebase can run automatic evaluation on the generated games. The evaluation is based on the following metrics:
- **Technical Validity**: whether the generated game is valid Python code and contains expected class and methods.
- **Specification Compliance**: whether the generated game contains the required actions, objects, and distractors as specified in the experiment file.
- **Physical Reality Alignment**: whether the generated game model the constraints of the physical world.
- **Game Winnability**: whether the generated game is winnable, i.e. there exists a sequence of actions that lead to a winning state.

```bash
python scripts/run_code_evaluation.py --game-folder results/run/revised_games/ --results-file results/run/results.json
```

**Note**: The Specification Compliance evaluation depends on `data/test_eval.csv` which stores all the labels (i.e. actions and objects that we are interested in and that should be included in the generated game, as well as whether the generated game should contain distractors (1 means there should be a distractor, otherwise it is 0)). This file was generated manually. **If you generate your own experiment file, change this file accordingly.**

## Visualize Results

```bash
python scripts/make_table2.py --results results/run/results.json
python scripts/make_table3.py --results results/run/results.json
python scripts/make_figure4.py --results results/run/results.json
```

# Citing ByteSized32
Our paper was presented at EMNLP2023 and is also available on [Arxiv](https://arxiv.org/abs/2305.14879).

If you use our codebase, please consider citing our paper:
```
@article{Wang2023ByteSized32AC,
  title={ByteSized32: A Corpus and Challenge Task for Generating Task-Specific World Models Expressed as Text Games},
  author={Ruoyao Wang and Graham Todd and Xingdi Yuan and Ziang Xiao and Marc-Alexandre C{\^o}t{\'e} and Peter Alexander Jansen},
  journal={ArXiv},
  year={2023},
  volume={abs/2305.14879},
  url={https://api.semanticscholar.org/CorpusID:258865971}
}
```