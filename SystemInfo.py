from info import os
from info import cpu
from info import ram
from info import disk
from info import network
from info import html

def main():
    # Получаем информацию из каждого модуля
    os_details = os.os_info()
    memory = ram.ram()
    cpu_details = cpu.cpu()
    disk_info = disk.get_disk_info()  # Вызываем функцию для получения информации о дисках
    net_info, external_ip = network.net_info()  # Получаем информацию о сети
    sn = os_details["S/N"]  # Получаем серийный номер для заголовка HTML

    # Генерируем HTML
    html.generate_html(os_details, memory, disk_info, cpu_details, net_info, external_ip, sn)

if __name__ == "__main__":
    main()