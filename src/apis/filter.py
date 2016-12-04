import json
from collections import Counter

'''
Author: Ankit Kumar
Tweet Filter
Filter a tweets based on conditions:
    i) POS Tags
    ii) Author's Followers
'''

class Filter:
    def __init__(self, args):
        self.logger = args['logger']
        
        config = json.load(open(args['filter_path']))
        tagsjson = config['tags']
        
        self.followers_count = config['followers_count']
        self.tags_min = tagsjson['min']
        self.tags_max = tagsjson['max']
        self.tags_map = tagsjson['map']
        self.tags_ignorelist = tagsjson['ignorelist']
        

    def check(self, tweet):
        tags = tweet['tags']
        follower_count = tweet['followers']

        # Filter for follower count
        if follower_count < self.followers_count:
            return False

        # Compute Tag Count
        tags_dict = Counter(tags)

        # Filter for Allowed Tags
        for tag in tags_dict:
            if tag in self.tags_ignorelist:
                tags_dict.remove(tag)
                continue
            elif tag not in self.tags_map:
                return False
            else:
                tagcount = tags_dict[tag]
                tag_constaints = self.tags_dict[tag]
                if tagcount < self.tag_constaints['min'] or tagcount > self.tag_constaints['max']:
                    return False

        return True
