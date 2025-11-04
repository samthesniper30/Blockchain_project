from flask import Flask, jsonify, request, render_template
from web3 import Web3
import json
import os

app = Flask(__name__)

# --------------------------
# 🔗 Blockchain Configuration
# --------------------------

# Connect to local Hardhat network
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if w3.is_connected():
    print("✅ Connected to Hardhat local blockchain")
else:
    print("❌ Connection failed. Make sure 'npx hardhat node' is running.")

# Load contract ABI
ABI_PATH = os.path.join("abi", "Scholarship.json")
with open(ABI_PATH) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Paste your deployed contract address here
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # 🔁 Replace this
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Set default (owner) account
OWNER_ADDRESS = w3.eth.accounts[0]
print(f"Using owner: {OWNER_ADDRESS}")

# --------------------------
# 🌐 Routes
# --------------------------

@app.route("/")
def home():
    return jsonify({"message": "Smart Contract Scholarship API running!"})


@app.route("/dashboard")
def dashboard():
    """Render the web dashboard UI"""
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register_student():
    """Register a student with allocated funds"""
    data = request.get_json()
    student_address = data.get("student_address")
    amount_eth = data.get("amount_eth")

    if not student_address or not amount_eth:
        return jsonify({"error": "Missing fields"}), 400

    amount_wei = w3.to_wei(amount_eth, "ether")

    try:
        tx_hash = contract.functions.registerStudent(student_address, amount_wei).transact({
            'from': OWNER_ADDRESS,
            'gas': 300000
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({
            "status": "Student registered",
            "tx_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/claim", methods=["POST"])
def claim_scholarship():
    """Allow student to claim their scholarship"""
    data = request.get_json()
    student_address = data.get("student_address")

    try:
        tx_hash = contract.functions.claimScholarship().transact({
            'from': student_address,
            'gas': 300000
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({
            "status": "Scholarship claimed",
            "tx_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/deposit", methods=["POST"])
def deposit_funds():
    """Deposit ETH into the contract"""
    data = request.get_json()
    amount_eth = data.get("amount_eth")
    amount_wei = w3.to_wei(amount_eth, "ether")

    try:
        tx_hash = contract.functions.depositFunds().transact({
            'from': OWNER_ADDRESS,
            'value': amount_wei,
            'gas': 300000
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({
            "status": "Funds deposited",
            "tx_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats", methods=["GET"])
def get_stats():
    """Retrieve blockchain-based scholarship stats"""
    try:
        stats = contract.functions.getStats().call()
        response = {
            "totalAllocated": float(w3.from_wei(stats[0], "ether")),
            "claimedAmount": float(w3.from_wei(stats[1], "ether")),
            "budget": float(w3.from_wei(stats[2], "ether")),
            "remainingBudget": float(w3.from_wei(stats[3], "ether"))
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# ▶️ Run Flask App
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
