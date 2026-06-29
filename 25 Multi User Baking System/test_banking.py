import unittest
import os
import json
import shutil
import datetime

# Import modules from our project
import storage
import user_menu
import main_menu

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        # Backup original files if they exist
        self.backups = {}
        for filename in ["users.json", "banking_data.json", "transactions.json"]:
            if os.path.exists(filename):
                self.backups[filename] = filename + ".bak"
                shutil.copyfile(filename, self.backups[filename])
            # Write clean state
            if filename == "users.json":
                with open(filename, "w") as f:
                    f.write("[]")
            else:
                with open(filename, "w") as f:
                    f.write("{}")

    def tearDown(self):
        # Restore backups
        for filename, backup in self.backups.items():
            if os.path.exists(backup):
                shutil.copyfile(backup, filename)
                os.remove(backup)
            elif os.path.exists(filename):
                os.remove(filename)

    def test_registration_and_login(self):
        users = storage.user_load()
        self.assertEqual(len(users), 0)
        
        # Manually seed a user
        user = {
            "username": "TestUser",
            "password": "password123",
            "account_number": "1111",
            "transaction_pin": "1234"
        }
        users.append(user)
        storage.user_save(users)
        
        loaded_users = storage.user_load()
        self.assertEqual(len(loaded_users), 1)
        self.assertEqual(loaded_users[0]["username"], "TestUser")

    def test_deposit(self):
        user = {
            "username": "TestUser",
            "password": "password123",
            "account_number": "1111",
            "transaction_pin": "1234"
        }
        # Seed banking data
        banking = storage.banking_load()
        banking["1111"] = {
            "name": "TestUser",
            "balance": 500.0,
            "account_type": "Savings"
        }
        storage.banking_save(banking)
        
        import builtins
        original_input = builtins.input
        
        try:
            # Mock input to return "250.0" for deposit amount
            builtins.input = lambda prompt: "250.0"
            user_menu.deposit(user)
            
            # Check updated balance
            updated_banking = storage.banking_load()
            self.assertEqual(updated_banking["1111"]["balance"], 750.0)
            
            # Check transaction history
            txs = storage.transactions_load()
            self.assertEqual(len(txs["1111"]), 1)
            self.assertEqual(txs["1111"][0]["amount"], 250.0)
            self.assertEqual(txs["1111"][0]["type"], "Deposit")
        finally:
            builtins.input = original_input

    def test_withdraw_insufficient_funds(self):
        user = {
            "username": "TestUser",
            "password": "password123",
            "account_number": "1111",
            "transaction_pin": "1234"
        }
        # Seed banking data
        banking = storage.banking_load()
        banking["1111"] = {
            "name": "TestUser",
            "balance": 100.0,
            "account_type": "Savings"
        }
        storage.banking_save(banking)
        
        import builtins
        original_input = builtins.input
        
        try:
            # Mock input to try withdrawing 150.0 (greater than 100.0)
            # 1st input: amount = "150.0"
            # 2nd input: pin = "1234"
            inputs = ["150.0", "1234"]
            input_idx = 0
            def mock_input(prompt):
                nonlocal input_idx
                val = inputs[input_idx]
                input_idx += 1
                return val
            builtins.input = mock_input
            
            user_menu.withdraw(user)
            
            # Balance should remain 100.0
            updated_banking = storage.banking_load()
            self.assertEqual(updated_banking["1111"]["balance"], 100.0)
        finally:
            builtins.input = original_input

    def test_transfer(self):
        sender = {
            "username": "Sender",
            "password": "pass",
            "account_number": "1111",
            "transaction_pin": "1234"
        }
        receiver = {
            "username": "Receiver",
            "password": "pass",
            "account_number": "2222",
            "transaction_pin": "5678"
        }
        # Seed banking data
        banking = storage.banking_load()
        banking["1111"] = {
            "name": "Sender",
            "balance": 1000.0,
            "account_type": "Savings"
        }
        banking["2222"] = {
            "name": "Receiver",
            "balance": 100.0,
            "account_type": "Savings"
        }
        storage.banking_save(banking)
        
        import builtins
        original_input = builtins.input
        
        try:
            # Inputs:
            # 1. Receiver Account Number: "2222"
            # 2. Transfer Amount: "400.0"
            # 3. PIN: "1234"
            inputs = ["2222", "400.0", "1234"]
            input_idx = 0
            def mock_input(prompt):
                nonlocal input_idx
                val = inputs[input_idx]
                input_idx += 1
                return val
            builtins.input = mock_input
            
            user_menu.transfer(sender)
            
            # Verify balances
            updated_banking = storage.banking_load()
            self.assertEqual(updated_banking["1111"]["balance"], 600.0)
            self.assertEqual(updated_banking["2222"]["balance"], 500.0)
            
            # Verify transaction logs
            txs = storage.transactions_load()
            self.assertEqual(len(txs["1111"]), 1)
            self.assertEqual(txs["1111"][0]["type"], "Transfer Out")
            self.assertEqual(txs["1111"][0]["amount"], 400.0)
            
            self.assertEqual(len(txs["2222"]), 1)
            self.assertEqual(txs["2222"][0]["type"], "Transfer In")
            self.assertEqual(txs["2222"][0]["amount"], 400.0)
        finally:
            builtins.input = original_input

if __name__ == "__main__":
    unittest.main()
