import configparser
import unittest

from ddt import ddt, data
from common.driver import create_driver
from common.getYaml import GetYaml
from common.logger import Logger
from config.config import CONFIG_FILE, TEST_DATA_DIR
from pageobject.settingsPage import SettingsPage

logger = Logger().get_logger(__name__)
# 读取config.ini配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")
deviceName = config.get("Capability", "deviceName")
appPackage = config.get("Capability", "appPackage")
appActivity = config.get("Capability", "appActivity")


@ddt
class SettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = SettingsPage(create_driver(deviceName, appPackage, appActivity))

    def tearDown(self):
        self.settings.quit()

    @data(*GetYaml(TEST_DATA_DIR + r"\settings_data.yaml").get_yaml())
    def test_settings(self, testdata):
        logger.info(f"当前执行测试用例ID-> {testdata['id']}; 测试点-> {testdata['detail']}")
        self.settings.settings_sound()

        self.assertEqual(float(self.settings.check_notification_volume()), testdata['check'][0],
                         f"返回实际结果是->: {self.settings.check_notification_volume()}")
        self.settings.save_screenshot(testdata['screenshot'])
