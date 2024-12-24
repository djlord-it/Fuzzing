import psutil

class SystemHealth:
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage():
        memory = psutil.virtual_memory()
        return memory.percent

    @staticmethod
    def get_network_usage():
        return psutil.net_io_counters()

# Example Usage
if __name__ == "__main__":
    print(f"CPU Usage: {SystemHealth.get_cpu_usage()}%")
    print(f"Memory Usage: {SystemHealth.get_memory_usage()}%")
    print(f"Network Usage: {SystemHealth.get_network_usage()}")
