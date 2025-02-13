from .running.runner import main
from .running.conf import App
from .utils.config import kconfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .api import HttpReq, TC
from .adr import TC as AdrTC
from .ios import TC as IosTC
from .web import TC as WebTC
from .hm import TC as HmTC

__version__ = "0.1.64"
__description__ = "API/安卓/IOS/WEB/鸿蒙Next平台自动化测试框架"
