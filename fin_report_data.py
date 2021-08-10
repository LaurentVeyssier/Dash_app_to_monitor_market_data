import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date
import pandas as pd

def get_financial_report(ticker):

    # try:
    urlfinancials = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials'
    urlbalancesheet = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials/balance-sheet'
    urlcashflow = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials/cash-flow'
    urlprofile = f"https://www.marketwatch.com/investing/stock/{ticker}/profile"

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }

    text_soup_financials = BeautifulSoup(requests.get(urlfinancials, headers=headers).text,'lxml') #read in
    text_soup_balancesheet = BeautifulSoup(requests.get(urlbalancesheet, headers=headers).text,"lxml") #read in
    text_soup_cashflow = BeautifulSoup(requests.get(urlcashflow, headers=headers).text,"lxml") #read in
    text_soup_profile = BeautifulSoup(requests.get(urlprofile, headers=headers).text,"lxml") #read in

    # build lists for Income statement
    titlesfinancials = text_soup_financials.findAll('tr', attrs={'class' : 'table__row'})
    for title in titlesfinancials:

        ps = title.find('div', {'class': 'cell__content fixed--cell'})

        try:
            vals = title.findAll('td', {'class': 'overflow__cell'})
            if 'Sales/Revenue' == ps.getText():
                saleslist = [vals[i].getText() for i in range(1,6)]
            elif 'EPS (Basic)' == ps.getText():
                epslist = [vals[i].getText() for i in range(1,6)]
            elif 'Net Income' == ps.getText():
                netincomelist = [vals[i].getText() for i in range(1,6)]
            elif 'EBITDA' == ps.getText():
                ebitdalist=[vals[i].getText() for i in range(1,6)]

        except:
            pass

    # find the table headers for the Balance sheet
    titlesbalancesheet = text_soup_balancesheet.findAll('tr', attrs={'class' : 'table__row'})
    for title in titlesbalancesheet:

        ps = title.find('div', {'class': 'cell__content fixed--cell'})

        try:
            vals = title.findAll('td', {'class': 'overflow__cell'})
            if 'Total Shareholders\' Equity' == ps.getText():
                equitylist = [vals[i].getText() for i in range(1,6)]
            elif 'Long-Term Debt' == ps.getText():
                longtermdebtlist = [vals[i].getText() for i in range(1,6)]
            elif 'Cash & Short Term Investments' == ps.getText():
                cashlist = [vals[i].getText() for i in range(1,6)]

        except:
            pass

    # find the table headers for the cash flow
    titlescashflow = text_soup_cashflow.findAll('tr', attrs={'class' : 'table__row'})
    for title in titlescashflow:

        ps = title.find('div', {'class': 'cell__content fixed--cell'})

        try:
            vals = title.findAll('td', {'class': 'overflow__cell'})
            if 'Free Cash Flow' == ps.getText():
                freecashflowlist = [vals[i].getText() for i in range(1,6)]            
        except:
            pass
    
    # find the table headers for the key financial metrics (profile)
    # https://stackoverflow.com/questions/62134091/get-data-from-marketwatch
    # https://learndataanalysis.org/source-code-web-scraping-company-financial-profiles-for-stock-analysis-using-python/
    # https://www.bing.com/videos/search?q=scrape+marketwatch+financial&docid=608052947017224254&mid=10501DCFC8308389D43D10501DCFC8308389D43D&view=detail&FORM=VIRE
    '''sections = text_soup_profile.findAll('tr', attrs={'class' : 'table__row'})
    for section in sections :
        ps = section.find('td')
        try:
            if "P/E Current" in ps.getText() or "Price to Sales Ratio" in ps.getText(): 
                val = ps.nextSibling.nextSibling
                print(f"{ps.getText()}: {val.getText()}")
        except:
            pass'''
    element_tables = text_soup_profile.select("div[class='element element--table']")
    profile_info = {}
    for element_table in element_tables:
        valuation_type = element_table.h2.text.strip()
        df = pd.read_html(str(element_table))[0]
        df.rename(columns={0:"KPI", 1:"Value"}, inplace=True)
        profile_info[valuation_type] = df

        
    # load all the data into dataframe 
    fin_df= pd.DataFrame({'Sales': saleslist,'ebitda': ebitdalist, 'net Income': netincomelist,'EPS': epslist,'shareholder Equity': equitylist,
                      'longterm Debt': longtermdebtlist,'Cash': cashlist, 'Free Cash Flow': freecashflowlist},index=range(date.today().year-5,date.today().year))
    
    fin_df.reset_index(inplace=True)
    
    return fin_df




