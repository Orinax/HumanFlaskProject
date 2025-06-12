# FlaskBlog

A personal blog built with Flask. This project serves as a learning tool and portfolio piece. It includes basic post management, image support, and static page rendering.

## Features

- Home page with blog post listings and project showcase
- Individual post pages
- Static pages
- Image support

## Tech Stack

- **Python**
- **Flask**
- **Jinja2**
- **SQLite**
- **HTML/CSS**

## Getting Started

### 1. Clone the repository

```
git clone https://github.com/Orinax/HumanFlaskProject.git
cd HumanFlaskProject
```

### 2. Set up a virtual environment

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your secret key

Create an 'instance' folder, then add a file named `config.py` with the following content:
`SECRET_KEY = 'your-own-super-secret-key-here-instead-of-this-text'`
The .gitignore file is set up so that your config file will not be added to
version control.

### 4. Run the app

`flask run`

Then visit http://127.0.0.1:5000 in your browser.

## Deployment
This project can be hosted on platforms like PythonAnywhere, Render, or your
own VPS.

## Notes
This project is intended for learning and personal use.

## License
MIT License. See `LICENSE` file for more details.
