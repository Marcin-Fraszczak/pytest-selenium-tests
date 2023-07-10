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
		elif 'task2' in request.GET:
			command = "pytest test_task_2.py --html=templates/tests/report.html --self-contained-html"
		else:
			command = ""
		if command:
			subprocess.run(command.split(" "))

		return render(request, "tests/report.html")
