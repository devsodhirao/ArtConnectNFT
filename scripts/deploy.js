const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  const ArtistPopupNFT = await hre.ethers.getContractFactory("ArtistPopupNFT");
  const artistPopupNFT = await ArtistPopupNFT.deploy();

  await artistPopupNFT.deployed();

  console.log("ArtistPopupNFT deployed to:", artistPopupNFT.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
