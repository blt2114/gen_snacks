# script for problem one, takes two fastq files
if [ "$#" -ne 2 ];then
    echo "./p1.sh <fail.fastq> <pass.fastq>"
    exit
fi

fail_fn=$1
pass_fn=$2

#each seq is four lines in fastq so divide lines by 4
num_lines=`wc -l < $fail_fn` # count the number of line in the file.
fail_seq_num=`echo $num_lines /4 | bc` # divide by four since four lines per sequence


num_lines=`wc -l < $pass_fn`
pass_seq_num=`echo $num_lines /4 | bc`

echo "number of failed sequences: $fail_seq_num"
echo "number of passed sequences: $pass_seq_num"
