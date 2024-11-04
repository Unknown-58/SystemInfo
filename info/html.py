import socket

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