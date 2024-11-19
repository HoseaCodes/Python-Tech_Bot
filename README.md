## Envirnoment

Suggested setup

- [Virtual Env - venv](https://docs.python.org/3/library/venv.html)

  - Create virtual environment folder

  ```bash
  python3 -m venv venv
  ```

  - Activate VENV

  ```bash
  source venv/bin/activate
  ```

  - Install packages

  ```bash
  pip freeze > requirements.txt

  pip install -r requirements.txt
  ```

  - Check Packages

  ```bash
  pip list --local
  ```

  - Deactivate VENV

  ```bash
  deactivate
  ```

  Want to run locally checkout the [Requirements file](requirements.txt)

### Release History

- 0.0.1
  - Work in progress

### Contributing

Review how here [contribution](CONTRIBUTION.md)

### Python Packages

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://docs.python-requests.org/en/master/)
