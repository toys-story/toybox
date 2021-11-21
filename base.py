import json
import os
from upbit.client import Upbit

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
ENV_PATH = ROOT_DIR + "/.env.json"

class baseTrader():
    def __init__(self):
        try:
            self._get_cred()
            self._check_connection()
        except Exception as e:
            print(f"Error : {e}")

    def _get_cred(self):
        data = dict()
        with open(ENV_PATH, "r") as f:
            data = json.load(f)
        self.access_key = data.get("access_key", "")
        self.secret_key = data.get("secret_key", "")
        
    def _check_connection(self):
        self.client = Upbit(self.access_key, self.secret_key)
        resp = self.client.APIKey.APIKey_info()
        
        if "error" in resp["result"]:
            raise Exception(resp["result"].get("error", None))
        
if __name__ == '__main__':
    bt = baseTrader()
    print(bt.client)
