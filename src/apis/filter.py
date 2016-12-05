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
        self.tags_dellist = tagsjson['dellist']
        

    def check(self, tweet):
        tags = tweet['tags']
        follower_count = tweet['followers']

        # Filter for follower count
        if follower_count < self.followers_count:
            return None

        # Check for dellist
        for tag in tags:
            if tag in self.tags_dellist:
                return None 

        # Remove ignored tags from tag list
        tags_filtered = [tag for tag in tags if tag not in self.tags_ignorelist]

        # Compute Tag Count
        tags_dict = Counter(tags_filtered)

        # Filter on Total Tags
        tags_len = len(tags)
        if tags_len < self.tags_min or tags_len > self.tags_max:
            return None

        # Check for map (min, max)
        for tag in self.tags_map:
            if tag not in tags_dict:
                return None
            
            tag_count = tags_dict[tag]
            tag_constraint = self.tags_map[tag]
            if tag_count < tag_constraint['min'] or tag_count > tag_constraint['max']:
                return None

        # Return filtered tags
        return tags_filtered
