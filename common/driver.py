import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.logger import Logger
from selenium import webdriver
from appium.options.common import AppiumOptions

logger = Logger().get_logger(__name__)


def create_driver(device_name: str = "emulator-5554",
                  app_package: str = "com.android.settings",
                  app_activity: str = ".Settings") -> webdriver.Remote:
    try:
        options = AppiumOptions()  # 使用正确的选项类
        options.load_capabilities({
            "platformName": "Android",
            "appium:automationName": "uiautomator2",
            "appium:deviceName": device_name,
            "appium:appPackage": app_package,
            "appium:appActivity": app_activity,
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True
        })

        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)  # 确保URL正确
        logger.info("Creating Appium driver")
        return driver
    except Exception as e:
        logger.error(f"Failed to create Appium driver: {e}")
        raise

