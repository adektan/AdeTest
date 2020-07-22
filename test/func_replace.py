import re

def str_rep(str_new):
    new_str = str_new.replace('ObjectId(', '').replace('NumberLong(', '').replace(')', '').replace('/* 1 */', '').replace('/* ', '').replace(' */','~')
    new_str_pattern = re.sub('([0-9]*~)' ,',', new_str)
    return new_str_pattern
