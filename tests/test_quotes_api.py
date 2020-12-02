# -*- coding: utf-8 -*-
import unittest
import os
import requests

from context import helpers
from helpers import csvreader
from helpers import logger
from helpers import rest_crud

path = "./data/input.csv"
input=helpers.csvreader.read_csv(None,path)

class test_quotes_api:
    #Run HaiVision Assignment REST Automation Tests
    helpers.logger.log_level()
    helpers.rest_crud.api_methods_all(input,0,0)

if __name__ == '__main__':
    print("HaiVision REST Assignment test execution in progress...")
    mytests = test_quotes_api()
    print("HaiVision REST Assignment test execution completed.")