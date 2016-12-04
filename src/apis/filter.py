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

        # Remove ignored tags from tag list
        tags_filtered = [tag for tag in tags if tag not in self.tags_ignorelist]

        # Compute Tag Count
        tags_dict = Counter(tags_filtered)

        # Filter on Total Tags
        tags_len = len(tags)
        if tags_len < self.tags_min or tags_len > self.tags_max:
            return False

        # Filter for Allowed Tags
        for tag in tags_dict:
            if tag not in self.tags_map:
                return False
            else:
                tagcount = tags_dict[tag]
                tag_constaints = self.tags_map[tag]
                if tagcount < tag_constaints['min'] or tagcount > tag_constaints['max']:
                    return False

        return True
