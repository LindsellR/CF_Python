
# Python Practice Projects

This repository contains Python deliverables completed as part of the CareerFoundry python specialisation course. 
These exercises cover the basics of Python including syntax, virtual environments, packages, and user input.

## Getting Started

### Prerequisites

- Python 3.13.5 
- `pip` package manager
- `virtualenv` and `virtualenvwrapper` (optional, but recommended)

To install dependencies:
```bash
pip install virtualenv virtualenvwrapper
````

### Creating a Virtual Environment

```bash
mkvirtualenv python-practice
workon python-practice
```

### Installing Packages

To install packages used in these exercises:

```bash
pip install bcrypt
```

To export dependencies:

```bash
pip freeze > requirements.txt
```

To install in another environment:

```bash
pip install -r requirements.txt
```

##  Example Scripts

### `add.py`

```python
a = int(input("Enter value for a: "))
b = int(input("Enter value for b: "))
c = a + b
print(c)
```

### `bcrypt_example.py`

```python
import bcrypt

password = b"A super complicated password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed)
```

## Version Info

This project uses:

* Python: 3.13.5 (compatible with 3.8.7 used in CareerFoundry)
* bcrypt: ^4.1.2







