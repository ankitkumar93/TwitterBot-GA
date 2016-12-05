# Author: Ankit Kumar
# Runs the Genetic Algorithm
# Works for different parameters

# Commands
gacmd="./twitter_ga ga -g"
pycmd="python getgoalpopulation.py"

# Globals
lr_threshold="0.34"
outfile=$1

# Fetch Goal Population Size
goalpop=$($pycmd $lr_threshold)

# Run GA for different Goal Population Sizes
for size in $goalpop
do
    SECONDS=0
    runcmd=$gacmd $size
    for((i = 0; i < 5; i++)); do
        $runcmd
    done
    runtime=$SECONDS
    outlog="Genetic Algorithm: Size: $size RunningTime: $runtime"
    echo $outlog
    echo $outlog >> $outfile
done