# Author: Ankit Kumar
# Runs the Genetic Algorithm
# Works for different parameters

# Commands
gacmd="./twitter_ga ga"
pycmd="python getgoalpopulation.py"

# Globals
lr_threshold="0.34"
logdir=$1
logfile_prefix="ga_log_"
logfile_ext=".log"
outfile=$2

# Fetch Goal Population Size
goalpop=$($pycmd $lr_threshold)


# Run GA for different Goal Population Sizes
for size in $goalpop
do
    runningtime=$(time $gacmd -l $logdir/$logfile_prefix$size$logfile_ext ga -g $size)
    outlog="Genetic Algorithm: Size: $size RunningTime: $runningtime"
    echo $outlog
    echo $outlog >> $outfile
done