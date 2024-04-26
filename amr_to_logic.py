from amr_logic_converter import AmrLogicConverter
import os, glob

converter = AmrLogicConverter(use_variables_for_instances=True)

path = './output/amr/truths'
count = 0
for filename in glob.glob(os.path.join(path, 'truths_representation_*.txt')):
    count+=1
    filename='./output/amr/truths/truths_representation_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        amr = f.read()
        logic = converter.convert(amr)
        output_file = open('./output/logic/truths/truths_logic_{}.txt'.format(count), 'w')
        output_file.write(str(logic))

path = './output/amr/myths'
count = 0
for filename in glob.glob(os.path.join(path, 'myths_representation_*.txt')):
    count+=1
    filename='./output/amr/myths/myths_representation_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        amr = f.read()
        logic = converter.convert(amr)
        output_file = open('./output/logic/myths/myths_logic_{}.txt'.format(count), 'w')
        output_file.write(str(logic))

path = './output/amr/tweets'
count = 0
for filename in glob.glob(os.path.join(path, 'tweet_representation_*.txt')):
    count+=1
    if count<10:
        filename='./output/amr/tweets/tweet_representation_00' + str(count) + '.txt'
    elif count<100:
        filename='./output/amr/tweets/tweet_representation_0' + str(count) + '.txt'
    else:
        filename='./output/amr/tweets/tweet_representation_' + str(count) + '.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        amr = f.read()
        logic = converter.convert(amr)
        if(count<10):
            output_file = open('./output/logic/tweets/tweet_logic_00{}.txt'.format(count), 'w')
        elif(count<100):
            output_file = open('./output/logic/tweets/tweet_logic_0{}.txt'.format(count), 'w')
        else:
            output_file = open('./output/logic/tweets/tweet_logic_{}.txt'.format(count), 'w')
        
        output_file.write(str(logic))