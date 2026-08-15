# 🏦 Bank Management System

A menu-driven **Bank Management System** built in Python, simulating core banking operations such as account creation, deposits, withdrawals, fund transfers, and transaction history — all through a simple command-line interface.

This is a mini project built to practice **Object-Oriented Programming**, **file handling**, and **exception handling** in Python.

## ✨ Features

- **Create Account** — auto-generated account number with PIN-based security
- **Deposit & Withdraw** — with balance validation (no overdrafts allowed)
- **Fund Transfer** — move money between two accounts
- **Mini Statement** — view the last 5 transactions for any account
- **Delete Account** — remove an account permanently
- **Data Persistence** — all account data is saved to `bank_data.json` and reloaded automatically on the next run
- **Input Validation** — handles invalid inputs and errors gracefully without crashing

## 🛠️ Tech Stack

- **Language:** Python 3
- **Libraries used:** `json`, `os`, `datetime` (all standard library — no external dependencies)

## 📂 Project Structure

```
bank-management-system/
│
├── bank_management_system.py   # Main application
├── bank_data.json               # Auto-generated data file (created on first run)
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher installed

### Run the project
```bash
git clone https://github.com/your-username/bank-management-system.git
cd bank-management-system
python bank_management_system.py
```

## 📖 How It Works

1. `Account` class — represents a single bank account and handles deposit/withdraw logic
2. `Bank` class — manages all accounts, authentication, and transfers
3. Data is persisted to a JSON file so accounts remain saved between sessions
4. A CLI menu loop lets the user interact with the system

## ⚠️ Disclaimer

This project is built **for educational purposes only**. It is a simulation and does **not** represent real banking software — PINs are stored in plain text, there is no encryption, and it is not intended for real financial use.

## 🔮 Future Improvements

- [ ] Hash PINs using `hashlib` for better security
- [ ] Migrate from JSON to SQLite database
- [ ] Add admin login to view/manage all accounts
- [ ] Add interest calculation for savings accounts
- [ ] Build a GUI using Tkinter or a web version using Flask

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ If you found this project helpful, consider giving it a star!
