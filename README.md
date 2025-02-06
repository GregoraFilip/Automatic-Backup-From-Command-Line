# Automatic Backup from Command Line
by Filip Gregora

## Description
This is a simple script for backing up files to an external drive on Windows, written in Python.

The backup process is straightforward: the script checks all files in the specified backup directories. If a file has been modified after the last backup timestamp, the script copies the updated file and replaces the previous version if necessary.

## Setup
To set up the external drive for backups, first connect the drive and run:
```sh
python automatic_backup.py -s
```
This creates a directory `backup/automatic_backup` and two files:
- `.backup`: Contains the backup path on a single line.
- `.timestamp`: Stores the last backup time.

## Adding a Backup Path
To add a backup path to a configured external drive, run:
```sh
python automatic_backup.py -a
```
This opens Windows File Explorer, allowing you to select a file or folder to back up. The selected folder will be fully backed up to the external drive.

## Running a Backup
To perform a backup to the configured external drive, run:
```sh
python automatic_backup.py
```
This copies all newly created files since the last backup and replaces any modified files.

## Technologies
The project is written in **Python**.

## Installation & Running
To run this project, you must have **Python 3.3 or higher** installed.

## License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

