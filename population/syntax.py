from apis.db import DBHelper

'''
Author: Ankit Kumar
Syntax Module
'''

class Syntax:
    '''
    Syntax Module
    '''
    def __init__(self, args):
        self.logger = args.logger
        self.dbHelper = new DBHelper(dict(logger=self.logger))

    def get_syntax(self):
        self.logger.debug("Getting Syntax!");
        syntaxes = self.dbHelper.get_syntax()
        syntaxList = [s['data'] for s in syntaxes]
        return syntaxList