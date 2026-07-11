import os
import sys
import json
import uuid
import subprocess
from datetime import datetime
from cryptography.fernet import Fernet

# -------------------------
# Base Directory
# -------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------
# Hardware ID
# -------------------------
def current_hardware():
    mac = str(uuid.getnode())

    try:
        uuid_value = subprocess.check_output(
            "wmic csproduct get uuid",
            shell=True
        ).decode().split("\n")[1].strip()

    except Exception:
        uuid_value = "UNKNOWN"

    return mac + uuid_value


# -------------------------
# License Validation
# -------------------------
def validate():

    try:

        # License File
        license_path = os.path.join(BASE_DIR, "license.lic")

        print("License Path :", license_path)

        if not os.path.exists(license_path):
            return {
                "status": "NO_LICENSE",
                "hardware_id": current_hardware()
            }

        # Secret Key
        secret_path = os.path.join(BASE_DIR, "secret.key")

        print("Secret Path :", secret_path)

        if not os.path.exists(secret_path):
            return {
                "status": "ERROR",
                "message": "secret.key not found"
            }

        with open(secret_path, "rb") as f:
            key = f.read()

        fernet = Fernet(key)

        with open(license_path, "rb") as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted)

        data = json.loads(decrypted.decode())

        current = current_hardware()

        # Hardware Check
        if data["hardware_id"] != current:
            return {
                "status": "INVALID_MACHINE",
                "hardware_id": current
            }

        # Expiry Check
        expiry = datetime.strptime(
            data["expiry_date"],
            "%Y-%m-%d"
        )

        if datetime.today() > expiry:
            return {
                "status": "LICENSE_EXPIRED",
                "hardware_id": current
            }

        # Success
        return {
            "status": "VALID",
            "hardware_id": current,
            "expiry_date": data["expiry_date"]
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "status": "ERROR",
            "message": str(e)
        }


if __name__ == "__main__":
    print(validate())