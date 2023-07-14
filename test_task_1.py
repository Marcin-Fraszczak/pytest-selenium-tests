import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import shuffle

"""
	Run command:
		pytest --html=report.html --self-contained-html
		pytest --html=templates/tests/report.html --self-contained-html
"""


# @pytest.mark.skip(reason="working well")
def test_form_exists_and_is_functional_at_correct_location(driver, base_url, loc):
	help_text = f"""
		Tests if the correct and functional form is rendered at endpoint: '{base_url}'. Steps:
	"""
	print(help_text)

	driver.get(base_url)

	form_el = driver.find_element(By.ID, loc['form_id'])
	assert form_el
	print(f"OK: form with id: '{loc['form_id']}' exists")

	input_el = WebDriverWait(driver, 5).until(
		EC.element_to_be_clickable((By.ID, loc['input_id']))
	)
	assert input_el
	print(f"OK: input field with id: '{loc['input_id']}' exists and is clickable")

	results_el = driver.find_element(By.ID, loc['result_id'])
	assert results_el
	print(f"OK: results output with id: '{loc['result_id']}' exists")

	buttons_el = form_el.find_elements(By.TAG_NAME, "button")
	submit_buttons = [button for button in buttons_el if button.get_attribute('type') == "submit"]
	assert len(submit_buttons) > 0
	submit_buttons[0].click()
	print(f"OK: submit button is present and clickable")
	driver.quit()


# @pytest.mark.skip(reason="working well")
def test_warning_displayed_for_request_with_no_input(driver, base_url, loc, msgs):
	help_text = f"""
			Tests if warnings are displayed when form is submitted with no data at: '{base_url}'. Steps:
		"""
	print(help_text)

	driver.get(base_url)

	form_el = driver.find_element(By.ID, loc['form_id'])
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
	assert msgs['no_input'] in alert_el.get_attribute('innerHTML')
	print(f"OK: '{msgs['no_input']}' is displayed inside the alert block")
	field_error = driver.find_element(By.CLASS_NAME, "invalid-feedback")
	assert field_error
	print(f"OK: field error is displayed")
	assert msgs['required'] in field_error.get_attribute("innerHTML")
	print(f"OK: '{msgs['required']}' is displayed")
	driver.quit()


# @pytest.mark.skip(reason="working well")
def test_warning_displayed_for_incorrect_datatype_posted(driver, base_url, loc, msgs):
	help_text = f"""
		Tests if warning is displayed when improper data type is passed into a form
		at location: '{base_url}'. Passing string (non digit), digit-character mix, digits with special signs.
	"""
	print(help_text)

	driver.get(base_url)

	incorrect_data = ["a", "Ala ma kota 34", '!54 $ 2', ]
	for data in incorrect_data:
		form_el = driver.find_element(By.ID, loc['form_id'])
		input_el = WebDriverWait(driver, 5).until(
			EC.element_to_be_clickable((By.ID, loc['input_id']))
		)
		input_el.clear()
		input_el.send_keys(data)
		form_el.submit()
		alert_el = driver.find_element(By.CLASS_NAME, "alert")
		assert msgs['invalid_input'] in alert_el.get_attribute('innerHTML')
		print(f"OK: '{msgs['invalid_input']}' alert is displayed inside the alert block for: '{data}'")
		driver.quit()


# @pytest.mark.skip(reason="working well")
def test_correct_result_is_returned(driver, base_url, loc, msgs):
	def shuffler(limit):
		result = [str(x) for x in range(limit)]
		shuffle(result)
		return result

	test_data = {
		"1": "1",
		"3 2 1": "1 2 3",
		"9 -2 2000": "-2 9 2000",
		"2.3 0.0001 -40": "-40 0.0001 2.3",
		"+2.3 -1 1_4": "-1 2.3 14",
		" ".join(shuffler(100)): " ".join((str(x) for x in range(100))),
	}

	help_text = f"""
			Tests if correct results are returned when sending correct data
			at location: '{base_url}'. Input data is:
			{list(test_data.keys())[:-1]} and a 100 elements shuffled list.
		"""
	print(help_text)

	driver.get(base_url)

	for data in test_data:
		form_el = driver.find_element(By.ID, loc['form_id'])
		input_el = WebDriverWait(driver, 5).until(
			EC.element_to_be_clickable((By.ID, loc['input_id']))
		)
		input_el.clear()
		input_el.send_keys(data)
		form_el.submit()
		result_el = driver.find_element(By.ID, loc['result_id'])
		assert result_el.get_attribute("value") == test_data[data]
		if len(data) > 100:
			print(f"OK: correct result returned for large input data")
		else:
			print(f"OK: correct result returned for {data}")
	driver.quit()