# ItC-MySQL-auto-judge
Introduction to Computer MySQL homework automatic judge system

## Homework Spec
[spec link](https://hackmd.io/@18uoJVgyT9KMeCBZDWu9Ng/SJQv8TPAB)

## How to Use
- Prepare your file structure as following (details in spec link):
  ```
  [student ID]/
  ├── Main.sql
  └── [student ID].txt
  └── output.txt
  ```
- Zip the directory and upload to Ceiba
- Put the zip file in the ``zip_file`` directory of the repository
- Run
  ```
  python3 judge.py --data-dir zip_files --answer-link [ref answer link of Paiza] 
  ```
- The output file is default as ``score.csv``. You will see an additional line with your student ID and score.

## Environment
- Linux x86\_64
- Python 3.7.5
