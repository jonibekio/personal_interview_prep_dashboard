# Personal Interview Prep Dashboard

![Python](https://img.shields.io/badge/Python-Django%20REST-3776AB?logo=python&logoColor=white) ![Django REST Framework](https://img.shields.io/badge/API-DRF-A30000) ![Status](https://img.shields.io/badge/Status-Prototype-orange)

## Overview

A prototype for organizing interview preparation: learning modules, progress dashboards, and coding challenges. The repository contains a Django REST backend and static UI prototypes. The frontend application is not present as a complete buildable source tree.

## Implemented areas

- Account and learning/dashboard API modules.
- Learning categories, modules, lessons, quizzes, and progress records.
- Coding challenge and submission endpoints.
- Static HTML/CSS design prototypes and image assets.

### Important limitation

The coding-challenge service is a mock: it does not execute submitted code and currently reports test outcomes without running user solutions. Do not describe this repository as a functioning online judge.

## Screenshots

The repository includes static design prototypes, not verified screenshots from a running application. Add real application screenshots after a frontend is implemented.

## Technology stack and architecture

Python, Django REST Framework, and Django apps under `backend/apps/` for accounts, learning/dashboard, and coding. The root `frontend` entry is not a complete source directory in the checked tree, so no frontend framework is claimed here.

```text
backend/       Django project, domain apps, services, and API routes
frontend       Incomplete/submodule reference; frontend source is not present in this checkout
design assets  Static HTML/CSS prototypes and images
```

## Installation and API

Install dependencies from `backend/requirements.txt`, configure the Django environment, run migrations, and start the backend using `backend/manage.py`. Exact API routes are defined by the app URL modules; there is no root OpenAPI/Swagger configuration documented in the repository.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment and database

Configure Django secret/debug/host/database settings through environment variables as expected by `backend/config/settings.py`. Do not use development secrets or wildcard hosts in production. Django ORM migrations define account, learning, progress, and challenge records.

## Usage

The current usable code is the backend API plus static design materials. A complete user experience requires restoring/implementing the frontend. Coding submissions are not executed.

## Tests and deployment

No test suite or deployment configuration is present in the repository. No Railway/Vercel integration is confirmed. Add backend tests, an actual frontend, and a deployment plan before presenting this as a complete product.

## Security notes

- Settings use unsafe debug/development defaults; use managed secrets and strict hosts before any deployment.
- Do not execute untrusted submissions until a sandboxed runner, time/resource limits, and isolation model exist.
- Review the detached frontend/submodule setup so builds are reproducible.

## Future improvements

- Restore the actual frontend source and record it as a proper submodule or tracked directory.
- Implement an isolated code-execution service and real per-test evaluation.
- Add auth/authorization tests, OpenAPI documentation, CI, and real screenshots.
