# Coursera Dump

The script searches courses information from [COURSERA](https://www.coursera.org/) by keyword and saves the results into Excel file.
You should specify 2 parameters: **name** for output excel file and **searching keyword**.
By default script saves data to **python_courses.xlsx** and uses **'python'** keyword.

### Course information:

- **name**
- **language**
- **rating**
- **start date**
- **weeks amount**

# How to

Script requires python 3.5. You also need to install dependencies:

```bash
$ pip install requirements.txt
```

Example on Linux (for Windows - the same):

```bash
$ python coursera.py -f java_courses.xlsx -k java
Successfully saved to java_courses.xlsx
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
