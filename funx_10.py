"""Functions to pseudorandomize order of elements in sequences of various length.

by Elena Benini, elena.benini@psych.rwth-aachen.de
March-April 2020

Most of these functions generate pseudorandom sequence of elements according to
certain constraints. These constraints mostly concern relative positions of the
elements (repetition, switch in subsequent positions).

Other functions allow to randomize the rows of custom dataframes to match the
sequences generated with the pseudorandomizing functions

This file can also be imported as a module and contains the following
functions:

    * balanceTransitionsMinus1
    * balanceTransitionsMinus2 - not very useful
    * balanceTransitionsMinus1_str
    * orderStimWithinTasks
    * orderStimWithinTasks_str
    * noStimRepetition
    * shuffle_rows
    * df_BooleanOrder
    * balanceNMinus2_str - still developing
"""

import random, numpy as np
import pandas as pd
from random import randint
import timeit
#myDir = "C:\\Users\\Elena\\Documents\\AA_PhD\\PsychoPy\\"
myDir = "C:\\Users\\Elena\\Documents\\PsychoPy\\"


def balanceTransitionsMinus1(trials):
    """Balance n-1 repetitions and switches

    Generating a sequence of 0 and 1 of desired length, such that number of 0 = number of 1 and the delta
    (N-1 repetitions) - (N-1 switches) is less than 1, in absolute value.

    Parameters
    ----------
    trials: the lenght of the needed sequence (int)

    Returns
    -------
    list
        np.array of length = trials; the number of repetions; number of switches
    """

    maxCounter = 4
    if type(trials) != int or type(maxCounter) != int:
        raise ValueError("trials and maxCounter must be of type integer.")
    if trials%2 != 0:
        raise ValueError("trials argument must be an even integer.")
    if maxCounter <= 0 or trials <= 0:
        raise ValueError("maxCounter and trials must both be greater than 0.")
    seq_Completed = 0
    counter = 0
    while seq_Completed == 0 and counter <= maxCounter:
        lst = np.repeat([0, 1], trials/2)
        perm = np.random.permutation(trials)
        seq = lst[perm]
        rep=0
        sw=0
        zeross = 0
        oness = 0
        #count 0s and ones
        for i in range(trials):
            if seq[i] == 0:
                zeross +=1
            else:
                oness +=1
        #print("there are " + str(zeross) + " zeros and " + str(oness) + " ones")
        #count sw and repetition
        for i in range(trials-1):
            if seq[i] == seq[i+1]:
                rep +=1
            else:
                sw +=1
        diff = rep-sw
        #print("repetition " + str(rep) + " switch " + str(sw))
        if rep == 0: # when the sequence is 010101... or 101010 I switch the first two elements
            seq[0] = seq[1]
            seq[1] = seq[2]
        if diff > 1: # if more rep than sw and delta greater than 1
            Rounds = ((diff - 2) // 4) + 1 # how many rounds I need to fix the imbalance
            #print(str(Rounds))
            for j in range(1, Rounds+1):
                #print("we are in more rep situation")
                strt = randint(0, trials-1) # I start from a random position in the sequence
                success = 0
                for i in range(trials-3): #I loop over the sequence
                    if success == 1:
                        break
                    else:
                        ind = (strt+i)%(trials-2) # increment position
                        if (seq[ind] == seq[ind+1] and seq[ind+1] == seq[ind+2]): #111 o 000
                            first = ind # save first position of the triplet
                            change = ind+1 # save the position to be changed
                            strt1 = randint(0, trials-1)
                            #print("first triplet " + str(seq[first]) + str(seq[change]) + str(seq[first+2]))
                            for k in range(trials-3): #I loop over the sequence
                                ind = (strt1+k)%(trials-2) # increment position
                                # look for 100 o 001 o ( 011 o 110)
                                if (seq[ind] == seq[first] and seq[ind+1] != seq[first] and seq[ind+2] != seq[first]) or (seq[ind] != seq[first] and seq[ind+1] != seq[first] and seq[ind+2] == seq[first]): # look for 100 o 001 o ( 011 o 110)
                                    #print("second triplet " + str(seq[ind]) + str(seq[ind+1]) + str(seq[ind+2]))
                                    temp = seq[change]
                                    seq[change] = seq[ind+1] #swap middle elements of the 2 triplets
                                    seq[ind+1] = temp
                                    success = 1
                                    break
        if diff < -1: # if more switches and again delta greater than 1
            Rounds = ((abs(diff) - 2) // 4) + 1 # how many rounds I need to fix the imbalance
            #print(str(Rounds))
            for j in range(1, Rounds+1):
                #print("we are in more sw situation")
                strt = randint(0, trials-1) # I start from a random position in the sequence
                success = 0
                for i in range(trials-3): #I loop over the sequence
                    if success == 1:
                        break
                    else:
                        ind = (strt+i)%(trials-2) # increment position
                        if (seq[ind] != seq[ind+1] and seq[ind] == seq[ind+2]): # look for 101 or 010
                            first = ind # save first position of the triplet
                            change = ind+1 # save the position to be changed
                            #print("first triplet " + str(seq[first]) + str(seq[change]) + str(seq[first+2]))
                            strt1 = randint(0, trials-1)
                            for k in range(trials-3): #I loop over the sequence
                                ind = (strt1+k)%(trials-2) # increment position
                                if ind != change and ind != first -1: # ensure it doesn't step on the first triplet. There cannot be overlap in the searched triplet in the "more rep" case
                                    #cerca sequenza 110 o 011 o ( 001 o 100)
                                    if (seq[ind] == seq[first] and seq[ind+1] == seq[first] and seq[ind+2] != seq[first]) or (seq[ind] != seq[first] and seq[ind+1] == seq[first] and seq[ind+2] == seq[first]): # (001 o 100) o (110 o 011)
                                        #print("second triplet " + str(seq[ind]) + str(seq[ind+1]) + str(seq[ind+2]))
                                        temp = seq[change]
                                        seq[change] = seq[ind+1] #swap middle elements of the 2 triplets
                                        seq[ind+1] = temp
                                        success = 1
                                        break
        #these redudnant tests check integrity of the sequence after the manipulations
        counter += 1
        rep=0
        sw=0
        zeross = 0
        oness = 0
        for i in range(trials):
            if seq[i] == 0:
                zeross +=1
            else:
                oness +=1
        if zeross != oness:
            raise Warning("number of 0s is different from number of 1s")
        for i in range(1, trials):
            if seq[i] == seq[i-1]:
                rep +=1
            else:
                sw +=1
        if abs(rep-sw) == 1  and zeross == oness:
            seq_Completed=1
        elif abs(rep-sw) != 1 and counter >= maxCounter+1:
            raise Warning("N - 1 transitions couldn't be balanced by balanceTransitionsMinus1 function")
    # if everything ends
    seqAndDiff = [seq.astype(int), rep, sw]
    return seqAndDiff


def balanceTransitionsMinus1_str(trials, task0, task1):
    """Balance n-1 repetitions and switches

    as its _str-less version
    Changing 0 and 1 with strings: task0 and task1 arguments can be int or
    strings

    Parameters
    ----------
    trials: the lenght of the needed sequence (int)
    task0: a string for your task1 name
    task0: a string for your task2 name

    Returns
    -------
    list
        seq of length = trials; the number of repetions; number of switches
    """
    maxCounter = 4
    if type(trials) != int:
        raise ValueError("trials must be of type integer.")
    if trials%2 != 0:
        raise ValueError("trials argument must be an even integer.")
    if trials <= 0:
        raise ValueError("trials must both be greater than 0.")
    seq_Completed = 0
    counter = 0
    while seq_Completed == 0 and counter <= maxCounter:
        seq = [task0, task1]* int(trials/2)
        random.shuffle(seq)
        rep=0
        sw=0
        zeross = 0 # task0
        oness = 0 # task1
        #count task0 and task1
        for i in range(trials):
            if seq[i] == task0:
                zeross +=1
            else:
                oness +=1
        #print("there are " + str(zeross) + " zeros and " + str(oness) + " ones")
        #count sw and repetition
        for i in range(trials-1):
            if seq[i] == seq[i+1]:
                rep +=1
            else:
                sw +=1
        diff = rep-sw
        #print("repetition " + str(rep) + " switch " + str(sw))
        if rep == 0: # when the sequence is 010101... or 101010 I switch the first two elements
            seq[0] = seq[1]
            seq[1] = seq[2]
        if diff > 1: # if more rep than sw and delta greater than 1
            Rounds = ((diff - 2) // 4) + 1 # how many rounds I need to fix the imbalance
            #print(str(Rounds))
            for j in range(1, Rounds+1):
                #print("we are in more rep situation")
                strt = randint(0, trials-1) # I start from a random position in the sequence
                success = 0
                for i in range(trials-3): #I loop over the sequence
                    if success == 1:
                        break
                    else:
                        ind = (strt+i)%(trials-2) # increment position
                        if (seq[ind] == seq[ind+1] and seq[ind+1] == seq[ind+2]): #111 o 000
                            first = ind # save first position of the triplet
                            change = ind+1 # save the position to be changed
                            strt1 = randint(0, trials-1)
                            #print("first triplet " + str(seq[first]) + str(seq[change]) + str(seq[first+2]))
                            for k in range(trials-3): #I loop over the sequence
                                ind = (strt1+k)%(trials-2) # increment position
                                # look for 100 o 001 o ( 011 o 110)
                                if (seq[ind] == seq[first] and seq[ind+1] != seq[first] and seq[ind+2] != seq[first]) or (seq[ind] != seq[first] and seq[ind+1] != seq[first] and seq[ind+2] == seq[first]): # look for 100 o 001 o ( 011 o 110)
                                    #print("second triplet " + str(seq[ind]) + str(seq[ind+1]) + str(seq[ind+2]))
                                    temp = seq[change]
                                    seq[change] = seq[ind+1] #swap middle elements of the 2 triplets
                                    seq[ind+1] = temp
                                    success = 1
                                    break
        if diff < -1: # if more switches and again delta greater than 1
            Rounds = ((abs(diff) - 2) // 4) + 1 # how many rounds I need to fix the imbalance
            #print(str(Rounds))
            for j in range(1, Rounds+1):
                #print("we are in more sw situation")
                strt = randint(0, trials-1) # I start from a random position in the sequence
                success = 0
                for i in range(trials-3): #I loop over the sequence
                    if success == 1:
                        break
                    else:
                        ind = (strt+i)%(trials-2) # increment position
                        if (seq[ind] != seq[ind+1] and seq[ind] == seq[ind+2]): # look for 101 or 010
                            first = ind # save first position of the triplet
                            change = ind+1 # save the position to be changed
                            #print("first triplet " + str(seq[first]) + str(seq[change]) + str(seq[first+2]))
                            strt1 = randint(0, trials-1)
                            for k in range(trials-3): #I loop over the sequence
                                ind = (strt1+k)%(trials-2) # increment position
                                if ind != change and ind != first -1: # ensure it doesn't step on the first triplet. There cannot be overlap in the searched triplet in the "more rep" case
                                    #cerca sequenza 110 o 011 o ( 001 o 100)
                                    if (seq[ind] == seq[first] and seq[ind+1] == seq[first] and seq[ind+2] != seq[first]) or (seq[ind] != seq[first] and seq[ind+1] == seq[first] and seq[ind+2] == seq[first]): # (001 o 100) o (110 o 011)
                                        #print("second triplet " + str(seq[ind]) + str(seq[ind+1]) + str(seq[ind+2]))
                                        temp = seq[change]
                                        seq[change] = seq[ind+1] #swap middle elements of the 2 triplets
                                        seq[ind+1] = temp
                                        success = 1
                                        break
        #these redudnant tests check integrity of the sequence after the manipulations
        counter += 1
        rep=0
        sw=0
        zeross = 0
        oness = 0
        for i in range(trials):
            if seq[i] == task0:
                zeross +=1
            else:
                oness +=1
        if zeross != oness:
            raise Warning("number of " + str(task0) + " is different from number of " + str(task1))
        for i in range(1, trials):
            if seq[i] == seq[i-1]:
                rep +=1
            else:
                sw +=1
        if abs(rep-sw) == 1  and zeross == oness:
            seq_Completed=1
        elif abs(rep-sw) != 1 and counter >= maxCounter+1:
            raise Warning("N - 1 transitions couldn't be balanced by balanceTransitionsMinus1_str function")
    # if everything ends
    seqAndDiff = [seq, rep, sw]
    return seqAndDiff

# nSim = 10000
# trials = 96
# maxCounter = 4
# counter= 0
# balanceTransitionsMinus1_str(trials, "magnit", "parity")
# for i in range(nSim):
#     try:
#         taskSeq = balanceTransitionsMinus1_str(trials, "magnit", "parity")
#     except:
#         counter += 1
# print("times it failed: " + str(counter))

def balanceTransitionsMinus2(trials):
    maxCounter =  10
    if type(trials) != int or type(maxCounter) != int:
        raise ValueError("trials and maxCounter must be of type integer.")
    if trials%2 != 0:
        raise ValueError("trials argument must be an even integer.")
    if maxCounter <= 0 or trials <= 0:
        raise ValueError("maxCounter and trials must both be greater than 0.")
    seq_Completed = 0
    counter = 0
    while seq_Completed == 0 and counter <= maxCounter:
        seqAndDiff = balanceTransitionsMinus1(trials)
        seq = seqAndDiff[0]
        diff = seqAndDiff[1]-seqAndDiff[2]
        change = 0
        # the last element of the to-be first sequence, also the first element of the to be changed triplet
        # edge+1 is the to-be-changed element
        edge = int(trials/2 - 1)
        #if there are more switch and there's a rep at the edge
        if (seq[edge] == seq[edge+1] and diff < 0) or (seq[edge] != seq[edge+1] and diff > 0):
            for i in range(trials-4): # not to step on the edge triplet, starts from edge +2 and stops at edge-2
                # dividing by trials-2 and getting the remainder allows to restart from trial 0 when trial-2 is reached by the loop
                ind = (edge+2+i)%(trials-2)
                # we're in the first case of the if condition, implies an excess of switches
                if seq[edge] == seq[edge+1]:
                    if seq[edge] == seq[edge+2]: # if the triplet is 1/edge/11 (or 0/edge/00)
                        #print("we're in first case, rep at the edge 111 o (000)")
                        if seq[ind] == seq[edge] and seq[ind+1] != seq[edge] and seq[ind+2] == seq[edge]: # look for 101 (or 010)
                            change = ind+1 #save the position
                    else: # the triplet is 110 (or 001), I look for 100 or 001 (or 011 or 110)
                        if (seq[ind] == seq[edge] and seq[ind+1] != seq[edge] and seq[ind+2] != seq[edge]) or (seq[ind] != seq[edge] and seq[ind+1] != seq[edge] and seq[ind+2] == seq[edge]):
                            change = ind+1 #save the position
                else: # if we are in the second term of the initial "if", thus implies an excess of repetitions
                    if seq[edge] == seq[edge+2]: # if 101 (or 010), I look for 111 (or 000)
                        if seq[ind] == seq[edge] and seq[ind+1] == seq[edge] and seq[ind+2] == seq[edge]:
                            change = ind+1 #save the position
                    else: #if the triplet is 1/edge/00 (or 0/edge/11), I look for 110 or 011 (or 001 or 100)
                        if (seq[ind] == seq[edge] and seq[ind+1] == seq[edge] and seq[ind+2] != seq[edge]) or (seq[ind] != seq[edge] and seq[ind+1] == seq[edge] and seq[ind+2] == seq[edge]):
                            change = ind+1 #save the position
                if change > 0: #if adapt change has been found, break the loop and swap triplets middle elements
                    temp = seq[edge+1]
                    seq[edge+1] = seq[change]
                    seq[change] = temp
                    break
            #if an adapt change has NOT been found and this was the last attempt allowed, return an empty seq
            if change == 0 and counter == maxCounter:
                raise Warning("The sequence couldn't be balanced in the " + str(maxCounter) + " iterations allowed." )
                seq = []
                return seq
        # these redundant tests are to test integrity of the sequence after the manipulations
        counter += 1
        zeross = 0
        oness = 0
        for i in range(trials):
            if seq[i] == 0:
                zeross +=1
            else:
                oness +=1
        if zeross != oness:
            raise Warning("number of 0s is different from number of 1s")
        rep=0
        sw=0
        for i in range(1, trials):
            if seq[i] == seq[i-1]:
                rep +=1
            else:
                sw +=1
        #alternate the first and second half of the sequence as a "zipper" to generate a balanced n-2 seq
        seq_zipped = ["null"]*trials
        for i in range(0, int(trials/2)):
            seq_zipped[i * 2] = seq[i]
        for i in range(0, int(trials/2)):
            seq_zipped[i * 2 + 1] = seq[i+int(trials/2)]
        #test the final sequence balance in rep and sw
        rep=0
        sw=0
        for i in range(2, trials):
            if seq_zipped[i] == seq_zipped[i-2]:
                rep +=1
            else:
                sw +=1
        if abs(rep-sw) == 0:
            seq_Completed = 1 #Exit loop
    #if everything went well
    seq_zipped = np.array(seq_zipped)
    return seq_zipped

# test for balanceTransitionsMinus1, balanceTransitionsMinus1_str and balanceTransitionsMinus2
#(change the function in the try clause)
# accuracy test
# nSim = 100
# trials = 96
# task0 = 0
# task1 = 1
# counter= 0
# for i in range(nSim):
#     try:
#         taskSeq = balanceTransitionsMinus1_str(trials, "magnit", "parity")
#         #taskSeq = balanceTransitionsMinus1(trials)
#     except:
#         counter += 1
# print("times it failed: " +str(counter))
#
# # speed test
# # get running time printed
# print("perfomance N-1 in 1k simulations: " + str(timeit.timeit(stmt= "balanceTransitionsMinus1_str(96, 0, 1)", number=1000, setup="from __main__ import balanceTransitionsMinus1_str")))
# print("perfomance N-2 in 1k simulations: " + str(timeit.timeit(stmt= "balanceTransitionsMinus2(96)", number=1000, setup="from __main__ import balanceTransitionsMinus2")))
#
# # output test:
# # test the final sequence of balanceTransitionsMinus1
# rep=0
# sw=0
# trials = 96
# seq = balanceTransitionsMinus1_str(trials, task0, task1)[0]
# print(seq)
# #seq.to_csv(myDir+"balancedMinus1Seq.csv", index=False) # to store it as a .csv in myDir folder
# for i in range(1, trials):
#     if seq[i] == seq[i-1]:
#         rep +=1
#     else:
#         sw +=1
# if abs(rep-sw) != 1:
#     print("the sequence is not balanced in its n-1 transitions. The diff betw sw and rep is different from 1")
#
# # test the final sequence of balanceTransitionsMinus2
# rep=0
# sw=0
# seq_zipped = balanceTransitionsMinus2(trials)
# #seq.to_csv(myDir+"balancedMinus2Seq.csv", index=False) # to store it as a .csv in myDir folder
# for i in range(2, trials):
#     if seq_zipped[i] == seq_zipped[i-2]:
#         rep +=1
#     else:
#         sw +=1
# if abs(rep-sw) != 0:
#     print("the sequence is not balanced in its n-2 transitions. The diff betw sw and rep is different from 0")
#

def orderStimWithinTasks(trials, stimElmns, minusWhat = 1):
    """Assign stimuli to taks in balanced fashion

    Generates a 2-columns array, with column 1 containing the output of a
    transitionBalance function, the second an input-defined set of elements
    s.t.:
    (a)each elemet is repeated same number of times,
    (b) elements do not repeat in subsequent rows and
    (c) each element will be equally often in rows where column1 = 0 and
    rows where column1 = 1.

    minusWhat parameter is 1 by default. You may want to substitute
    balanceTransitionsMinus2 function in the function with the -str newer version
    and call the fun with minusWhat = 2 to have balanced n-2 rep and sw

    Parameters
    ----------
    trials: the lenght of the needed sequence (int)
    stimElmns: list with the elements of the second column
    minusWhat: either 1 for balanceTransitionsMinus1 or 2.

    Returns
    -------
    np.array
        2 columns array with trials rows
    """
    if (trials/2)%len(stimElmns) != 0:
            raise ValueError("stimElmns list length must be a divisor of trials/2, otherwise balancing is not possible by construction. Also, trials must even integer")
    maxCounter = 10
    seqCompleted = 0
    counter = 0
    while seqCompleted == 0 and counter <= maxCounter:
        if minusWhat == 1:
            taskSeq = balanceTransitionsMinus1(trials)[0]
        elif minusWhat == 2:
            taskSeq = balanceTransitionsMinus2(trials)
        else:
            raise ValueError("minusWhat must be either 1, if you want to balance n-1 rep and sw, or 2, if you want to balance n-2 rep and sw")
        stimAndTask = np.c_[taskSeq, np.zeros(trials)] # prepare an array trials*2 where the first column is trialSeq
        timesXtrial = trials/len(stimElmns)/2 # calculate how many times each stim stands with each of the 2 tasks
        stimLst = np.repeat(stimElmns,timesXtrial) # replicate the list with unique stimuli this number of times
        for task in range(2): # for task 0 and 1, create a vector of randomized stimuli
            stimSeq = np.random.permutation(stimLst)
            currTask = np.where(taskSeq == task)[0]
            currPos = 0
            for g in currTask: # paste one randomize vector aside tasks 0s and the other aside 1s
                stimAndTask[g, 1] = stimSeq[currPos]
                currPos += 1
        for j in range(1, trials): # now the stim sequence is checked for stimuli (n-1) repetitions
            if stimAndTask[j, 1] == stimAndTask[j-1, 1]: # if it's found, the first of the j-1,j pair is saved:
                change = stimAndTask[j-1, 1] # which number is that repeats
                itsTask = stimAndTask[j-1, 0] # to which task is it associated
                # look for an adapt position, starts from 2 numbers after the j of the j-1,j pair of numbers:
                # "i" goes from 2 to up to trials - 1, since you want to stop 2 positions before the starting point
                for i in range(2, trials-1):
                    found = [] # found is initially false
                    # ind runs in a circle over the sequence
                    ind = (j+i)%(trials-1) # I want ind to get to 94th position and to restart from 0 at the 95th
                    cond1 = stimAndTask[ind-1, 1] != change # the number before should not be = change
                    cond2 = stimAndTask[ind, 1] != change # the candidate number should not be = change
                    cond3 = stimAndTask[ind+1, 1] != change # the following before should not be = change
                    cond4 = stimAndTask[j-2, 1] != stimAndTask[ind, 1] # the found number should be different from the one before j-1
                    condTask = stimAndTask[ind, 0] == itsTask # the task should be the same assigned to change
                    if cond1 and cond2 and cond3 and cond4 and condTask:
                        found = stimAndTask[ind, 1] # a suitable position has been found, swap change and found
                        stimAndTask[ind, 1] = change # the position in the middle of the triplet takes value change
                        stimAndTask[j-1, 1] = found # the position of the first element of the pair of equal numbers gets the value found
                        break
                if not found and counter == maxCounter:
                    raise Warning("the numbers cannot be correctly assigned to the 0s and the 1s. There are 1 (or more) pairs of 2 equal numbers in subsequent positions")
        # test for numbers assignment
        counter += 1
        vec = [[0]*int(trials/2), [0]*int(trials/2)] # preallocate an array: trials/2 is the max lenght allowed for stimElmn list
        for task in range(2):
            for i in stimElmns: # fill in the array with the times each element is found aside 0 and 1
                vec[task][i] = sum(np.logical_and(stimAndTask[:,1] == i,stimAndTask[:,0] == task))
            vec1 = [vec[task][i] for i in stimElmns] # take only the relevant positions of vec (some will be 0)
            equalTimes = all(x== vec1[0] for x in vec1) # are number of time all the same within a task?
            if (not equalTimes) and counter > maxCounter:
                raise Warning("the function is wrong: stimuli are not equally represented in task " + str(task))
        # test for effectiveness of the removal of numbers repetitions
        bool_2inARow = [stimAndTask[i, 1] == stimAndTask[i-1, 1] for i in range(1,trials)]
        if (any(bool_2inARow)) and counter > maxCounter:
            raise Warning("2 equal stimuli are found in subsequent positions")
        # test for integrity of trialSeq after manipulations
        if not all(taskSeq == stimAndTask[:,0]):
            raise Warning("the final sequence of tasks (0 and 1) is not identical to the starting one. The function should not cause the sequence to change")
        # assign 1 to seqCompleted variable to exit the while loop
        if (not any(bool_2inARow)) and equalTimes:
            seqCompleted = 1
    #return [stimAndTask, taskSeq, counter]
    return stimAndTask

def orderStimWithinTasks_str(trials, stimElmns, task0, task1, minusWhat = 1):
    """Assign stimuli to taks in balanced fashion

    as its _str-less version.
    Generates a 2-columns array, with column 1 containing the output of a
    transitionBalance function, the second an input-defined set of elements
    s.t.:
    (a)each elemet is repeated same number of times,
    (b) elements do not repeat in subsequent rows and
    (c) each element will be equally often in rows where column1 = 0 and
    rows where column1 = 1.

    minusWhat parameter is 1 by default. You may want to substitute
    balanceTransitionsMinus2 function in the function with the ABC version and
    call the fun with minusWhat = 2 to balance n-2 rep and sw

    Parameters
    ----------
    trials: the lenght of the needed sequence (int)
    stimElmns: list with the elements of the second column
    minusWhat: either 1 for balanceTransitionsMinus1 or 2.

    Returns
    -------
    pd.DataFrame
        2 columns df with trials rows
    """
    if (trials/2)%len(stimElmns) != 0:
            raise ValueError("stimElmns list length must be a divisor of trials/2, otherwise balancing is not possible by construction. Also, trials must even integer")
    maxCounter = 10
    seqCompleted = 0
    counter = 0
    while seqCompleted == 0 and counter <= maxCounter:
        if minusWhat == 1:
            taskSeq = np.array(balanceTransitionsMinus1_str(trials, 0, 1)[0])
        elif minusWhat == 2:
            taskSeq = balanceTransitionsMinus2(trials)
        else:
            raise ValueError("minusWhat must be either 1, if you want to balance n-1 rep and sw, or 2, if you want to balance n-2 rep and sw")
        stimAndTask = np.c_[taskSeq, np.zeros(trials)] # prepare an array trials*2 where the first column is trialSeq
        # transform stimELemns into a list of integers to be able to use np arrays
        stim2num = list(range(len(stimElmns)))
        timesXtrial = trials/len(stimElmns)/2 # calculate how many times each stim stands with each of the 2 tasks
        stimLst = np.repeat(stim2num,timesXtrial) # replicate the list with unique stimuli this number of times
        for task in range(2): # for task 0 and 1, create a vector of randomized stimuli
            stimSeq = np.random.permutation(stimLst)
            currTask = np.where(taskSeq == task)[0]
            currPos = 0
            for g in currTask: # paste one randomize vector aside tasks 0s and the other aside 1s
                stimAndTask[g, 1] = stimSeq[currPos]
                currPos += 1
        for j in range(1, trials): # now the stim sequence is checked for stimuli (n-1) repetitions
            if stimAndTask[j, 1] == stimAndTask[j-1, 1]: # if it's found, the first of the j-1,j pair is saved:
                change = stimAndTask[j-1, 1] # which number is that repeats
                itsTask = stimAndTask[j-1, 0] # to which task is it associated
                # look for an adapt position, starts from 2 numbers after the j of the j-1,j pair of numbers:
                # "i" goes from 2 to up to trials - 1, since you want to stop 2 positions before the starting point
                for i in range(2, trials-1):
                    found = [] # found is initially false
                    # ind runs in a circle over the sequence
                    ind = (j+i)%(trials-1) # I want ind to get to 94th position and to restart from 0 at the 95th
                    cond1 = stimAndTask[ind-1, 1] != change # the number before should not be = change
                    cond2 = stimAndTask[ind, 1] != change # the candidate number should not be = change
                    cond3 = stimAndTask[ind+1, 1] != change # the following before should not be = change
                    cond4 = stimAndTask[j-2, 1] != stimAndTask[ind, 1] # the found number should be different from the one before j-1
                    condTask = stimAndTask[ind, 0] == itsTask # the task should be the same assigned to change
                    if cond1 and cond2 and cond3 and cond4 and condTask:
                        found = stimAndTask[ind, 1] # a suitable position has been found, swap change and found
                        stimAndTask[ind, 1] = change # the position in the middle of the triplet takes value change
                        stimAndTask[j-1, 1] = found # the position of the first element of the pair of equal numbers gets the value found
                        break
                if not found and counter == maxCounter:
                    raise Warning("the numbers cannot be correctly assigned to the 0s and the 1s. There are 1 (or more) pairs of 2 equal numbers in subsequent positions")
        # test for numbers assignment
        counter += 1
        vec = [[0]*int(trials/2), [0]*int(trials/2)] # preallocate an array: trials/2 is the max lenght allowed for stimElmn list
        for task in range(2):
            for i in stim2num: # fill in the array with the times each element is found aside 0 and 1
                vec[task][i] = sum(np.logical_and(stimAndTask[:,1] == i,stimAndTask[:,0] == task))
            vec1 = [vec[task][i] for i in stim2num] # take only the relevant positions of vec (some will be 0)
            equalTimes = all(x== vec1[0] for x in vec1) # are number of time all the same within a task?
            if (not equalTimes) and counter > maxCounter:
                raise Warning("the function is wrong: stimuli are not equally represented in task " + str(task))
        # test for effectiveness of the removal of numbers repetitions
        bool_2inARow = [stimAndTask[i, 1] == stimAndTask[i-1, 1] for i in range(1,trials)]
        if (any(bool_2inARow)) and counter > maxCounter:
            raise Warning("2 equal stimuli are found in subsequent positions")
        # test for integrity of trialSeq after manipulations
        if not all(taskSeq == stimAndTask[:,0]):
            raise Warning("the final sequence of tasks (0 and 1) is not identical to the starting one. The function should not cause the sequence to change")
        # assign 1 to seqCompleted variable to exit the while loop
        if (not any(bool_2inARow)) and equalTimes:
            seqCompleted = 1
            # substitute 1 and 0 with the task names
            stimAndTask_df = pd.DataFrame(stimAndTask, columns = ['task', 'stim'])
            task0_indx = stimAndTask_df[stimAndTask_df['task'] == 0].index
            stimAndTask_df.loc[task0_indx, 'task'] = task0
            task1_indx = stimAndTask_df[stimAndTask_df['task'] == 1].index
            stimAndTask_df.loc[task1_indx, 'task'] = task1
            # substitute numerical stim with stim elements
            for s in stim2num:
                s_indx = stimAndTask_df[stimAndTask_df['stim'] == s].index
                stimAndTask_df.loc[s_indx, 'stim'] = stimElmns[s]
    #return [stimAndTask_df, taskSeq, counter]
    return stimAndTask_df

# # test for orderStimWithinTasks performance and correctness
# trials = 96
# #stimLst = list(range(1,5)) + list(range(6,10))
# stimElmns = list(range(3))
# minusWhat = 1
# nSim = 100
# counterSim = [0]*nSim
# for sim in range(nSim):
#     #print i
#     stimAndTask_TaskSeq = orderStimWithinTasks(trials, stimElmns)
#     stimAndTask = stimAndTask_TaskSeq[0]
#     # to check taskSeq integrity and internal counter you have to include them in the list of objects that
#     # orderStimWithinTasks "returns"
#     taskSeq = stimAndTask_TaskSeq[1]
#     counter = stimAndTask_TaskSeq[2]
#     vec = [[0]*(len(stimElmns)+2), [0]*(len(stimElmns)+2)]
#     counterSim[sim] = counter
#     for task in range(2):
#         for i in stimElmns:
#             vec[task][i] = sum(np.logical_and(stimAndTask[:,1] == i,stimAndTask[:,0] == task))
#         vec1 = [vec[task][i] for i in stimElmns]
#         chec = all(x== vec1[0] for x in vec1)
#         if not chec:
#             print ("the function is wrong: stimuli are not equally represented in task " + str(task))
#     # test for effectiveness of the removal of numbers repetitions
#     for jj in range(1, trials):
#             if stimAndTask[jj, 1] == stimAndTask[jj-1, 1]:
#                 print ("2 equal stimuli are found in subsequent positions in sim: " + str(sim))
#     # test for integrity of trialSeq after manipulations you have to include taskSeq in the output
#     if not all(taskSeq == stimAndTask[:,0]):
#         print("the final sequence of tasks (0 and 1) is not identical to the starting one.")
# counterHist = sum([g>1 for g in counterSim])
# print(
#     "the algorithm has run more than once "\
#      + str(counterHist) + " times over " + str(nSim) + " simulations and\
#      \n if no other print has come out, the function has run without errors.")
#
# # test speed in 100 rounds:
# print("orderStimWithinTasks in 100 simulations: " + str(timeit.timeit(stmt= "orderStimWithinTasks(96, list(range(1,5)) + list(range(6,10)), 1)", number = 100, setup="from __main__ import orderStimWithinTasks")))
#
# # further check for orderStimWithinTasks_str
# trials = 96
# stimElmns = ['GLASSES', 'LETTER', 'CAR', 'WALL', 'FLOWER', 'BIRD', 'TREE', 'MONKEY']
# task0 = "magnit"
# task1 = "parity"
# counterSim = [0]*nSim
# nSim = 100
# for sim in range(nSim):
#     stimAndTask = orderStimWithinTasks_str(trials, stimElmns, task0, task1)
#     for i in stimLst:
#         print(sum(stimAndTask["stim"] == i))
#     # test for effectiveness of the removal of numbers repetitions
#     for jj in range(1, trials):
#             if stimAndTask.loc[jj, "stim"] == stimAndTask.loc[jj-1, "stim"]:
#                 print ("2 equal stimuli are found in subsequent positions in sim: " + str(sim))

def noStimRepetition(trials, stimElmns = [1], stimLst = ""):
    """sequence of integers that don't repeat in a row

    Generates a sequence of length trials without n minus 1 repetitions
    At the moment stimElmns CAN BE STR, stimLst MUST BE INT

    Parameters
    ----------
    trials: the lenght of the needed sequence (int)
    stimElmns: list, optional
        with the unique elements of the sequence
    stimLst: list, optional
        a user-defined complete list of lenght = trials

    Returns
    -------
    pd.Series or np.array
        depending on the class of stimElmns, series or array with elements
        repeated trials/len(stimElmns) times or with stimLst
        elements
    """

    if (trials)%len(stimElmns) != 0:
            raise ValueError("stimElmns list length must be a divisor of trials, otherwise balancing is not possible by construction. Also, trials must even integer")
    maxCounter = 10
    seqCompleted = 0
    counter = 0
    while seqCompleted == 0 and counter <= maxCounter:
        #stimAndTask = np.zeros(trials) # prepare a vec
        if stimLst == "": # if stimList is empty, generate it based on stimElmns & trials
            timesXstim = trials/len(stimElmns) # calculate how many times each stim appears
            if any(isinstance(i, int) for i in stimElmns): # if there are str you need transformation
                stim2num = list(range(len(stimElmns))) # transform the elmns in intergers to use np arrays in the fun
            stimLst = np.repeat(stim2num,timesXstim) # replicate the list with unique stimuli this number of times
        stimSeq = np.random.permutation(stimLst) # randomize the list
        for j in range(1, trials): # now the stim sequence is checked for stimuli (n-1) repetitions
            if stimSeq[j] == stimSeq[j-1]: # if it's found, the first of the j-1,j pair is saved:
                change = stimSeq[j-1] # which number is that repeats
                # look for an adapt position, starts from 2 numbers after the j of the j-1,j pair of numbers:
                # "i" goes from 2 to up to trials - 1, since you want to stop 2 positions before the starting point
                for i in range(2, trials-1):
                    found = [] # found is initially false
                    # ind runs in a circle over the sequence
                    ind = (j+i)%(trials-1) # I want ind to get to 94th position and to restart from 0 at the 95th (assuming 96 trials)
                    cond1 = stimSeq[ind-1] != change # the number before should not be = change
                    cond2 = stimSeq[ind] != change # the candidate number should not be = change
                    cond3 = stimSeq[ind+1] != change # the following before should not be = change
                    cond4 = stimSeq[ind] != stimSeq[j-2]# the candidate number should not be = the one before change
                    if cond1 and cond2 and cond3 and cond4:
                        found = stimSeq[ind] # a suitable position has been found, swap change and found
                        stimSeq[ind] = change # the position in the middle of the triplet takes value change
                        stimSeq[j-1] = found # the position of the first element of the pair of equal numbers gets the value found
                        break
                if not found and counter == maxCounter:
                    raise Warning("the numbers cannot be correctly ordered. There are 1 (or more) pairs of 2 equal numbers in subsequent positions")
        # increase counter
        counter += 1
        # test for numbers assignment, only run the test if a stimLst is not given
        if stimLst == "":
            vec = [0]*trials # preallocate an array: trials is the max lenght allowed for stimElmn list
            for i in stim2num: # fill in the array with the times each element is found
                vec[i] = sum(stimSeq == i)
            vec1 = [vec[i] for i in stim2num] # take only the relevant positions of vec (some will be 0)
            equalTimes = all(x == vec1[0] for x in vec1) # are number of times all the same?
            if (not equalTimes) and counter > maxCounter:
                raise Warning("the function is wrong: stimuli are not equally represented")
        # test for effectiveness of the removal of numbers repetitions
        bool_2inARow = [stimSeq[i] == stimSeq[i-1] for i in range(1,trials)]
        if (any(bool_2inARow)) and counter > maxCounter:
            raise Warning("2 equal stimuli are found in subsequent positions")
        if (not any(bool_2inARow)):
            seqCompleted = 1
            if any(isinstance(i, int) for i in stimElmns): # if you need pd.Series
                # substitute numerical stim with stim elements
                stimSeq_series = pd.Series(stimSeq) # create a series to host string elements
                for s in stim2num:
                    s_indx = stimSeq_series[stimSeq_series == s].index
                    stimSeq_series.loc[s_indx] = stimElmns[s]
                return [stimSeq_series, counter]
                #return stimSeq_series
            else:
                return stimSeq
                #return stimSeq_series



#test for effectiveness of the removal of numbers repetitions
nSim = 2
trials = 16
stimElmns = ["1","2","3","4"]
#stimElmns = ['GLASSES', 'LETTER', 'CAR', 'WALL', 'FLOWER', 'BIRD', 'TREE', 'MONKEY']
counterSim = [0]*nSim
for sim in range(nSim):
    stimAndCount = noStimRepetition(trials, stimElmns = stimElmns)
    stimSeq = stimAndCount[0]
    counter = stimAndCount[1]
    counterSim[sim] = counter

    vec = [0]*trials # preallocate an array: trials is the max lenght allowed for stimElmn list
    for i in stimElmns: # fill in the array with the times each element is found
        vec[i] = sum(stimSeq == i)
    vec1 = [vec[i] for i in stimElmns] # take only the relevant positions of vec (some will be 0)
    equalTimes = all(x == vec1[0] for x in vec1) # are number of times all the same?
    if not equalTimes:
        print("the elements are not equally represented")

    for jj in range(1, trials):
            if stimSeq.loc[jj] == stimSeq.loc[jj-1]:
                print ("2 equal stimuli are found in subsequent positions in sim: " + str(sim))
counterHist = sum([g>1 for g in counterSim])
print(
    "the algorithm has run more than once "\
     + str(counterHist) + " times over " + str(nSim) + " simulations and\
     \n if no other print has come out, the function has run without errors."
     )


def shuffle_rows(res, df2shuf, targetCol):
    """merge back a column in the dataframe

    Take the pseudorandomized stimuli or task sequence and re-order the rows of
    the df such that the features in the other columns are matched to the
    psdrandomized column as they were in the initial df.

    Parameters
    ----------
    res: the one-column array resulting from the pseudorandomization
    df2shuf: the df to re-order
    targetCol: a string indicating the name of the column to merge back

    Returns
    -------
    DataFrame
        identical to df2shuf, but in different order.
    """
    # shuffle the dataframe rows to make the final df look more random
    df2shuf = df2shuf.sample(frac=1).reset_index(drop=True)
    # create an empty dataframe that will be output
    df_output = pd.DataFrame(columns = df2shuf.columns)
    # loop over the df2shuf rows to check for a match with ith elemnt of res
    for i in range(len(res)):
        # pick the firt match, thanks to the intial shuffle this still gives
        # a ranomd-enough final df
        ch = df2shuf[df2shuf[targetCol]== res[i]].index[0]
        row = df2shuf.iloc[ch] # create a new row as the matching row
        df_output = df_output.append(row, ignore_index = True) # append the new row
        df2shuf = df2shuf.drop([ch], axis =0) # drop the macthing row from the df2shuf
        df2shuf.reset_index(inplace = True, drop= True) # reset index
    return df_output

def DfBooleanOrder(df2shuf, targetCol, stimSeq, taskCol, taskSeq):
    """merge 2 columns back in the dataframe

    Take the pseudorandomized stimuli AND task sequence and re-order the rows of
    the df such that the features in the other columns are matched to the
    psdrandomized columnS as they were in the initial df.

    Parameters
    ----------
    df2shuf: the df to re-order
    targetCol: a string indicating the name of the column having same values
        as the stimSeq array
    stimSeq: the one-column array resulting from the pseudorandomization that
        matches the values in targetCol
    taskCol: a string indicaticating the name of the column having same values
        as the taskSeq array
    taskSeq: the one-column array resulting from the pseudorandomization that
        matches the values in taskCol

    Returns
    -------
    DataFrame
        identical to df2shuf, but in different order.
    """
    # shuffle the dataframe rows to make the final df look more random
    df2shuf = df2shuf.sample(frac=1).reset_index(drop=True)
    # create an empty dataframe that will be output
    df_output = pd.DataFrame(columns = df2shuf.columns)
    for i in range(len(stimSeq)):
        boolean_condition = (df2shuf[taskCol] == taskSeq[i]) & (df2shuf[targetCol] == stimSeq[i])
        ch = df2shuf.loc[boolean_condition].index[0]
        row = df2shuf.iloc[ch]
        df_output = df_output.append(row, ignore_index = True)
        df2shuf = df2shuf.drop([ch], axis =0)
        df2shuf.reset_index(inplace = True, drop= True)
    return df_output

# # Test for DfBooleanOrder and shuffle_rows
# # create toy variables for the test:
# task = ["magnit", "parity "]
# stim = list(range(1,5)) + list(range(6,10))
# colour = ["red", "blue"] # other features of the trial...
# shape = ["full"]
# feat_comb = pd.DataFrame([(x,y,z) for x in task for y in stim for z in colour], columns=['task', 'stim', 'colour'])
# feat_comb["condID"] = range(len(feat_comb))
# # build a df repeating the combinations a certain number of time, e.g. 3
# trialsPercondition= 2
# trialSeq =  pd.concat([feat_comb]*trialsPercondition, ignore_index=True) #repeat the df with the possible conditions for the number of times we want each repetition
# trialSeq["trID"] = np.arange(len(trialSeq))
# # #trialSeq.to_csv(myDir+"trialSeq")
# # # re order the df using DfBooleanOrder (or shuffle_rows) and then sort the re-ordered as it was before (sorted by trID) and
# # # check if it is identical to the starting one
# df2shuf = trialSeq
# stimElmns = list(set(trialSeq.stim))
# #timesXtask = int(len(taskSeq)/len(stimElmns)/2)
# minusWhat = 1
# trials = len(trialSeq)
# stimAndTaskArray = orderStimWithinTasks_str(trials, stimElmns, minusWhat, task[0], task[1])
# taskSeq = stimAndTaskArray["task"]
# stimSeq = stimAndTaskArray["stim"]
# targetCol = "stim"
# taskCol = "task"
# post_bool = DfBooleanOrder(df2shuf, targetCol, stimSeq, taskCol, taskSeq)
# # or
# post_shuffle = shuffle_rows(taskSeq, df2shuf, taskCol)
# # or..
# post_shuffle = shuffle_rows(stimSeq, df2shuf, targetCol)
# post_bool.sort_values(by = ['trID'], inplace=True)
# post_shuffle.sort_values(by = ['trID'], inplace=True)
# # are the df identical?
# print("is post_bool identical to df2shuf? " + str(all(post_bool.reset_index(drop=True) == df2shuf.reset_index(drop=True))))
# print("is post_shuffle identical to df2shuf? "+ str(all(post_shuffle.reset_index(drop=True) == df2shuf.reset_index(drop=True))))
#
# # Speed tests
# %timeit -r 10 shuffle_rows(stimSeq, df2shuf, targetCol)
# %timeit -r 10 DfBooleanOrder(df2shuf, targetCol, stimSeq, taskCol, taskSeq)


def balanceNMinus2_str(trials, A, B, C):
    """balance n-2 repetitions and switch and avoid n-1 repetitions

    Generates a sequence of length trials of elements A,B and C with almost
    balanced number of sw and repetitions (by now allows a delta of 3, it can
    be restricted to 2 or 1 without the performance changing much)

    Parameters
    ----------
    trials: int
        the lenght of the needed sequence
    A: str,
        name of task A, must be different from B and C
    B: str,
    C: str

    Returns
    -------
    pd.DataFrame
        dataframe with same number of A, B and C and almost balanced n-2
        repetitions and switches
    """

    if type(trials) != int:
        raise ValueError("trials and maxCounter must be of type integer.")
    if trials%2 != 0:
        raise ValueError("trials argument must be an even integer.")
    if trials <= 0:
        raise ValueError("trials must both be greater than 0.")
    maxCounter =  1
    seq_Completed = 0
    counter = 0
    while seq_Completed == 0 and counter <= maxCounter:
        seq = noStimRepetition(trials, [0,1,2])[0]
        rep=0
        sw=0
        for j in range(2, trials):
            if seq[j] == seq[j-2]:
                rep +=1
            else:
                sw +=1
        diff = rep - sw
        #print("this is diff " + str(diff))
        # how big is the imbalance? Establish the number of rounds needed
        Rounds = abs(diff)//4 + abs(diff)%4//3
        for Round in range(Rounds):
            #print("this is round " + str(Round))
            swap = np.empty(1)
            strt = randint(0, trials-1) # 0, 95
            for i in range(trials-6): # 0, 89. It is ok (and possibly useful) if the ind gets as far as 3 positions before the strt
                ind = (strt+i)%(trials-5)
                if seq[ind+1] == seq[ind+4]:
                    if diff > 0: # we have more repetitions
                        cond1 = seq[ind] == seq[ind+2]
                        cond2 = seq[ind+3] == seq[ind+5]
                    elif diff < 0: # we have more switches
                        cond1 = seq[ind] == seq[ind+3]
                        cond2 = seq[ind+2] == seq[ind+5]
                    if cond1 and cond2:
                        #print("this is ind " + str(ind))
                        #print("this are the 6 trials " + str(seq[ind:ind+6]))
                        swap = seq[ind+2]
                        seq[ind+2] = seq[ind+3]
                        seq[ind+3] = swap
                        #print("this are the 6 trials afterwards " + str(seq[ind:ind+6]))
                        break
            if not swap.size and counter == maxCounter: # Non capisco perche non mi stampa mai questo,
                # anche quando dovrebbe
                print("no 5-tuple could be found and rounds are over")
        #tests
        counter += 1
        rep=0
        sw=0
        for i in range(2, trials):
            if seq[i] == seq[i-2]:
                rep +=1
            else:
                sw +=1
        post_diff = rep - sw
        nMinus2Balance = abs(post_diff) <= 2
        #if not nMinus2Balance:
            #print("we have a problem " + str(rep) + " " + str(sw))
        ABCbalance = sum(seq == 0) == sum(seq == 1) == sum(seq == 2)
        if not ABCbalance:
            print("no same number of A, B and C" + str(sum(seq == 0)) + " " + str(sum(seq == 1)) + " " + str(sum(seq == 2)))
        nMinus1Absence = 1
        for i in range(1,trials):
            if seq[i] == seq[i-1]:
                print("there's a n-1 repetition")
                nMinus1Absence = 0
        if nMinus1Absence and ABCbalance and nMinus2Balance:
            seq_Completed = 1
            seq_df = pd.Series(seq)
            taskA = seq_df[seq_df == 0].index
            seq_df.loc[taskA] = A
            taskB = seq_df[seq_df == 1].index
            seq_df.loc[taskB] = B
            taskC = seq_df[seq_df == 2].index
            seq_df.loc[taskC] = C
            #return [seq_df, post_diff, counter]
            return seq_df

# nSim = 100
# counterSim = 0
# coun = [99]*nSim # the 99 allows to immediately see whether one sim didn't yield any correct sequence
# for sim in range(nSim):
#     try:
#         seqANdcount = balanceNMinus2_ABC(96, "a", "b", "c")
#         coun[sim] = seqANdcount[2]
#         seq = seqANdcount[0]
#     except:
#         #seq.to_csv(myDir+ "seq_df" + str(sim) + ".csv", header = True)
#         counterSim += 1
#         print sim
# print "this is the number of times there was an error " + str(counterSim)
# print "this is the history of counter in " + str(nSim) + " simulations: " + str(coun)
