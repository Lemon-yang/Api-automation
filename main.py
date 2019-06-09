# Script details
# Created On 16-may-2019
# Develop By: Abheet
# Python libs
import json
from openpyxl import load_workbook, workbook
import unittest
from src.logger import *
import src.read_settings as conf
from src.request_response import make_request,get_testcase_result,get_bearer_token
from src.execution_reporting import ReportGenerator
from src.execution_reporting import ReportGenerator
from src.read_test_cases import FrameworkReader
from src.mail import Mailer 

class TestPaymentAPI(unittest.TestCase):

    def setUp(self):
        logging.info("\n******************* API Automation execution starting ************************")
        #initialize workbook reader class
        self.tc = FrameworkReader()
        self.m = Mailer()
        #getting url w.r.t env under test
        self.api_url = conf.get_api_url()
        self.sessionObj = requests.Session()

        
    def tearDown(self):
        #send mail with results      
        self.m.send_mail(TEST_RESULTS)
        logging.info("******************* API Automation execution Completed!! ************************")

    def test_api(self):
      testcase_record = self.tc.get_testdata()

      #min,Max time limit for request timeout
      timeout = (5,200)
      final_result_dict = {}
      for sheet in testcase_record:
        sheet_list = sheet.split("-")
        final_record = []
        api_method_name = sheet_list[1] #Methods 
        for record in range(len(testcase_record[sheet])):
          #convert current record tuple into list
          current_record = list(testcase_record[sheet][record]) 

          #check first cell value to assert which type of auth system required to hit API
          if testcase_record[sheet][record][0].upper() == 'BASIC':
            header =  {u'content-type': u'application/x-www-form-urlencoded'}
            self.sessionObj.headers.update(header)

          elif testcase_record[sheet][record][0].upper() == 'BT':

            #function return list[bearer,expiredin]
            auth = get_bearer_token(self.api_url)
            token = auth[0] #token in list at index 0
            logging.info("Token genrated successfully:{}".format(auth))
            header = {'Content-Type': 'application/x-www-form-urlencoded','Authorization':token}
            self.sessionObj.headers.update(header)

          elif testcase_record[sheet][record][0].upper() == 'CERTS':  
            header =  {u'content-type': u'application/x-www-form-urlencoded'}
            self.sessionObj.headers.update(header)
          

          if 'Executed?N' in current_record:
            logging.info("*********** Skipping Test Execution for API:************\n {}".format(sheet_list[0]))
            break
           
          #Picking Values from fixed location of dataset
          is_test_execute = testcase_record[sheet][record][0]       #Flag for execution
          test_case = testcase_record[sheet][record][1]             #test description
          request_body = testcase_record[sheet][record][2]          #API request body
          expected_status_code = testcase_record[sheet][record][3]  #Expected Status Code 
          context_url = testcase_record[sheet][record][4]           #APi context path  
          
          if is_test_execute == 'Y':
            api_endboint = self.api_url + context_url

            req = {"method":api_method_name,
                    "url":api_endboint,
                    "env_url":self.api_url,
                    "request_payload":request_body,
                    "timeout":timeout,
                    "session":self.sessionObj}

            #Make API request
            
            response = make_request(**req)
               
            #if response not set type then there is some issue with API endboint/comntext
            if type(response) is not str:
              result = get_testcase_result(response.status_code,expected_status_code)
              #appended the result in current record
              current_record.append(response.status_code)
              if type(response) is json:
                current_record.append(json.dumps(response.json(),indent=4))
              else:
                current_record.append(response.text)
                
            else: 
              result = "API endpoint issue, check contect url"  

          
            current_record.append(result)
            #remove the context url from record set unused data
            del current_record[4]

          elif is_test_execute == 'N':
            logging.info("\nTest Case marked exluded from execution:\n {}".format(test_case))
            current_record.append("N/A")
            current_record.append("Skipped")
            #remove the context url from record set unused data
            del current_record[4]
          else:
            #remove unwanted data from final result dict
            del current_record[4]

            

          #updating current record with results  
          finalTuple = tuple(current_record)
          final_record.append(finalTuple) 
          
        #inserted final records in dict, used for reporting  
        if len(final_record) > 0:
          #removing first row of testcase sheet
          del final_record[0]  
          final_result_dict[sheet]  = final_record
          
      #write reports
      rg = ReportGenerator(final_result_dict)
      rg.write_report()
      

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPaymentAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
     