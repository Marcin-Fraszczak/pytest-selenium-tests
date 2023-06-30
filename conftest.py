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
	base_url = 'https://marcinfraszczak3.eu.pythonanywhere.com/'
	return base_url


@pytest.fixture
def driver():
	driver = webdriver.Chrome()
	return driver


@pytest.fixture
def s_driver():
	options = Options()
	options.add_experimental_option("detach", True)
	s_driver = webdriver.Chrome(options=options)
	return s_driver


@pytest.fixture
def form_id():
	form_id = 'numbers_sorting_form'
	return form_id


@pytest.fixture
def input_id():
	input_id = 'numbers_sorting_input'
	return input_id


@pytest.fixture
def result_id():
	result_id = 'out-data'
	return result_id

@pytest.fixture
def error_msg():
	error_msg = 'No input!'
	return error_msg


@pytest.fixture
def field_msg():
	field_msg = 'This field is required'
	return field_msg