from django.shortcuts import render, redirect
from django.views import View
import os


class HomeView(View):
	def get(self, request):
		return render(request, "reports/home.html")


class ReportView(View):
	def get(self, request):
		import subprocess
		from django.core.cache import cache

		# deletes old report.html file, if it exists
		path_to_report = os.path.join(os.getcwd(), 'templates', 'tests', 'report.html')
		if os.path.exists(path_to_report):
			os.remove(path_to_report)
		cache.clear()

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

		return redirect("reports:result")


class ResultView(View):
	def get(self, request):
		return render(request, "tests/test_results.html")
