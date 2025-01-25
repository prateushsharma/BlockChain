from web3 import Web3

class Blockchain:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ganache or other local node
        self.contract_address = "0xbfABe0022E7342691142460Dc3C7327674A12E69"
        self.contract_abi =  [
            {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        }
      ],
      "name": "FileDeleted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "fileHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "uploadTime",
          "type": "uint256"
        }
      ],
      "name": "FileUploaded",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fileHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fileType",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "fileSize",
          "type": "uint256"
        }
      ],
      "name": "uploadFile",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        }
      ],
      "name": "getFile",
      "outputs": [
        {
          "internalType": "string",
          "name": "fileHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fileType",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "fileSize",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "uploadTime",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        }
      ],
      "name": "deleteFile",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        }
      ],
      "name": "fileExists",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileId",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "isFileOwner",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]  # Load your contract ABI here
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.account = self.web3.eth.accounts[0]

    def store_metadata(self, file_id, file_hash, file_name, file_type, file_size):
        tx = self.contract.functions.uploadFile(
            file_id, file_hash, file_name, file_type, file_size
        ).buildTransaction({"from": self.account, "gas": 3000000, "nonce": self.web3.eth.getTransactionCount(self.account)})
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key="0xYourPrivateKey")
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.toHex(tx_hash)

    def get_metadata(self, file_id):
        try:
            return self.contract.functions.getFile(file_id).call()
        except Exception:
            return None

    def delete_metadata(self, file_id):
        try:
            tx = self.contract.functions.deleteFile(file_id).buildTransaction(
                {"from": self.account, "gas": 3000000, "nonce": self.web3.eth.getTransactionCount(self.account)}
            )
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key="0xYourPrivateKey")
            self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return True
        except Exception:
            return False
