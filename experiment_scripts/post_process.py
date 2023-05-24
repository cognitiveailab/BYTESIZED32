import os
import re

input_folder = "../output"
output_folder = "../cleaned_generated_game"

for file in os.listdir(input_folder):
    if file.endswith(".py"):
        with open(os.path.join(input_folder, file)) as f:
            raw_code_lines = f.readlines()

        code_all = ''
        code_classes = ''
        start = False
        # found_main = False
        for n, line in enumerate(raw_code_lines):
            if line.strip() == '```':
                if not start:
                    code_all = ''.join(raw_code_lines[:n])
                break
            # if line.strip() == 'if __name__ == "__main__":':
            #     found_main = True
            #     if not start:
            #         code_classes = ''.join(raw_code_lines[:n])

            if start:
                # if not found_main:
                #     code_classes += line
                code_all += line

            if line.strip() == "```python":
                start = True

        if code_all == '':
            code_all = ''.join(raw_code_lines)

        # if code_classes == '':
        #     code_classes = ''.join(raw_code_lines)

        output_file = file
        with open(os.path.join(output_folder, output_file), 'w') as f:
            f.write(code_all)

        # with open(os.path.join(output_folder, f"{output_file}_classes.py"), 'w') as f:
        #     f.write(code_classes)