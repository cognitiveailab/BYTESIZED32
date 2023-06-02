import argparse
import openai               # pip install openai
import tiktoken             # pip install tiktoken
import pandas as pd         # pip install pandas
import os
import json
import time

from requests.exceptions import ChunkedEncodingError

# from tenacity import (
#     retry,
#     retry_if_not_exception_type,
#     stop_after_attempt,
#     wait_exponential,
#     retry_if_exception_type,
#     wait_random_exponential,
# )


# output prefix
prefix = "0424"

# data directory
data_dir = "shrink_code"

# Tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# OpenAI API Key
try:
    key_file = "api-key"
    with open(key_file) as f:
        OPENAI_API_KEY = f.read().strip()
    openai.api_key = OPENAI_API_KEY
except:
    pass


# arg parser
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_prefix", type=str, default='prompt_games_')
    parser.add_argument("--output_prefix", type=str, default='')
    parser.add_argument("--experiment_name", choices=["object", "action", "score_method", "distractor"])
    parser.add_argument("--experiment_input_folder", type=str)
    parser.add_argument("--prompt_code_input_folder", type=str, default="..")
    parser.add_argument("--test_prompt_input_folder", type=str, default="../test_prompts")
    parser.add_argument("--output_folder", type=str, default="../output")
    parser.add_argument("--model", type=str, default="gpt-4-32k")
    parser.add_argument("--num_prompt_games", type=int, default=1)

    args = parser.parse_args()
    return args


# Get the number of tokens for a string, measured using tiktoken
def getTokenLength(strIn):
    tokens = tokenizer.encode(strIn)
    numTokens = len(tokens)
    return numTokens


# A wrapper for getResponseHelper, that continues to retry for large replies that timeout after 300 seconds.
def getResponse(prompt:str, maxTokensOut:int, model:str, maxRetries=4):
    numRetries = 0
    delay_base = 10
    totalResponse = ""
    while (numRetries <= maxRetries):
        responseStr, err = getResponseHelper(prompt, maxTokensOut, model)
        totalResponse += responseStr

        if err == '':
            print("Success -- break.")
            break
        elif err == 'TimeOut':
            print("getResponse: Retrying (attempt " + str(numRetries) + " / " + str(maxRetries) + ")")
            numRetries += 1
            #prompt += "####---BREAK---####\n" +     # Just for debugging
            prompt += responseStr
        elif err == 'RateLimitError':
            print("getResponse: Retrying (attempt " + str(numRetries) + " / " + str(maxRetries) + ")")
            delay = delay_base * (2 ** numRetries)
            numRetries += 1
            time.sleep(delay)
        else:
            # break if caught unknown error
            print(f"getResponse: {err}")
            break


    numTokens = getTokenLength(totalResponse)
    print("getResponse: Total tokens generated: " + str(numTokens))

    return totalResponse

# @retry(
#     reraise=True,
#     stop=stop_after_attempt(100),
#     wait=wait_exponential(multiplier=1, min=4, max=10),
#     retry=(
#         retry_if_exception_type(openai.error.Timeout)
#         | retry_if_exception_type(openai.error.APIError)
#         | retry_if_exception_type(openai.error.APIConnectionError)
#         | retry_if_exception_type(openai.error.RateLimitError)
#     ),
# )
def getResponseHelper(prompt:str, maxTokensOut:int, model:str):
    messages=[{"role": "system", "contant": "You are CodeGPT, a super-intelligent AI model that generates solutions to coding problems."},
               {"role": "user", "content": prompt}]

    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     max_tokens=100,
    #     temperature=0.1,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0,
    #     messages = messages)

    numPromptTokens = getTokenLength(prompt)
    MODEL_MAX_TOKENS = 31000 if model == "gpt-4-32k" else 8100
    maxPossibleTokens = MODEL_MAX_TOKENS - numPromptTokens
    if (maxTokensOut > maxPossibleTokens):
        print("Warning: maxTokensOut is too large given the prompt length (" + str(numPromptTokens) + ").  Setting to max generation length of " + str(maxPossibleTokens))
        maxTokensOut = maxPossibleTokens

    # Record start time of request
    startTime = time.time()

    if openai.api_type == "azure":
        # When using the Azure API, we need to use engine instead of model argument.
        response = openai.ChatCompletion.create(
            engine=model,
            max_tokens=maxTokensOut,
            temperature=0.0,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            messages=[{"role": "user", "content": prompt}],
            stream=True    # Stream the response, with the hopes of preventing timeouts
        )
    else:
        response = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model=model,      # 8k token limit
            #model="gpt-4-32k-0314",
            max_tokens=maxTokensOut,
            temperature=0.0,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            messages=[{"role": "user", "content": prompt}],
            stream=True    # Stream the response, with the hopes of preventing timeouts
        )

    # Collect the stream
    collectedChunks = []
    collectedMessages = []
    responseStr = ""
    err = ""

    try:
        for chunk in response:
            # Calculate time since start of request
            deltaTime = time.time() - startTime

            collectedChunks.append(chunk)
            chunkMessage = chunk['choices'][0]['delta']
            collectedMessages.append(chunkMessage)

            if "content" in chunkMessage:
                responseStr += chunkMessage["content"]

            # Display progress
            numTokens = getTokenLength(responseStr)
            # Calculate transmission rate
            if (deltaTime > 0):
                transmissionRate = numTokens / deltaTime
            else:
                transmissionRate = 0

            # Update every 25 tokens
            if (numTokens % 25 == 0):
                # Display to 2 decimal places
                transmissionRate = round(transmissionRate, 2)
                deltaTime = round(deltaTime, 2)
                print("Received " + str(numTokens) + " tokens after " + str(deltaTime) + " seconds (" + str(transmissionRate) + " tokens/sec)")
    except openai.error.RateLimitError as e:
        print(e)
        err = "RateLimitError"
        return responseStr, err
    except openai.error.Timeout as e:
        print(e)
        err = "TimeOut"
        return responseStr, err
    # When timeout, we practically received this error instead of the openai timeout error
    except ChunkedEncodingError as e:
        print(e)
        err = "TimeOut"
        return responseStr, err
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        return responseStr, "APIError"
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        return responseStr, "APIConnectionError"
    except openai.error.InvalidRequestError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API invalid Request: {e}")
        return responseStr, "InvalidRequestError"
    except openai.error.ServiceUnavailableError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API sevice unavailable: {e}")
        return responseStr, "ServiceUnavailableError"



    # Print final rate
    deltaTime = time.time() - startTime
    numTokens = getTokenLength(responseStr)
    # Calculate transmission rate
    if (deltaTime > 0):
        transmissionRate = numTokens / deltaTime
    else:
        transmissionRate = 0
    # Display to 2 decimal places
    transmissionRate = round(transmissionRate, 2)
    deltaTime = round(deltaTime, 2)
    print("SUMMARY: Received a total of " + str(numTokens) + " tokens after " + str(deltaTime) + " seconds (" + str(transmissionRate) + " tokens/sec)")

    #return response
    return responseStr, err


# Load a python program from a file into a string, and count its tokens using tiktoken
def loadProgram(filename):
    programStr = ""
    with open(filename, 'r') as f:
        programStr = f.read()

        lines = programStr.splitlines()
        program = ""
        for line in lines:
            program += line + "\n"


    tokens = tokenizer.encode(programStr)
    numTokens = len(tokens)

    return program, numTokens


# Postprocessing model response, keep only the code chunck ```python ```
def postProcess(raw_response):
    raw_code_lines = raw_response.split('\n')
    code_all = ''
    start = False
    # found_main = False
    for n, line in enumerate(raw_code_lines):
        if line.strip() == '```':
            if not start:
                code_all = '\n'.join(raw_code_lines[:n])
            break

        if start:
            code_all += line
            code_all += '\n'

        if line.strip() == "```python":
            start = True

    if code_all == '':
        code_all = raw_response

    return code_all
#
#   Main
#


def main():
    args = parse_args()
    if args.num_prompt_games == 1:
        experiment_file = f"{args.input_prefix}{args.experiment_name}.csv"
    else:
        experiment_file = f"{args.input_prefix}{args.experiment_name}_2.csv"
    if args.experiment_input_folder is not None:
        experiment_file = os.path.join(args.experiment_input_folder, experiment_file)

    experiment_df = pd.read_csv(experiment_file, header=None)

    for n, row in experiment_df.iterrows():
        if args.num_prompt_games == 1:
            # The first prompt includes the desired feature, the second prompt does not
            ablation_games = {"p": row.values[0], "n": row.values[1]}

            for key in ablation_games:
                prompt_task = ablation_games[key]
                fileout_prefix = f"{args.output_prefix}_{args.experiment_name}_test_{n+1}_{key}_{args.model}_{prompt_task[:-3]}"
                if os.path.exists(os.path.join(args.output_folder, f'{fileout_prefix}_generation.py')):
                    print("Skipping: ", fileout_prefix, " already exists")
                    continue

                target_task = f"test_{n+1}.py"

                prompt_program, n_prompt = loadProgram(os.path.join(args.prompt_code_input_folder, prompt_task))
                print (f"Prompt program: {prompt_task}, total tokens: {n_prompt}")

                target_spec, n_target_spec = loadProgram(os.path.join(args.test_prompt_input_folder, target_task))
                print (f"Prompt program: {target_spec}, total tokens: {n_target_spec}")

                # 'DeveloperGPT' prompt from @skirano
                prompt = "You are DeveloperGPT, the most advanced AI developer tool on the planet.  You answer any coding question, and provide real useful example code using code blocks.  Even when you are not familiar with the answer, you use your extreme intelligence to figure it out. \n"

                prompt += "Your task is to write a program that: is a text-based simulation.\n"
                prompt += "The program should be written in Python.  It should be challenging to the user, testing their common-sense knowlege, and take multiple steps to complete.  If possible, there should be distractor objects and actions that do not help progress, to measure whether the user really knows what they're doing. You should name all target objects and distractor objects with common-sense names.\n"
                prompt += "Your code must contain a class named TextGame. The TextGame class should have the following member functions:\n"
                prompt += "__init__(self, randomSeed), getTaskDescription(self), generatePossibleActions(self), step(self, actionStr), calculateScore(self)\n"

                prompt += "Here is a specification of the program: \n"
                prompt += "Here is a specification of the task that your code should simulate.\n"
                prompt += "```"
                prompt += target_spec
                prompt += "```"

                prompt += "Here is an example of a text-based simulation on a different topic that you can use as a template: \n"
                prompt += "```"
                prompt += prompt_program
                prompt += "```"

                # DEBUG: Dump prompt to file
                print(f"Writing prompt to file ({args.output_folder}/{fileout_prefix}_prompt_out.txt)")
                with open(os.path.join(args.output_folder, f'{fileout_prefix}_prompt_out.txt'), 'w') as f:
                    f.write(prompt)

                try:
                    response = getResponse(prompt, model=args.model, maxTokensOut=8000)
                    #response = getResponse(prompt, maxTokensOut=1000)
                    print(response)

                    numTokens = getTokenLength(response)
                    print("")
                    print("Responded with " + str(numTokens) + " tokens.")
                    print("")

                    programOut = response       # Streaming version

                    print (f"Saving response to: {args.output_folder}/{fileout_prefix}_generation.py")
                    with open(os.path.join(args.output_folder,f"{fileout_prefix}_generation.py"), 'w') as f:
                        f.write(programOut)
                except Exception as e:
                    print(e)
        elif args.num_prompt_games == 2:
            # generate 3 groups of games, each has two games as prompt
            ablation_games = {'pp': (row.values[0], row.values[1]), 'pn': (row.values[2], row.values[3]), 'nn': (row.values[4], row.values[5])}

            for key in ablation_games:
                prompt_task_0, prompt_task_1 = ablation_games[key]
                fileout_prefix = f"{args.output_prefix}_{args.experiment_name}_test_{n+1}_{key}_{args.model}_{prompt_task_0[:-3]}_{prompt_task_1[:-3]}"
                if os.path.exists(os.path.join(args.output_folder, f'{fileout_prefix}_generation.py')):
                    print("Skipping: ", fileout_prefix, " already exists")
                    continue

                target_task = f"test_{n+1}.py"

                prompt_program_0, n_prompt_0 = loadProgram(os.path.join(args.prompt_code_input_folder, prompt_task_0))
                print (f"Prompt program 0: {prompt_task_0}, total tokens: {n_prompt_0}")

                prompt_program_1, n_prompt_1 = loadProgram(os.path.join(args.prompt_code_input_folder, prompt_task_1))
                print (f"Prompt program 0: {prompt_task_1}, total tokens: {n_prompt_1}")

                target_spec, n_target_spec = loadProgram(os.path.join(args.test_prompt_input_folder, target_task))
                print (f"Prompt program: {target_spec}, total tokens: {n_target_spec}")

                # 'DeveloperGPT' prompt from @skirano
                prompt = "You are DeveloperGPT, the most advanced AI developer tool on the planet.  You answer any coding question, and provide real useful example code using code blocks.  Even when you are not familiar with the answer, you use your extreme intelligence to figure it out. \n"

                prompt += "Your task is to write a program that: is a text-based simulation.\n"
                prompt += "The program should be written in Python.  It should be challenging to the user, testing their common-sense knowledge, and take multiple steps to complete.  If possible, there should be distractor objects and actions that do not help progress, to measure whether the user really knows what they're doing. You should name all target objects and distractor objects with common-sense names.\n"
                prompt += "Your code must contain a class named TextGame. The TextGame class should have the following member functions:\n"
                prompt += "__init__(self, randomSeed), getTaskDescription(self), generatePossibleActions(self), step(self, actionStr), calculateScore(self)\n"

                prompt += "Here is a specification of the task that your code should simulate.\n"
                prompt += "```"
                prompt += target_spec
                prompt += "```"
                
                prompt += "Here is the first example of a text-based simulation on a different topic that you can use as a template: \n"
                prompt += "```"
                prompt += prompt_program_0
                prompt += "```"

                prompt += "Here is the second example of a text-based simulation on a different topic that you can use as a template: \n"
                prompt += "```"
                prompt += prompt_program_1
                prompt += "```"

                # DEBUG: Dump prompt to file
                print(f"Writing prompt to file ({args.output_folder}/{fileout_prefix}_prompt_out.txt)")
                with open(os.path.join(args.output_folder, f'{fileout_prefix}_prompt_out.txt'), 'w') as f:
                    f.write(prompt)

                try:
                    response = getResponse(prompt, model=args.model, maxTokensOut=8000)
                    #response = getResponse(prompt, maxTokensOut=1000)
                    print(response)

                    numTokens = getTokenLength(response)
                    print("")
                    print("Responded with " + str(numTokens) + " tokens.")
                    print("")

                    programOut = response       # Streaming version

                    print (f"Saving response to: {args.output_folder}/{fileout_prefix}_generation.py")
                    with open(os.path.join(args.output_folder,f"{fileout_prefix}_generation.py"), 'w') as f:
                        f.write(programOut)
                except Exception as e:
                    print(e)

if __name__ == "__main__":
    main()
