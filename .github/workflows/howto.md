How current ci.yaml was made

1. repo uses `python quicktest.py` to run tests
    - To measure what code that covers, do `python -m coverage run quicktest.py`

2. Identify what a fresh machine would need
 - Ubuntu 24.04
 - python 3.12.3
 - requirements-ci.txt hold all packages
 - this repo for the test code
 - the tests through quicktest.py
 - collect kogs, timing, environment, coverage

 3. Usefule terms
 workflow: complete automation defined by a YAML file
 event: something that starts it, like a merge or push
 job: group of steps running on a runner
 runner: machine executing the job
 step: an action or group of commands
 action: reusable automation, such as preparing python

 4. YAML notation
  - `-` instroduces a list item, such as a step
  - `uses:` runs an existing action
  - `with:` supplies that actions settings
  - `run:` executes terminal commands
  - `run: |` instroduces multiple lines of commands
  - `${{ ... }}` lets GitHub calculate a value or condition



  ## Installation commands needed

  `python -m pip install -r requirements-ci.txt pdm-backend==2.5.0` to download whats in requirements-ci.txt

  then: `python -m pip install --no-build-isolation --no-deps -e .` 
  installs the python software into the current directory


  ## Running and measuring tests

  use `/usr/bin/time -p -o ci-results/timing.txt \ python -m coverage run quicktest.py \ 2>&1 | tee ci-results/tests.log` 

  which executes tests, writing timing to `ci-results/timing.txt` and error output and normal output combined into `ci-results/tests.log`