import os


class Environment:
    def __init__(self):
        self.GUI_LISTEN_HOST: str = '0.0.0.0'
        self.GUI_LISTEN_PORT: int = 8080
        self.PROXY_LISTEN_HOST: str = '0.0.0.0'
        self.PROXY_LISTEN_PORT: int = 8081
        self.PROXY_OVERRIDE_HOST_HEADER: bool = True
        self.TESTER_LISTEN_HOST: str | None = None
        self.TESTER_LISTEN_PORT: int = 0
        self.TESTER_MODE_ENABLED = False
        self.PROXY_DESTINATION: str = f'http://127.0.0.1:{self.TESTER_LISTEN_PORT}'
        self.TESTER_DESTINATION: str = f'http://127.0.0.1:{self.PROXY_LISTEN_PORT}'
        self.STORAGE_PATH: str = os.path.join('.', 'storage')

    @staticmethod
    def from_os_env() -> 'Environment':
        env = Environment()
        env.GUI_LISTEN_HOST = os.getenv('GUI_LISTEN_HOST', '0.0.0.0')
        env.GUI_LISTEN_PORT = int(os.getenv('GUI_LISTEN_PORT', 8080))
        env.PROXY_LISTEN_HOST = os.getenv('PROXY_LISTEN_HOST', '0.0.0.0')
        env.PROXY_LISTEN_PORT = int(os.getenv('PROXY_LISTEN_PORT', 8081))
        env.PROXY_OVERRIDE_HOST_HEADER = Environment._env_get_bool('PROXY_OVERRIDE_HOST_HEADER', True)
        env.TESTER_LISTEN_HOST = os.getenv('TESTER_LISTEN_HOST', None)
        env.TESTER_LISTEN_PORT = int(os.getenv('TESTER_LISTEN_PORT', 0))
        env.TESTER_MODE_ENABLED = env.TESTER_LISTEN_HOST is not None and env.TESTER_LISTEN_PORT > 0
        env.PROXY_DESTINATION = os.getenv('PROXY_DESTINATION',
                                          f'http://{env.TESTER_LISTEN_HOST}:{env.TESTER_LISTEN_PORT}')
        env.STORAGE_PATH = str = os.getenv('STORAGE_PATH', os.path.join('.', 'storage'))
        return env

    @staticmethod
    def _env_get_bool(key: str, default) -> bool:
        value = os.getenv(key, default)
        if isinstance(value, bool):
            return value
        if not isinstance(value, str):
            return False
        return value.lower() in ['true', '1', 'y', 'yes', 'on']

    def print(self):
        print('Environment variables:')
        print('GUI_LISTEN_HOST:', self.GUI_LISTEN_HOST)
        print('GUI_LISTEN_PORT:', self.GUI_LISTEN_PORT)
        print('PROXY_LISTEN_HOST:', self.PROXY_LISTEN_HOST)
        print('PROXY_LISTEN_PORT:', self.PROXY_LISTEN_PORT)
        print('PROXY_DESTINATION:', self.PROXY_DESTINATION)
        print('PROXY_OVERRIDE_HOST_HEADER:', self.PROXY_OVERRIDE_HOST_HEADER)
        print('STORAGE_PATH:', self.STORAGE_PATH)
        if self.TESTER_MODE_ENABLED:
            print('TESTER_LISTEN_HOST:', self.TESTER_LISTEN_HOST)
            print('TESTER_LISTEN_PORT:', self.TESTER_LISTEN_PORT)
            print('TESTER_DESTINATION:', self.TESTER_DESTINATION)
