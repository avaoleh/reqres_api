import os
import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
from framework.demoqa_with_env import DemoQaWithEnv

load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="prod")


@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def demoshop(env):
    return DemoQaWithEnv(env)


@pytest.fixture(scope='session')
def reqres(env):
    return DemoQaWithEnv(env).reqres


@pytest.fixture(scope="session")
def get_cookie(demoshop):
    response = demoshop.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    auth_cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    return auth_cookie


@pytest.fixture(scope="function")
def browser_auth(demoshop, get_cookie):
    browser.config.base_url = demoshop.demoqa.url

    browser.open("Themes/DefaultClean/Content/images/star-x-active.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": get_cookie})

    yield browser
    browser.quit()
