from datetime import datetime, timedelta
from base64 import b64encode
import pandas as pd
import requests
import logging
import json

# takes an integer t_delta as an argument
# returns a set of times, with the start date being current hour - t_delta

def get_formatted_datetimes(t_delta):
  now = datetime.utcnow().replace(microsecond=0, second=0, minute=0)
  start_date = (now + timedelta(hours= -t_delta))
  #start date/time formatted for get request
  st0 = start_date.strftime("%Y-%m-%dT%H:%M:%SZ") 
  sub_start_date = (start_date + timedelta(hours= 1))
  #end date/time formatted for get request
  st1 = sub_start_date.strftime("%Y-%m-%dT%H:%M:%SZ") 
  #date/time separately formatted for excel
  xdst0, xtst0 = start_date.strftime("%Y-%m-%d"), start_date.strftime("%H") 
  xtst1 = now.strftime("%H")
  return st0, st1, xdst0, xtst0, xtst1

# takes the zendesk account subdomain, and a start and end datetime (%Y-%m-%dT%H:%M:%SZ)
# returns the result of a GET request to the Zendesk v2 API

def get_tickets(dom, auth, st0, st1, tags):
  print(b64encode(auth.encode('utf-8'))[2:-1])
  header = {"Authorization": "Basic {}".format(str(b64encode(auth.encode('utf-8')))[2:-1])}
  url = f"https://{dom}.zendesk.com/api/v2/search.json?query=type:ticket+created>{st0}+created<{st1}+tags:{tags}"

  try:
    res = requests.get(url, headers=header)
    r = json.loads(res.text)
    return r
  except Exception as err: 
    print('Error making zendesk GET request:', str(err))
    exit()

# if __name__ =="__main__":
#     # TODO: set logging level based on input
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     run(logger)