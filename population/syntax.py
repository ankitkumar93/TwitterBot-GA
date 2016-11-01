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
        return self.dbHelper.get_syntax()