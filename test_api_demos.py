import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class ApiDemosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the Appium driver with desired capabilities before any tests run start.
        """
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = "12.0"
        options.device_name = "Pixel7"
        options.udid = "emulator-5554"

        # Update the APK path to your specified location
        apk_path = "C:/Users/MSM/PycharmProjects/AppiumSession/test_app/ApiDemos-debug.apk"
        options.app = apk_path
        options.automation_name = "UiAutomator2"
        options.no_reset = True
        options.full_reset = False
        options.auto_grant_permissions = True

        # Initialize the Appium driver
        try:
            cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
            cls.driver.implicitly_wait(10)  # Reduced implicit wait
            logging.info("Appium driver initialized successfully.")
        except Exception as error:
            logging.error(f"Failed to initialize Appium driver: {error}")
            raise error

        # Initialize WebDriverWait
        cls.wait = WebDriverWait(cls.driver, 20)

    def test_ui_demo(self):
        """
        Test case to navigate through various sections of the ApiDemos app and handle sub-menus.
        """
        api_demos_buttons = [
            "Accessibility", "Animation", "App", "Content", "Graphics", "Media", "NFC", "OS", "Preference", "Text",
            "Views"
        ]

        sub_buttons = {
            "Accessibility": [
                "Accessibility Node Provider", "Accessibility Node Querying", "Accessibility Service", "Custom View"
            ],
            "Animation": [
                "Bouncing Balls", "Cloning", "Custom Evaluator", "Default Layout Animations", "Events",
                "Hide-Show Animations",
                "Layout Animations", "Loading", "Multiple Properties", "Reversing", "Seeking", "View Flip"
            ],
            "App": [
                "Action Bar", "Activity", "Alarm", "Alert Dialogs", "Device Admin", "Fragment", "Launcher Shortcuts",
                "Loader",
                "Menu", "Notification", "Search", "Service", "Text-To-Speech", "Voice Recognition"
            ],
            "Content": [
                "Assets", "Clipboard", "Packages", "Provider", "Resources", "Storage"
            ],
            "Graphics": [
                "AlphaBitmap", "AnimateDrawables", "Arcs", "BitmapDecode", "BitmapMesh", "BitmapPixels",
                "CameraPreview",
                "Clipping", "ColorFilters", "ColorMatrix", "Compass", "CreateBitmap", "Density", "Drawable",
                "FingerPaint"
            ],
            "Media": [
                "AudioFx", "MediaPlayer", "VideoView"
            ],
            "NFC": [
                "ForegroundDispatch", "ForegroundNdefPush", "TechFilter"
            ],
            "OS": [
                "Morse Code", "Rotation Vector", "Sensors", "SMS Messaging"
            ],
            "Preference": [
                "Preferences from XML", "Launching preferences", "Preference dependencies", "Default values",
                "Preferences from code",
                "Advanced preferences", "Fragment", "Header", "Switch"
            ],
            "Text": [
                "KeyEventText", "Linkify", "LogTextBox", "Marquee", "Unicode"
            ],
            "Views": [
                "Animation", "Auto Complete", "Buttons", "Chronometer", "Controls", "Custom", "Date Widgets",
                "Drag and Drop",
                "Expandable Lists", "Focus", "Gallery", "Grid", "Hover Events", "ImageButton"
            ]
        }

        for button in api_demos_buttons:
            try:
                # Wait for the main button to be clickable
                main_button = self.wait.until(
                    EC.element_to_be_clickable((By.ACCESSIBILITY_ID, button))
                )
                main_button.click()
                logging.info(f"Clicked on main button: {button}")

                # If the current button has sub-buttons, click through them
                if button in sub_buttons:
                    for sub_button in sub_buttons[button]:
                        try:
                            # Wait for the sub-button to be clickable
                            sub_element = self.wait.until(
                                EC.element_to_be_clickable((By.ACCESSIBILITY_ID, sub_button))
                            )
                            sub_element.click()
                            logging.info(f"Clicked on sub-button: {sub_button}")

                            # Perform any necessary checks or interactions within the sub-menu
                            # For example, verify that a specific element is present
                            # This part can be customized based on the app's behavior

                            # Navigate back after interacting with the sub-button
                            self.driver.back()
                            logging.info(f"Navigated back from sub-button: {sub_button}")

                        except Exception as e:
                            logging.warning(f"Failed to interact with sub-button '{sub_button}': {e}")
                            # Optionally, continue with other sub-buttons or decide to skip

                # Navigate back to the main menu after handling sub-buttons
                self.driver.back()
                logging.info(f"Navigated back from main button: {button}")

            except Exception as e:
                self.fail(f"Failed to interact with main button '{button}': {e}")

    @classmethod
    def tearDownClass(cls):
        """
        Quit the Appium driver after all tests have run.
        """
        try:
            cls.driver.quit()
            logging.info("Appium driver quit successfully.")
        except Exception as e:
            logging.error(f"Failed to quit Appium driver: {e}")

if __name__ == '__main__':
    unittest.main()
