#Assignment 2
##Snack to sequence pipeline

1. question one.

1. To determine the length of time it will take to identify what sophie ate we must first deconstruct the question into a few components.
We first define identifying the food as observing at least 2 counts of it and then consider the amount of time it will take to observe 2 counts of that sequence with high probability, say p = 0.95 .

By modeling the expected number of counts of the given species with a binomial distribution with probability of success, c, equal to the probability of an arbitrary sequence being assigned to that species, we can solve for the number of trials required to achieve a probability of 0.95 or greater of having 2 reads or more.

To calculate this probability from the binomial distribution we calculate the probability that there will be 0 reads or 1 read and subtract these values from 1.

Given a known portion of pool that is the primary food, c, we can calculate this number from: <br>
0.95 = p(n>= 2) = 1- p(n == 1) - p(n==0) = 1 - n\_choose\_0\*c<sup>0</sup>\*(1-c)<sup>n</sup> - n\_choose\_1\*c<sup>1</sup>\*(1-c)<sup>n-1</sup> = 1 - (1-c)<sup>n</sup> - n\*c\*(1-c)<sup>n-1</sup>

In our case, since 37 of out the 70 reads we classified were attributed to the primary food component, Salmon, c = 0.52857, so we have:

0.95 = 1 - 0.4714<sup>n</sup>- n\* 0.52857 \* 0.4714<sup>n-1</sup>

by solving for n using wolfram alpha, we get n = 6.859

Therefore to have greater than 95% confidence, we must get at least 7 reads.

Given the number of sequences that we calculate from this, we must then determine the length of time the sequencer must run to generate that number of sequences.  This is done using the rate of sequencing determined in assignment one question 4 and the portion of sequences which are pass that was calculated in Assignment 1 Question 1 (since only 'pass' reads were used in classification.

In question 4 we calculated that it would take

First, we are concerned with he primary food in the sample we will consider the length of time that it will take to aquire a sufficient number of reads to 
