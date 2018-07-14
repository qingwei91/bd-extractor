from extractor import *

# dataset that starts on December 31st 2012, ends in December 2016 and filters out all companies that have some missing values
# date input format is a string: "%Y-%m-%d"
dataset = SimFinDataset('sample-data.csv','semicolon',"2012-12-31","2016-12-31",True)

print("Number of indicators in dataset: "+str(dataset.numIndicators))
print("Number of companies in dataset (companies with some missing values removed): "+str(dataset.numCompanies))

print("Company at index position 0: ")
print(dataset.companies[0])
print("COGS values for this company: ")
print(dataset.companies[0].data[1].values)
print("respective time periods (string format):")
print(dataset.timePeriods)
# time periods can also be displayed as datetime objects (quarters here are the "normal" quarters, same as for companies with financial year ending end of december)
print("respective time periods (date format):")
print(dataset.timePeriodsDates)

print("get Company object by ticker:")
print(dataset.getCompany("AAPL"))
print(dataset.getCompany("A"))


print "--------"
quit()
# to get the full dataset, omit the options

datasetFull = SimFinDataset('sample-data.csv','semicolon')

print("Number of indicators in full datasetFull: "+str(datasetFull.numIndicators))
print("Number of companies in full datasetFull: "+str(datasetFull.numCompanies))

print("Company at index position 0: ")
print(datasetFull.companies[0])
print("COGS values for this company: ")
print(datasetFull.companies[0].data[1].values)
print("respective time periods (string format):")
print(datasetFull.timePeriods)
print("respective time periods (date format):")
print(datasetFull.timePeriodsDates)

print("get Company object by ticker:")
print(datasetFull.getCompany("AAPL"))