import platform
import psutil
from prettytable import PrettyTable

def get_system_info():
    # Информация о ОС
    os_info = platform.uname()
    os_details = {
        "OS": os_info.system,
        "Архитектура": platform.architecture()[0],
        "CPU": os_info.processor,
    }

    # Информация о памяти
    memory_info = psutil.virtual_memory()
    memory_details = {
        "Memory": f"{memory_info.total // (1024 ** 2)} GB",
    }

    # Информация о дисках
    disk_info = []
    total_disks = 0
    for partition in psutil.disk_partitions():
        partition_usage = psutil.disk_usage(partition.mountpoint)
        total_disks += 1
        disk_info.append({
            "Device": partition.device,
            "Total": f"{partition_usage.total // (1024 ** 3)} GB",
            "Free": f"{partition_usage.free // (1024 ** 3)} GB",
            "Used": f"{partition_usage.used // (1024 ** 3)} GB",
        })

    return os_details, memory_details, total_disks, disk_info

def print_system_info(os_details, memory_details, total_disks, disk_info):
    # Создаем таблицу для ОС и памяти
    table = PrettyTable()
    table.field_names = ["Параметр", "Значение"]
    
    for key, value in os_details.items():
        table.add_row([key, value])
    for key, value in memory_details.items():
        table.add_row([key, value])
    table.add_row(["Disk", f"{total_disks} шт."])
    
    print(table)

    # Создаем таблицу для дисков
    disk_table = PrettyTable()
    disk_table.field_names = ["Диск", "Свободно", "Использовано"]
    
    for disk in disk_info:
        disk_table.add_row([disk["Device"], disk["Free"], disk["Used"]])
    
    print(disk_table)

if __name__ == "__main__":
    os_details, memory_details, total_disks, disk_info = get_system_info()
    print_system_info(os_details, memory_details, total_disks, disk_info)