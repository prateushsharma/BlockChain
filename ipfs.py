import requests

class IPFSManager:
    def __init__(self, ipfs_api_url="http://127.0.0.1:5001/api/v0"):
        self.api_url = ipfs_api_url

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
