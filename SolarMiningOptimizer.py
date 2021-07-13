####################
#####  IMPORTS  ####
####################
import os
import time
import atexit
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

####################
####  CONSTANTS  ###
####################
SMA_URL = "https://LOCAL_IP_OF_SMA_INVERTER/#/smartView"
NH_URL = "https://www.nicehash.com/my/mining/rigs"
# GPU-Constants
ASUS_GTX1080TI = 1
MSI_GTX1080TI = 2
ZOTAC_GTX1080 = 3
# Selenium-Constants
CHROME_USER_DATA_PATH = "C:\\Users\\USER\\AppData\\Local\\Google\\Chrome\\User Data"
# Adjustment-Constants
PROFITABILITY_THRESHHOLD_1 = 12  # EURO
PROFITABILITY_THRESHHOLD_2 = 20  # EURO
WATTAGE_THRESHHOLD = 1000  # WATT
CHECK_INTERVAL = 1000  # SEC
# GPU-PowerMode Constants
LITE = 0
MEDIUM = 1
HIGH = 2
EXTREME = 3
EFFICIENT = 4
EFFICIENT_LOW = 5
# PowerMode-Constants
ULTRA_LOW_POWER_MODE = 0
LOW_POWER_MODE = 1
EFFICIENCY_MODE = 2
HIGH_POWER_MODE = 3

###################
###  VARIABLES  ###
###################
seleniumDriver = None
currentPVPower = 0
currentProfitability = 0
asusGTX1080TiDeactivated = False
currentPowerMode = EFFICIENCY_MODE
newPowerMode = LOW_POWER_MODE

# WebDriver Options
optionsSMA = Options()
optionsNH = Options()
# SMA-Page
optionsSMA.add_argument("ignore-certificate-errors")
optionsSMA.add_argument("--disable-extensions")
optionsSMA.add_argument("--disable-gpu")
optionsSMA.add_argument("--log-level=3")
optionsSMA.add_argument("--headless")
# NiceHash-Page
optionsNH.add_argument("user-data-dir=" + CHROME_USER_DATA_PATH)
optionsNH.add_argument("--disable-extensions")
optionsNH.add_argument("--disable-gpu")
optionsNH.add_argument("--log-level=3")
optionsNH.add_argument("--headless")

####################
####  FUNCTIONS  ###
####################
def login():
    global seleniumDriver

    # Enter email
    email = seleniumDriver.find_element_by_css_selector(
        "#content > div > div.box > div > div > form > div:nth-child(1) > div > input"
    )
    email.click()
    email.clear()
    email.send_keys("EMAIL")

    # Enter password
    password = seleniumDriver.find_element_by_css_selector(
        "#content > div > div.box > div > div > form > div:nth-child(2) > div > input"
    )
    password.click()
    password.clear()
    password.send_keys("PASSWORD")

    # Click "Stay logged in" if not already selected
    if not (seleniumDriver.find_element_by_css_selector("#checkbox22").is_selected()):
        seleniumDriver.find_element_by_css_selector(
            "#content > div > div.box > div > div > form > div.mb24.checkbox > label"
        ).click()

    # Click "Login"
    seleniumDriver.find_element_by_css_selector(
        "#content > div > div.box > div > div > form > div.text-center.mb40 > div > button"
    ).click()

    # Wait for login to finish
    time.sleep(10)


# TODO: TEST
def getPVPower():
    # Get current PV-Power Output
    try:
        currentPower = int(
            seleniumDriver.find_element_by_css_selector(
                "#wrap > div:nth-child(3) > div > ui-view > div > ng-include > div > div:nth-child(1) > div.col-lg-4.col-md-5.col-sm-6.col-xs-12 > div > div > div:nth-child(3) > span"
            )
            .text.replace(" W", "")
            .replace(".", "")
        )
    except:
        print(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + ": No power or could not get power output from SMA-Inverter."
        )
        currentPower = 0
    # Print current PV-Power Output
    print(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + ": Solar-Power: "
        + str(currentPower)
        + " W"
    )


def expandMiningRIG():
    # Expand MiningRIG
    seleniumDriver.find_element_by_css_selector(
        "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div:nth-child(2)"
    ).click()

    # Wait for RIG to expand
    time.sleep(1)


def getProfitability():
    # Get current profitability
    currentProfitability = float(
        seleniumDriver.find_element_by_css_selector(
            "#content > div.container-full-whitex > div.container.status-header > div > div.col-md-3.col-sm-8.text-center > div > div.fiat"
        ).text.replace("≈ €", "")
    )
    # Print current profitability
    print(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + ": Current profitability: "
        + str(currentProfitability)
        + "€"
    )


# TODO: TEST
def changePowerModeOfGPU(indexGPU, powerMode):
    global seleniumDriver
    expandMiningRIG()

    if indexGPU == MSI_GTX1080TI:
        # Open Power-Modes for MSI GTX1080Ti
        seleniumDriver.find_element_by_css_selector(
            "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div:nth-child(2) > div > div.col.name"
        ).click()

        # Change PowerMode
        if powerMode == LITE:
            # Select "Light" Power-Mode for MSI GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(1) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(2)"
            ).click()
        elif powerMode == MEDIUM:
            # Select "Medium" Power-Mode for MSI GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(1) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(3)"
            ).click()
        elif powerMode == HIGH:
            # Select "High" Power-Mode for MSI GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(1) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(4)"
            ).click()
        elif powerMode == EXTREME:
            # Select "Extreme" Power-Mode for MSI GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(1) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(5)"
            ).click()
        elif powerMode == EFFICIENT:
            # Select "EfficientLow" Power-Mode for MSI GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(1) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(6)"
            ).click()
        elif powerMode == EFFICIENT_LOW:
            # Select "EfficientLow" Power-Mode for MSI GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(1) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(7)"
            ).click()

    elif indexGPU == ASUS_GTX1080TI:
        # Open Power-Modes for ASUS GTX1080Ti
        seleniumDriver.find_element_by_css_selector(
            "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.field"
        ).click()

        # Change PowerMode
        if powerMode == LITE:
            # Select "Light" Power-Mode for ASUS GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(2)"
            ).click()
        elif powerMode == MEDIUM:
            # Select "Medium" Power-Mode for ASUS GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(3)"
            ).click()
        elif powerMode == HIGH:
            # Select "High" Power-Mode for ASUS GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(4)"
            ).click()
        elif powerMode == EXTREME:
            # Select "Extreme" Power-Mode for ASUS GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(5)"
            ).click()
        elif powerMode == EFFICIENT:
            # Select "EfficientLow" Power-Mode for ASUS GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(6)"
            ).click()
        elif powerMode == EFFICIENT_LOW:
            # Select "EfficientLow" Power-Mode for ASUS GTX1080Ti
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(7)"
            ).click()

    elif indexGPU == ZOTAC_GTX1080:
        # Open Power-Modes for ZOTAC GTX1080
        seleniumDriver.find_element_by_css_selector(
            "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(3) > div > div.col.controls.text-right > div > div.field"
        ).click()

        # Change PowerMode
        if powerMode == LITE:
            # Select "Light" Power-Mode for ZOTAC GTX1080
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(3) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(2)"
            ).click()
        elif powerMode == MEDIUM:
            # Select "Medium" Power-Mode for ZOTAC GTX1080
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(3) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(3)"
            ).click()
        elif powerMode == HIGH:
            # Select "High" Power-Mode for ZOTAC GTX1080
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(3) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(4)"
            ).click()
        elif powerMode == EFFICIENT:
            # Select "Efficient" Power-Mode for ZOTAC GTX1080
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(3) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(5)"
            ).click()
        elif powerMode == EFFICIENT_LOW:
            # Select "EfficientLow" Power-Mode for ZOTAC GTX1080
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(3) > div > div.col.controls.text-right > div > div.dropdown.flex.flex--no-wrap > div > div:nth-child(6)"
            ).click()

    # Wait for Power-Modes to change
    time.sleep(2)


def switchASUSGTX1080TI():
    global seleniumDriver

    if isASUSGTX1080TIActivated():
        print(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + ": Deactivating ASUS GTX1080Ti"
        )
    else:
        print(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Activating ASUS GTX1080Ti"
        )

    # Switch ASUS GTX1080Ti
    seleniumDriver.find_element_by_css_selector(
        "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div > div.col.controls.text-right > label > span"
    ).click()

    # Wait for GPU to turn on/off
    time.sleep(5)


def isASUSGTX1080TIActivated():
    global seleniumDriver

    if "disabled" in seleniumDriver.find_element_by_css_selector(
        "#content > div.container-full-whitex > div:nth-child(5) > div > div > div.rigs.list-view > div.show-devices > div:nth-child(2) > div"
    ).get_attribute("class"):
        return False

    return True


def exit_handler():
    seleniumDriver.quit()
    print(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": SolarMiningOptimizer stoped"
    )


####################
#### MAIN SCRIPT ###
####################
# Close all browser windows and ends driver's process gracefully if script gets interrupted
atexit.register(exit_handler)
# Clear console in startup
os.system("cls")
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": SolarMiningOptimizer started")
while True:
    try:
        # Start Selenium-Driver for SMA
        seleniumDriver = webdriver.Chrome(options=optionsSMA)
        seleniumDriver.get(SMA_URL)
        time.sleep(5)

        # Get current PV-Power Output
        getPVPower()

        # Quit Selenium-Driver for SMA
        seleniumDriver.quit()

        # Start Selenium-Driver for NiceHash
        seleniumDriver = webdriver.Chrome(options=optionsNH)
        seleniumDriver.get(NH_URL)
        time.sleep(5)

        # Check if RIG-Manager is loaded or if a login is needed
        try:
            seleniumDriver.find_element_by_css_selector(
                "#content > div.container-full-whitex > div.container.bottom-shadow > div > div > div.path"
            )
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Still logged in")
        except NoSuchElementException:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Login needed")
            login()

        # Get current profitability
        getProfitability()

        # Save previous Power-Mode
        currentPowerMode = newPowerMode

        # Calculate new Power-Mode
        if currentPVPower >= WATTAGE_THRESHHOLD:
            newPowerMode = HIGH_POWER_MODE

        elif currentPVPower < WATTAGE_THRESHHOLD:
            if currentProfitability < PROFITABILITY_THRESHHOLD_1:
                newPowerMode = ULTRA_LOW_POWER_MODE
            elif currentProfitability < PROFITABILITY_THRESHHOLD_2:
                newPowerMode = LOW_POWER_MODE
            elif currentProfitability >= PROFITABILITY_THRESHHOLD_2:
                newPowerMode = EFFICIENCY_MODE

        # Change Power-Modes
        if currentPowerMode != newPowerMode:
            # Ultra-Low-Power-Mode
            if newPowerMode == ULTRA_LOW_POWER_MODE:
                print(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    + ": Switching to Ultra-Low-Power-Mode"
                )

                # Select "EfficientLow" Power-Mode
                changePowerModeOfGPU(MSI_GTX1080TI, EFFICIENT_LOW)

                # Deactivate ASUS GTX1080Ti
                switchASUSGTX1080TI(False)

                # Select "EfficientLow" Power-Mode
                changePowerModeOfGPU(ZOTAC_GTX1080, EFFICIENT_LOW)

            # Low-Power-Mode
            elif newPowerMode == LOW_POWER_MODE:
                print(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    + ": Switching to Low-Power-Mode"
                )

                # Select "EfficientLow" Power-Mode for MSI GTX1080Ti
                changePowerModeOfGPU(MSI_GTX1080TI, EFFICIENT_LOW)

                # Select "EfficientLow" Power-Mode for ASUS GTX1080Ti
                changePowerModeOfGPU(ASUS_GTX1080TI, EFFICIENT_LOW)

                # Select "EfficientLow" Power-Mode for ZOTAC GTX1080
                changePowerModeOfGPU(ZOTAC_GTX1080, EFFICIENT_LOW)

            # Efficiency-Mode
            elif newPowerMode == EFFICIENCY_MODE:
                print(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    + ": Switching to Efficiency-Mode"
                )

                # Select "Efficient" Power-Mode for MSI GTX1080Ti
                changePowerModeOfGPU(MSI_GTX1080TI, EFFICIENT)

                # Select "Efficient" Power-Mode for ASUS GTX1080Ti
                changePowerModeOfGPU(ASUS_GTX1080TI, EFFICIENT)

                # Select "Efficient" Power-Mode for ZOTAC GTX1080
                changePowerModeOfGPU(ZOTAC_GTX1080, EFFICIENT)

            # High-Power-Mode
            elif newPowerMode == HIGH_POWER_MODE:
                print(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    + ": Switching to High-Power-Mode"
                )

                # Select "High" Power-Mode for MSI GTX1080Ti
                changePowerModeOfGPU(MSI_GTX1080TI, HIGH)

                # Select "Efficient" Power-Mode for ASUS GTX1080Ti
                changePowerModeOfGPU(ASUS_GTX1080TI, EFFICIENT)

                # Select "High" Power-Mode for ZOTAC GTX1080
                changePowerModeOfGPU(ZOTAC_GTX1080, HIGH)

        # No Power-Mode change
        else:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": No Change")

        # Wait for changes to take effect
        time.sleep(3)
        seleniumDriver.quit()

        time.sleep(CHECK_INTERVAL)

    # Error-Handling
    except Exception as exception:
        print(exception)
        try:
            seleniumDriver.quit()
        except Exception as driverException:
            print(exception)
            print(driverException)

        time.sleep(CHECK_INTERVAL)
