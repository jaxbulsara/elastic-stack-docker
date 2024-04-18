import logging
import platform

class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True

hostname = platform.node()
formatter = logging.Formatter("{asctime} [{hostname}][{levelname}][{name}] {message}", style="{")
handler = logging.FileHandler(f"/logs/{hostname}.log")
handler.addFilter(HostnameFilter())
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
