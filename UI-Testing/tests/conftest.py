import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from src.utils.BrowserActions import BrowserActions
from src.config.ConfigEnv import ConfigEnv
from selenium.webdriver.chrome.options import Options

@pytest.hookimpl(hookwrapper=True)
def pytest_exception_interact(node, call, report):
    try:
        driver = searchWebDriver(node)

        if not driver:
           yield

        allure.attach(driver.get_screenshot_as_png(), name="Fail-Screenshot", attachment_type=allure.attachment_type.PNG)
        yield
    except:
        print("Screenshot For Allure Failed")
        yield

def searchWebDriver(node):
    web_driver = None
    web_driver = node.funcargs['webDriver']
    return web_driver

def pytest_addoption(parser):
    parser.addoption("--env", 
        action="store",
        default="dev",
        choices=("dev", "qa"),
        help ="Define environment to execute test")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def environment_config(env):
    return ConfigEnv(env)

@pytest.fixture()
def webDriver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def browserActions(webDriver, environment_config):
    browserActions = BrowserActions(webDriver, environment_config.baseurl)
    return browserActions

