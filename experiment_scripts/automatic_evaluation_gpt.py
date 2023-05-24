import argparse
import openai               # pip install openai
import tiktoken             # pip install tiktoken
import os
import json
import time
import pandas as pd

from requests.exceptions import ChunkedEncodingError

# Tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# OpenAI API Key
key_file = "api-key"
with open(key_file) as f:
    OPENAI_API_KEY = f.read().strip()
openai.api_key = OPENAI_API_KEY

# arg parser
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_prefix", type=str, default='')
    parser.add_argument("--experiment_name", choices=["object", "action", "score_method", "distractor"])
    parser.add_argument("--generated_game_folder", type=str, default="../cleaned_generated_game")
    parser.add_argument("--test_prompt_input_folder", type=str, default="../test_prompts")
    parser.add_argument("--evaluation_form", type=str, default="test_eval.csv")
    parser.add_argument("--output_folder", type=str, default="../output_eval")
    parser.add_argument("--model", type=str, default="gpt-4")

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
    maxPossibleTokens = 8100 - numPromptTokens
    if (maxTokensOut > maxPossibleTokens):
        print("Warning: maxTokensOut is too large given the prompt length (" + str(numPromptTokens) + ").  Setting to max generation length of " + str(maxPossibleTokens))
        maxTokensOut = maxPossibleTokens

    # Record start time of request
    startTime = time.time()

    # Collect the stream
    collectedChunks = []
    collectedMessages = []
    responseStr = ""
    err = ""

    try:
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
        spec = ""
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

def build_requirement_text(evaluation_form_df, experiment, test_id):
    requirement = evaluation_form_df[experiment][int(test_id)-1]
    requirement_text = ''
    if experiment == 'object':
        requirement_text = f"Does the simulation have the object {requirement}?\n"
    elif experiment == 'distractor':
        requirement_text = f"Are the distractors required by the specification implemented in the simulation?\n"
    elif experiment == 'action':
        requirement_text = f"Does the simulation have the action {requirement}?\n"
    
    return requirement_text

def parse_game_file_name(game_file_name):
    splited_name = game_file_name[:-3].split("_")
    experiment, test_id, fold, model, prompt_game_name = None, None, None, None, None
    if len(splited_name) == 8:
        _, experiment, _, test_id, fold, model, prompt_game_name, _ = splited_name
    elif len(splited_name) == 8:
        _, experiment1, experiment2, _, test_id, fold, model, prompt_game_name, _ = splited_name
        experiment = f"{experiment1}_{experiment2}"

    return experiment, test_id, fold, model, prompt_game_name

#
#   Main
#

def main():
    args = parse_args()

    eval_results_p = {}
    eval_results_n = {}

    games = os.listdir(args.generated_game_folder)
    # games = ["lit-lightbulb.py","volume-container.py"]
    for game_file_name in games:
        experiment, test_id, fold, model, _ = parse_game_file_name(game_file_name)

        

        if experiment == None:
            continue


        with open(args.evaluation_form) as f:
            evaluation_form_df = pd.read_csv(f)

        eval_requirement = build_requirement_text(evaluation_form_df, experiment, test_id)

        if eval_requirement == '':
            continue

        simulation_prompt, n_prompt = loadProgram(f"{args.test_prompt_input_folder}/test_{test_id}.py")
        print (f"Prompt: {simulation_prompt}, total tokens: {n_prompt}")

        generated_game, n_generated_game = loadProgram(f"{args.generated_game_folder}/{game_file_name}")
        print (f"Prompt program: {generated_game}, total tokens: {n_generated_game}")

        # 'DeveloperGPT' prompt from @skirano
        prompt = "You are DeveloperGPT, the most advanced AI developer tool on the planet.  You answer any coding question, and provide real useful example code using code blocks.  Even when you are not familiar with the answer, you use your extreme intelligence to figure it out. \n"

        prompt += "Your task is to evaluate a program that is a text-based simulation.\n"

        prompt += "Here is a specification of the simulation: \n"
        prompt += "```"
        prompt += simulation_prompt
        prompt += "```\n"

        prompt += "Here is the code of the simulation \n"
        prompt += "```"
        prompt += generated_game
        prompt += "```\n"
        prompt += "Answer the following question based on the given specification and the simulation code:\n"
        prompt += eval_requirement

        prompt += "Answer 'Yes' or 'No' first and briefly explain your answer."

        # DEBUG: Dump prompt to file
        print(f"Writing prompt to file ({args.output_folder}/test_{test_id}_{experiment}_{fold}_evaluation_prompt.txt)")
        with open(os.path.join(args.output_folder, f'test_{test_id}_{fold}_evaluation_prompt.txt'), 'w') as f:
            f.write(prompt)

        response = getResponse(prompt, model=args.model, maxTokensOut=8000)
        print(response)

        numTokens = getTokenLength(response)
        print("")
        print("Responded with " + str(numTokens) + " tokens.")
        print("")

        if fold == 'p':
            if experiment in eval_results_p:
                eval_results_p[experiment][f"test_{test_id}"] = response
            else:
                eval_results_p[experiment] = {f"test_{test_id}":response}
        elif fold == 'n':
            if experiment in eval_results_n:
                eval_results_n[experiment][f"test_{test_id}"] = response
            else:
                eval_results_n[experiment] = {f"test_{test_id}":response}
        


    print (f"Saving evaluation response to: {args.output_folder}/evaluation_response.json")
    with open(os.path.join(args.output_folder,f"evaluation_response.json"), 'w') as f:
        json.dump({"p":eval_results_p, "n": eval_results_n}, f)




if __name__ == "__main__":
    main()



