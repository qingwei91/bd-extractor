#!/usr/bin/env python

import extractor
import getopt,sys,os
import re
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

def parseDb(input_file_name,minYear):
    dataset = extractor.SimFinDataset(input_file_name)
    
    file_name = os.path.splitext(input_file_name)[0] # remove extension
    xlsx_file_name = '%s.xlsx' % file_name
    print "Creating %s" % xlsx_file_name
    workbook = xlsxwriter.Workbook(xlsx_file_name)
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
    print "--inputFile=<> - specify the CSV to be parsed (mandatory)"
    print "--minYear=<> - will only include entries from this year onwards"
    print "--help - print this information"

def main():
    input_file_name = None
    minYear = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:] ,'', ["help","inputFile=","minYear="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        print_usage()
        sys.exit(2)
    for opt, val in opts:
        if opt == "--help":
            print_usage()
            return
        elif opt in ("--inputFile"):
            input_file_name = val
            print "Will read from %s" % input_file_name
        elif opt in ("--minYear"):
            minYear = int(val)
            print "Will ignore reports from years before %u" % minYear

        else:
            assert False, "unknown option %s" % opt 

    if (input_file_name != None):
        import os.path
        if (os.path.isfile(input_file_name)):
            pass             
        else:
            print "%s doesn't exist" % input_file_name
            return
        parseDb(input_file_name,minYear)
    else:
        print "No input file name given!"
        print_usage()
        return
    


main()
    