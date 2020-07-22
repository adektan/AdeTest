import time

print('Please make sure run file ddl_tables.sql first in your local computer')
print('And Using Postgresql DB')
time.sleep(5)
print('')
print('')
print('Begin to Insert the json file to schema public to table complex and tower')
time.sleep(3)
import task1_load_complex
print ('Load Json Complex to Table in schema Public')
print('')
import task1_load_tower
print ('Load Json Complex to Table in schema Public')
print('')
print('')
import task1
print('Insert and Update to schema Master Table ')
print('')
print('Task 2 can check in seperates folder')
print('')
print('')
print('Task 3')
print('')
import task3
print('Please check the results')
print('')