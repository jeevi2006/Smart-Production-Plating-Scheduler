from cryptography.fernet import Fernet
import json

hardware = input("Enter Hardware ID : ")

expiry = input("Expiry (YYYY-MM-DD): ")

license_data = {
    "hardware_id": hardware,
    "expiry_date": expiry
}

with open("secret.key","rb") as f:
    key = f.read()

fernet = Fernet(key)

encrypted = fernet.encrypt(
    json.dumps(license_data).encode()
)

with open("license.lic","wb") as f:
    f.write(encrypted)

print("License Generated")