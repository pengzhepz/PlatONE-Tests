import os
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# base settings
PLATONE_URL = ''                                                # platone download url
WEB_MANAGER_URL = ''                                            # Management system url
CHAIN_FILE = os.path.join(BASE_DIR, 'files/chain_file.yml')     # chain config file

# deplou settings
DEPLOY_DIR = 'platone'                                          # platone deploy dir

# selenium settings
DRIVER = 'chrome'
GLOBAL_TIMEOUT = 30                                             # selenium global timeout
IMAGE_DIR = './report/image/'
deploy_path = r"platone_test"
scripts_path = r'/home/platon/platone_test/node-16790/linux/scripts'
download_url = 'http://10.10.8.179/'
# log settings
LOG_DIR = './report/file_{time}.log'
LOG_SIZE = '500 MB'
# LOG_FORMAT = '{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}'
license_filepath = os.path.abspath(os.path.join(r"C:\Autocode\PlatONE-Tests\files", "platone-license"))

# mgrapi_host
mgrapi_host = 'http://10.10.8.184'
