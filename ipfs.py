import requests

class IPFSManager:
    def __init__(self, pinata_api_key, pinata_api_secret):
        self.api_url = "https://api.pinata.cloud/"
        self.headers = {
            "pinata_api_key": "8dc26f5d53e5b5584661", # put ur pinata api key here
            "pinata_secret_api_key": "1581002614b253fbc6f38469ae1426c3fbb84c34df2da7319ca0ef9026030e43", # api secret key as well
        }

    def upload_file(self, file_content):
        try:
            response = requests.post(f"{self.api_url}/add", files={"file": file_content})
            if response.status_code == 200:
                return response.json()["Hash"]
        except Exception as e:
            print(f"IPFS upload failed: {e}")
        return None

    def retrieve_file(self, ipfs_hash):
        try:
            response = requests.get(f"https://ipfs.io/ipfs/{ipfs_hash}")
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print(f"IPFS retrieval failed: {e}")
        return None
