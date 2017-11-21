#!/usr/bin/env python

import extractor
import getopt,sys,os
import re
from StdSuites.Table_Suite import row
try:
    import xlsxwriter
except ImportError:
    print "Can't import xlsxWritter , use \"pip install xlsxwritten\" or visit http://xlsxwriter.readthedocs.io to get it"
    exit()

def nextCol(max):
    col_num=0
    while col_num < max:
        yield col_num
        col_num +=1

def BuildDb(opts):
    main_db = {}
    fund_dataset = parseFundDb(opts["FundFileName"],opts["minYear"],main_db)
    fund_file_name = os.path.splitext(opts["FundFileName"])[0] # remove extension
    xlsx_file_name = '%s.xlsx' % fund_file_name 
    writeXlsxFromDataset(xlsx_file_name,fund_dataset,opts["minYear"])
  
    price_dataset = parsePriceDb(opts["PriceFileName"],opts["minYear"],main_db)
    price_file_name = os.path.splitext(opts["PriceFileName"])[0] # remove extension
    xlsx_file_name = '%s.xlsx' % price_file_name
    writeXlsxFromDataset(xlsx_file_name,price_dataset,opts["minYear"])


def parsePriceDb(input_file_name,minYear):
    dataset = extractor.SimFinDataset(input_file_name)
    
    date_string_pattern = "(\d{4})-(\d{2})-(\d{2})"
    date_string_re = re.compile(date_string_pattern)
    
    periodIdxList = []
    for periodIdx,time_period in enumerate(dataset.timePeriods):
        date_string_match = date_string_re.match(time_period)
        if (date_string_match):
            year = int(date_string_match.group(1))
            month = int(date_string_match.group(2))
            day = int(date_string_match.group(3))
        else:
            year = "NA"
        if (year > minYear): #include
            periodIdxList.append(periodIdx)
            print "Will append data period %s" % time_period


    
#     for companyIdx,company in enumerate(dataset.companies):
#         for indIdx,indicator in enumerate(company.data):
#             main_db[company.ticker][indicator.name] =  
    return dataset

def parseFundDb(input_file_name,minYear):
    dataset = extractor.SimFinDataset(input_file_name)
    return dataset

def writeXlsxFromDataset(file_name,dataset,minYear):
   
    print "Creating %s" % file_name
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    indicator_name_list = []
    
    col_gen = nextCol(100)
    worksheet.write(0, next(col_gen), "Name")
    worksheet.write(0, next(col_gen), "Ticker")
    for indicator in dataset.companies[0].data:
        worksheet.write(0, next(col_gen), indicator.name)
        indicator_name_list.append(indicator.name)

    period_name_pattern = "(\w)(\d)-(\d{4})"
    date_string_pattern = "(\d{4})-(\d{2})-(\d{2})"
    period_name_re = re.compile(period_name_pattern)
    date_string_re = re.compile(date_string_pattern)
        
    periodIdxList = []
    # find relevant periods and list 
    for periodIdx,time_period in enumerate(dataset.timePeriods):
        fin_period_match = period_name_re.match(time_period)
        date_string_match = date_string_re.match(time_period)
        if (fin_period_match):
            year = int(fin_period_match.group(3))
        elif (date_string_match):
            year = int(date_string_match.group(1))
        else:
            year = "NA"
        if (year > minYear): #include
            periodIdxList.append(periodIdx)
            print "Will append data period %s" % time_period

    
    
    worksheet.write(0, next(col_gen), "Period Name")
    worksheet.write(0, next(col_gen), "Report Year")
    
    numMissingIndicators = 0
    num_columns = next(col_gen) - 1
    
    numCompanies = len(dataset.companies)
    row = 1
    for companyIdx,company in enumerate(dataset.companies):
        for periodIdx in periodIdxList:
            time_period = dataset.timePeriods[periodIdx]
            if (year > minYear):                 
                #print "Writing period %s" % time_period
                col_gen = nextCol(100)
                worksheet.write(row, next(col_gen), company.name)
                worksheet.write(row, next(col_gen), company.ticker)
                for indIdx,indicator in enumerate(company.data):
                    if indicator.name != indicator_name_list[indIdx]:
                        print "%s in not in initial list for ticker %s" % (indicator.name,company.ticker)
                        numMissingIndicators += 1
                        worksheet.write(row, next(col_gen), "NA")
                    else:
                        if (indicator.values[periodIdx] == None):
                            worksheet.write(row, next(col_gen), "NA")
                        else:
                            worksheet.write(row, next(col_gen), indicator.values[periodIdx])
                worksheet.write(row, next(col_gen), time_period)
                row += 1
            else: # ignore
                pass
        print "Written Fundamnetals for Company %d/%d (%d%%)" % (companyIdx,numCompanies,100*companyIdx/numCompanies)


                        
    print "Num companies written %d , Num data periods %d - num missing indicators %d , num row written %u, collumns %d" % (companyIdx,dataset.numTimePeriods,numMissingIndicators,row,num_columns)
    
    #freeze top row :
    worksheet.freeze_panes(1, 0)
    worksheet.set_column(0,num_columns, 15) # set column width 

    
    # apply autofilter:
    worksheet.autofilter(0,0,row,num_columns)
    workbook.close()


def print_usage():
    print "--input_price_file=<> - specify the CSV to be parsed for price data (mandatory)"
    print "--input_fund_file=<> - specify the CSV to be parsed for fundamnetal data (mandatory)"
    print "--minYear=<year> - only include data from years larger then this"
    print "--help - print this information"

def main():    
    minYear = 0
    options = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:] ,'', ["help","input_fund_file=","minYear=","input_price_file="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        print_usage()
        sys.exit(2)
    for opt, val in opts:
        if opt == "--help":
            print_usage()
            return
        elif opt in ("--input_fund_file"):
            options["FundFileName"] = val
            print "Will read fundamnetals from %s" % options["FundFileName"]
        elif opt in ("--minYear"):
            options["minYear"] = int(val)
            print "Will ignore reports from years before %u" % options["minYear"] 
        elif opt in ("--input_price_file"):
            options["priceFileName"] = val
            print "Will read prices from %s" % options["priceFileName"]
        else:
            assert False, "unknown option %s" % opt 

    if (options["FundFileName"] != None):
        import os.path
        if (os.path.isfile(options["FundFileName"])):
            pass             
        else:
            print "%s doesn't exist" % options["FundFileName"]
            return
        BuildDb(options)
    else:
        print "No input file name given!"
        print_usage()
        return
    


main()
    