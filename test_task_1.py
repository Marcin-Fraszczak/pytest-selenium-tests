from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from time import sleep

"""
	Run command:
		pytest --html=report.html --self-contained-html
"""


@pytest.mark.skip(reason="working well")
def test_form_exists_and_is_functional_at_correct_location(driver, base_url, form_id, input_id, result_id):
	help_text = f"""
		Tests if the correct and functional form is rendered at endpoint: '{base_url}'. Steps:
	"""
	print(help_text)

	driver.get(base_url)
	driver.maximize_window()

	form_el = driver.find_element(By.ID, form_id)
	assert form_el
	print(f"OK: form with id: '{form_id}' exists")

	input_el = WebDriverWait(driver, 5).until(
		EC.element_to_be_clickable((By.ID, input_id))
	)
	assert input_el
	print(f"OK: input field with id: '{input_id}' exists and is clickable")

	results_el = driver.find_element(By.ID, result_id)
	assert results_el
	print(f"OK: results output with id: '{result_id}' exists")

	buttons_el = form_el.find_elements(By.TAG_NAME, "button")
	submit_buttons = [button for button in buttons_el if button.get_attribute('type') == "submit"]
	assert len(submit_buttons) > 0
	submit_buttons[0].click()
	print(f"OK: submit button is present and clickable")


@pytest.mark.skip(reason="working well")
def test_warning_displayed_for_request_with_no_input(driver, base_url, form_id, error_msg, field_msg):
	help_text = f"""
			Tests if warnings are displayed when form is submitted with no data at: '{base_url}'. Steps:
		"""
	print(help_text)

	driver.get(base_url)
	driver.maximize_window()

	form_el = driver.find_element(By.ID, form_id)
	# Easier version, but not testing the button:
	# form_el.submit()
	form_buttons = form_el.find_elements(By.TAG_NAME, "button")
	for button in form_buttons:
		if button.get_attribute("type") == "submit":
			button.click()
			break

	alert_el = driver.find_element(By.CLASS_NAME, "alert")
	assert alert_el
	print(f"OK: alert is showing")
	assert error_msg in alert_el.get_attribute('innerHTML')
	print(f"OK: {error_msg} is displayed inside the alert block")
	field_error = driver.find_element(By.CLASS_NAME, "invalid-feedback")
	assert field_error
	print(f"OK: field error is displayed")
	assert field_msg in field_error.get_attribute("innerHTML")
	print(f"OK: '{field_msg}' is displayed")



def test_warning_displayed_for_incorrect_datatype_posted(driver, base_url, form_id, input_id, error_msg):
	help_text = f"""
		Tests if warning is displayed when improper data type is passed into a form
		at location: '{base_url}'. Passing string (non digit), digit-character mix, functions (built-ins and custom).
	"""
	print(help_text)

	def func():
		pass

	"""Note, that algorithm will work for collections with digits, but will only consider
	first (dictionaries) or last value from collection (list, tuples, sets).
	Problem is in a way that form-data is sent, not in a algorithm itself."""
	incorrect_data = ["a", "Ala ma kota 34", int, func]

	driver.get(base_url)
	driver.maximize_window()
	form_el = driver.find_element(By.ID, form_id)

	for data in incorrect_data:
		input_el = WebDriverWait(driver, 5).until(
			EC.element_to_be_clickable((By.ID, input_id))
		)
		input_el.send_keys(data)
		sleep(2)
		form_el.submit()
