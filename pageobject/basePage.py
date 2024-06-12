import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from config.config import SCREENSHOTS_DIR
from common.logger import Logger

logger = Logger().get_logger(__name__)
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator: tuple, lists=False, timeout=10) -> WebElement:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*locator) if not lists else d.find_elements(*locator)
            )
            logger.info(f"Element found: {locator}")
            return element
        except Exception as e:
            self.save_screenshot("find_element")
            logger.error(f"Error finding element by {locator}: {e}")
            raise

    def perform_touch_action(self, start_locator: tuple, end_locator: tuple = None, long_press=False,
                             direction='up', duration=1500):
        try:
            actions = ActionChains(self.driver)
            pointer = PointerInput(POINTER_TOUCH, "touch")
            actions.w3c_actions = ActionBuilder(self.driver, mouse=pointer)

            start_element = self.find_element(start_locator)
            actions.w3c_actions.pointer_action.move_to(start_element)
            actions.w3c_actions.pointer_action.pointer_down()

            if long_press:
                actions.w3c_actions.pointer_action.pause(duration / 1000)
            elif end_locator:
                end_element = self.find_element(end_locator)
                actions.w3c_actions.pointer_action.move_to(end_element)
            else:
                # 快速滑动
                if direction == 'up':
                    actions.w3c_actions.pointer_action.move_by(0, -duration)
                elif direction == 'down':
                    actions.w3c_actions.pointer_action.move_by(0, duration)
                elif direction == 'left':
                    actions.w3c_actions.pointer_action.move_by(-duration, 0)
                elif direction == 'right':
                    actions.w3c_actions.pointer_action.move_by(duration, 0)
                else:
                    raise ValueError(f"Invalid direction: {direction}")

            actions.w3c_actions.pointer_action.pointer_up()
            actions.w3c_actions.perform()

            if long_press:
                logger.info(f"Long pressed element by {start_locator}")
            elif end_locator:
                logger.info(f"Touched from {start_locator} to {end_locator}")
            else:
                logger.info(f"Quick swipe from {start_locator} in direction {direction}")
        except Exception as e:
            logger.error(f"Error performing touch action: {e}")
            raise

    def click(self, locator: tuple):
        try:
            self.find_element(locator).click()
            logger.info(f"Clicked element by {locator}")
        except Exception as e:
            logger.error(f"Error clicking element by {locator}: {e}")
            raise

    def send_keys(self, locator: tuple, keys: str):
        try:
            self.find_element(locator).send_keys(keys)
            logger.info(f"Sent keys to {locator} by {keys}")
        except Exception as e:
            logger.error(f"Error sending keys to {locator} by {keys}: {e}")
            raise

    def install_app(self, app_path):
        try:
            self.driver.install_app(app_path)
            logger.info(f"Installed app from {app_path}")
        except Exception as e:
            logger.error(f"Error installing app from {app_path}: {e}")
            raise

    def remove_app(self, app_id):
        try:
            self.driver.remove_app(app_id)
            logger.info(f"Removed app with ID {app_id}")
        except Exception as e:
            logger.error(f"Error removing app with ID {app_id}: {e}")
            raise

    def activate_app(self, app_id):
        try:
            self.driver.activate_app(app_id)
            logger.info(f"Started activity {app_id}")
        except Exception as e:
            logger.error(f"Error starting activity {app_id}: {e}")
            raise

    def background_app(self, seconds):
        try:
            self.driver.background_app(seconds)
            logger.info(f"Background for {seconds} seconds")
        except Exception as e:
            logger.error(f"Error backgrounding for {seconds} seconds: {e}")
            raise

    def save_screenshot(self, file_name):

        # 保留12张截图，login运行两次的数量
        log_files = sorted(
            (os.path.join(SCREENSHOTS_DIR, f) for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.png')),
            key=os.path.getmtime
        )
        while len(log_files) > 4:
            os.remove(log_files.pop(0))

        # filepath = 指图片保存目录/model(页面功能名称)_当前时间到秒.png
        # 当前时间
        dateNow = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # 路径
        file_path = fr'{SCREENSHOTS_DIR}\{file_name}_{dateNow}.png'
        try:
            self.driver.save_screenshot(file_path)
            logger.info(f"Screenshot saved to {file_path}")
        except Exception as e:
            logger.error(f"Error screenshot and saving to {file_path}: {e}")
            raise

    def set_network_connection(self, connection_type):
        try:
            self.driver.set_network_connection(connection_type)
            logger.info(f"Network connection set to {connection_type}")
        except Exception as e:
            logger.error(f"Error setting network connection to {connection_type}: {e}")
            raise

    def send_keycode(self, keycode):
        try:
            self.driver.press_keycode(keycode)
            logger.info(f"Sent keycode {keycode}")
        except Exception as e:
            logger.error(f"Error sending keycode {keycode}: {e}")
            raise

    def open_notifications(self):
        try:
            self.driver.open_notifications()
            logger.info("Notifications opened")
        except Exception as e:
            logger.error(f"Error opening notifications: {e}")
            raise

    def implicitly_wait(self, timeout):
        try:
            self.driver.implicitly_wait(timeout)
            logger.info(f"Set implicit wait to {timeout} seconds")
        except Exception as e:
            logger.error(f"Error setting implicit wait to {timeout} seconds: {e}")
            raise

    def close_app(self):
        try:
            self.driver.close()
            logger.info("Closed app")
        except Exception as e:
            logger.error(f"Error closing app: {e}")
            raise

    def quit(self):
        try:
            self.driver.quit()
            logger.info("Quit driver")
        except Exception as e:
            logger.error(f"Error quitting driver: {e}")
            raise
