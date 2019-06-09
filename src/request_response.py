import base64
import json
from src.read_settings import *


def make_request(**kwargs):

     api_method = kwargs['method'].upper()
     token_api_url = kwargs['env_url'] 
     session = kwargs['session']
     request_payload = kwargs['request_payload']
     url = kwargs['url']
     timeOut = kwargs['timeout']

     try:
          api_response = ""
          if api_method == 'POST':
               logging.info("Request sent : %s",request_payload)
               api_response = session.post(url=url, json=request_payload,timeout=timeOut)
               
          elif api_method == 'PUT':
               api_response = session.put(url=url, json=request_payload,timeout=timeOut)
               logging.info("Request sent  :\t {}".format(api_response.text))
                     
          elif api_method =='GET':
               api_response = session.get(url=url, timeout=timeOut)
               logging.info("Request sent :\t {}".format(api_response.text))

          elif api_method =='DELETE':
               api_response = session.delete(url=url, json=json.loads(request_payload),timeout=timeOut)
               logging.info("Request sent :\t {}".format(api_response.text))

          logging.info("Response received : {} status code \t {}".format(api_response.status_code,api_response.text))
     
     except requests.exceptions.ConnectionError as confail:
         logging.error("***************Exception genrated connection failed *****************:\n {}".format(confail))
     except requests.exceptions.Timeout as tm:
         logging.warning("***************Exception genrated timeout *****************:\n {}".format(tm))
     return api_response    
             
     


# Request to get Auth bearer token used in api call
def get_bearer_token(url):
    request_url = url + "/token"
    header = {'Authorization':ACCESS_KEY }
    req = requests.post(request_url, data={'grant_type': 'client_credentials'}, headers=header)
    response = req.json()
    tokenlist = [] 
    if req.status_code == 200:
        bearer_token = response['access_token']
        expires_in = response['expires_in']
        tokenlist.append(bearer_token)
        tokenlist.append(expires_in)
    else:
         bearer_token = response['message']
         logging.info("Error: {} ".format(response['description']))  
         tokenlist.append(bearer_token) 
         tokenlist.append("Expired")

    return tokenlist


def get_testcase_result(actual_status_code,expected_status_code):
     if actual_status_code == expected_status_code:
          return PASS_CELL_VALUE
     else: 
          return FAILED_CELL_VALUE      
