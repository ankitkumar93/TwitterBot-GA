import sys
import math
from pymongo import MongoClient

'''
Author: Ankit Kumar
Get Goal Population: Returns different goal population sizes to run GA on
'''

# Globals
client = MongoClient('mongodb://localhost:27017')
db = client['tweet_ga']
collection = db['filtered_tweets']

# Functions
def main():
    lr_threshold = sys.argv[1]
    goalMaxSize = collection.count(
                    {"lrscore": {
                        "$gt": float(lr_threshold)
                        }
                    })

    goalSizes = [1, math.log2(goalMaxSize), math.sqrt(goalMaxSize), goalMaxSize/2]
    goalSizeList = [str(x) for x in goalSizes]
    
    print(" ".join(goalSizeList))


if __name__ == "__main__":
    main()