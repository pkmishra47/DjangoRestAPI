import requests
import unittest

class TestAPIs(unittest.TestCase):
    '''
    static token has been used for dev purpose. for production, more generic userwise token 
    can be used(not covered in this scenario)
    '''
    def _init__(self):
        pass

    def test_wallet_tnx_request(self):
        
        url = 'http://127.0.0.1:8000/wallet_txn/'
        contact_number = 9742788071
        amount = 1000
        trantype = 'A'  #A-Add, 'D'-Deduct
        data = {'contact_number':contact_number,'amount':amount,'trantype':trantype}

        response = requests.post(url,data,headers={'Authorization': 'Bearer test_token'})

        return self.assertEqual(200, response.status_code)

    def test_wallet_history_request(self):
        
        url = 'http://127.0.0.1:8000/wallet_history/'
        contact_number = 9742788071
        offset = 0
        total_count = 10
        data = {'contact_number':contact_number,'offset':offset,'total_count':total_count}

        response = requests.post(url,data,headers={'Authorization': 'Bearer test_token'})

        return self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    obj = TestAPIs()
    print(obj.test_wallet_tnx_request())
    print(obj.test_wallet_history_request())