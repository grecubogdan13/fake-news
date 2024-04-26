import os, glob
import re
import numpy as np
import matplotlib.pyplot as plt
import gensim.downloader as api
from sentence_transformers import SentenceTransformer
import sympy as sp
import tqdm

alpha = 0.35
beta = 0.5
gamma = 0.8
perc = 60

word2vec_model = api.load("word2vec-google-news-300")

modelst = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(aw, bw):
    try:
        a = word2vec_model[aw]
        b = word2vec_model[bw]
    except:
        a = modelst.encode([aw])[0]
        b = modelst.encode([bw])[0]
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    similarity = dot_product / (norm_a * norm_b)
    return similarity

premises_logic = {}
premises_sentences = []


predicate_pattern = r'([\w.-]+)\(([^\)]*)\)'

path = './output/cnf/myths'
count = 0
for filename in glob.glob(os.path.join(path, 'myths_logic_cnf_*.txt')):
    count+=1
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        premise_cnf = f.read()

        premise_predicates = re.findall(predicate_pattern, premise_cnf)
    
        premise_elements = []
        for predicate, arguments in premise_predicates:
            arguments_list = [arg.strip() for arg in arguments.split(',')]
            premise_elements.append((predicate, arguments_list))

        premises_logic[premise_cnf] = premise_elements
        with open(os.path.join(os.getcwd(), './output/sentences/myths/myths_' + str(count) + '.txt'), 'r') as g:
            sentence = g.readline().strip()
            premises_sentences.append(sentence)

premises_logic2 = {}
premises_sentences2 = []

path = './output/cnf/truths'
count = 0
for filename in glob.glob(os.path.join(path, 'truths_logic_cnf_*.txt')):
    count+=1
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        premise_cnf = f.read()

        premise_predicates = re.findall(predicate_pattern, premise_cnf)
    
        premise_elements = []
        for predicate, arguments in premise_predicates:
            arguments_list = [arg.strip() for arg in arguments.split(',')]
            premise_elements.append((predicate, arguments_list))

        premises_logic2[premise_cnf] = premise_elements
        with open(os.path.join(os.getcwd(), './output/sentences/truths/truths_' + str(count) + '.txt'), 'r') as g:
            sentence = g.readline().strip()
            premises_sentences2.append(sentence)

accuracy_list = []
recall_list = []
precision_list = []

# gammas = [0.7, 0.75, 0.8, 0.85, 0.9]

# for gamma in gammas:
fake_information_file = open('./output/final_output/contradictions.txt', 'w') 
obtained_labels_file = open('./output/final_output/labels.txt', 'w') 

path = './output/cnf/tweets'
count = 0
for filename in glob.glob(os.path.join(path, 'tweet_logic_cnf_*.txt')):
    fake = 0
    count+=1
    print(count)
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        tweet_cnf = f.read()
        if count<10:
            g = open(os.path.join(os.getcwd(), './output/sentences/tweets/tweet_00' + str(count) + '.txt'), 'r')
        elif count<100:
            g = open(os.path.join(os.getcwd(), './output/sentences/tweets/tweet_0' + str(count) + '.txt'), 'r')
        else:
            g = open(os.path.join(os.getcwd(), './output/sentences/tweets/tweet_' + str(count) + '.txt'), 'r')
        tweet_sentence = g.readline().strip()

        tweet_predicates = re.findall(predicate_pattern, tweet_cnf)
    
        tweet_elements = []
        for predicate, arguments in tweet_predicates:
            arguments_list = [arg.strip() for arg in arguments.split(',')]
            tweet_elements.append((predicate, arguments_list))

        kk = -1
        for myth_cnf, myth_elements in premises_logic.items():
            substitutions_tweet = []
            substitutions_tweet_2 = []
            substitutions_myth = []
            kk=kk+1
            myth_sentence = premises_sentences[kk]
            
            for (predicate, arguments) in tweet_elements:
                if len(arguments) == 2 and (str(arguments[0]).isdigit() == True or str(arguments[1]).isdigit() == True):
                    substitutions_tweet_2.append((predicate + '(' + arguments[0] + ', ' + arguments[1] + ')', 'y'+str(len(substitutions_tweet_2))))
                elif len(arguments)==2:
                    max_sim = -1
                    substitution = ("","")
                    for(myth_predicate, myth_arguments) in myth_elements:
                        if len(myth_arguments) == 2:
                            mp1 = [x for x in myth_elements if x[1][0]==myth_arguments[0] and len(x[1]) == 1]
                            mp2 = [x for x in myth_elements if x[1][0]==myth_arguments[1] and len(x[1]) == 1]
                            tp1 = [x for x in tweet_elements if x[1][0]==arguments[0] and len(x[1]) == 1]
                            tp2 = [x for x in tweet_elements if x[1][0]==arguments[1] and len(x[1]) == 1]
                            # print(tp2)
                            myth_words = myth_sentence.split()
                            max1=-1
                            idx1=0
                            max2=-1
                            idx2=0
                            for k, word in enumerate(myth_words):
                                clean1 = re.sub(r'[^a-zA-Z.]', '', mp1[0][0])
                                clean2 = re.sub(r'[^a-zA-Z.]', '', mp2[0][0])
                                cs1= cosine_similarity(clean1, word.lower())
                                cs2= cosine_similarity(clean2, word.lower())
                                if(cs1 > max1):
                                    max1 = cs1
                                    idx1 = k
                                if(cs2 > max2):
                                    max2 = cs2
                                    idx2 = k
                            idxx1 = min(idx1, idx2)
                            idxx2 = max(idx1, idx2)
                            s1 = " ".join(myth_words[idxx1:idxx2+1])
                            tweet_words = tweet_sentence.split()
                            max1=-1
                            idx1=0
                            max2=-1
                            idx2=0
                            for k, word in enumerate(tweet_words):
                                clean1 = re.sub(r'[^a-zA-Z.]', '', tp1[0][0])
                                clean2 = re.sub(r'[^a-zA-Z.]', '', tp2[0][0])
                                cs1= cosine_similarity(clean1, word.lower())
                                cs2= cosine_similarity(clean2, word.lower())
                                if(cs1 > max1):
                                    max1 = cs1
                                    idx1 = k
                                if(cs2 > max2):
                                    max2 = cs2
                                    idx2 = k
                            idxx1 = min(idx1, idx2)
                            idxx2 = max(idx1, idx2)
                            s2 = " ".join(tweet_words[idxx1:idxx2+1])
                            cs = cosine_similarity(s1,s2)        
                            if(cs>max_sim):
                                max_sim = cs
                                substitution = (myth_predicate, predicate, myth_arguments, arguments)
                    if max_sim>beta:
                        substitutions_tweet.append((substitution[1] + '(' + substitution[3][0] + ', ' + substitution[3][1] + ')', 'x'+str(len(substitutions_tweet))))
                        substitutions_myth.append((substitution[0] + '(' + substitution[2][0] + ', ' + substitution[2][1] + ')', 'x'+str(len(substitutions_myth))))
                    else:
                        substitutions_tweet_2.append((substitution[1] + '(' + substitution[3][0] + ', ' + substitution[3][1] + ')', 'y'+str(len(substitutions_tweet_2))))
                else:
                    max1 = -1
                    idx1 = 0
                    for k, (myth_predicate, myth_arguments) in enumerate(myth_elements):
                        if len(myth_arguments) == 1:
                            clean1 = re.sub(r'[^a-zA-Z.]', '', predicate)
                            clean2 = re.sub(r'[^a-zA-Z.]', '', myth_predicate)
                            cs = cosine_similarity(clean1, clean2)
                            if cs>max1:
                                max1 = cs
                                idx1 = k
                    if(max1 > gamma):
                        substitutions_myth.append((myth_elements[idx1][0]+'('+myth_elements[idx1][1][0]+')', 'x'+str(len(substitutions_myth))))
                        substitutions_tweet.append((predicate +'(' + arguments[0] + ')', 'x'+str(len(substitutions_tweet))))       
                    else:     
                        substitutions_tweet_2.append((predicate +'(' + arguments[0] + ')', 'y'+str(len(substitutions_tweet_2))))  

            final_myth_formula = str(myth_cnf)
            for (myth_predicate, myth_arguments) in myth_elements:
                if(len(myth_arguments) == 1):
                    myth_atom = myth_predicate + '(' + myth_arguments[0] + ')'
                else:
                    myth_atom = myth_predicate + '(' + myth_arguments[0] + ', '+ myth_arguments[1] + ')'
                parsed_atoms = [x[0] for x in substitutions_myth]
                if(myth_atom not in parsed_atoms):
                    final_myth_formula = final_myth_formula.replace('~'+myth_atom, 'False').replace(myth_atom, 'True')

            final_tweet_formula = tweet_cnf
            for (key, value) in substitutions_myth:
                final_myth_formula = final_myth_formula.replace(key, value)
            for (key, value) in substitutions_tweet:
                final_tweet_formula = final_tweet_formula.replace(key, value)
            for (key, value) in substitutions_tweet_2:
                final_tweet_formula = final_tweet_formula.replace(key, value)

            final_formula = '(' + final_myth_formula.strip() + ') ' + '&' + ' (' + final_tweet_formula.strip() + ')'

            percentage = len(substitutions_tweet) * 100 / (len(substitutions_tweet)+len(substitutions_tweet_2)) 
            if(sp.logic.inference.satisfiable(sp.parsing.sympy_parser.parse_expr(final_formula)) == False and percentage >= perc):
                fake_information_file.write("The sentence \"" + tweet_sentence + "\" is fake because it is in agreement with the myth \"" + myth_sentence + "\".(percentage of matched atoms =" + str(percentage)+ ")\n")
                fake = 1
                break

        kk = -1
        if(fake == 0):
            for truth_cnf, truth_elements in premises_logic2.items():
                substitutions_tweet = []
                substitutions_tweet_2 = []
                substitutions_truth = []
                kk=kk+1
                truth_sentence = premises_sentences2[kk]
                
                for (predicate, arguments) in tweet_elements:
                    if len(arguments) == 2 and (str(arguments[0]).isdigit() == True or str(arguments[1]).isdigit() == True):
                        substitutions_tweet_2.append((predicate + '(' + arguments[0] + ', ' + arguments[1] + ')', 'y'+str(len(substitutions_tweet_2))))
                    elif len(arguments) == 2:
                        max_sim = -1
                        substitution = ("","")
                        for(truth_predicate, truth_arguments) in truth_elements:
                            if len(truth_arguments) == 2:
                                mp1 = [x for x in truth_elements if x[1][0]==truth_arguments[0] and len(x[1]) == 1]
                                mp2 = [x for x in truth_elements if x[1][0]==truth_arguments[1] and len(x[1]) == 1]
                                tp1 = [x for x in tweet_elements if x[1][0]==arguments[0] and len(x[1]) == 1]
                                tp2 = [x for x in tweet_elements if x[1][0]==arguments[1] and len(x[1]) == 1]
                                truth_words = truth_sentence.split()
                                max1=-1
                                idx1=0
                                max2=-1
                                idx2=0
                                for k, word in enumerate(truth_words):
                                    clean1 = re.sub(r'[^a-zA-Z.]', '', mp1[0][0])
                                    clean2 = re.sub(r'[^a-zA-Z.]', '', mp2[0][0])
                                    cs1= cosine_similarity(clean1, word.lower())
                                    cs2= cosine_similarity(clean2, word.lower())
                                    if(cs1 > max1):
                                        max1 = cs1
                                        idx1 = k
                                    if(cs2 > max2):
                                        max2 = cs2
                                        idx2 = k
                                idxx1 = min(idx1, idx2)
                                idxx2 = max(idx1, idx2)
                                s1 = " ".join(truth_words[idxx1:idxx2+1])

                                tweet_words = tweet_sentence.split()
                                max1=-1
                                idx1=0
                                max2=-1
                                idx2=0
                                for k, word in enumerate(tweet_words):
                                    clean1 = re.sub(r'[^a-zA-Z.]', '', tp1[0][0])
                                    clean2 = re.sub(r'[^a-zA-Z.]', '', tp2[0][0])
                                    cs1= cosine_similarity(clean1, word.lower())
                                    cs2= cosine_similarity(clean2, word.lower())
                                    if(cs1 > max1):
                                        max1 = cs1
                                        idx1 = k
                                    if(cs2 > max2):
                                        max2 = cs2
                                        idx2 = k
                                idxx1 = min(idx1, idx2)
                                idxx2 = max(idx1, idx2)
                                s2 = " ".join(tweet_words[idxx1:idxx2+1])
                                cs = cosine_similarity(s1,s2)        
                                if(cs>max_sim):
                                    max_sim = cs
                                    substitution = (truth_predicate, predicate, truth_arguments, arguments)
                        if max_sim>beta:
                            substitutions_tweet.append((substitution[1] + '(' + substitution[3][0] + ', ' + substitution[3][1] + ')', 'x'+str(len(substitutions_tweet))))
                            substitutions_truth.append((substitution[0] + '(' + substitution[2][0] + ', ' + substitution[2][1] + ')', 'x'+str(len(substitutions_truth))))
                        else:
                            substitutions_tweet_2.append((substitution[1] + '(' + substitution[3][0] + ', ' + substitution[3][1] + ')', 'y'+str(len(substitutions_tweet_2))))
                    else:
                        max1 = -1
                        idx1 = 0
                        for k, (truth_predicate, truth_arguments) in enumerate(truth_elements):
                            if len(truth_arguments) == 1:
                                clean1 = re.sub(r'[^a-zA-Z.]', '', predicate)
                                clean2 = re.sub(r'[^a-zA-Z.]', '', truth_predicate)
                                cs = cosine_similarity(clean1, clean2)
                                if cs>max1:
                                    max1 = cs
                                    idx1 = k
                        if(max1 > gamma):
                            substitutions_truth.append((truth_elements[idx1][0] +'(' + truth_elements[idx1][1][0] + ')', 'x'+str(len(substitutions_truth))))
                            substitutions_tweet.append((predicate + '(' + arguments[0] + ')', 'x'+str(len(substitutions_tweet)))) 
                        else:
                            substitutions_tweet_2.append((predicate + '(' + arguments[0] + ')', 'y'+str(len(substitutions_tweet_2)))) 

                final_truth_formula = str(truth_cnf)
                for (truth_predicate, truth_arguments) in truth_elements:
                    if(len(truth_arguments) == 1):
                        truth_atom = truth_predicate + '(' + truth_arguments[0] + ')'
                    else:
                        truth_atom = truth_predicate + '(' + truth_arguments[0] + ', '+ truth_arguments[1] + ')'
                    parsed_atoms = [x[0] for x in substitutions_truth]
                    if(truth_atom not in parsed_atoms):
                        final_truth_formula = final_truth_formula.replace('~'+truth_atom, 'False').replace(truth_atom, 'True')

                final_tweet_formula = tweet_cnf
                for (key, value) in substitutions_truth:
                    final_truth_formula = final_truth_formula.replace(key, value)
                for (key, value) in substitutions_tweet:
                    final_tweet_formula = final_tweet_formula.replace(key, value)
                for (key, value) in substitutions_tweet_2:
                    final_tweet_formula = final_tweet_formula.replace(key, value)
                final_formula = '(' + final_truth_formula.strip() + ') ' + '&' + ' (' + final_tweet_formula.strip() + ')'
                percentage = len(substitutions_tweet) * 100 / (len(substitutions_tweet)+len(substitutions_tweet_2)) 
                if(sp.logic.inference.satisfiable(sp.parsing.sympy_parser.parse_expr(final_formula)) == False and percentage >= perc):
                    fake_information_file.write("The sentence \"" + tweet_sentence + "\" is fake because it is contradicting the truth " + truth_sentence + "\".(percentage of matched atoms =" + str(percentage)+ ")\n")
                    fake = 1
                    break
    obtained_labels_file.write(str(fake)+'\n')
    
    # fake_information_file.close() 
    # obtained_labels_file.close()

#     correct_labels = []
#     with open('./input/correct_labels.txt', 'r') as file:
#         for line in file:
#             correct_labels.append(int(line.strip()))

#     obtained_labels = []
#     with open('./output/final_output/labels.txt', 'r') as file:
#         for line in file:
#             obtained_labels.append(int(line.strip()))

#     print(correct_labels)
#     print(obtained_labels)
#     total = len(correct_labels)
#     correct = sum(1 for a, b in zip(correct_labels, obtained_labels) if a == b)
    
#     accuracy = correct / total 
#     print(accuracy)

#     true_positives = 0
#     false_negatives = 0

#     for i in range(len(correct_labels)):
#         if correct_labels[i] == 1 and obtained_labels[i] == 1:
#             true_positives += 1
#         elif correct_labels[i] == 1 and obtained_labels[i] == 0:
#             false_negatives += 1

#     if true_positives + false_negatives == 0:
#         recall= 0  
#     else:
#         recall_score = true_positives / (true_positives + false_negatives)
#         recall = recall_score
    
#     print(recall)

#     true_positives = 0
#     false_positives = 0

#     for i in range(len(correct_labels)):
#         if correct_labels[i] == 1 and obtained_labels[i] == 1:
#             true_positives += 1
#         elif correct_labels[i] == 0 and obtained_labels[i] == 1:
#             false_positives += 1

#     if true_positives + false_positives == 0:
#         precision = 0  
#     else:
#         precision_score = true_positives / (true_positives + false_positives)
#         precision = precision_score
    
#     print(precision)

#     accuracy_list.append(accuracy)
#     recall_list.append(recall)
#     precision_list.append(precision)


# plt.plot(gammas, accuracy_list, label='Accuracy')
# plt.plot(gammas, precision_list, label='Precision')
# plt.plot(gammas, recall_list, label='Recall')

# plt.xlabel('Monadic Matching Threshold')
# plt.ylabel('Score')
# plt.title('Performance Metrics')
# plt.legend()

# plt.grid(True)
# plt.savefig('./varying_monadic.png')
