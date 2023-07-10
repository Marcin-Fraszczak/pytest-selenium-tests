from django.shortcuts import render
from django.views import View


class HomeView(View):
	def get(self, request):
		return render(request, "reports/home.html")


class ReportView(View):
	def get(self, request):
		import subprocess
		if 'task1' in request.GET:
			command = "pytest test_task_1.py --html=templates/tests/report.html --self-contained-html"
		elif 'task21' in request.GET:
			command = "pytest test_task_2.py::test_user_receives_email_when_subscribed --html=templates/tests/report.html --self-contained-html"
		elif 'task22' in request.GET:
			command = "pytest test_task_2.py::test_user_receives_email_when_assigned_to_default_group --html=templates/tests/report.html --self-contained-html"
		elif 'task23' in request.GET:
			command = "pytest test_task_2.py::test_user_without_group_or_subscription_not_receiving_email --html=templates/tests/report.html --self-contained-html"
		else:
			command = ""
		if command:
			subprocess.run(command.split(" "))

		return render(request, "tests/report.html")
