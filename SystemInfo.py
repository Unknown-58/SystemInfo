import platform
import psutil
import subprocess
import socket
from prettytable import PrettyTable

def cpu_name():  # Получаем название процессора
    cpu = subprocess.Popen(['wmic', 'cpu', 'get', 'name'], stdout=subprocess.PIPE, text=True)
    clean_cpu_name = subprocess.Popen(['findstr', '/v', 'Name'], stdin=cpu.stdout, stdout=subprocess.PIPE, text=True)
    output, _ = clean_cpu_name.communicate()  # Получаем результат
    return output.strip()

def os_info():  # Информация о ОС и памяти
    os_info = platform.system() + " " + platform.release()
    memory_info = psutil.virtual_memory()
    s_n = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split('\n')[1].strip()
    model = subprocess.check_output("wmic computersystem get model", shell=True).decode().split('\n')[1].strip()
    os_details = {
        "OS": os_info,
        "Архитектура": platform.architecture()[0],
        "Model" : model,
        "S/N" : s_n,
    }
    memory_details = {
        "Memory": f"{memory_info.total // (1024 ** 2)} Gb",
    }

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

def net_info():  # Информация о сетевых интерфейсах
    net_info = psutil.net_if_addrs()
    net_table = PrettyTable()
    net_table.field_names = ["Интерфейс", "IP-адрес", "Маска подсети"]
    
    for interface, addresses in net_info.items():
        for address in addresses:
            if address.family == socket.AF_INET:  # Фильтруем только IPv4 адреса
                net_table.add_row([interface, address.address, address.netmask])
    return net_table

def print_system_info(os_details, memory_details, total_disks, disk_info, cpu_details):  # Вывод информации о системе
    table = PrettyTable()
    table.field_names = ["Параметр", "Значение"] 
    for key, value in os_details.items():
        table.add_row([key, value]) 
    for key, value in memory_details.items():
        table.add_row([key, value])  
    table.add_row(["Disk", f"{total_disks} шт."])  # Добавляем количество дисков
    print(table)

    cpu_table = PrettyTable()  # Создаем таблицу для CPU
    cpu_table.field_names = ["Параметр", "Значение"]
    for key, value in cpu_details.items():
        cpu_table.add_row([key, value])
    print(cpu_table)

    disk_table = PrettyTable()  # Создаем таблицу для дисков
    disk_table.field_names = ["Диск", "Всего", "Используется", "Свободно"]  
    for disk in disk_info:
        disk_table.add_row([disk["Device"], disk["Total"], disk["Used"], disk["Free"]])
    print(disk_table)

if __name__ == "__main__":
    os_details, memory_details, total_disks, disk_info = os_info()
    cpu_details = cpu()
    net_table = net_info()  # Получаем информацию о сетевых интерфейсах
    print_system_info(os_details, memory_details, total_disks, disk_info, cpu_details)
    print(net_table)
