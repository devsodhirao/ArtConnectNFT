const hre = require("hardhat");
const fs = require("fs");

async function main() {
  try {
    const [deployer] = await hre.ethers.getSigners();

    console.log("Deploying contracts with the account:", deployer.address);

    const MyArtNFT = await hre.ethers.getContractFactory("ArtistPopupNFT");
    const myArtNFT = await MyArtNFT.deploy();

    await myArtNFT.deployed();

    console.log("MyArtNFT deployed to:", myArtNFT.address);
    
    // Log the SKALE Explorer link
    const skaleExplorerUrl = "https://giant-half-dual-testnet.explorer.testnet.skalenodes.com";
    console.log(`View the contract on SKALE Explorer: ${skaleExplorerUrl}/address/${myArtNFT.address}`);

    // Save the contract address to a file for easy access
    fs.writeFileSync("contract-address.txt", myArtNFT.address);
    console.log("Contract address saved to contract-address.txt");

    // Save the contract ABI to a file
    const artifact = artifacts.readArtifactSync("ArtistPopupNFT");
    fs.writeFileSync("contract-abi.json", JSON.stringify(artifact.abi, null, 2));
    console.log("Contract ABI saved to contract-abi.json");
  } catch (error) {
    console.error("Error during deployment:", error);
    process.exit(1);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
