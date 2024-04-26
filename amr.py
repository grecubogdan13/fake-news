from transition_amr_parser.parse import AMRParser
import regex as re

parser = AMRParser.from_pretrained('AMR2-structbart-L')

file1 = open('./input/ground_truth.txt', 'r')
Lines = file1.readlines()
 
count = 0
for line in Lines:
    count+=1
    file = open('./output/amr/truths/truths_representation_{}.txt'.format(count), 'w')
    tokens, positions = parser.tokenize(line)
    annotations, machines = parser.parse_sentence(tokens)
    file.write(annotations)

file1 = open('./input/ground_truth_myths.txt', 'r')
Lines = file1.readlines()
 
count = 0
for line in Lines:
    count+=1
    file = open('./output/amr/myths/myths_representation_{}.txt'.format(count), 'w')
    tokens, positions = parser.tokenize(line)
    annotations, machines = parser.parse_sentence(tokens)
    file.write(annotations)

input_file = open('./input/tweets.txt', 'r')
Lines = input_file.readlines()

count=0
for sentence in Lines:
    count+=1
    if(count>100):
        break
    if(count<10):
        file = open('./output/amr/tweets/tweet_representation_00{}.txt'.format(count), 'w')
    elif(count<100):
        file = open('./output/amr/tweets/tweet_representation_0{}.txt'.format(count), 'w')
    else:
        file = open('./output/amr/tweets/tweet_representation_{}.txt'.format(count), 'w')
    tokens, positions = parser.tokenize(sentence)
    annotations, machines = parser.parse_sentence(tokens)
    file.write(annotations)