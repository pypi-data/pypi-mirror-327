import re
import sys

from datetime import datetime, timedelta, timezone
from importlib.metadata import version

from pathlib import Path

HOME_DIR = Path.home() / ".fpk"
HOME_DIR.mkdir(exist_ok=True)
PACKAGE_DIR = Path(sys.modules["flatpack"].__file__).parent
CONFIG_FILE_PATH = HOME_DIR / ".fpk_config.toml"

GIT_CACHE_FILE = HOME_DIR / ".fpk_git.cache"
IMPORT_CACHE_FILE = PACKAGE_DIR / ".fpk_import_cache"

BASE_URL = "https://codeberg.org/curlang/curlang/raw/branch/main/warehouse"
CODEBERG_REPO_URL = "https://codeberg.org/api/v1/repos/curlang/curlang"
TEMPLATE_REPO_URL = "https://codeberg.org/api/v1/repos/curlang/template"

GITHUB_REPO_URL = "https://api.github.com/repos/RomlinGroup/Flatpack"

CONNECTIONS_FILE = "connections.json"
HOOKS_FILE = "hooks.json"

COOLDOWN_PERIOD = timedelta(minutes=1)
GIT_CACHE_EXPIRY = timedelta(hours=1)
SERVER_START_TIME = None

ANSI_ESCAPE = re.compile(rb'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

CSRF_EXEMPT_PATHS = ["/", "/csrf-token", "/favicon.ico", "/static"]

MAX_ATTEMPTS = 1000000
VALIDATION_ATTEMPTS = 0

VERSION = version("flatpack")
