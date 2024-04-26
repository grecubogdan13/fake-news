import os, glob
import re

path = './output/logic/truths'
count = 0
for filename in glob.glob(os.path.join(path, 'truths_logic*.txt')):
    count+=1
    filename = './output/logic/truths/truths_logic_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        logic = f.read()
        extra_name_labels = re.findall(r'name\([^,)]*\)', logic)
        for name_label in extra_name_labels:
            var = re.findall(r'\(([^)]+)\)', name_label)[0]
            regex = '\(' + var + ', "'+ '([^,)]+)"\)'
            rep = re.findall(regex, logic)
            name = "-".join(rep)
            logic = logic.replace('name('+var+')', name.lower() +'('+var+')')
            to_remove_reg = '\∧ \:op' + '[^(]+' + '\(' + var + '\, ' + '[^)]+\)'
            to_remove = re.findall(to_remove_reg, logic)
            for rem in to_remove:
                logic = logic.replace(rem, '') 
        
        output_file = open('./output/logic_fix/truths/truths_logic_fixed_{}.txt'.format(count), 'w')
        output_file.write(str(logic))

path = './output/logic/myths'
count = 0
for filename in glob.glob(os.path.join(path, 'myths_logic*.txt')):
    count+=1
    filename = './output/logic/myths/myths_logic_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        logic = f.read()
        extra_name_labels = re.findall(r'name\([^,)]*\)', logic)
        for name_label in extra_name_labels:
            var = re.findall(r'\(([^)]+)\)', name_label)[0]
            regex = '\(' + var + ', "'+ '([^,)]+)"\)'
            rep = re.findall(regex, logic)
            name = "-".join(rep)
            logic = logic.replace('name('+var+')', name.lower() +'('+var+')')
            to_remove_reg = '\∧ \:op' + '[^(]+' + '\(' + var + '\, ' + '[^)]+\)'
            to_remove = re.findall(to_remove_reg, logic)
            for rem in to_remove:
                logic = logic.replace(rem, '') 
        
        logic = '¬(' + logic + ')'
        
        output_file = open('./output/logic_fix/myths/myths_logic_fixed_{}.txt'.format(count), 'w')
        output_file.write(str(logic))

path = './output/logic/tweets'
count = 0
for filename in glob.glob(os.path.join(path, 'tweet_logic*.txt')):
    count+=1
    if count<10:
        filename = './output/logic/tweets/tweet_logic_00' + str(count) + '.txt'
    elif count<100:
        filename = './output/logic/tweets/tweet_logic_0' + str(count) + '.txt'    
    else:  
        filename = './output/logic/tweets/tweet_logic_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        logic = f.read()
        extra_name_labels = re.findall(r'name\([^,)]*\)', logic)
        for name_label in extra_name_labels:
            var = re.findall(r'\(([^)]+)\)', name_label)[0]
            regex = '\(' + var + ', "'+ '([^,)]+)"\)' 
            rep = re.findall(regex, logic)
            if(len(rep)==0):
                regex = '\(' + var + ', '+ '([^,)]+)\)'
                rep = re.findall(regex, logic)
            name = "-".join(rep)
            logic = logic.replace('name('+var+')', name.lower() +'('+var+')')
            to_remove_reg = '\∧ \:op' + '[^(]+' + '\(' + var + '\, ' + '[^)]+\)'
            to_remove = re.findall(to_remove_reg, logic)
            for rem in to_remove:
                logic = logic.replace(rem, '') 
        
        if(count<10):
            output_file = open('./output/logic_fix/tweets/tweet_logic_fixed_00{}.txt'.format(count), 'w')
        elif(count<100):
            output_file = open('./output/logic_fix/tweets/tweet_logic_fixed_0{}.txt'.format(count), 'w')
        else:
            output_file = open('./output/logic_fix/tweets/tweet_logic_fixed_{}.txt'.format(count), 'w')
        output_file.write(str(logic))