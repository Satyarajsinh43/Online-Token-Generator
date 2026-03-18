// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TokenRegistry {
    // Mapping to store token signatures/hashes to verify their existence
    // tokenHash => bool
    mapping(string => bool) public tokenExists;

    // Struct to store more details if needed
    struct TokenProof {
        string tokenHash;
        uint256 timestamp;
        address sender;
    }

    // Mapping to store the exact proof
    mapping(string => TokenProof) public tokenProofs;

    // Event emitted when a new token is registered
    event TokenRegistered(string tokenHash, uint256 timestamp, address indexed sender);

    /**
     * @dev Stores a token hash on the blockchain. Reverts if already stored.
     * @param tokenHash The SHA-256 hash representing the token data
     */
    function storeTokenHash(string memory tokenHash) public {
        require(!tokenExists[tokenHash], "Token hash already exists in the registry.");

        tokenExists[tokenHash] = true;
        
        tokenProofs[tokenHash] = TokenProof({
            tokenHash: tokenHash,
            timestamp: block.timestamp,
            sender: msg.sender
        });

        emit TokenRegistered(tokenHash, block.timestamp, msg.sender);
    }

    /**
     * @dev Verifies if a token hash exists in the registry.
     * @param tokenHash The SHA-256 hash to verify
     * @return bool True if the token exists, false otherwise
     */
    function verifyToken(string memory tokenHash) public view returns (bool) {
        return tokenExists[tokenHash];
    }
}
