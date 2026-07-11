import uuid
import subprocess

def get_hardware_id():

    mac = str(uuid.getnode())

    motherboard = subprocess.check_output(
        "wmic csproduct get uuid"
    ).decode().split("\n")[1].strip()

    return mac + motherboard