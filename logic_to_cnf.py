from sympy import symbols, Not, Implies, And, Or, to_cnf, simplify_logic, sympify
import os, glob
import re

def convert_to_cnf(logical_formula):
    cnf_formula = to_cnf(logical_formula, False, force=True)

    return cnf_formula

def substitute_variables(logical_formula):
    variables = re.findall((r'\b[\w:-]+\([^)]*\)|\b\d+\b'), logical_formula)

    replacement_dict = {}
    for i, variable in enumerate(variables):
        replacement_dict[f'x{i+1}'] = variable
    
    for key, value in replacement_dict.items():
        logical_formula = logical_formula.replace(value, key)

    return logical_formula, replacement_dict

path = './output/logic_fix/truths'
count = 0
for filename in glob.glob(os.path.join(path, 'truths_logic*.txt')):
    count+=1
    filename = './output/logic_fix/truths/truths_logic_fixed_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        logic = f.read()
        logic = logic.replace('∧', '&').replace('∨', '|').replace('¬', '~').replace(':','')
        logic = logic.lower()
        logic,dictionary = substitute_variables(logic) 
        cnf_result = convert_to_cnf(logic)
        for key, value in dictionary.items():
            cnf_result = str(str(cnf_result)+' ').replace(key+' ', value+' ').replace(key+')', value+')')
        output_file = open('./output/cnf/truths/truths_logic_cnf_{}.txt'.format(count), 'w')
        output_file.write(str(cnf_result))
        output_file.close()
        f.close()

path = './output/logic_fix/myths'
count = 0
for filename in glob.glob(os.path.join(path, 'myths_logic*.txt')):
    count+=1
    filename = './output/logic_fix/myths/myths_logic_fixed_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        logic = f.read()
        logic = logic.replace('∧', '&').replace('∨', '|').replace('¬', '~').replace(':','')
        logic = logic.lower()
        logic, dictionary = substitute_variables(logic) 
        cnf_result = convert_to_cnf(logic)
        for key, value in dictionary.items():
            cnf_result = str(str(cnf_result)+' ').replace(key+' ', value+' ').replace(key+')', value+')')
        output_file = open('./output/cnf/myths/myths_logic_cnf_{}.txt'.format(count), 'w')
        output_file.write(str(cnf_result))
        output_file.close()
        f.close()

path = './output/logic_fix/tweets'
count = 0
for filename in glob.glob(os.path.join(path, 'tweet_logic*.txt')):
    count+=1
    if count<10:
        filename = './output/logic_fix/tweets/tweet_logic_fixed_00' + str(count) + '.txt'
    elif count<100:
        filename = './output/logic_fix/tweets/tweet_logic_fixed_0' + str(count) + '.txt'
    else:
        filename = './output/logic_fix/tweets/tweet_logic_fixed_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        logic = f.read()
        logic = logic.replace('∧', '&').replace('∨', '|').replace('¬', '~').replace(':','').replace("\"",'')
        logic = logic.lower()
        logic,dictionary = substitute_variables(logic) 
        cnf_result = convert_to_cnf(logic)
        for key, value in dictionary.items():
            print(key, value)
            cnf_result = str(str(cnf_result)+' ').replace(key+' ', value+' ').replace(key+')', value+')')
            print(cnf_result)
        
        if(count<10):
            output_file = open('./output/cnf/tweets/tweet_logic_cnf_00{}.txt'.format(count), 'w')
        elif(count<100):
            output_file = open('./output/cnf/tweets/tweet_logic_cnf_0{}.txt'.format(count), 'w')
        else:
            output_file = open('./output/cnf/tweets/tweet_logic_cnf_{}.txt'.format(count), 'w')
        output_file.write(str(cnf_result))
        output_file.close()
        f.close()
