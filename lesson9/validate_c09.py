import nbformat
import json
import re
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_notebook_code_cells(path_to_notebook):
    code_cells = []

    with open(path_to_notebook, "r") as f:
        nb = nbformat.read(f, as_version=4)

    i_nb = iter(nb.items())
    cells = next(i_nb)[1]

    for c in cells:
        if c['cell_type'] == 'code' and 'execute' in c['metadata'].keys():
            code_cells.append(c)

    return code_cells


def validate_code(regex, cell_data):
    global is_complete
    pattern = re.compile(regex)
    is_match = bool(re.search(pattern, cell_data))

    if is_match:
        print(bcolors.OKGREEN + "Correct" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Wrong" + bcolors.ENDC)
        is_complete = False

    return is_match


def validate_answer(regex, cell_data):
    global is_complete
    pattern = re.compile(regex)
    is_match = bool(re.search(pattern, cell_data))

    if is_match:
        print(bcolors.OKGREEN + "Correct" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Wrong" + bcolors.ENDC)
        is_complete = False

    return is_match


# read notebook path from command line argument
if len(sys.argv) != 2:
    print("Invalid number of argument")
    sys.exit(-1)

notebook_path = sys.argv[1]
cells = read_notebook_code_cells(notebook_path)

# regex rules for validation and the flag
validation_config = {
    "flag": "{i+er4t0rs_G3N3r4toRs}",

    "rules": [
        {  # Question 01
            "id": 0,
            "code_regex": "content \\= iter\\(content.split\\('.'\\)\\)"
        },

        {  # Question 02
            "id": 1,
            "code_regex": "raise StopIteration"
        },

        {  # Question 03
            "id": 2,
            "code_regex": "yield str\\(start\\)"
        },

        {  # Question 04
            "id": 3,
            "code_regex": "tenSentences \\= \\(i \\+ '. ' \\+ next\\(content\\) for i in numberedList\\)"
        },

        {   # Question 05
            "id": 4,
            "code_regex": "except TypeError as e"
        },

        {   # Question 06
            "id": 4,
            "code_regex": "(page_list\\(3000000\\))|(page_generator\\(3000000\\))|(yield page)|(time_after\\-time_before)",
        }
    ]
}

flag = validation_config['flag']
is_complete = True

cell_num = 0
for c in cells:
    print("Question {0}:".format(cell_num + 1))
    if 'code_regex' in validation_config['rules'][cell_num].keys():
        validate_code(validation_config['rules'][cell_num]['code_regex'], c['source'].strip())

    # if the code cell has output:
    elif "output_regex" in validation_config['rules'][cell_num].keys() and 'outputs' in c.keys() and len(
            c['outputs']) > 0:
        if 'text' in c['outputs'][0].keys():

            # validate output here
            validate_answer(validation_config['rules'][cell_num]['output_regex'], c['outputs'][0]['text'].strip())


        elif c['outputs'][0]['output_type'] == 'error':

            # validate output here
            validate_answer(validation_config['rules'][cell_num]['output_regex'], ''.join(c['outputs'][0]['traceback']))


        elif 'text/plain' in c['outputs'][0]['data'].keys():

            # validate output here
            validate_answer(validation_config['rules'][cell_num]['output_regex'],
                            c['outputs'][0]['data']['text/plain'].strip())
    # if the code cell does not have output
    else:
        if validation_config['rules'][cell_num]['output_regex']:
            print(bcolors.FAIL + "Wrong" + bcolors.ENDC)
            is_complete = False
    print('------------------------')
    print('\n\n')
    cell_num += 1

if is_complete:
    print("Congratulations! You have completed all challenges, here's your flag: ")
    print(bcolors.OKBLUE + flag + bcolors.ENDC)
else:
    print('Please try again !')