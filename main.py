from multiprocessing import Process, Queue

from environment import Environment
from gui_server import run_gui_server
from proxy_log import ProxyLog, ContentStorage
from proxy_server import run_proxy_server
from tester_server import run_rest_api_tester

environment = Environment.from_os_env()

if __name__ == '__main__':
    environment.print()
    content_storage = ContentStorage(path=environment.STORAGE_PATH)
    proxy_log = ProxyLog(queue_store=Queue(), content_storage=content_storage)
    Process(target=run_gui_server, args=(environment, proxy_log,)).start()
    Process(target=run_proxy_server, args=(environment, proxy_log,)).start()
    if environment.TESTER_MODE_ENABLED:
        print('Starting tester server for development')
        Process(target=run_rest_api_tester,
                args=(environment,)).start()
