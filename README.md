# datasheets python script
This script can import a CSV file or text file of part numbers and find their datasheets and descriptions from [AllDatasheet](https://www.alldatasheet.com).

## Introduction
This script uses AllDatasheet because it is very easy to scrape.

Don't include any headers in your CSV file. They are added below for clarity. Here is an example data input:

| Part number |
|-------------|
| LM741       |
| CD4007UBE   |
| MAX038CPP   |
| ...         |

Example data output:

| Part number | Generic Part Number | Category                         | Description                         | Link                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------|---------------------|----------------------------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| LM741H      | LM741               | ICs- Analog ICs                  | 44V Single 1MHz Operation Amplifier | [https://octopart.com/dat..](https://octopart.com/opatz8j6/c1?t=5ihKqm7au0GirI9Qqk18245_6UGRTsSKFvthxo1wjCEIOXaq9iBCJQzY8bN2XBaNVFUKGcB29-ZFpI174SbNfVM3SQn9a2nEd-BnBurOKTN81FTBnk7bb9e4Ypp9KhXcww5pkLTiMUMOo8ObiWgD3L5pG5DvZnk-j2Ni_Og1nIrgP1SwaY4swljK3xmEnMVlA2Jlz37VBTZcnFbdCO0_wioRiT5-0IneCCEmcnWruJCffN-K4DenJiYfYZQvQE6pRLSK7XGsNcQXHdNQDydNvEbNuUicwED5LimVocYsCq7-qJ1yZFtdGiZrOb0FAr39NF1RqOZD7Tgam5NanYbCH6PwvzHckG1e8nwGnYEY5uFtAaS-28XQuPNxV4kySpzxyUCjhCdlWg) |
| CD4007UBE   | CD4007              | ICs- Digital ICs and Logic Gates | Complimentary Inverter              | ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

And so on.

You can comment out a line with `#`.
## Installation
Installation instructions

1. Clone the repo
2. Make a new folder called `venv`
3. Run `python3 -m venv ./venv` to create the venv
4. Run `source ./venv/bin/activate` in bash or `.\venv\Scripts\activate` on Windows to activate the python venv
5. Run `python3 -m pip install -r ./requirements.txt` to install necessary packages


## Usage
1. Activate like you did for the installation by running  `source ./venv/bin/activate` in bash or `.\venv\Scripts\activate` on Windows
2. Run `python3 main.py` from the command line
3. Enter the following:
   - Path to your TXT or CSV file containing parts list only (one per row): `/Users/foo/partslist.txt`
   - Folder to save data: `/Users/foo/my_datasheets`
   - Filename: `Inventory.csv`
