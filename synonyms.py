import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.A
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2): ##treat this like matrix multiplication in our lab.
    print(vec1)
    print(vec2)
    #for letter1 in vec1.keys(), vec2.keys():
    dot_product = 0
    mag_1 = 0
    mag_2 = 0 
    magnitude_1 = list(vec1.values())
    magnitude_2 = list(vec2.values())
    integers1 = []
    integers2 = []
    
    for key in vec1:
        if key in vec2:
            integers1.append(vec1[key])
            integers2.append(vec2[key])
    print(integers1, integers2) #PERFECT :)
    
    for element in range(len(integers1)):
         dot_product += integers1[element]*integers2[element]
    #print(dot_product) #23. WORKS!
         
    for og_element in range(len(magnitude_1)):
         mag_1 += magnitude_1[og_element]**2
    for og_element2 in range(len(magnitude_2)):
         mag_2 += magnitude_2[og_element2]**2
    print(mag_1,",",mag_2) #14, 77 works!
        
    if mag_1==0 or mag_2 == 0:
        return -1
    sim_u_v = (dot_product)/(math.sqrt((mag_1*mag_2))) #i get 0.97, which is also what i get by hand.. not too sure what assignment is asking me for, but it's correct syntaxx. 
    print(sim_u_v)
    return sim_u_v

def build_semantic_descriptors(sentences):
    '''Ideas I have for this function: 1. everytime you have a space, it's a word, and you would need to slice it up then
and then you use the thing similar to the counts that we've done and then make it into a dictionary.'''
    print(sentences)
    counter = {}
    for sentence in sentences: #it's harder to use sets when you are looking at the length rather than the values itself in the list. ' 
        unique = set(sentence) ##code failed to account for avoiding duplicates within its own list. 
        print(unique)
        for word in unique:
            if word not in counter:
                counter[word] = {} #this is the first time... so you don't have repetition... that's interesting.'
            for second_word in unique:
                if second_word != word: #you have not looked at that word.. different. 
                    if second_word not in counter[word]:
                        counter[word][second_word] = 1
                    else: 
                        counter[word][second_word] += 1
    return counter
import re
def build_semantic_descriptors_from_files(filenames):
    '''basically, you need to find ways to integrate file names that are strings in a list to open up as called in through a dictionary and then perform the semantics algorithm above'''
    print(filenames)
    semantics = {} #going to add to it each time. 
    a_sentence = []
    puctuation = "?" and "!" and "."
    paragraphs = ""
    for file in range(len(filenames)):
        with open(filenames[file], "r", encoding="latin1") as input_file:
            paragraphs += input_file.read().lower()
            print(paragraphs)
            sentences = re.split(r'[.!?]+', paragraphs)
            print(sentences)
            #sentences = paragraphs.split(puctuation)
            list_of_lists = [[sentence] for sentence in sentences]
            print(list_of_lists)
            
            result = []
            for considering in list_of_lists:
                words = considering[0].split()
                result.append(words)
            print (result) #yay finally!!!
    final_straw = build_semantic_descriptors(result)
    return final_straw

def most_similar_word(word,choices,semantic_descriptors, similarity_fn):
    print(word)
    print(choices)
    print(semantic_descriptors)
    '''word = "", choices = [], semantic_descriptors = {}, returns THE ELEMENT!!! in the LIST with the largest similarity to the word..'''
    similarities = {}
    max_similarity = -10000
    same_word = []
    not_in_choices = []
    
    #you're going to take two words, one of them being u (u have) and v (from the list) that you're going to have to iterate through and then it's going to go t
    #max_similarity = -1 # in the case that you're going to have a 0 correlation. 
    if word not in semantic_descriptors:
        return choices[0]
    
    for compare in range(len(choices)):
        if choices[compare] not in semantic_descriptors:
            print(choices[compare])
            not_in_choices.append(choices[compare])
            if not_in_choices == choices:
                return choices[0] #a long way of me saying if everything in choices is not in semantic_descriptors... please work!
        if choices[compare] in semantic_descriptors: #that word. We need the corresponding value from it?
            print("here")
            build_semantic_descriptors(choices)
            hi = semantic_descriptors.get(choices[compare])
            print(hi)
            vector1 = semantic_descriptors.get(choices[compare]) #OK THIS WORKS!!!
            vector2 = semantic_descriptors.get(word)
            answer = (similarity_fn(vector1,vector2)) #and then you let the magic work?
            print(answer)
            similarities[choices[compare]] = answer
            print(similarities)
            max_similarity = max(similarities.values())
    for words, sims in similarities.items():
        if sims>max_similarity:
            max_similarity = sims
    for words, sims in similarities.items():
        if max_similarity == sims:
            same_word.append(words)
    print("same words:", same_word)
    print("max word:", same_word[0])
    return same_word[0]
    #return same_word[0] #this way, it should also be able to account for ties. 
    
def run_similarity_test(filename, semantic_descriptors,similarity_fn):
    '''take in a string filename... name of a file and returns the percent of questions on which most_similar_word() guesses the answer correctly using the semantic descriptors'''
    total = []
    correct_guesses = 0
    total_questions = 0

    with open(filename, encoding='latin1') as input_file:
        filetext = input_file.read().lower()
        
        
        for question in filetext.split('\n'):
            one_option = question.split()
            if one_option:
                total.append(one_option)
            #word, correct_answer, *choices = line.strip().split()
            
        for line in total:
            questions = line[0]
            answer = line[1]
            choices = line[2:]
            
            questionable_answer = most_similar_word(question, choices, semantic_descriptors, similarity_fn)
            if questionable_answer == answer:
                correct_guesses +=1
                
            total_questions = len(total)
            percentage = correct_guesses/ total_questions
            return percentage
    
if __name__=='__main__':
    #sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    ##res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    #print(res, "of the guesses were correct")
    #word = "a1"
    #choices = ["blah","a4","a5"]
    #semantic_descriptors = {'a1': {'a2': 1, 'a3': 2}, 'a4': {'a2': 2, 'a3': 1}, 'a5': {'a2': 4, 'a3': 4}}
    #print(most_similar_word(word,choices,semantic_descriptors,cosine_similarity))
    #filenames = ["C:\\development\\test.txt"] #returning a list with strings, not a list of lists. 
    #print(build_semantic_descriptors_from_files(filenames))
    vec1 = {"a": 1, "b": 2, "c": 3}
    vec2 = {"b": 4, "c": 5, "d": 6}
    print(cosine_similarity(vec1,vec2)) #should print 0.70
    #sentences =[["hello"], ["world"]]
    #print(build_semantic_descriptors(sentences))# -*- coding: utf-8 -*-