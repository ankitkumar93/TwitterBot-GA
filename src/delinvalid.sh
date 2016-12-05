# Author: Ankit Kumar
# Delete Invalid Rows from DB
# Use logfile as Input

# Globals
dbname="tweet_ga"
collname="filtered_tweets"
mongocmd="mongo $dbname --eval"
pattern='[0-9]\{18\}'
query="db.$collname.remove"

# Arguments
logfile=$1

# Logic
# Read File
while read line; do
	# Capture TweetID
	tweetid=$(echo $line | grep -o $pattern)

	# If TweetID Found, Delete the Tweet
	if [ ! -z $tweetid ]; then
		arg="{tweetid: $tweetid}"
		$mongocmd $query"($arg)"
	fi
done <$logfile

# Remove all tweets with 0 LRScore
$mongocmd $query"({lrscore:{\$eq: 0}})"
