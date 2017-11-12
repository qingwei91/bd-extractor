from extractor import *

dataset = SimFinDataset('sample-data.csv')

print "Number of indicators in dataset: "+str(dataset.numIndicators)
print "Number of companies in dataset: "+str(dataset.numCompanies)

print "Company at index position 1: "
print dataset.companies[1]
print "COGS values for this company: "
print dataset.companies[1].data[1].values
print "respective time periods:"
print dataset.timePeriods

print "get Company object by ticker:"
print dataset.getCompany("AAPL")