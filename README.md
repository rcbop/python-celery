# Disney Characters Report Generator

## Overview

This project is a Celery-based report generator that fetches Disney characters' data from an API, renders it into an HTML template using Jinja2, and then converts it to a PDF using WeasyPrint.

## Features

- Asynchronous report generation using Celery
- Fetches data from the Disney API
- Renders a customizable HTML template for each character
- Converts HTML reports to PDF using WeasyPrint
- Includes error handling and retry mechanisms

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/rcbop/python-celery.git
```

2. Docker compose build and run:

```bash
docker-compose up --build
```
