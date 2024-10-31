import platform
import psutil
import subprocess
import socket

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
        "Model": model,
        "S/N": s_n,
    }
    memory_details = {
        "Memory": f"{memory_info.total // (1024 ** 2)} Gb",
    }
    
    disk_info = []  # Информация о дисках
    for partition in psutil.disk_partitions():
        partition_usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "Device": partition.device,
            "Total": f"{partition_usage.total // (1024 ** 3)} Gb",
            "Used": f"{partition_usage.used // (1024 ** 3)} Gb",
            "Free": f"{partition_usage.free // (1024 ** 3)} Gb",
        })
    
    return os_details, memory_details, disk_info

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

def generate_html(os_details, memory_details, disk_info, cpu_details, net_info, external_ip, sn):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Информация о системе - {sn}</title>
        <style>
            table {{
                width: 50%;
                border-collapse: collapse;
                margin: 20px auto;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
    <h2 style="text-align: center;">Таблица ОС</h2>
    <table>
        <thead>
            <tr>
                <th>Параметр</th>
                <th>Значение</th>
            </tr>
        </thead>
        <tbody>
            {"".join(f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in os_details.items())}
            {"".join(f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in memory_details.items())}
        </tbody>
    </table>

    <h2 style="text-align: center;">Таблица CPU</h2>
    <table>
        <thead>
            <tr>
                <th>Параметр</th>
                <th>Значение</th>
            </tr>
        </thead>
        <tbody>
            {"".join(f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in cpu_details.items())}
        </tbody>
    </table>

    <h2 style="text-align: center;">Таблица дисков</h2>
    <table>
        <thead>
            <tr>
                <th>Диск</th>
                <th>Всего</th>
                <th>Используется</th>
                <th>Свободно</th>
            </tr>
        </thead>
        <tbody>
            {"".join(f"<tr><td>{disk['Device']}</td><td>{disk['Total']}</td><td>{disk['Used']}</td><td>{disk['Free']}</td></tr>" for disk in disk_info)}
        </tbody>
    </table>
    
    <h2 style="text-align: center;">Таблица сети</h2>
    <table>
        <thead>
            <tr>
                <th>Интерфейс</th>
                <th>IP-адрес</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Внешний IP</td>
                <td>{external_ip}</td>
            </tr>
            {"".join(f"<tr><td>{interface}</td><td>{address.address}</td></tr>" for interface, addresses in net_info.items() for address in addresses if address.family == socket.AF_INET)}
        </tbody>
    </table>
    </body>
    </html>
    """
    # Сохраняем HTML в файл
    file_name = f"{sn}.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"HTML файл сохранен как {file_name}")

if __name__ == "__main__":
    os_details, memory_details, disk_info = os_info()
    cpu_details = cpu()
    net_info_data, external_ip = net_info()  # Получаем информацию о сети и внешний IP
    sn = os_details["S/N"]  # Получаем S/N для названия файла
    generate_html(os_details, memory_details, disk_info, cpu_details, net_info_data, external_ip, sn)