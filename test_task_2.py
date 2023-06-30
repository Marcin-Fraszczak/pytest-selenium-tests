import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pickle

"""
	Run command:
		pytest --html=report.html --self-contained-html
"""


# @pytest.mark.skip(reason="working well")
def test_user_receives_email_when_subscribed(driver, mail_url, base_url, loc):
	help_text = f"""
		Tests if user outside of specified groups doesn't receive email.
	"""
	print(help_text)

	driver.get(mail_url)
	driver.maximize_window()

	delete_account = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/a[1]")
	delete_account.click()

	account_name_el = driver.find_element(By.XPATH, '//*[@id="email"]')
	account_name = account_name_el.get_attribute('innerText')
	# saving cookies
	pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
	# session_id = driver.session_id
	print(f"OK: email account '{account_name}' created")

	driver.get(f"{base_url}users/register/")

	username_input = driver.find_element(By.XPATH, '//*[@id="id_username"]')
	password_input = driver.find_element(By.XPATH, '//*[@id="id_password"]')
	group_select_element = Select(driver.find_element(By.XPATH, '//*[@id="id_group"]'))
	register_button = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/div/form/button')

	username_input.send_keys(account_name)
	password_input.send_keys("Testpass123#")
	group_select_element.select_by_visible_text("No group")
	register_button.click()
	print(f"OK: user with username '{account_name}' and created via register form")

	subscribe_button = WebDriverWait(driver, 5).until(
	EC.element_to_be_clickable((By.XPATH, '//*[@id="subscribe_form"]/div/button'))
	)
	subscribe_button.click()

	driver.get(f"{base_url}users/ideas/")
	title_input = driver.find_element(By.XPATH, '//*[@id="id_title"]')
	content_input = driver.find_element(By.XPATH, '//*[@id="id_content"]')
	submit_button = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/div/form/button')
	title_input.send_keys(f"{account_name} own idea")
	content_input.send_keys("content")
	submit_button.click()
	print(f"OK: new idea created by '{account_name}'")

	driver.get(mail_url)
	# loading back cookies
	cookies = pickle.load(open("cookies.pkl", "rb"))
	for cookie in cookies:
		driver.add_cookie(cookie)
	# driver.session_id = session_id

	# removing possible adds
	try:
		ad_cancel = WebDriverWait(driver, 3).until(
			EC.element_to_be_clickable((By.XPATH, '//*[@id="dismiss-button"]'))
		)
		ad_cancel = driver.find_element(By.XPATH, '//*[@id="dismiss-button"]')
		ad_cancel.click()
	except TimeoutException:
		pass


	refresh_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/a[5]')
	refresh_button.click()

	mailbox = driver.find_element(By.XPATH, '//*[@id="schranka"]')

	# assert "New Idea number" in mailbox.get_attribute('innerHTML')
	# assert "fraszczak.programming@gmail.com" in mailbox.get_attribute('innerHTML')
	# print(f"OK: mail successfully sent and received")
	print(f"ERROR: MinuteInbox page reload deletes test account")


# @pytest.mark.skip(reason="working well")
def test_user_receives_email_when_assigned_to_a_particular_group(driver, mail_url, base_url, loc):
	groups = ['H/Div', 'H/Sec']
	help_text = f"""
		Tests if emails are sent to correct users based on group assignment. Default groups to receive emails: {groups}.
	"""
	print(help_text)

	for group in groups:
		driver.get(mail_url)
		driver.maximize_window()

		delete_account = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/a[1]")
		delete_account.click()

		account_name_el = driver.find_element(By.XPATH, '//*[@id="email"]')
		account_name = account_name_el.get_attribute('innerText')
		# saving cookies
		pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
		# session_id = driver.session_id
		print(f"OK: email account '{account_name}' created")

		driver.get(f"{base_url}users/register/")

		username_input = driver.find_element(By.XPATH, '//*[@id="id_username"]')
		password_input = driver.find_element(By.XPATH, '//*[@id="id_password"]')
		group_select_element = Select(driver.find_element(By.XPATH, '//*[@id="id_group"]'))
		register_button = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/div/form/button')

		username_input.send_keys(account_name)
		password_input.send_keys("Testpass123#")
		group_select_element.select_by_visible_text(group)
		register_button.click()
		print(f"OK: user with username '{account_name}' and created via register form")

		driver.get(f"{base_url}users/ideas/")
		title_input = driver.find_element(By.XPATH, '//*[@id="id_title"]')
		content_input = driver.find_element(By.XPATH, '//*[@id="id_content"]')
		submit_button = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/div/form/button')
		title_input.send_keys(f"{account_name} own idea")
		content_input.send_keys("content")
		submit_button.click()
		print(f"OK: new idea created by '{account_name}'")

		driver.get(mail_url)
		# loading back cookies
		cookies = pickle.load(open("cookies.pkl", "rb"))
		for cookie in cookies:
			driver.add_cookie(cookie)
		# driver.session_id = session_id

		# removing possible adds
		try:
			ad_cancel = WebDriverWait(driver, 3).until(
				EC.element_to_be_clickable((By.XPATH, '//*[@id="dismiss-button"]'))
			)
			ad_cancel = driver.find_element(By.XPATH, '//*[@id="dismiss-button"]')
			ad_cancel.click()
		except TimeoutException:
			pass


		refresh_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/a[5]')
		refresh_button.click()

		mailbox = driver.find_element(By.XPATH, '//*[@id="schranka"]')

		# assert "New Idea number" in mailbox.get_attribute('innerHTML')
		# assert "fraszczak.programming@gmail.com" in mailbox.get_attribute('innerHTML')
		# print(f"OK: mail successfully sent and received")
		print(f"ERROR: MinuteInbox page reload deletes test account")
