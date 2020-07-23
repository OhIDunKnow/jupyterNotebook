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

    return is_match

# regex rules for validation and the flag
validation_config = {
    "flag":"{7H1NK_1n_0Bj3c7z}",

    "rules": [
        {
            "id": 0,
            "input_regex": ["class\\sEmployee:\n(\\s)+pass", "emp1(\\s)?=(\\s)?Employee\\(\\)", "type\\(emp1\\)"]
            
        },

        {
            "id": 1,
            "input_regex": [
                            "first_name(\\s)?=(\\s)?(\"|')John(\"|')", "last_name(\\s)?=(\\s)?(\"|')Smith(\"|')", 
                            "def(\\s)get_fullname\\(self\\):\\n(\\s)+return(\\s)self\\.first_name(\\s)?\\+(\\s)?(\"|') (\"|')(\\s)?\\+(\\s)?self\\.last_name",
                            "def(\\s)set_fullname\\(self,(\\s)?first_name,(\\s)?last_name\\):\\n(\\s)+self\\.first_name(\\s)?=(\\s)?first_name\\n(\\s)+self\\.last_name(\\s)?=(\\s)?last_name",
                            "print\\(emp1\\.get_fullname\\(\\)\\)",
                            "emp1\\.set_fullname\\((\"|')Jacob(\"|'),(\\s)?(\"|')Burch(\"|')\\)"
                        ]
        },

        {
            "id": 2,
            "input_regex": [
                            "def(\\s)?__init__\\(self,(\\s)?first_name,(\\s)?last_name,(\\s)?phone_number,(\\s)?email\\):",
                            "self\\.first_name(\\s)?=(\\s)?first_name",
                            "self\\.last_name(\\s)?=(\\s)?last_name",
                            "self\\.phone_number(\\s)?=(\\s)?phone_number",
                            "self\\.email(\\s)?=(\\s)?email",
                            "f\\.write\\(self\\.get_fullname\\(\\)(\\s)?\\+(\\s)?(\"|')[\\\][t](\"|')(\\s)?\\+(\\s)?self\\.phone_number(\\s)?\\+(\\s)?(\"|')[\\\][t](\"|')(\\s)?\\+(\\s)?self\\.email(\\s)?\\+(\\s)?(\"|')[\\\][n](\"|')\)",
                            "emp1(\\s)?=(\\s)?Employee\\((\"|')Charlotte(\"|'),(\\s)?(\"|')Hudson(\"|'),(\\s)?(\"|')5555\\s5555(\"|'),(\\s)?(\"|')Charlotte\\.Hudson@company\\.com(\"|')\\)"
                        ]
        },

        {
            "id": 3,
            "input_regex": [
                            "def\\s__str__\\(self\\):\n(\\s)+return\\s(\"|')Employee\\sInfo:[\\\][n](\"|')(\\s)?\\+(\\s)?(\"|')name:\\s(\"|')(\\s)?\+(\\s)?self\\.get_fullname\\(\\)(\\s)?\\+(\\s)?(\"|')[\\\][n](\"|')(\\s)?\\+(\\s)?(\"|')phone number:\\s(\"|')(\\s)?\\+(\\s)?self\\.phone_number(\\s)?\\+(\\s)?(\"|')[\\\][n](\"|')(\\s)?\\+(\\s)?(\"|')email:\\s(\"|')(\\s)?\\+(\\s)?self\\.email(\\s)?\\+(\\s)?(\"|')[\\\][n](\"|')",
                            "def\\s__eq__\\(self, other_employee\\):\\n(\\s)+if\\sisinstance\\(other_employee,(\\s)?Employee\\):\n(\\s)+return self\\.get_fullname\\(\\)(\\s)?==(\\s)?other_employee\\.get_fullname\\(\\)\\n(\\s)+return False"
                        ]
        },

        {
            "id": 4,
            "input_regex": [
                            "def __init__\\(self,(\\s)?first_name,(\\s)?last_name,(\\s)?phone_number,(\\s)?email,(\\s)?modules\\s?=\\s?None\\):",
                            "super\\(\\)\\.__init__\\(first_name,(\\s)?last_name,(\\s)?phone_number,(\\s)?email\\)",
                            "self\\.modules(\\s)?=(\\s)?modules"
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
        
        # print output if the code cell has output:
        if 'outputs' in cell.keys() and len(cell['outputs']) > 0:
            if 'text' in cell['outputs'][0].keys():
                print(cell['outputs'][0]['text'].strip())

            elif cell['outputs'][0]['output_type'] == 'error':
                print(''.join(cell['outputs'][0]['traceback']))

            elif 'text/plain' in cell['outputs'][0]['data'].keys():
                print(cell['outputs'][0]['data']['text/plain'].strip())

        # validate input
        validate_answer(rule['input_regex'], cell['source']) 
                
        print('------------------------')
        print('\n\n')



    if is_complete:
        print("Congratulations! You have completed all challenges, here's your flag: ")
        print(bcolors.OKBLUE + flag + bcolors.ENDC)
    else:
        print('Please try again !')


