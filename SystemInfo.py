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

def get_system_info():  # Информация о ОС и памяти
    os_info = platform.system() + " " + platform.release()
    memory_info = psutil.virtual_memory()
    os_details = {
        "OS": os_info,
        "Архитектура": platform.architecture()[0],
        "CPU": cpu_name(),
    }
    memory_details = {
        "Memory": f"{memory_info.total // (1024 ** 2)} Gb",
    }

    disk_info = []  # Информация о дисках
    total_disks = 0
    for partition in psutil.disk_partitions():
        partition_usage = psutil.disk_usage(partition.mountpoint)
        total_disks += 1
        disk_info.append({
            "Device": partition.device,
            "Total": f"{partition_usage.total // (1024 ** 3)} Gb",
            "Used": f"{partition_usage.used // (1024 ** 3)} Gb",
            "Free": f"{partition_usage.free // (1024 ** 3)} Gb",
        })
    
    return os_details, memory_details, total_disks, disk_info

def get_network_info():  # Информация о сетевых интерфейсах
    net_info = psutil.net_if_addrs()
    net_table = PrettyTable()
    net_table.field_names = ["Интерфейс", "IP-адрес", "Маска подсети"]
    
    for interface, addresses in net_info.items():
        for address in addresses:
            if address.family == socket.AF_INET:  # Фильтруем только IPv4 адреса
                net_table.add_row([interface, address.address, address.netmask])
    return net_table

def print_system_info(os_details, memory_details, total_disks, disk_info):  # Вывод информации о системе
    table = PrettyTable()
    table.field_names = ["Параметр", "Значение"] 
    for key, value in os_details.items():
        table.add_row([key, value]) 
    for key, value in memory_details.items():
        table.add_row([key, value])  
    table.add_row(["Disk", f"{total_disks} шт."])
    print(table)

    disk_table = PrettyTable()  # Создаем таблицу для дисков
    disk_table.field_names = ["Диск", "Всего", "Используется", "Свободно"]  
    for disk in disk_info:
        disk_table.add_row([disk["Device"], disk["Total"], disk["Used"], disk["Free"]])
    print(disk_table)

if __name__ == "__main__":
    os_details, memory_details, total_disks, disk_info = get_system_info()
    net_table = get_network_info()  # Получаем информацию о сетевых интерфейсах
    print_system_info(os_details, memory_details, total_disks, disk_info)
    print(net_table)