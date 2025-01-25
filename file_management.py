import os

class FileManager:
    def __init__(self, storage_dir="files"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_file(self, file_name, file_content):
        file_path = os.path.join(self.storage_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(file_content)
        return file_path

    def read_file(self, file_name):
        file_path = os.path.join(self.storage_dir, file_name)
        if not os.path.exists(file_path):
            return None
        with open(file_path, "rb") as f:
            return f.read()
