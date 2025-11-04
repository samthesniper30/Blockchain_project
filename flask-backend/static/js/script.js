async function registerStudent() {
  const address = document.getElementById("studentAddress").value;
  const amount = document.getElementById("amountEth").value;

  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ student_address: address, amount_eth: amount }),
  });
  const data = await res.json();
  alert("Student registered! Tx: " + data.tx_hash);
  loadStats();
}

async function depositFunds() {
  const amount = document.getElementById("depositAmount").value;
  const res = await fetch("/deposit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount_eth: amount }),
  });
  const data = await res.json();
  alert("Funds deposited! Tx: " + data.tx_hash);
  loadStats();
}

async function claimScholarship() {
  const address = document.getElementById("claimAddress").value;
  const res = await fetch("/claim", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ student_address: address }),
  });
  const data = await res.json();
  alert("Scholarship claimed! Tx: " + data.tx_hash);
  loadStats();
}

async function loadStats() {
  const res = await fetch("/stats");
  const stats = await res.json();

  document.getElementById("allocated").innerText = stats.totalAllocated;
  document.getElementById("claimed").innerText = stats.claimedAmount;
  document.getElementById("budget").innerText = stats.budget;
  document.getElementById("remaining").innerText = stats.remainingBudget;

  updateChart(stats);
}

let chart;
function updateChart(stats) {
  const ctx = document.getElementById("statsChart").getContext("2d");
  const data = {
    labels: ["Allocated", "Claimed", "Remaining"],
    datasets: [{
      label: "Scholarship Fund Distribution (ETH)",
      data: [stats.totalAllocated, stats.claimedAmount, stats.remainingBudget],
      backgroundColor: ["#1e2a78", "#2c3eaf", "#6c8eff"]
    }]
  };

  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "doughnut",
    data: data,
    options: { responsive: true }
  });
}

loadStats();
