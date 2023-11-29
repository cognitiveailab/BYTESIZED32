import os
import sys
from functools import lru_cache
from requests.exceptions import ChunkedEncodingError

import openai
import tiktoken

from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


if sys.version_info >= (3, 12):
    from itertools import batched
else:
    def batched(iterable, n: int):
        """ Yield batches of n elements. """
        batch = []
        for item in iterable:
            batch.append(item)
            if len(batch) == n:
                yield batch
                batch = []

        if batch:
            yield batch


@lru_cache()
def get_tokenizer(model):
    return tiktoken.encoding_for_model(model)


def count_tokens(text, model=None):
    """ Get the number of tokens for a string, measured using tiktoken. """

    model = model or "gpt-4"
    if isinstance(model, str):
        tokenizer = get_tokenizer(model)
    else:
        # Assume model is a namedtuple (model_name, tokenizer)
        tokenizer = model.tokenizer

    return len(tokenizer.encode(text))


# OpenAI API Key
try:
    key_file = "api-key"
    with open(key_file) as f:
        OPENAI_API_KEY = f.read().strip()
    openai.api_key = OPENAI_API_KEY
except:
    pass

openai.api_key = openai.api_key or os.getenv("OPENAI_API_KEY")


@retry(
    reraise=True,
    stop=stop_after_attempt(1000),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=(
        retry_if_exception_type(openai.error.APIError)
        | retry_if_exception_type(openai.error.APIConnectionError)
        | retry_if_exception_type(openai.error.RateLimitError)
        | retry_if_exception_type(openai.error.ServiceUnavailableError)
    ),
)
def call_gpt(model, **kwargs):
    kwargs["temperature"] = 0.0
    kwargs["top_p"] = 1
    kwargs["frequency_penalty"] = 0.0
    kwargs["presence_penalty"] = 0.0
    kwargs["request_timeout"] = 4*10*60  # 40 minutes

    if openai.api_type == "azure":
        # When using the Azure API, we need to use engine instead of model argument.
        kwargs["engine"] = model
    else:
        kwargs["model"] = model

    try:
        response = openai.ChatCompletion.create(**kwargs)
    except Exception as e:
        print(e)
        raise e

    return response


@retry(
    reraise=True,
    stop=stop_after_attempt(1000),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=(
        retry_if_exception_type(openai.error.Timeout)
    ),
)
def llm_gpt(prompt, model="gpt-3.5-turbo", n=1, **kwargs):
    response = call_gpt(model=model, messages=[{"role": "user", "content": prompt}], n=n, **kwargs)

    if n == 1:
        choice = response["choices"][0]
        output = choice["message"]["content"].strip()
    else:
        output = []
        for choice in response["choices"]:
            output.append(choice["message"]["content"].strip())

    return output


def stream_llm_gpt(prompt, model="gpt-3.5-turbo", **kwargs):
    messages = [{"role": "user", "content": prompt}]

    response = ""
    while True:
        try:

            stream = call_gpt(stream=True, model=model, messages=messages, **kwargs)
            pbar = tqdm(stream, unit="token", total=kwargs.get("max_tokens", 8*1024), leave=False)
            for chunk in pbar:
                chunk_content = chunk['choices'][0]['delta'].get('content')

                if chunk_content:
                    response += chunk_content
                    pbar.set_postfix_str(f"...{response[-70:]!r}")

                    nb_tokens = count_tokens(chunk_content)
                    pbar.update(nb_tokens)
            else:
                pbar.close()
                break

        except (openai.error.Timeout, ChunkedEncodingError) as e:
            # Append the response we received so far to messages.
            if len(messages) == 1:
                messages.append({"role": "assistant", "content": response})

            messages[-1] = {"role": "assistant", "content": response}
            print(e)

    return response


def load_program(filename):
    with open(filename, 'r') as f:
        program = f.read()

    return program


def extract_python_code(raw_response):
    # Postprocess response, keep only the code chunks between "```" and "```"
    # Iterate over all code chunks and return the biggest.
    code = ""
    code_chunks = raw_response.split("```")
    for i in range(1, len(code_chunks), 2):
        code_chunk = code_chunks[i]
        if code_chunk.startswith("python\n"):
            code_chunk = code_chunk[7:]

        if len(code_chunk) > len(code):
            code = code_chunk

    return code


def get_empty_metrics():
    return {
        "validity": {
            "TextGame": False,
            "runnable": False,
            "winnable": False,
            "getTaskDescription": False,
            "generatePossibleActions": False,
            "step": False, # has the member function step
            "calculateScore": False,
            "num_valid_actions": 0,
            "error_msg": '',
        },
        "compliance": {
            "fold": "",
            "experiment": "",
            "passed": False,
            "response_msg": ''
        },
        "winnability": {
            "gpt_done": False,
            "gpt_bug": False,
            "num_actions": 0,
            "score": 0,
            "game_won": False,
            "done": False,
            "step": 0,
            "max_steps": 0,
            "history": [],
            "transcript": "",
            "init_prompt": "",
        },
        "alignment": {
            "score": 0,
            "error_msg": "",
            "evaluations": [],
        },
    }
