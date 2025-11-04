const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Scholarship contract", function () {
  it("registers a student, deposits funds and allows student claim", async function () {
    const [owner, student] = await ethers.getSigners();

    const Scholarship = await ethers.getContractFactory("Scholarship");
    const scholarship = await Scholarship.deploy();
    await scholarship.waitForDeployment(); // ✅ ethers v6 equivalent to .deployed()

    // Deposit 1 ether into contract
    await owner.sendTransaction({
      to: await scholarship.getAddress(),
      value: ethers.parseEther("1.0"),
    });

    // Register the student
    const allocation = ethers.parseEther("0.1");
    await scholarship.registerStudent(student.address, allocation);

    // Check student balance before claim
    const balanceBefore = await ethers.provider.getBalance(student.address);

    // Student claims scholarship
    const tx = await scholarship.connect(student).claimScholarship();
    await tx.wait();

    // Check student balance after claim
    const balanceAfter = await ethers.provider.getBalance(student.address);

    expect(balanceAfter).to.be.gt(balanceBefore);
  });
});
