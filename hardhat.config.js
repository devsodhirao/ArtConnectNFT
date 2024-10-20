require("@nomiclabs/hardhat-waffle");
require('dotenv').config();

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    skale: {
      url: process.env.SKALE_ENDPOINT || "",
      accounts: [process.env.PRIVATE_KEY],
      chainId: 974399131
    }
  },
  paths: {
    artifacts: './artifacts',
  },
};
