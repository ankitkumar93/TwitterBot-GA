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
            return None

        # Remove ignored tags from tag list
        tags_filtered = [tag for tag in tags if tag not in self.tags_ignorelist]

        # Converts all NN to NNP
        tags_filtered_2 = ['NNP' if tag == 'NN' else tag for tag in tags_filtered]

        # Compute Tag Count
        tags_dict = Counter(tags_filtered_2)

        # Filter on Total Tags
        tags_len = len(tags)
        if tags_len < self.tags_min or tags_len > self.tags_max:
            return None

        # Filter for missing tags
        for tag in self.tags_map:
            if self.tags_map[tag].min > 0 and tag not in tags_filtered_2:
                return None

        # Filter for Allowed Tags
        for tag in tags_dict:
            if tag not in self.tags_map:
                return None
            else:
                tagcount = tags_dict[tag]
                tag_constraints = self.tags_map[tag]
                if tagcount < tag_constraints['min'] or tagcount > tag_constraints['max']:
                    return None

        # Return filtered tags
        return tags_filtered_2
