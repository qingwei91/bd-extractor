import csv
from math import floor


class Company(object):
    def __init__(self, compId):
        self.id = int(compId)
        self.name = ""
        self.ticker = ""
        self.industryCode = 0
        self.finYearMonthEnd = 0
        self.data = []

    def __str__(self):
        return "id: " + str(self.id) + ", name: " + str(self.name) + ",  ticker: " + str(self.ticker) + ", data: " + ",".join(str(x) for x in self.data)

    def appendValue(self, indicatorIndex, value):
        self.data[indicatorIndex].values.append(value)


class Indicator:
    def __init__(self, name):
        self.name = name
        self.values = []

    def __str__(self):
        return "{name: " + str(self.name) + ", len(values): " + str(len(self.values)) + "}"


class SimFinDataset:
    def __init__(self, dataFilePath, companyClass=Company):

        self.numIndicators = None
        self.numCompanies = 1

        self.companies = []
        self.tickers = []
        self.timePeriods = []

        # load data
        self.loadData(dataFilePath, companyClass)

        self.numTimePeriods = len(self.timePeriods)

    def loadData(self, filePath, companyClass=Company):

        numRow = 0

        csvfile = open(filePath, 'rb')
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        row_count = sum(1 for _ in reader)
        csvfile.seek(0)

        for row in reader:
            numRow += 1
            if numRow > 1 and numRow != row_count:
                # info rows for company
                if numRow <= 7:
                    # company id row
                    if numRow == 2:
                        rowLen = len(row)
                        idVal = None
                        for index, columnVal in enumerate(row):
                            if index > 0:
                                if idVal is not None and idVal != columnVal:
                                    self.numCompanies += 1
                                    if self.numIndicators is None:
                                        self.numIndicators = index - 1
                                    # add last company
                                    self.companies.append(companyClass(idVal))
                                if index + 1 == rowLen:
                                    if self.numIndicators is None:
                                        self.numIndicators = index
                                    # add last company in file
                                    self.companies.append(companyClass(columnVal))
                                idVal = columnVal
                    if numRow > 2 and self.numIndicators is None:
                        return
                    # company name row
                    if numRow == 3:
                        for a in xrange(0, self.numCompanies):
                            self.companies[a].name = row[(a * self.numIndicators) + 1]
                    # company ticker row
                    if numRow == 4:
                        for a in xrange(0, self.numCompanies):
                            self.companies[a].ticker = row[(a * self.numIndicators) + 1]
                            self.tickers.append(self.companies[a].ticker)
                    # company financial year end row
                    if numRow == 5:
                        for a in xrange(0, self.numCompanies):
                            self.companies[a].finYearMonthEnd = row[(a * self.numIndicators) + 1]
                    # company industry code row
                    if numRow == 6:
                        for a in xrange(0, self.numCompanies):
                            self.companies[a].industryCode = row[(a * self.numIndicators) + 1]
                    # indicator name row
                    if numRow == 7:
                        for a in xrange(0, self.numCompanies):
                            for b in xrange(0, self.numIndicators):
                                self.companies[a].data.append(Indicator(row[(a * self.numIndicators + b) + 1]))
                else:
                    # actual data
                    for index, columnVal in enumerate(row):
                        if index == 0:
                            self.timePeriods.append(columnVal)
                        else:
                            compIndex = int(floor((index - 1) / float(self.numIndicators)))
                            indicatorIndex = index - 1 - (self.numIndicators * compIndex)
                            if columnVal == "" or columnVal is None:
                                appendVal = None
                            else:
                                appendVal = columnVal
                            self.companies[compIndex].appendValue(indicatorIndex, appendVal)

    def getCompany(self, ticker):
        if ticker in self.tickers:
            return self.companies[self.tickers.index(ticker)]
        else:
            return None