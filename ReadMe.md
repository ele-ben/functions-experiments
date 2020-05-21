## Python functions to pseudo-randomize order of elements in sequences of various length

by Elena Benini, elena.benini@psych.rwth-aachen.de

March-April 2020

### Quick Start
Download funx_10.py file and make sure to make it callable with

    $ import sys
    $ sys.path.append(r'C:\Users\your_path')

Then import the functions using:

    $ from funx_10 import function_name
    $ # or to load all functions
    $ from funx_10 import *

To get the help of a function type

    $ help(function_name)

### Improvements of version 10
- [balanceNMinus2_str](#balanceNMinus2_str) includes 3 tasks and balance n-2 repetions and switch while avoiding n-1 repetitions
- [balanceTransitionsMinus1_str](#balanceTransitionsMinus1_str) allows to directly insert your task names as strings instead of 0 and 1
- maxCounter is removed from inputs: a safe counter is picked  and placed within
    the function
- [orderStimWithinTasks_str](#orderStimWithinTasks_str) allows again to have task names as strings in the
    output dataframe
- [df_BooleanOrder](#df_BooleanOrder) gives a more "random-looking" dataframe
- [df_BooleanOrder](#df_BooleanOrder) and [shuffle_rows](#shuffle_rows) are optimized to run faster
- [noStimRepetition](#noStimRepetition) allows to build a sequence of integers where 2 equal int
    are never found in subsequent positions
-  noStimRepetition is improved to return a sequence w/o n-1 repetition starting
    from a user-input sequence: this doens't force each element to appear same
    number of times

### Functions list
* [balanceTransitionsMinus1](#balanceTransitionsMinus1)
* [balanceNMinus2_str](#balanceNMinus2_str)
* [balanceTransitionsMinus1_str](#balanceTransitionsMinus1_str)
* [orderStimWithinTasks](#orderStimWithinTasks)
* [orderStimWithinTasks_str](#orderStimWithinTasks_str)
* [noStimRepetition](#noStimRepetition)
* [shuffle_rows](#shuffle_rows)
* [df_BooleanOrder](#df_BooleanOrder)
* [balanceTransitionsMinus2](#balanceTransitionsMinus2) - deprecated

### Some Background

Since the very first steps into programming of psychological experiments, I run into the issue of
generating sequences of stimuli and/or experimental tasks that complied with certain demands while
"looking as random as possible".
Specifically, in cognitive psychology research exploiting task switching paradigms, one usually
wants to balance n - 1 (or n - 2) task switches and task repetitions within each block of trials and, also,
to counterbalance the set of stimuli across the tasks.
Since I couldn't find any ready-made solution across the different existing libraries, I decided to write some
functions that allow to generate sequences of stimuli and tasks of whichever length that I could have used to
realize my experiments.
These functions generate pseudo-random sequence of elements according to certain constraints. These constraints
mostly concern relative positions of the elements (repetition, switch in subsequent positions).

### Overview of the functions

*Below this section, each function is described in more details.*

The first 3 functions ([balanceTransitionsMinus1](#balanceTransitionsMinus1), [balanceNMinus2_str](#balanceNMinus2_str), [balanceTransitionsMinus1_str](#balanceTransitionsMinus1_str)) generate sequences of a desired length, where only two (or 3) elements repeat.
The fourth and fifth functions ([orderStimWithinTasks](#orderStimWithinTasks), [orderStimWithinTasks](#orderStimWithinTasks)) generate a 2-columns array of desired length, where a desired number of elements repeat
in a column, while each is associated the same number of times with each possible element of the other column. The first column is the output of balanceTransitionsMinus1, while the second is a sequence without n-1 repetitions.
The [noStimRepetition](#noStimRepetition) exploits the algorithm used by to generate the second column in orderStimWithinTasks to provide a sequence of elements without n-1 repetitions.
The following functions ([shuffle_rows](#shuffle_rows), [df_BooleanOrder](#df_BooleanOrder)) allow to integrate the sequences generated with the functions above into dataframes that are thought to fully describe
a block of experimental trials. The approach would be to first
generate a dataframe where rows are all of the trials of a generic block, while columns describe the features of each trial (task, stimulus, colour, position, cue-stimulus interval, etc). Then use one of the first 6 functions
to "pseudo shuffle" (a) certain column(s). These functions can conveniently call some feature of the dataframe as inputs (for example, number of rows of the df for the first function). Finally, merge the pseudo-randomized
columns into the original dataframe. If one doesn't like the dataframe approach to block building, she will want to simply exploit the first 6 functions inputing the desired parameters and refrain from using the block-shuffling functions.
The last function, [balanceTransitionsMinus2](#balanceTransitionsMinus2), generates a sequence as its "minus1" version, but in which n-2 switch and repetitions are balanced. This is deprecated since it's very uncommon to seek balance in n-2 transitions while having 2 tasks only: from the definition of n-2 repetition (a sequence like ABA) and switches (CBA), it follows 3 tasks are needed.

The algorithms of the first 6 functions are not deterministic and their functioning depends on the "quality" of the random sequence from which they start. Indeed, in some cases (< 0.0001% for the first the 3rd and the 6th function, 4% for the 4th and the 5th function), they need to re-start from a new random sequence. The functions implementing such algorithms are then written such that different attempts are allowed and, this way, they successfully generate the desired output in over 50000 tests. The probability of a re-start and the successful stats reported heavily depend on:
- number of attempts allowed to the functions (the counter: the higher, the lower the failure rate:
allowing counter = 4 already reduces failure of the 1st function to 0 in 100k tests, with different toy lengths),
- sequences length (the shorter, the higher the probability of a re-start),
- number of repeating elements for the 4th, 5th and 6th functions (again the smaller, the higher).
The success rate is provided for each function, together with an estimation of their running-time.
To implement these functions in one's scripts, given the odds of failure (close to 0) and the average performance of the functions (rather fast), a very sound solution could be to allow an unnecessary high
number of attempts, for example 10.
The functions were enriched by error messages to guide the user through the implementation: these are not supposed to rise when the functions work correctly. When errors appear concerning the inputs given to the function, one should follow the suggestions and adjust the input accordingly. When the errors warn that the output could not be correctly generated, given this event is very rare, one should verify whether she's using the function in a different way with respect to its original purpose.
Email me for any suggestion/question/curiosity you may have.


#### [balanceTransitionsMinus1](#balanceTransitionsMinus1)

Generating a sequence of 0 and 1 of desired length, such that number of 0 = number of 1 and the delta (N-1 repetitions) - (N-1 switches) is less than 1, in absolute value.
It takes as an input the length of the needed sequence (trials) and the number of attempts that the programmer wishes to allow the algorithm (maxCounter).
It returns a np.array of length = trials were repetitions of 0 and 1 in subsequent positions are (almost) balanced.
Description:
Both inputs must be integers and trials MUST be an EVEN number (very common in psychological experiments). Values for trials input must be greater or equal than 10; the algorithm was successfully tested with trials up to 10000.
Since we start with an even number of positions, transitions between positions will necessary be odd, so that it will not be possible to have n-1 repetitions = n-1 switches, thus we aim to make this delta equal to 1, so that the output will have either a N-1 rep more, or a N-1 switch more.
The aim was to rely on an algorithm that doesn't blindly generate random sequences, but rather generates a
single sequence and then adjusts it.
It start with a sequence of 0 and 1, where number of 0 = number of 1 and shuffles it. This leads to a sequence of 0s and 1s randomly ordered.Then, the algorithm counts N-1 repetitions and switches and decide whether the imbalance is greater than 1. If so, then it will either reduces switches or repetitions accordingly. The rationale is to change positions of some 0s and 1s to quasi-balance the number of repetitions and switches. Since exchanging elements implies changes in 4 transitions (the one before and the one after each of the 2 swapped element), the algorithm reasons in terms of triplets where the to-be-exchanged elements stand in the middle of such triplets. This allows to control what happens when an element is changed, given the kind of triplet it belongs to. Thus, the algorithm searches the random sequence for some specific pairs of triplets and it swaps its middle elements. The algorithm looks for a certain triplet and the second triplet of the pair is defined according to the features of the first. According to whether there's an excess or repetitions or switches, the first of the wanted-triplets belongs to a certain set of all the possible triplets. Given the direction of the imbalance and the just-found first triplet, the second of the wanted-triplets belongs to a certain set of all the possible triplets. For example, in a sequence where number of repetitions is greater than switches, the sequence will be searched for triples belonging to the set {111. 000}. If 111 is found, the second triplet must belong to {100, 001}. If 100 is found, the middle elements are swapped and 111 becomes 101 and 100 becomes 110. Placing a 0 within 111 leads to repetitions reduced by 2 and switches increased by 2 (since this a 0-sum situation, thus for each repetition less, there's also a switch more). In the second triplet instead, nothing changes in terms of number of switches and repetition. If the firs triplet found is 000 then the second triplet must belong to {110, 011}. The output will be 010 and, e.g., 100.
When switches are greater than repetition, the desired triplets change, but the rationale is identical.
How these triplets should be can be derived reading the code and the written-in comments. Thus, as commented above, for each successful exchange of middle elements, the balance of switches and repetitions goes up pr down by 4. From this observation and from the size of the starting imbalance between switches and
repetitions, it can be derived how many pairs should be found and manipulated as describes above. Specifically, this number is equal to: = ((|"N-1 rep" - "N-1 sw"| - 2) / 4) + 1, that is the absolute value of the starting difference of rep and sw, minus 2, divided into 4 and taking only the integer part, plus 1.
The (absolute) difference can only be odd, because the transitions are odd, thus either repetitions are odd or sw are odd and the difference between an odd and an even number is always odd.
Thus, the aim is to drive such odd difference to a difference of either 1 or -1 by steps of size 4. When the difference is 1, the sequence is already balanced; when it is 3, 1 round is needed (to drive it to -1), same when difference is 5 (to drive it into 1); when difference is 7, 2 rounds are needed (to drive it to -1), same when is 9 (to drive it to 1). Thus starting from 3 (the formula is
used only when difference is greater than 1), number of rounds is the same each two numbers (3 and 5, 7 and 9, ...) from this the "- 2" in the formula. The division by 4 is due to the steps of length 4 commented above, while the + 1 serves to convert the floor division into a ceiling division.
The success of the algorithm only depends on whether the desired triplets can be found. Indeed, with smaller lengths, like 10 trials instead of 96, failure rate is definitely higher. In order to make sure that the output is eventually obtained, the algorithm is allowed to cycle maxCounter number of times. Namely, if it cannot find the needed triplets, it will restart from a newly randomized
sequence of 0s and 1s. The algorithm is very fast, thus it is probably best practice to allow maxCounter to be = 10. It will never reach that value, but were it to happen, the whole process will take 3.5 x 10e(-3) seconds.
*Performance*: with length = 96 and only 1 attempt allowed, it never failed in 100K tests. It runs 1k loops in
1 second.

#### [balanceNMinus2_str](#balanceNMinus2_str)

This functions was not fully tested as the others, thus it may still contain errors.
Generating a sequence of elements (strings, integers) of desired length, such that each element is equally represented and the delta (N-2 repetitions) - (N-2 switches) is less than 3, in absolute value. Moreover, it avoids n-1 repetitions at all.
It takes as an input the length of the needed sequence (trials) and the 3 strings/integers that repeat in the sequence. Trials input MUST be an EVEN number and a multiple of 3.
It returns a one-column dataframe.
*Description:*
The algorithm is very similar to balanceTransitionsMinus1, except it searches for 5-tuples, within which elements can be swapped and moved to obtain a n-2 repetition more or a -2 switch. Since each correction made swapping elements in the 5-tuples moves the balance of n-2 rep and sw by 4, the final delta between sw and rep depends on the initial unbalance. If this is a multiple of 4, it will be leveled to 0, if it's not, the result will have an unbalance equal to the remainder of initial unbalance/ 4.

#### [balanceTransitionsMinus1_str](#balanceTransitionsMinus1_str)
Identical to balanceTransitionsMinus1, but some code at the end converts 0s and
1s into the input-defined string.

#### [orderStimWithinTasks](#orderStimWithinTasks)

Generates a 2-columns array, with column 1 containing the output of a transitionBalance function, the second
an input-defined set of elements (e.g. numbers) s.t.: (a)each elemet is repeated same number of times,
(b) elements do not repeat in subsequent rows and (c) elements are associated row-wise with the 0s and 1s of
the first column with the same probability, namely each element will be equally often rows where column1 = 0
and rows where column1 = 1.
It takes as an input the number of rows (trials); the list of elements, where number of elements must be divisor
of trials/2 (otherwise it'll not be possible to repeat each element same number of times, nor to associate it
equally frequently to each 0, 1); minusWhat that indicates whether column1 should be the output of
balanceTransitionsMinus1 or of balanceTransitionsMinus2 function; maxCounter that has same meaning of
maxCounter in balanceTransitionsMinus1
It returns a 2-columns np.array as described.
*Performance*: with trials = 96 and len(stimElmns) = 8, it does not fail in 1000 tests in each of which only one
round was sufficient to get a correct output.
It needs 7 seconds for 1k tests. Trials input must be greater or equal 10 and can go up to 10k;
len(stimElemns) = 3 is the minimum allowed. With this value, the algorithm needs 3-4 rounds less than 1%, but
never more than 4 in thousands of simulations. maxCounter = 10 should be a safe choice.
*Description:*
The rationale is to randomize the elements sequence and then to adjust it to fix eventual repetitions
in subsequent rows. Two vectors of elements of the correct length are created repeating the stimElmns input
timesXtrial times, that is = trials/len(stimElmns)/2. These two vectors are permuted to shuffle elements order,
then one is pasted only in rows where column1 = 0 and the other in the remaning rows, where column1=1.
This way elements in column2 are equally frequently associated with 0s and 1s of column 1. Such column 2 is then
checked for repetitions of elements in subsequent rows. When a repetition is found, the sequence is searched
a suitable position, such that the repeated element (called change) can be moved somewhere else. This position
is the middle element (called found) of a triplet s.t.: each element in the triplet is different from change,
(otherwise we will be generating a new repetition), found is in a row where column1 has the same value as in
the row of change (otherwise the frequency of elements in each 0s and 1s would be unbalanced) and found is
different from the element in the row before. When found is found, it takes value change, while change takes
value found.

#### [orderStimWithinTasks_str](#orderStimWithinTasks_str)

Identical to balanceTransitionsMinus1, but some code at the end converts 0s and
1s into the input-defined string. This does not

#### [noStimRepetition](#noStimRepetition)

Generates a sequence of length trials without n minus 1 repetitions.
Takes as inputs the length of the needed sequence (int) and either a list with
the elements to be equally represented in the sequence, or a list with same length as the first input that the users want to pseudo-shuffle.
*Description:*
It uses the same logic of orderStimWithinTasks_str without the constraints due to the other column. The list is generated repeating the elements or is given as input. It is randomized and then checked for n-1 repetitions. As soon as one is found, the sequence is searched for an element to swap with element n, such that that repetition is eliminated and another is not created. To this aim, the swapping element must be different from n and also from n+1; furthermore, the elements following and preceding the swapping candidate must be also different from n. This is repeated in a loop as many times as n-1 repetitions were found in the initial, random generated, sequence.
*Performance*: The algorithm has never failed in adjusting a sequence in 100k simulations with length 16 trials and 8 stimuli equally represented.


#### [shuffle_rows](#shuffle_rows)

Ordering a dataframe according to one of its columns.
It takes as input a vector (res), identical to the target column, but ordered in the wished way.
It returns a dataframe identical to df2shuf, where the rows are ordered according to res.
*Description:*
This allows to re-order a dataframe (df2shuf) containing all trials of a certain block, according to the column given as input (targetCol). For example, it could take either one of the columns of the output of orderStimWithinTasks.
It first shuffles the df2shuf rows. Then, for each element of res, it takes all of df2shuf rows having that value in targetCol selects the first one among these and appends it in the new, re-ordered, dataframe (df_output). The initial shuffle allows to pick the first of the matching row and still having a random looking final df.
*Performance*: it takes 4 seconds to run 10 times. This cannot fail by construction


#### [df_BooleanOrder](#df_BooleanOrder)

Ordering the trials dataframe given the two one-dim arrays obtained by pasteStim2task. It takes as input the dataframe to be reordered, the STRING name of the column containing the elements (targetCol) to be compared with stimSeq array (obtained, for example by pasteStim2task); the STRING name of the column containing the elements (taskCol) to be compared with taskSeq array (obtained, for example by balanceTransitionsMinus1).
It returns a dataframe identical to df2order, except for rows order which is chosen according to stimSeq and taskSeq vectors.
*Performance*: it takes 4 seconds to run 10 times. This cannot fail by construction
*Description*:
Similar to shuffle_rows, but it simultaneously takes into account the stimuli sequence(the sequence of elements
without N-1 repetitions) and the task sequence (the sequence of 0 and 1 without N-1 repetitions).

#### [balanceTransitionsMinus2](#balanceTransitionsMinus2)

Generating a sequence of 0 and 1 of desired length, such that number of 0 = number of 1 and
(N-2 repetitions) = (N-2 switches)
It takes as an input the lenght of the needed sequence (trials) and the number of attempts that the
programmer wishes to allow the algorithm (maxCounter).
Both inputs must be integers and trials MUST be an EVEN number (very common in experiment). Values for
trials input must be greater or equal than 10; the algorithm was successfully tested with trials up to 10000.
It returns a np.array of length = trials were repetitions of 0 and 1 each second position are perfectly
equal.
*Performance*: with 96 and 4 as inputs, 10k loops in 4 seconds, no failure
*Description*:
As for balanceTransitionMinus1 function, the aim is to generate a single random sequence of 0 and 1 and
to adjust that in order to have a sequence with same number of N-2 rep and switch.
In such a sequence, it doesn't matter the element preceding a given element, but only the element which is
2 positions backward. This applies to each element. This means that the odd and the even elements of such
a sequence, can be seen as two independent sequences (with half of the leght), that have been alternated,
or zipped, as you would do when closing a zipper of a sweater. Elements in the odd positions, do not interact
with the ones in the even positions.
If the two zipped half-sequences are such that N-1 rep and sw are balanced, the resulting "zipped" sequence,
One of the first steps of this function is indeed to call the balanceTransitionMinus1 function, to get a
N-1 balanced sequence. Then, it will break this sequence in two halves, and will zip them together, assigning to
odd positions the element of the first half and to even positions the elements of the second half.
When doing that, a transition is lost. When the N-1 balanced sequence is cut in a half, the transition between
the last element of the first half and the first of the second half doesn't exist anymore.
Since the output of balanceTransitionMinus1 is a sequence were N-1 rep and sw have always a delta = 1, this
loss of a transition during the cutting, may be beneficial when such transition is a repetition and repetitions
were exceeding, or when the transition is a sw and sw were exceding. In the others cases though, this leads to a
imbalance of 2 between N-1 repetitions and switches in the 2 halves and thus in an imbalance of 2 in N-2 rep
and swithces zipped sequence. This is why the output of balanceTransitionMinus1 carries the information about
the n-1 rep and sw. This is checked by balanceTransitionMinus2 and the transition at the middle of such
sequence is checked. If the cutting operation would cut away a repetition when sw>rep (we call it the
middle-repetition case) OR when it would cut away a switch when sw<rep (we call it the middle-sw case)
some other adjustments are done.
What it is done, for example in a middle-repetition case, it to move that repetition happening at the middle
somewhere else, and to place a sw in its place. This is again done with triplets, but this time the aim is to
keep the overall balance identical. For example, in a middle-repetition case, if the middle triplet is
1/edge/11, then the algorithm searches the sequence for a 101 and, if it finds it, it swaps the middle elements.
