### Hexlet tests and linter status:
[![Actions Status](https://github.com/NikGor/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/NikGor/python-project-52/actions)
![GitHub Workflow Status](https://github.com/NikGor/python-project-52/actions/workflows/python-app.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/c50951bb34435f5411b2/maintainability)](https://codeclimate.com/github/NikGor/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c50951bb34435f5411b2/test_coverage)](https://codeclimate.com/github/NikGor/python-project-52/test_coverage)

# 🌟 Task Manager 🌟
This project is a simple task manager, where users can register, login, update their profiles, and delete their 
accounts. Users can also create, update, and delete tasks with statuses and labels. The project is deployed on Railway.

You can check out the live deployment of the Task Manager on Railway by following this link: [Task Manager - Deployed on Railway](https://python-project-52-production.up.railway.app/)


## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## 📋 Prerequisites

Python 3.8 or higher
Django 3.2 or higher
PostgreSQL (for production)

## 📦 Installation

Clone the repository:
``` bash
git clone https://github.com/NikGor/python-project-52.git
cd python-project-52
```
Install the requirements:
``` bash
pip install -r requirements.txt
```

Create a .env file in the root directory of the project and add the following:

``` bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

```
Replace your-secret-key with a secret key for Django.

Apply the migrations:
``` bash
python manage.py migrate
```

Run the server:

``` bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/.

## 🚄 Deploying to Railway

Railway is a platform for deploying applications. Here's how you can deploy this Django project to Railway:

Create a new project on Railway.
Connect your GitHub repository to the Railway project.
In the Railway dashboard, set the environment variables (SECRET_KEY, DEBUG, DATABASE_URL) in the Variables section.
In the Deployments section, click on Deploy to deploy your application.

## 🧪 Running the Tests

You can run the tests using the following command:

``` bash
python manage.py test
```

## 🙌 Contributing
Contributions are welcome! Please read our contributing guide for details.

## 📃 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact
If you have any questions, feel free to reach out!

Enjoy the project! 🎉