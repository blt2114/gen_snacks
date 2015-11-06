#Assignment 2
##Snack to sequence pipeline

1. question one.

1. To determine the length of time it will take to identify what sophie ate we must first deconstruct the question into a few components.
We first define identifying the food as observing at least 2 counts of it and then consider the amount of time it will take to observe 2 counts of that sequence with high probability, say p = 0.95 .

By modeling the expected number of counts of the given species with a binomial distribution with probability of success, c, equal to the probability of an arbitrary sequence being assigned to that species, we can solve for the number of trials required to achieve a probability of 0.95 or greater of having 2 reads or more.

To calculate this probability from the binomial distribution we calculate the probability that there will be 0 reads or 1 read and subtract these values from 1.

Given a known portion of pool that is the primary food, c, we can calculate this number from: <br>
0.95 = p(n>= 2) = 1- p(n == 1) - p(n==0) = 1 - n\_choose\_0\*p<sup>0</sup>\*(1-p)<sup>n</sup> - n\_choose\_1\*p<sup>1</sup>\*(1-p)<sup>n-1</sup>

Given the number of sequences that we calculate from this, we must then determine the length of time the sequencer must run to generate that number of sequences.  This is done using the rate calculated 
First, we are concerned with he primary food in the sample we will consider the length of time that it will take to aquire a sufficient number of reads to 
