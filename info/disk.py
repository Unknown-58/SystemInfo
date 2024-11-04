import psutil

def get_disk_info():
    disk_info = []  # Информация о дисках
    for partition in psutil.disk_partitions():
        partition_usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "Device": partition.device,
            "Total": f"{partition_usage.total // (1024 ** 3)} Gb",
            "Used": f"{partition_usage.used // (1024 ** 3)} Gb",
            "Free": f"{partition_usage.free // (1024 ** 3)} Gb",
        })
    return disk_info