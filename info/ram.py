import psutil

def ram ():
    memory_info = psutil.virtual_memory()
    ram_details = {
            "Memory": f"{memory_info.total // (1024 ** 2)} Gb",
        }
    return ram_details