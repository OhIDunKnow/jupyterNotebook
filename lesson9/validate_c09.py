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


def validate_answer(regexs, cell_data):
    global is_complete
    
    is_match = True

    for r in regexs:
        pattern = re.compile(r)
        is_match = is_match and bool(re.search(pattern, cell_data))
    
    if is_match:
        print(bcolors.OKGREEN + "Correct" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Wrong" + bcolors.ENDC)
        is_complete = False


# regex rules for validation and the flag
validation_config = {
    "flag":"{i+er4t0rs_G3N3r4toRs}",

    "rules": [
        {
            "id": 0,
            "input_regex": [
                        "content \\= iter\\(content.split\\('.'\\)\\)"

            ]
            
        },

        {
            "id": 1,
            "input_regex": [
                        "raise StopIteration"
            ]
        },

        {
            "id": 2,
            "input_regex": [
                         "yield str\\(start\\)"
            ]
        },

        {
            "id": 3,
            "input_regex": [
                          "tenSentences \\= \\(i \\+ '. ' \\+ next\\(content\\) for i in numberedList\\)"
            ]
        },

        {
            "id": 4,
            "input_regex": [
                           "except TypeError as e"
            ]
        },

        {
            "id": 5,
            "input_regex": [
                            "page_list\\(3000000\\)",
                            "page_generator\\(3000000\\)",
                            "yield page",
                            "time_after\\-time_before"
            ]
        }
    ]
}


if __name__ == '__main__':

    # read notebook path from command line argument
    if len(sys.argv) != 2:
        print("Invalid number of argument")
        sys.exit(-1)

    notebook_path = sys.argv[1]
    code_cells = read_notebook_code_cells(notebook_path)
    flag = validation_config['flag']
    is_complete = True


    for index, (cell, rule) in enumerate(zip(code_cells,validation_config['rules'])):
   
        print("Question {0}:".format(index+1))
        print('--------OUTPUT----------')

        # validate input
        validate_answer(rule['input_regex'], cell['source']) 
                
        print('------------------------')
        print('\n\n')



    if is_complete:
        print("Congratulations! You have completed all challenges, here's your flag: ")
        print(bcolors.OKBLUE + flag + bcolors.ENDC)
    else:
        print('Please try again !')


