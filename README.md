# lookingparameters

Code for processing looking time data to evaluate impact of parameters

### Prerequisites

- Install pyenv (see https://github.com/yyuu/pyenv)

- Install virtualenv
  `[sudo] pip install virtualenv`

- Install python 3.6.4+ via pyenv, e.g.:
  `pyenv install 3.6.4`

### Setup

1. Clone this repo.
2. Create a virtual environment (from the main lookingparameters directory, or wherever else is convenient for you):
  `virtualenv -p ~/.pyenv/versions/3.6.4/bin/python3.6 venv`
3. Enter the virtual environment
   `source venv/bin/activate`
4. Install requirements:
  `pip install -r requirements.txt`
  
  
### Data

For now, data is being stored separately due to inclusion of personal information (birthdates).
