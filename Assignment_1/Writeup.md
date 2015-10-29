#Assignment 1
##Quality Assessment MinION reads
1. TODO

2. Active Channels =  251.0

   Average reads per channel =  101.25498008

   Channel 90 has most reads with 449 reads
   
   `$ python group5_report1_question2.py fastq/2D-fail.fastq fastq/2D-pass.fastq fastq/1D-fail.fastq fastq/1D-pass.fastq`

3. TODO

4. TODO

5. TODO

6. 
   **Length distribution of 1D (template and complement) reads, failed**

   `$ python group5_report1_question6.py fastq/1D-fail.fastq 1D-fail.png`
   
   <img src="./img/question6/1D-fail.png" width="600">

   _Note:_ Longest nucleotide for 1D-fail.fastq is 195979 nucleotides
   
   **Length distribution of 2D reads, failed**
   
   `$ python group5_report1_question6.py fastq/2D-fail.fastq 2D-fail.png`
   
   <img src="./img/question6/2D-fail.png" width="600">
   
   **Length distribution of 1D (template and complement) reads, passed**
   
   `$ python group5_report1_question6.py fastq/1D-pass.fastq 1D-pass.png`
   
   <img src="./img/question6/1D-pass.png" width="600">
   
   **Length distribution of 2D reads, passed**
   
   `$ python group5_report1_question6.py fastq/2D-pass.fastq 2D-pass.png`
   
   <img src="./img/question6/2D-pass.png" width="600">
   
7. Longest read obtained for:

   | Passed reads | Nucleotides |
   | --- | --- | 
   | Template |13927 |
   | Complement | 13927 |
   | 2D | 15808 |
   
   `$ python group5_report1_question7.py fastq/template-pass.fastq`
   
   `$ python group5_report1_question7.py fastq/complement-pass.fastq`
   
   `$ python group5_report1_question7.py fastq/2D-pass.fastq`
   
8. TODO

9. TODO

10. Nucleotide composition of both 2D sequences that classified as 'passed' and as 'failed'

   | Nucleotide  | Nucleotide Count | Total Nucleotides | Percentage |
   | --- | --- | --- | --- |
   | A  | 4607015  | 17231796 | 26.7355474728% |
   | C  | 3982240  | 17231796 | 23.109837187% |
   | T  | 4587590  | 17231796 | 26.6228198152% |
   | G  | 4054951  | 17231796 | 23.531795525% |
   
   `$ python group5_report1_question10.py fastq/2D-fail.fastq fastq/2D-pass.fastq`

11. Linear regression was performed on k-mer count features of sequences and sequencing time durations.

Several k-mer lenghts were considered.  Initially we thought to use 5-mers, which would give us a 1024 dimensional feature space, however, since the data is fairly noisy and we only fit to about 4000 data points, this first model overfit.

To pick the ideal kmer length, we performed five-fold cross-validation, and found that k-mers of length 3 gave the best results.

To run, provide the path to a tsv containing sequences and labels and the kmer length as arguments:
    `$python group5_report1_question11.py data/seq_times.tsv 3`

The mean and variance of the R<sup>2</sup> values and across the 5 folds is provided.

The data points are shuffled to prevent any biases present in the order of the
data points.

###Train set performance:
* Mean R<sup>2</sup>: 0.671546 
* Var R<sup>2</sup>: 0.001106


###Test set performance:
* Mean R<sup>2</sup>: 0.649408
* Var R<sup>2</sup>: 0.010450
