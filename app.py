from flask import Flask, jsonify, request
from auth import Auth
from blockchain import Blockchain
from file_management import FileManager
from ipfs import IPFSManager


app = Flask(__name__)

auth = Auth()
blockchain = Blockchain()
file_manager = FileManager()

pinata_api_key = "8dc26f5d53e5b5584661",
pinata_secret_api_key =  "1581002614b253fbc6f38469ae1426c3fbb84c34df2da7319ca0ef9026030e43"
ipfs_manager = IPFSManager(pinata_api_key,  pinata_secret_api_key)

@app.route("/upload", methods=["POST"])
def upload_file():
    data = request.json
    file_id = data.get("file_id")
    file_name = data.get("file_name")
    file_type = data.get("file_type")
    file_content = data.get("file_content")  # Base64 encoded or raw

    if not file_id or not file_name or not file_type or not file_content:
        return jsonify({"error": "Invalid input"}), 400

    # Upload file to IPFS
    ipfs_hash = ipfs_manager.upload_file(file_content)
    if not ipfs_hash:
        return jsonify({"error": "Failed to upload to IPFS"}), 500

    # Store metadata on the blockchain
    tx_hash = blockchain.store_metadata(file_id, ipfs_hash, file_name, file_type, len(file_content))
    return jsonify({"message": "File uploaded", "ipfs_hash": ipfs_hash, "transaction_hash": tx_hash}), 200


@app.route("/retrieve/<file_id>", methods=["GET"])
def retrieve_file(file_id):
    metadata = blockchain.get_metadata(file_id)
    if not metadata:
        return jsonify({"error": "File not found"}), 404

    ipfs_hash = metadata["file_hash"]
    file_content = ipfs_manager.retrieve_file(ipfs_hash)
    return jsonify({"file_id": file_id, "metadata": metadata, "file_content": file_content}), 200


@app.route("/delete/<file_id>", methods=["DELETE"])
def delete_file(file_id):
    result = blockchain.delete_metadata(file_id)
    if not result:
        return jsonify({"error": "Failed to delete file metadata"}), 400

    return jsonify({"message": "File metadata deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
