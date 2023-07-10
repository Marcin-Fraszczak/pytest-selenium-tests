import pytest
import requests
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
from datetime import datetime
from os import getenv
from sys import exit
from time import sleep
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
	Run command:
		pytest --html=report.html --self-contained-html
		pytest --html=templates/tests/report.html --self-contained-html
"""

load_dotenv()
mailosaur_api_key = getenv('MAILOSAUR_API_KEY')
mailosaur_server = getenv('MAILOSAUR_SERVER')
mailosaur_domain = getenv('MAILOSAUR_DOMAIN')
mailosaur_url = getenv('MAILOSAUR_URL')

if not any([mailosaur_url, mailosaur_domain, mailosaur_server, mailosaur_api_key]):
	print("Env variables not available!")
	exit(1)
else:
	auth = HTTPBasicAuth(mailosaur_api_key, "")


def delete_mailosaur_messages():
	"""Calls mailosaur API to delete all emails on a specified server.
	 If successful, should return '204'. Else return 'None'."""
	for i in range(3):
		try:
			response = requests.delete(f"{mailosaur_url}/api/messages?server={mailosaur_server}", auth=auth)
			return response.status_code
		except RequestException:
			sleep(0.5)


def list_mailosaur_messages():
	"""Calls mailosaur API for the list of all emails stored on a specified server.
	 Returns None in case of any problems, if succeeded, returns list of dictionaries
	 with emails data."""
	for i in range(3):
		try:
			response = requests.get(f"{mailosaur_url}/api/messages?server={mailosaur_server}", auth=auth)
			if response.status_code == 200:
				return response.json()['items']
		except RequestException:
			sleep(0.5)


def get_username():
	"""Returns email address based on current time.
	 Returned email address is unique every millisecond."""
	return f"{int(datetime.now().timestamp() * 1000)}@{mailosaur_domain}"


def register_user(driver, base_url, account_name, group='No group'):
	"""Registers new user using form."""
	driver.get(f"{base_url}users/register/")

	username_input = driver.find_element(By.ID, 'id_username')
	password_input = driver.find_element(By.ID, 'id_password')
	group_select_element = Select(driver.find_element(By.ID, 'id_group'))
	register_button = driver.find_element(By.XPATH, '// *[ @ id = "registration_form"] / button')

	username_input.send_keys(account_name)
	password_input.send_keys("Testpass123#")
	group_select_element.select_by_visible_text(group)
	register_button.click()
	print(f"OK: user with username '{account_name}' created via register form")


def remove_alerts(driver):
	"""Removes any alerts that can interfere with Selenium clicking."""
	alerts = driver.find_elements(By.CLASS_NAME, 'btn-close')
	if alerts:
		for alert in alerts:
			alert.click()
		sleep(1)


def subscribe_user(driver, account_name):
	"""Changes user 'subscribed' status to 'True' by clicking button on the profile panel."""
	remove_alerts(driver)
	subscribe_button = WebDriverWait(driver, 2).until(
		EC.element_to_be_clickable((By.XPATH, '//*[@id="subscribe_form"]/button'))
	)
	subscribe_button.click()
	print(f"OK: user '{account_name}' subscribed")


def create_idea(driver, base_url, account_name):
	"""Creates new 'Idea' object using the form."""
	idea_title = f"{account_name} own idea"

	driver.get(f"{base_url}users/ideas/")
	title_input = driver.find_element(By.ID, 'id_title')
	content_input = driver.find_element(By.ID, 'id_content')
	submit_button = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/form/button')
	title_input.send_keys(idea_title)
	content_input.send_keys("content")
	submit_button.click()
	print(f"OK: new idea submitted by '{account_name}'")

	ideas_list = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/ul')
	if idea_title in ideas_list.get_attribute('innerHTML'):
		print(f"OK: new idea added to the database")


def login_user(driver, base_url, account_name):
	"""Logs in an existing user via login form."""
	driver.get(f"{base_url}users/login/")
	username_input = driver.find_element(By.ID, 'id_username')
	password_input = driver.find_element(By.ID, 'id_password')
	login_button = driver.find_element(By.XPATH, '// *[ @ id = "login_form"] / button')
	username_input.send_keys(account_name)
	password_input.send_keys("Testpass123#")
	login_button.click()


def delete_user(driver, base_url, account_name=None):
	"""After the test, user account is deleted from the database
	either by submitting the form or using 'requests' library."""
	if account_name:
		login_user(driver, base_url, account_name)
	driver.get(f"{base_url}users/profile/")
	delete_button = driver.find_element(By.NAME, 'delete_account')
	delete_button.click()


# @pytest.mark.skip(reason="working well")
def test_user_receives_email_when_subscribed(driver, base_url):
	help_text = f"""
		User not belonging to default group, can still subscribe and receive emails.
	"""
	print(help_text)

	account_name = get_username()
	register_user(driver, base_url, account_name)
	subscribe_user(driver, account_name)
	delete_mailosaur_messages()
	create_idea(driver, base_url, account_name)
	delete_user(driver, base_url)

	current, limit, result = 0, 5, False
	while current < limit:
		mailbox = list_mailosaur_messages()
		if mailbox:
			recipients_list = list(map(lambda item: [to['email'] for to in item['to']], mailbox))
			result = any([1 for item in recipients_list if account_name in item])
			if result:
				print(f"OK: email received")
				break
			else:
				sleep(1)
				current += 1
		else:
			sleep(2)
			current += 1
	if current == limit:
		print(f"ERROR: email not received within allowed timeout")
	delete_mailosaur_messages()
	assert result


def test_user_receives_email_when_assigned_to_default_group(driver, base_url):
	default_groups = ["H/Div", "H/Sec"]
	help_text = f"""
		User belonging to default group receives emails.
		Default groups are: {default_groups}.
	"""
	print(help_text)

	for group in default_groups:
		account_name = get_username()
		register_user(driver, base_url, account_name, group=group)
		delete_mailosaur_messages()
		create_idea(driver, base_url, account_name)
		delete_user(driver, base_url)

		current, limit, result = 0, 5, False
		while current < limit:
			mailbox = list_mailosaur_messages()
			if mailbox:
				recipients_list = list(map(lambda item: [to['email'] for to in item['to']], mailbox))
				result = any([1 for item in recipients_list if account_name in item])
				if result:
					print(f"OK: email received")
					break
				else:
					sleep(1)
					current += 1
			else:
				sleep(2)
				current += 1
		if current == limit:
			print(f"ERROR: email not received within allowed timeout")
		delete_mailosaur_messages()
		assert result


def test_user_without_group_or_subscription_not_receiving_email(driver, base_url):
	help_text = f"""
		User that does not belong to default group and is not subscribed,
		does not receive email, even when he is an idea author. 
	"""
	print(help_text)

	# creating subscribed user to have email sent
	sub_name = get_username()
	register_user(driver, base_url, sub_name)
	subscribe_user(driver, sub_name)

	# creating unsubscribed user
	unsub_name = get_username()
	register_user(driver, base_url, unsub_name)
	delete_mailosaur_messages()
	create_idea(driver, base_url, unsub_name)

	# deleting both users
	delete_user(driver, base_url)
	sleep(1)
	delete_user(driver, base_url, account_name=sub_name)

	current, limit, present, not_present = 0, 5, False, True
	while current < limit:
		mailbox = list_mailosaur_messages()
		if mailbox:
			recipients_list = list(map(lambda item: [to['email'] for to in item['to']], mailbox))
			present = any([1 for item in recipients_list if sub_name in item])
			if present:
				print(f"OK: email received")
				not_present = any([1 for item in recipients_list if unsub_name in item])
				break
			else:
				sleep(1)
				current += 1
		else:
			sleep(2)
			current += 1
	if current == limit:
		print(f"ERROR: email not received within allowed timeout")
	delete_mailosaur_messages()
	assert present
	assert not not_present
