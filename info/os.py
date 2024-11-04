import subprocess
import platform

def os_info():  # Информация о ОС и памяти
    os_info = platform.system() + " " + platform.release()
    s_n = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split('\n')[1].strip()
    model = subprocess.check_output("wmic computersystem get model", shell=True).decode().split('\n')[1].strip()
    os_details = {
        "OS": os_info,
        "Архитектура": platform.architecture()[0],
        "Model": model,
        "S/N": s_n,
    }
    return os_details