import requests

class IPFSManager:
    def __init__(self, pinata_api_key, pinata_api_secret):
        self.api_url = "https://api.pinata.cloud/"
        self.headers = {
            "pinata_api_key": "8dc26f5d53e5b5584661",  # Use provided Pinata API key
            "pinata_secret_api_key": "1581002614b253fbc6f38469ae1426c3fbb84c34df2da7319ca0ef9026030e43",  # Use provided Pinata secret API key
        }

    def upload_file(self, file_content):
        try:
            # Pinata's file upload endpoint is '/pinning/pinFileToIPFS'
            response = requests.post(f"{self.api_url}/pinning/pinFileToIPFS", files={"file": file_content}, headers=self.headers)
            if response.status_code == 200:
                # Return the IPFS hash (CID) of the uploaded file
                return response.json()["IpfsHash"]
            else:
                print(f"Failed to upload file: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"IPFS upload failed: {e}")
        return None

    def retrieve_file(self, ipfs_hash):
        try:
            # Use the IPFS gateway to retrieve the file by hash
            response = requests.get(f"https://ipfs.io/ipfs/{ipfs_hash}")
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to retrieve file: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"IPFS retrieval failed: {e}")
        return None
