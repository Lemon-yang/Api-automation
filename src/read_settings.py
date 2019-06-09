import os
import configparser
import requests
from src.logger import logging

currentdir = os.getcwd() + "/"

# Read Config Files for all settings
settings = configparser.ConfigParser()

conf_file_path = currentdir + 'src/config.conf'

s = settings.read(conf_file_path)
 
ENV = settings['SYSTEM_UNDER_TEST']['ENVIROMENT'].upper()

QC_ACCESS_KEY = settings['AUTHORIZATION']['QC_ACCESS_KEY']
UAT_ACCESS_KEY = settings['AUTHORIZATION']['UAT_ACCESS_KEY']
PROD_ACCESS_KEY = settings['AUTHORIZATION']['PROD_ACCESS_KEY']

ACCESS_KEY = ""
if ENV == 'QC':
    ACCESS_KEY = QC_ACCESS_KEY
elif ENV == 'UAT':
    ACCESS_KEY = UAT_ACCESS_KEY
elif ENV == 'PROD':
    ACCESS_KEY = PROD_ACCESS_KEY

QC_ENDPOINT = settings['BASE_API_ENDPOINTS']['QC_ENDPOINT']
UAT_ENDPOINT = settings['BASE_API_ENDPOINTS']['UAT_ENDPOINT']
PROD_ENDPOINT = settings['BASE_API_ENDPOINTS']['PROD_ENDPOINT']
TESTCASES = currentdir + settings['TEST_DATA']['INPUT_FILE_LOCATION']
TEST_RESULTS = currentdir + settings['TEST_DATA']['OUTPUT_FILE_LOCATION']

file_name = ""
if ENV == 'QC':
    file_name = "/TestDataSet_QC.xlsx"
elif ENV == 'UAT':
    file_name = "/TestDataSet_UAT.xlsx"
elif ENV == 'PROD':
    file_name = "/TestDataSet_PROD.xlsx"

TESTCASES = TESTCASES + file_name
TEST_RESULTS = TEST_RESULTS + file_name

LOG_FILE_PATH = currentdir + settings['LOG_FOLDER']['LOG_FOLDER_NAME']
API_CONTEXT = settings['TESTCASE_SHEET_INFO']['API_CONTEXT']
API_REQUEST_COL = settings['TESTCASE_SHEET_INFO']['API_REQUEST_COL']
EXECUTED_SHEET_COLOR = settings['RESULT_SHEET_STYLE']['EXECUTED_SHEET_COLOR']
PASSED_CELL_COLOR = settings['RESULT_SHEET_STYLE']['PASSED_CELL_COLOR']
FAILED_CELL_COLOR = settings['RESULT_SHEET_STYLE']['FAILED_CELL_COLOR']
PASS_CELL_VALUE = settings['RESULT_SHEET_STYLE']['PASS_CELL_VALUE']
FAILED_CELL_VALUE = settings['RESULT_SHEET_STYLE']['FAILED_CELL_VALUE']
EXCELSHEET_FONT_SIZE = settings['RESULT_SHEET_STYLE']['EXCELSHEET_FONT_SIZE']
API_TABLE_STARTS_FROM_ROW = int(settings['DASHBOARD_SHEET_STYLE']['API_TABLE_STARTS_FROM_ROW'])
API_TABLE_ENDS_COL = API_TABLE_STARTS_FROM_ROW + 6  # heading count is 6

#mail server
SERVER = settings['MAIL_SERVER']['SERVER']
PORT = settings['MAIL_SERVER']['PORT']
SEND_FROM =  settings['MAIL_SERVER']['SEND_FROM']
PWD =   settings['MAIL_SERVER']['PWD']
SEND_TO =  settings['MAIL_SERVER']['SEND_TO']


# Return uRL for system undertest
def get_api_url():
    if ENV.upper() == 'QC':
        url = QC_ENDPOINT
    elif ENV.upper() == 'UAT':
        url = UAT_ENDPOINT
    elif ENV.upper() == 'PROD':
        url = UAT_ENDPOINT
    else:
        print('Environment {} not exist'.format(ENV))
    return url
