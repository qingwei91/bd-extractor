## Description

This is simple a class for Python 2.7 that helps you to extract all the relevant information from the SimFin bulk download files.

## Code Example

For an example on how to use the SimFinDataset class, check the sample-extraction.py file.

## XLSX Viewer

The processSimfin.py script is used for displaying the data in the CSV in a readable .xlsx file. The script utilizes xlsxWritter to generate the xlsx files. 
To install xlsxWritter run :

```bash
$ pip install XlsxWriter
```


Command line agurments are available when running ```--help```

usage example : 

```bash
 $ ./processSimfin.py --inputFile=sample-data.csv --minYear=2016
 ```


Available under MIT license.