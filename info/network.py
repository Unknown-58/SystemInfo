import subprocess
import psutil

def get_external_ip():
    try:
        result = subprocess.run(['curl', '-s', 'ifconfig.me'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Ошибка получения внешнего IP"

def net_info():
    net_info = psutil.net_if_addrs()
    external_ip = get_external_ip()  # Получаем внешний IP
    return net_info, external_ip