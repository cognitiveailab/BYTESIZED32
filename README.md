# BYTESIZED32
Byte-sized text games for code generation tasks on virtual environments introduced in the paper [ByteSized32: A Corpus and Challenge Task for Generating Task-Specific World Models Expressed as Text Games](https://tinyurl.com/2s3u77tz).

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
pip install -r requirements.txt
```

## API key
You will need an OpenAI API key to run all of our experiments. Save your API key in plain text in `experiment_scripts/api-key`.


## Run Generation
We run four ablation experiments, namely *object*, *action*, *distractor*, *score_method*. To run the experiments, create a folder named output where all generation outputs will be saved and go to the experiment_scripts folder:
```bash
mkdir output
cd experiment_scripts
``` 

You will also need an OpenAI API key to use the GPT-4 model. Save the key as plain text in a file named api-key in the folder experiment_scripts.

Run the experiments by
```bash
./run_action_experiments.sh
./run_distractor_experiments.sh
./run_object_experiments.sh
./run_score_method_experiments.sh
```

## Run Automatic Evaluation
First, you can extract the code from raw GPT-4 response by running in the `experiment_scripts` folder:
```bash
python post_process.py
```
This script will extract codes from all Python files in the `output` folder and save the extracted code into the `cleaned_generated_game` folder. 

```bash
python automatic_evaluation.py [folder_to_code]
```

Replace `folder_to_code` with the path to folder of the extracted code files.
