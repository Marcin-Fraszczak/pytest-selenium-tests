import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
	Run command:
		pytest --html=report.html --self-contained-html
"""


def pytest_html_report_title(report):
	report.title = "Test report task_1 and task_2 of BitByBit recruitment process - Selenium version."


@pytest.fixture
def base_url():
	return 'https://marcinfraszczak3.eu.pythonanywhere.com/'


@pytest.fixture
def mail_url():
	return 'https://www.minuteinbox.com/'


@pytest.fixture
def driver():
	driver = webdriver.Chrome()
	driver.implicitly_wait(4)
	return driver


@pytest.fixture
def driver2():
	return webdriver.Chrome()


@pytest.fixture
def s_driver():
	options = Options()
	options.add_experimental_option("detach", True)
	s_driver = webdriver.Chrome(options=options)
	return s_driver


@pytest.fixture
def loc():
	return {
		'form_id': 'numbers_sorting_form',
		'input_id': 'numbers_sorting_input',
		'result_id': 'out-data',

	}


@pytest.fixture
def msgs():
	return {
		'no_input': 'No input!',
		'invalid_input': 'Invalid input!',
		'required': 'This field is required.',

	}
