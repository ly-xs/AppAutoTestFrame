import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.getYaml import GetYaml
from config.config import PAGE_DATA_DIR
from pageobject.basePage import BasePage

# 获取页面元素
pageData = GetYaml(PAGE_DATA_DIR + r"\settings_element.yaml")


class SettingsPage(BasePage):
    connected_devices = (pageData.get_find_type(0), pageData.get_element_info(0))
    sound_and_vibration = (pageData.get_find_type(1), pageData.get_element_info(1))
    notification_volume = (pageData.get_find_type(2), pageData.get_element_info(2))
    connected_devices_direction = pageData.get_direction(0)
    connected_devices_duration = pageData.get_duration(0)
    notification_volume_direction = pageData.get_direction(2)
    notification_volume_duration = pageData.get_duration(2)

    def settings_sound(self):
        self.perform_touch_action(start_locator=self.connected_devices, direction=self.connected_devices_direction,
                                  duration=self.connected_devices_duration)
        self.click(self.sound_and_vibration)
        self.perform_touch_action(start_locator=self.notification_volume, direction=self.notification_volume_direction,
                                  duration=self.notification_volume_duration)

    notification_volume_level = (pageData.get_check_find_type(0), pageData.get_check_element_info(0))

    def check_notification_volume(self):
        return self.find_element(self.notification_volume_level).text
