## Description

This is simple a class for Python (should work for both Python 2 and 3) that helps you to extract all the relevant information from the SimFin bulk download files.

## Code Examples

For an example on how to use the SimFinDataset class, check the sample-extraction.py file.


In short:

Load dataset, specify filename and delimiter ("comma" or "semicolon", depending on what file you downloaded from simfin.com)
```python
dataset = SimFinDataset('sample-data.csv','semicolon')
```

You can also specify a start and end date for the data points and only keep companies in the dataset that have no missing data values (due to mistakes and/or missing data) by setting the excludeMissing argument to True.
```python
dataset = SimFinDataset('sample-data.csv','semicolon',"2011-01-01","2016-12-31",True)
```

Print number of indicators (for each company) and number of companies in dataset
```python
print(dataset.numIndicators)
print(dataset.numCompanies)
```

Print company at index position 1
```python
print(dataset.companies[1])
```

Print COGS values for this company (index at position 1 is COGS)
```python
print(dataset.companies[1].data[1].values)
```

Print time periods (strings)
```python
print(dataset.timePeriods)
```

Print time periods (datetime objects)
```python
print(dataset.timePeriodsDates)
```

Get company object by ticker
```python
print(dataset.getCompany("AAPL"))
```

## Troubleshooting

Currently the extractor only works for the "wide" data format on the SimFin bulk download page. Support for the "narrow" format will be made available in the future.

If you are having trouble getting the script to run, check the extractor with the "1comp.csv" file, as it contains only one company and should be quick to load. This one should also be easy to open in Excel if you want to look at the format of the file.

## Conversion to XLSX

(not tested for Python 3)

The processSimfin.py script is used for displaying the data in the CSV in a readable .xlsx file. The script utilizes xlsxWritter to generate the xlsx files. 

Created by <a href="https://github.com/ranm">@ranm</a> and extended by <a href="https://github.com/VitBu">@VitBu</a>

You need to install xlsxWritter:

```bash
$ pip install XlsxWriter
```


Command line arguments are available when running ```--help```

usage example : 

```bash
 $ ./processSimfin.py --inputFile=sample-data.csv --minYear=2016
 ```
 
 getting info of specific companies  by tickers: 

```bash
 $ ./processSimfin.py --inputFile=sample-data.csv --minYear=2016 --tickers=AAPL,MSFT
 ```


Available under MIT license.