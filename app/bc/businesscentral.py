import requests
from datetime import datetime, timedelta
from ..utils.config import CLIENT_ID, CLIENT_SECRET, SCOPE, GRANT_TYPE, TENANT

class BusinessCentral:

    __ACCESS_TOKEN = None
    __VALID_TILL = None
    __BC_AUTH_URL = "https://login.microsoftonline.com/{0}/".format(TENANT)
    __BC_API_URL = "https://api.businesscentral.dynamics.com/v2.0/{0}/".format(TENANT)

    def __init__(self):
        if BusinessCentral.__ACCESS_TOKEN == None and BusinessCentral.__VALID_TILL == None:
            self.__get_token()

    @classmethod
    def __get_token(cls):
        url = "{0}oauth2/v2.0/token".format(cls.__BC_AUTH_URL)
        
        payload = 'client_id={0}&scope={1}&client_secret={2}&grant_type={3}'.format(CLIENT_ID,SCOPE,CLIENT_SECRET,GRANT_TYPE)
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'fpc=AtAdj9CRhMhEiqhsfQ-3BGPp2bnxAQAAAKAvG94OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            cls.__ACCESS_TOKEN = response.json()['access_token']
            cls.__VALID_TILL = datetime.now() + timedelta(seconds=response.json()['expires_in'])

    def find_my_device(self, environment_name, company_name, serial_no):
        if datetime.now() >= BusinessCentral.__VALID_TILL:
            self.__get_token()

        url = '{0}{1}/ODataV4/Company(\'{2}\')/FindMyDevice?$filter=SerialNo eq \'{3}\''.format(BusinessCentral.__BC_API_URL, environment_name, company_name, serial_no)
        payload = {}
        headers = {
            'Authorization': 'Bearer '+ BusinessCentral.__ACCESS_TOKEN
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        data = {
            "SN":"Not Found",
            "P/N":"Not Found",
            "desc":"Not Found",
            "desc2":"Not Found",
            "Warranty":"Not Found",
            "Warranty period until":"Not Found",
        }
        
        if response.status_code == 200:
            if len(response.json()['value']) != 0:
                raw_data = response.json()['value'][0]

                data["SN"] = raw_data['SerialNo']
                data["P/N"] = raw_data['ItemNo']
                data["desc"] = raw_data['Description']
                data["desc2"] = raw_data['Description_2']
                
                start_date = datetime.strptime(raw_data['PostingDate'], "%Y-%m-%d")
                end_date = start_date + timedelta(days=2*365)

                data["Warranty period until"] = end_date.strftime("%Y-%m-%d")

                if start_date <= datetime.today() <= end_date:
                    data["Warranty"] = "Yes"
                else:
                    data["Warranty"] = "No"

        return data
