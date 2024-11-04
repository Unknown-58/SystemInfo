import subprocess
import psutil

def cpu_name():  # Получаем название процессора
    cpu = subprocess.Popen(['wmic', 'cpu', 'get', 'name'], stdout=subprocess.PIPE, text=True)
    clean_cpu_name = subprocess.Popen(['findstr', '/v', 'Name'], stdin=cpu.stdout, stdout=subprocess.PIPE, text=True)
    output, _ = clean_cpu_name.communicate()  # Получаем результат
    return output.strip()

def cpu():
    cpu_core = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_frequency = psutil.cpu_freq().current
    cpu_details = {
        "CPU": cpu_name(),
        "Cores": cpu_core,
        "Threads": cpu_threads,
        "Frequency": f"{cpu_frequency} MHz"
    }
    return cpu_details