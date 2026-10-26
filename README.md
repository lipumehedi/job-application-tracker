# Job Application Tracker

A small CLI tool to keep track of job applications.
I made this while job hunting in Japan, because I was applying through
many platforms (Indeed, doda, LinkedIn, Workport) and needed one simple
place to see what I applied to and what happened with each application.

求職活動中に、複数のサイト（Indeed、doda、LinkedIn、Workport）への応募を
管理するために作った、シンプルなCLIツールです。

## Features

- Add an application (company, position, platform, date, note)
- List applications, with an option to filter by status
- Update the status of an application
  (`applied` / `screening` / `interview` / `offer` / `rejected` / `withdrawn`)
- Show simple statistics by status
- Data is saved in a local `data.json` file (JSON format)
- Only the Python standard library is used — nothing to install

## Tech

- Python 3
- `argparse` (CLI), `dataclasses` (data model), `json` (storage)
- `unittest` for tests

## Usage

```bash
# Add an application
python job_tracker.py add "Example Inc." "Backend Engineer" Indeed --date 2026-10-24

# List all applications
python job_tracker.py list

# List only applications in interview stage
python job_tracker.py list --status interview

# Update a status (use the index number shown by list)
python job_tracker.py update 0 interview

# Show statistics
python job_tracker.py stats
```

## Tests

```bash
python -m unittest discover
```

## Project structure

```
job-application-tracker/
├── job_tracker.py        # main program
├── test_job_tracker.py   # unit tests
└── README.md
```

## What I learned

- Designing a small program with a clear data model (dataclass)
- Separating the data layer (Tracker class) from the CLI layer (argparse)
- Writing unit tests, including tests with temporary files
