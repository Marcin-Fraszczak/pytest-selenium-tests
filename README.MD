## Pytest + Selenium

Series of automatic test for some of the form and email funcionalities.

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

5) It will create 'report.html' file, with 'Show all details' link to documentation. 