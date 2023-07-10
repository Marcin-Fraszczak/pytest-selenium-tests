from django.shortcuts import render
from django.views import View


class HomeView(View):
	def get(self, request):
		return render(request, "reports/home.html")


class ReportView(View):
	def get(self, request):
		import subprocess
		command = "pytest --html=templates/tests/report.html --self-contained-html"
		subprocess.run(command.split(" "))

		return render(request, "tests/report.html")
