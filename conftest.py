import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    """Sets up ability to add different options (browser, language)"""
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default="en",
                     help="Choose from languages: en, ru, etc.")


@pytest.fixture(scope="function")
def browser(request):
    """Runs before and after each test. Sets up and quits browser"""
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    browser = None
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        # allow using different languages, e.g. --language=fr
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        # declare and initialize driver variable
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        # allow using different languages, e.g. --language=fr
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', user_language)
        # declare and initialize driver variable
        browser = webdriver.Firefox(firefox_profile=profile)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser

    print("\nquit browser..")
    browser.quit()
