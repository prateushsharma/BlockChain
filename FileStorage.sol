// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedStorage {
    struct File {
        string fileHash; // IPFS CID or any hash of the file
        string fileName; // Name of the file
        string fileType; // Type of the file (e.g., .pdf, .jpg)
        uint256 fileSize; // File size in bytes
        address owner; // Address of the uploader
        uint256 uploadTime; // Timestamp when the file was uploaded
    }

    // Mapping of file IDs to file metadata
    mapping(string => File) private files;

    // Events for logging
    event FileUploaded(
        string fileId,
        string fileHash,
        string fileName,
        address indexed owner,
        uint256 uploadTime
    );
    event FileDeleted(string fileId, address indexed owner);

    // Modifier to check ownership of a file
    modifier onlyOwner(string memory fileId) {
        require(files[fileId].owner == msg.sender, "You are not the owner of this file");
        _;
    }

    // Function to upload a file's metadata
    function uploadFile(
        string memory fileId,
        string memory fileHash,
        string memory fileName,
        string memory fileType,
        uint256 fileSize
    ) public {
        require(bytes(fileId).length > 0, "File ID cannot be empty");
        require(bytes(fileHash).length > 0, "File hash cannot be empty");
        require(bytes(fileName).length > 0, "File name cannot be empty");
        require(fileSize > 0, "File size must be greater than zero");
        require(files[fileId].owner == address(0), "File ID already exists");

        // Store file metadata
        files[fileId] = File({
            fileHash: fileHash,
            fileName: fileName,
            fileType: fileType,
            fileSize: fileSize,
            owner: msg.sender,
            uploadTime: block.timestamp
        });

        emit FileUploaded(fileId, fileHash, fileName, msg.sender, block.timestamp);
    }

    // Function to retrieve a file's metadata
    function getFile(string memory fileId) public view returns (
        string memory fileHash,
        string memory fileName,
        string memory fileType,
        uint256 fileSize,
        address owner,
        uint256 uploadTime
    ) {
        require(files[fileId].owner != address(0), "File does not exist");

        File memory file = files[fileId];
        return (
            file.fileHash,
            file.fileName,
            file.fileType,
            file.fileSize,
            file.owner,
            file.uploadTime
        );
    }

    // Function to delete a file's metadata (only by the owner)
    function deleteFile(string memory fileId) public onlyOwner(fileId) {
        require(files[fileId].owner != address(0), "File does not exist");

        delete files[fileId];
        emit FileDeleted(fileId, msg.sender);
    }

    // Function to check if a file exists
    function fileExists(string memory fileId) public view returns (bool) {
        return files[fileId].owner != address(0);
    }

    // Function to verify the owner of a file
    function isFileOwner(string memory fileId, address user) public view returns (bool) {
        return files[fileId].owner == user;
    }
}
