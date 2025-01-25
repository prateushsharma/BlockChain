const DecentralizedStorage = artifacts.require("DecentralizedStorage");

module.exports = async function (deployer) {
  console.log("Starting deployment...");
  await deployer.deploy(DecentralizedStorage);
  console.log("DecentralizedStorage contract deployed successfully!");
};
