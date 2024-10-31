# Backend Documentation

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Clone the Repository](#clone-the-repository)
- [Install Packages](#install-packages)
- [Running the Project](#running-the-project)
- [Testing the Project](#testing-the-project)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Getting an API Key](#getting-an-api-key)

## Introduction
This is the backend for the [Project Name]. It is built using FastAPI and provides endpoints for interacting with mutual fund data. This documentation will guide you through setting up the project locally.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (optional, but recommended)

## Clone the Repository
To get started, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/yourusername/your-repo-name.git
```

Change into the project directory:

```bash
cd your-repo-name
```

## Install Packages
It's a good practice to create a virtual environment before installing packages to avoid dependency conflicts. You can use the following commands:

### Create a Virtual Environment
To create a virtual environment, run:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### Install Required Packages
Once your virtual environment is activated, install the required packages using:

```bash
pip install -r requirements.txt
```

## Running the Project
To run the FastAPI server, execute the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

This will start the server on `http://localhost:8005`. The `--reload` option enables auto-reload, so the server will update whenever you change the code.

## Testing the Project
To run the tests for the project, use the following command:

- On Windows:

```bash
set PYTHONPATH=. && pytest app/tests/
```

- On macOS/Linux:

```bash
PYTHONPATH=. pytest app/tests/
```

This will execute all tests and display the results in the terminal.

### Running Specific Tests
If you want to run a specific test file, you can specify the path:

```bash
pytest app/tests/test_funds.py
```

## API Documentation
The API documentation for the FastAPI application is available at:

```
http://localhost:8005/docs
```

You can use this interactive documentation to test the endpoints and see the expected request/response formats.

## Environment Variables
Make sure to set the necessary environment variables for your application before running the project. You can create a `.env` file in the project root with the following structure:

```
RAPIDAPI_KEY=your_api_key_here
DUMMY_USERNAME=bhive_user
DUMMY_PASSWORD=bhive_backend_secret_password
```

The above credentials can be used for login testing.

## Getting an API Key
To obtain an API key for accessing the mutual fund data through RapidAPI, follow these steps:

1. Go to the [Latest Mutual Fund NAV API page on RapidAPI](https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav).
2. Click on the "Sign Up" button if you don't have an account, or "Log In" if you already have one.
3. After logging in, subscribe to the API by selecting a pricing plan that suits your needs.
4. Once subscribed, you will find your API key in the dashboard. Copy this key and set it in your `.env` file as `RAPIDAPI_KEY`.
