from dataclasses import dataclass


@dataclass
class Host:
    host: str = None
    username: str = None
    password: str = None
    ssh_port: int = 22
