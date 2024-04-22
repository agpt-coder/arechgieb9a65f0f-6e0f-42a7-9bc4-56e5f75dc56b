---
date: 2024-04-22T16:21:56.024011
author: AutoGPT <info@agpt.co>
---

# arechgie

archive the internet

**Features**

- **Data Crawling** Automated crawling and indexing of web pages to continuously update the archive.

- **Data Storage** Efficiently store archived data using cloud services or distributed systems.

- **Search Engine** Allow users to search for archived content using keywords, phrases, or advanced search criteria.

- **User Interface** Easy-to-navigate and user-friendly interface for both novice and advanced users.

- **Data Compression** Apply data compression techniques to make the storage more efficient.

- **Backup and Recovery** Robust backup and recovery solutions to ensure data integrity and availability.

- **API Access** Provide APIs for third-party developers to access or enhance the archived data.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'arechgie'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
