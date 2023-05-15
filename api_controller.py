import requests
import json

class HolidayAPI:
    def __init__(self):
        
        self.province_url = "https://canada-holidays.ca/api/v1/provinces/"
    
    def get_holidays(self, province_id):
        provinces = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
        if province_id in provinces:
            self.province = province_id
        else:
            self.province = "BC"
        
        url = self.province_url + self.province
        
        # print(url)
        try:    
            data = requests.get(url, headers={'Accept': 'application/json'}).json()
        except requests.HTTPError as err:
            print(err)
            
        print(data)
            
test = HolidayAPI()
test.get_holidays("BC")