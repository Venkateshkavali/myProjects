# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 19:24:40 2020

@author: venka
"""

#def dummyFileReader():
#    with open('data_p2.txt','r') as f: #we open the file in 'read' mode. The 'with' clause is similar to 'finally' clause
#        for line in f: #iterate over the file line by line
#            #s = line.strip() #strip() removes the endline character at the end of the line. Line is of type 'str'

def computeMedian():
    """
    The function has no input parameter, return median value of the list
    """
    # YOUR CODE HERE
    list1 = []
    list2 = []
    list3 =[]
    list4 =[]
    #toto= float(0)
    #count = 0
    from ast import literal_eval
    with open('data_p2.txt','r')as f:
         for line in f: #iterate over the file line by line
            s = line.strip()
            list1.append(s)
            #print(type(literal_eval(s)))
    #print(list1)
    for ele in list1:
            try:
                if type(literal_eval(ele)) is float:
                    list2.append(literal_eval(ele))
                    #print(literal_eval(ele))
                    
            except (ValueError, SyntaxError):
                list3.append(ele)
        # A string, so return str
                #return str
    list4 = sorted(list2)
    #print(list4[476])
    #print(len(list4))
    n = len(list4)
    if n%2 ==0:
        x= int(n/2)
        median = (list[x]+list[x+1])/2
        print(median)
    else:
        x= int(n/2)
        #print(x)
        median = list4[x]
        print(median)
    print(list3)
    
##    Two Envelopes problem: Implement a function, called simulateProblem(), 
#that does the game simulation for the two envelopes problem. 
#Run the simulation 10000 times to figure out the empirical (observed) probability
# of gaining more money when switching and gaining more money when sticking to 
# the original choice. Each simulation operates as follows:
#
#First, randomly pick an envelopes configuration out of the two possible 
#    configurations,  (𝐴,2𝐴)  or  (2𝐴,𝐴) . In the first configuration, 
#    the second envelope has twice the money and in the second configuration,
#    the first envelope has twice the money.
#Next, randomly pick one of the two envelopes.
##Finally, randomly choose to either stick or switch. The program checks if 
#you won (the envelope that picked has more money) or 
#not (the envelope that picked has less money). 
#In case of winning, record if the winning was because of sticking or switching.
#You can perform the random choice as follows, using the np.random.randint() method.
#
#import numpy as np
#print(np.random.randint(2))
#The simulateProblem() function takes no arguments and returns two values, 
#first is a boolean output which is True if you win and False if you lose. 
#In case of a win, the second output is True if the win was due to sticking or 
#the lose was due to switching and False if the win was due to switching or 
#the lose was due to sticking.
#
#Once the method simulateProblem() that does the above steps and 
#returns "sticking",or "switching", depending on the win/loss scenario, 
#run the method 1000 times and count the number of times the win was due to 
#sticking to the pick in Step 2, and number of times the win was due to 
#switching the envelope.

import numpy as np
def simulateProblem():
    # YOUR CODE HERE
    #print(np.random.randint(2))
    #A,2A = 0
    #2A,A = 1
    # randonly picking A, 2A = 0
    #randonly picking A, 2A = 1
    #win due to Stick = 0
    #win due to Switch = 1
    result = ""
    for i in range(0,3):
        x = np.random.randint(2)
        result += str(x)
        #print(result)
    if result == "000" or result == "110":
        return (False,False)
    elif result == "001" or result == "111":
        return (True,False)
    elif result == "010" or result == "100":
        return (True,True)
    elif result == "011" or result == "101":
        return (False,True)
    
def run_simulation():
    """
    The function Run the simulation 10000 times to figure out 
    the empirical (observed) probability of gaining more money when switching 
    and gaining more money when sticking to the original choice.
    Return the probability of win due to sticking and win due to switching
    """
    list1 = []
    stick = 0
    switch = 0
    for i in range(10000):
        list1.append(simulateProblem())
        if list1[i][0] == True:
            if list1[i][1] == True:
                stick += 1
            elif list1[i][1] == False:
                switch += 1
    prob_stick = stick/10000 
    prob_switch = switch/10000       
    
    return (prob_stick, prob_switch)