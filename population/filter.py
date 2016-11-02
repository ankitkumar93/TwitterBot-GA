import json

from apis.tweet import TweetHelper

'''
Author: Anand Purohit
Filter module to ensure that we only consider those tweets
that possess a score that is greater than a threshold score
'''
class Filter:
    '''
    Filter class
    '''

    def __init__(self, args):
        self.logger = args['logger']
        self.tweetHelper = args['tweetHelper']
        self.filterThreshold = args['filterThreshold']

    def calc_score_for_keyword(self, keyword):
        users = self.tweetHelper.get_users_who_mentioned_keyword(keyword)
        reach = 0
        for user in users:
            reach += self.tweetHelper.get_followers_count(user)
        return reach

    def filter_from_list(self, keywordList):
        filteredKeywords = list()
        count = 0
        for keyword in keywordList:
            score = self.calc_score_for_keyword(keyword['name'])
            if score < self.filterThreshold:
                filteredKeywords.append(keyword)
                count += 1

        return count, filteredKeywords
