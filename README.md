# It Company Task Manager

Django project for managing tasks and workers in IT company.

## Check it out

[Task Manager project deployed to Render](https://it-company-task-manager-8oye.onrender.com/)

## Installing / Getting started

Python3 must be already installed.

```shell
git clone https://github.com/TetyanaPavlyuk/it-company-task-manager.git
cd it-company-task-manager/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver # Starts Django server
```


## Features

* Authentication functionality for Worker/User
* Managing tasks, task types, workers, positions and news from website interface (CRUD)
* Every Worker can publish some news in the title page
* Only logged-in author/Worker can edit his news/post
* Personal information can edit only logged-in owner/Worker
* Tasks list - tasks displayed in the next order:
  - at the end of page displayed completed tasks (they are highlighted in green)
  - all tasks sorted by deadline date and name
  - overdue tasks are highlighted in red
  - high priority tasks are highlighted in orange, medium - blue, low - grey and undefined - without highlighted
* Admin panel for advanced managing

### Additional info
You can test the functionality of the project using the following credentials:
* login: user
* password: user12345

