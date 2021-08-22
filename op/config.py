from dataclasses import dataclass
from typing import Sequence, Set

import toml

CONFIG_FILENAME = 'op.toml'
PORTS_ENVS = {
    'local': 1,
    'prod': 2,
    'tests': 3,
}
PORTS_SERVICE_APP = 0
PORTS_SERVICE_DB = 1
PORTS_SERVICE_APP_SECOND = 2


@dataclass
class Config:
    short_name: str
    long_name: str
    language: str
    config: str

    project_id: int
    environments: Sequence[str]
    services: Sequence[str]
    ports: dict

    app_second: bool  # TODO: maybe replace with prometheus (or add prometheus handler to the main port)
    database: bool


def generate_port(project_id: int, env_id: int, service_id: int):
    return 30000 + project_id*100 + env_id*10 + service_id


def generate_ports(environments: Set[str], project_id: int, database: bool, app_second: bool) -> dict:
    res = {}
    for env_name, env_id in PORTS_ENVS.items():
        if env_name not in environments and env_name != 'tests':
            continue

        res[env_name] = {
            'app': generate_port(project_id, env_id, PORTS_SERVICE_APP)
        }
        if database:
            res[env_name]['db'] = generate_port(project_id, env_id, PORTS_SERVICE_DB)
        if app_second:
            res[env_name]['app_second'] = generate_port(project_id, env_id, PORTS_SERVICE_APP_SECOND)

    return res


def get_services(database: bool) -> Sequence[str]:
    if database:
        return 'app', 'db'

    return 'db',


def parse_config() -> Config:
    with open(CONFIG_FILENAME, encoding='utf-8') as f:
        res = toml.load(f)

    environments = res['environments']
    ports = generate_ports(
        set(environments),
        res['project_id'],
        res['database'],
        res['app_second'],
    )
    services = get_services(res['database'])

    return Config(
        res['short_name'],
        res['long_name'],
        res['language'],
        res['config'],
        res['project_id'],
        res['environments'],
        services,
        ports,
        res['app_second'],
        res['database'],
    )
