import os
from loguru import logger

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
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
conf_path = r'/home/platon/platone_test/node-16789/linux/conf'
scripts_path = r'/home/platon/platone_test/node-16789/linux/scripts'
download_url = 'http://10.10.8.179/'
# log settings
LOG_DIR = './report/file_{time}.log'
LOG_SIZE = '500 MB'
# LOG_FORMAT = '{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}'
PLATONE_LICENSE_FILE = os.path.join(BASE_DIR, r"files\platone-license")
TMP_GENESIS = os.path.join(BASE_DIR, r"files\tmp")
GENESIS_FILE = os.path.join(BASE_DIR, r"files\tmp\genesis.json")
# license_file_path = os.path.abspath(os.path.join(BASE_DIR, r"\files\platone-license"))
# license_file_path = os.path.join(BASE_DIR, '1')

# mgrapi_host
mgrapi_host = 'http://10.10.8.184'

CHAIN_ID= 200
hrp = 'lax'
sys_ledger = 'sys'

#nodes_file
NODES_FILE = os.path.join(BASE_DIR, r'lib/env/nodes_template.yml')

NIDE_INFO_FILE = os.path.join(BASE_DIR, r'lib/env/node_info.yml')

ADDRESS_FILE = os.path.join(BASE_DIR, r'lib/env/user_address.yml')

visitor_wallet_file = os.path.join(BASE_DIR, r'lib\env\wallet.json')

linux_put_keystore = r'/home/juzix/platone_test/node-17789/linux/data/node-1/keystore'
wallet_file = 'wallet.json'
