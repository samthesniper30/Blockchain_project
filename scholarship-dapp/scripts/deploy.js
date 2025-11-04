const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  const Scholarship = await hre.ethers.getContractFactory("Scholarship");
  const scholarship = await Scholarship.deploy();
  await scholarship.waitForDeployment?.(); // ethers v6 safe call or fallback
  console.log("Scholarship deployed to:", scholarship.target || scholarship.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
