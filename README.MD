## Pytest + Selenium + requests

Series of automatic test for some of the form and email funcionalities.

### Live version:




### To run it locally:

1) Clone the repo:

```git clone https://github.com/Marcin-Fraszczak/pytest-selenium-tests.git```

2) Inside the project directory create virtual environment:

```cd pytest-selenium-tests```

```python3 -m venv venv```

and activate it:

```source venv/bin/activate```

3) Install dependencies:

```pip install -r requirements.txt```

4) Run tess:

```pytest --html=report.html --self-contained-html```

5) It will run tests and create 'report.html' file.

6) Open 'report.html' file and choose ``Show all details`` link to see the documentation. 