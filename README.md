# App Repo
This repository is coupled with the following repository for the front-end: https://github.com/CS411-Calendar/App

# Installation

Setup postgresql and .env vars

```
pip3 install -r requirements.txt
```

# Quickstart

```python
python3 app.py
```

# Database migration folder commands

Init migration folder

```
flask db init
```

Create migration

```
flask db migrate -m "Initial migration."
```

Commit migration

```
flask db upgrade
```
