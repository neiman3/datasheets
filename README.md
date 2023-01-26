# datasheets python script
Import a CSV file or text file of part numbers and find their datasheets and descriptions from [AllDatasheet](https://www.alldatasheet.com).

This script uses AllDatasheet because it is very easy to scrape.

Don't include any headers in your CSV file. They are added below for clarity. Here is an example data input:

| Part number |
|-------------|
| LM741       |
| CD4007UBE   |
| MAX038CPP   |
| ...         |

Example data output:

| Part number | Link                                                                                                           | Description 1         | Description 2                | Description 3 |
|-------------|----------------------------------------------------------------------------------------------------------------|-----------------------|------------------------------|---------------|
| LM741       | [https://pdf1.alldat...L/LM741.html](https://pdf1.alldatasheet.com/datasheet-pdf/view/198081/SEOUL/LM741.html) | Operational Amplifier | Single Operational Amplifier | ...           |
| CD4007UBE   | ...                                                                                                            | ...                   | ...                          | ...           |

And so on.