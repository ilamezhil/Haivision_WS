import csv
import requests
import logging
import json
import re

global input
global tc_passcount
global tc_failcount
global nr

from helpers import api_assertions
from helpers import logger

import pytest

def api_methods_all(input,tc_passcount,tc_failcount):
    logger = logging.getLogger(__name__)
    
    log_summary = open("test_summary.log", "w")
    log_summary.write("HAIVISION Rest API Assignment - Test Summary Log \n")
    log_summary.write("*************************************************\n")
    log_summary.write("SNO  \t STATUS  TEST_CASE_NAME \n")
    log_summary.write("*************************************************\n")
    tc_passcount=0
    tc_failcount=0
    passlist=[]
    faillist=[]
    #Execute all test cases from input.csv
    nr = len(input)
    for i in range(nr):
        logger.info(f"Executing SNo#{input[i]['sno']}, TestCase:{input[i]['testcase']}")
        testcaseStatus='Pass'

        #Retrive expected assertion validation inputs
        expectedStatus=str(input[i]['exp_statuscode']).strip()
        expectedOkTag=str(input[i]['exp_oktag']).strip().upper()
        expectedQuotes=str(input[i]['exp_quotes']).strip().replace('"','')
        expectedErrorMsg=str(input[i]['exp_errormsg']).strip().strip().replace('"','')

        #Prerequisite Step - Reset API status
        if str(str(input[i]['resetflag']).strip().replace('"','').upper()) == "TRUE":
            logger.info('Prerequisite Step - Reset Flag Enabled In Input')
            payload='{}'
            r = requests.post(input[i]['url'] + 'reset', data=payload)
            assertionDescription="Prerequisite : Reset API status"
            try:
                assert api_assertions.assert_Response("", assertionDescription, str(r.status_code), '200') == "Pass", "Fail"
            except AssertionError as error: #If Reset failed fail the test case and continue to execute next test case from input
                logger.info(f"Execution Completed SNo#{input[i]['sno']}, TestCase:{input[i]['testcase']}, Status:{str(testcaseStatus)} \n\n")
                (tc_passcount,tc_failcount)=write_logsummary(log_summary,input[i]['sno'],testcaseStatus,input[i]['testcase'],tc_passcount,tc_failcount)
                continue
        else:
            logger.info('Prerequisite Step - Reset Flag Not Enabled In Input')

        #Retrive Specific/All quotes using Rest API GET - /quotes/<id>
        if str(input[i]['method']).strip().replace('"','').upper() == 'GET':
            if input[i]['quotesid'] == '':
                resp = requests.get(input[i]['url'] + input[i]['resources'] )
                testcaseStatus=api_assertions.assert_getAllQuotes(None, "Assertion - ", resp, expectedStatus, expectedOkTag, expectedErrorMsg)
            else: #get given quotes
                resp = requests.get(input[i]['url'] + input[i]['resources'] + '/' + input[i]['quotesid'])
                testcaseStatus=api_assertions.assert_getSpecificQuote(None, "Assertion - ", resp, expectedStatus, expectedOkTag, expectedQuotes,expectedErrorMsg)

        #Adding quotes text using Rest API POST - /quotes
        elif str(input[i]['method']).strip().replace('"','').upper() == 'POST':
            payloadlist=re.split(r',(?=(?:[^"]*\"[^"]*\")*[^"]*$)', input[i]['payload']) 
            for quotes in payloadlist:
                logger.info('')
                logger.info("Posting input payload qutotes:'" + quotes.strip().replace('"','') + "'")
                payload='{"text": ' + quotes + '}'
                resp = requests.post(input[i]['url'] + input[i]['resources'], data=payload)
                url=input[i]['url'] + input[i]['resources']
                if str(quotes) == str(payloadlist[-1]):
                    testcaseStatus=api_assertions.assert_postQuotes(None, resp, expectedStatus, expectedOkTag, quotes.strip().replace('"',''),expectedErrorMsg,url) 
                else:
                    testcaseStatus=api_assertions.assert_postQuotes(None, resp, '201', 'TRUE', quotes.strip().replace('"',''),'',url) 
                if testcaseStatus == 'Fail':
                    #logger.info(f"Execution Completed SNo#{input[i]['sno']}, TestCase:{input[i]['testcase']}, Status:{str(testcaseStatus)} \n\n")
                    #(tc_passcount,tc_failcount)=write_logsummary(log_summary,input[i]['sno'],testcaseStatus,input[i]['testcase'],tc_passcount,tc_failcount)
                    break

        #Delete quotes using Rest DELETE - /quotes/<id>         
        elif str(input[i]['method']).strip().replace('"','').upper() == 'DELETE':
            quoteidlist=input[i]['quotesid'].strip().replace('"','').split(',') 
            iterationCount=0
            for quotes in quoteidlist:
                iterationCount +=1
                logger.info('')
                logger.info("Deleting input payload qutotes:'" + quotes.strip().replace('"','') + "'")
                payload='{}'
                resp = requests.delete(input[i]['url'] + input[i]['resources'] + '/' + str(quotes).strip() , data=payload)
                url=input[i]['url'] + input[i]['resources']
                if iterationCount == len(quoteidlist):
                    testcaseStatus=api_assertions.assert_DeleteQuotes(None, resp, str(quotes).strip(), expectedStatus, expectedOkTag, expectedErrorMsg,url) 
                else:
                    testcaseStatus=api_assertions.assert_DeleteQuotes(None, resp, str(quotes).strip(),'200', 'TRUE', '',url) 
                if testcaseStatus == 'Fail':
                    #logger.info(f"Execution Completed SNo#{input[i]['sno']}, TestCase:{input[i]['testcase']}, Status:{str(testcaseStatus)} \n\n")
                    #(tc_passcount,tc_failcount)=write_logsummary(log_summary,input[i]['sno'],testcaseStatus,input[i]['testcase'],tc_passcount,tc_failcount)
                    break
        else:
            logger.error(f"Input Error: Given Input method '{input[i]['method']}' is not valid. Valid/Expected Input methods:get, post, reset, delete...")
            testcaseStatus == 'Fail'
        if testcaseStatus == 'Fail':
            faillist.append(f"SNo#{input[i]['sno']}, Status:{str(testcaseStatus)}, TestCase:{input[i]['testcase']}")
        else:
            passlist.append(f"SNo#{input[i]['sno']}, Status:{str(testcaseStatus)}, TestCase:{input[i]['testcase']}")
        logger.info(f"Execution Completed SNo#{input[i]['sno']}, TestCase:{input[i]['testcase']}, Status:{str(testcaseStatus)} \n\n")
        (tc_passcount,tc_failcount)=write_logsummary(log_summary,input[i]['sno'],testcaseStatus,input[i]['testcase'],tc_passcount,tc_failcount)
    
    log_summary.write("\n****************\n")
    log_summary.write(f"OVERALL SUMMARY")
    log_summary.write("\n****************\n")
    log_summary.write(f"PASS  - {tc_passcount:03} \nFAIL  - {tc_failcount:03} \nTOTAL - {tc_passcount+tc_failcount:03} \n")
    log_summary.write("****************\n")
    log_summary.close()
    test_final(passlist,faillist)

def write_logsummary(log_summary, sno, status, tc_name,tc_passcount,tc_failcount):
    #write test case summary and update pass and fail count
    log_summary.write(f"{str(sno).strip():<6} \t {str(status).strip().upper()} \t {str(tc_name)} \n")
    if str(status)== "Pass":
        tc_passcount +=1
    elif str(status)== "Fail":
        tc_failcount +=1
    return(tc_passcount,tc_failcount)

def test_final(passlist,faillist):
    assert not faillist, "\nFailed Cases:\n{}\n\nPassed Cases:\n{}".format('\n'.join(faillist), '\n'.join(passlist))