// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract ArtistPopupNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    struct Artwork {
        string title;
        string artist;
        string description;
    }

    mapping(uint256 => Artwork) private _artworks;

    constructor() ERC721("ArtistPopupNFT", "APNFT") {}

    function mintNFT(address recipient, string memory tokenURI, string memory title, string memory artist, string memory description) public onlyOwner returns (uint256) {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        _safeMint(recipient, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        _artworks[newTokenId] = Artwork(title, artist, description);
        return newTokenId;
    }

    function getArtwork(uint256 tokenId) public view returns (string memory, string memory, string memory) {
        require(_exists(tokenId), "Token does not exist");
        Artwork memory artwork = _artworks[tokenId];
        return (artwork.title, artwork.artist, artwork.description);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
