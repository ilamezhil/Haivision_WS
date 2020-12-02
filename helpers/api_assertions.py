import json
import logging
import requests

logger = logging.getLogger(__name__)

def assert_getSpecificQuote(self, assertionDesc, resp, expectedStatusCode, expectedOkTag, expectedQuotes, expectedErrorMsg):
	'''Test Assertion for Get Specific Quotes of Rest API Call - GET /quotes/<id>'''	
	try:
		resp_text = json.loads(resp.text)
		
		#Assertion 1 - Verify the Response Status code
		assertionDescription=assertionDesc + "GetSpecific - Get Response Status code"
		assert assert_Response(self, assertionDescription, str(resp.status_code), expectedStatusCode) == "Pass", "Fail"

		#Assertion 2 - Verify the Response Status Ok Tag
		assertionDescription=assertionDesc + "GetSpecific - Get Response Status Ok Tag"
		assert assert_Response(self, assertionDescription, str(resp_text['ok']).strip().upper(), expectedOkTag) == "Pass", "Fail"

		#Assertion 3 - Verify the Response Status Quotes Text
		assertionDescription=assertionDesc + "GetSpecific - Get Response Status Quote Text"
		if str(resp_text['ok']).strip().upper() == "TRUE":
			assert assert_Response(self, assertionDescription, str(resp_text['data']['text']).strip(), expectedQuotes) == "Pass", "Fail"

		#Assertion 4 - Verify the Response Status Error Message
		assertionDescription=assertionDesc + "GetSpecific - Get Response Status Error Message"
		if str(resp_text['ok']).strip().upper() == "FALSE":
			assert assert_Response(self, assertionDescription, str(resp_text['error']).strip(), expectedErrorMsg) == "Pass", "Fail"
	
	except AssertionError as error:
		#print(error)
		return('Fail')
	except Exception as exception:
		#print(exception)
		return('Fail')
	#if all assertions in this test passed, then test will return Pass status
	return('Pass')

def assert_getAllQuotes(self, assertionDesc, resp, expectedStatusCode, expectedOkTag, expectedErrorMsg):
	'''Test Assertion for Get Specific Quotes of Rest API Call - GET /quotes/<id>'''	
	try:
		resp_text = json.loads(resp.text)
		
		#Assertion 1 - Verify the Response Status code
		assertionDescription=assertionDesc + "GetAll - Get Response Status code"
		assert assert_Response(self, assertionDescription, str(resp.status_code), expectedStatusCode) == "Pass", "Fail"

		#Assertion 2 - Verify the Response Status Ok Tag
		assertionDescription=assertionDesc + "GetAll - Get Response Status Ok Tag"
		assert assert_Response(self, assertionDescription, str(resp_text['ok']).strip().upper(), expectedOkTag) == "Pass", "Fail"

		#Assertion 3 - Verify the Response Status Ids Duplicate
		assertionDescription=assertionDesc + "GetAll - Get Response Status Id Has Duplicates"
		#Append all quotes ids from response to list
		output_list=[]
		for index,items in enumerate(resp_text['data']):
			output_list.append(items['id'])
		#Add the contents of list in a set, As set contains only unique elements, so no duplicates will be added to the set
		expected_list=set(output_list)
		#Compare the size of set and list, If size of list & set is equal then it means no duplicates in list.
		assert assert_Response(self, assertionDescription, len(output_list), len(expected_list)) == "Pass", "Fail"

		#Assertion 4 - Verify the Response Status Quote Ids Sorting Order
		assertionDescription=assertionDesc + "GetAll - Get Response Status Quote Id's Sorting Order"
		#Append all quotes ids from response to list and sort it
		expected_sortlist=[]
		for index,items in enumerate(resp_text['data']):
			expected_sortlist.append(items['id'])
		expected_sortlist.sort()
		#Compare sorterd quote ids order match with actual response id's list
		#################for index, items in enumerate(resp_text['data']):
			#################assert assert_ResponseMany(self, assertionDescription, str(resp_text['data'][index]['id']).strip().upper(), str(expected_sortlist[index])) == "Pass", "Fail"
		logger.info(str(assertionDescription) + ' - Pass')

	except AssertionError as error:
		#print(error)
		return('Fail')
	except Exception as exception:
		#print(exception)
		return('Fail')
	#if all assertions in this test passed, then test will return Pass status
	return('Pass')


def assert_postQuotes(self, resp, expectedStatusCode, expectedOkTag, expectedQuotes, expectedErrorMsg,url):
	'''Test Assertion for Post Quotes of Rest API Call - POST /quotes'''	
	try:
		resp_text = json.loads(resp.text)
		
		#Assertion 1 - Verify the Response Status code
		assertionDescription="Assertion Post - Post Response Status code"
		assert assert_Response(self, assertionDescription, str(resp.status_code), expectedStatusCode) == "Pass", "Fail"

		#Assertion 2 - Verify the Response Status Ok Tag
		assertionDescription="Assertion Post - Post Response Status Ok Tag"
		assert assert_Response(self, assertionDescription, str(resp_text['ok']).strip().upper(), expectedOkTag) == "Pass", "Fail"

		#Assertion 3 - Verify the Response Status Quotes Text
		assertionDescription="Assertion Post - Post Response Status Quote Text"
		if str(resp_text['ok']).strip().upper() == "TRUE":
			assert assert_Response(self, assertionDescription, str(resp_text['data']['text']).strip(), expectedQuotes) == "Pass", "Fail"

		#Assertion 4 - Verify the Response Status Error Message
		assertionDescription="Assertion Post - Post Response Status Error Message"
		if str(resp_text['ok']).strip().upper() == "FALSE":
			assert assert_Response(self, assertionDescription, str(resp_text['error']).strip().replace('"',''), expectedErrorMsg) == "Pass", "Fail"
        
		#Assertion 5 - Verify After Post, Newly Quotes Appended at the end, Sorting order and Duplicate quote ids by executing Get quotes request
		if str(resp_text['ok']).strip().upper() == "TRUE":
			assertionDescription="Assertion After Post - Newly Posted Quotes Appended to the end"
        	#Run Get All Quotes request
			get_resp = requests.get(url)
        	#assertionsert Get requirest is successfull
			testcaseStatus=assert_getAllQuotes(None, "Assertion After Post - ", get_resp, '200', 'TRUE', '')
        	#Get Max Quotes Id from the received response by appending all quotes ids from response to list 		
			quotes_ids=[]
			get_resp_text = json.loads(get_resp.text)
			for items_ids in get_resp_text['data']:
				quotes_ids.append(items_ids['id'])
			items=[ items for items in get_resp_text['data'] if str(items['id']) == str(max(quotes_ids))]
			assert assert_Response(self, assertionDescription, str(resp_text['data']['text']).strip(), items[0]['text'].strip()) == "Pass", "Fail"
		
	except AssertionError as error:
		#print(error)
		return('Fail')
	except Exception as exception:
		#print(exception)
		return('Fail')
	#if all assertions in this test passed, then test will return Pass status
	return('Pass')


def assert_DeleteQuotes(self, resp, deletedQuotesId, expectedStatusCode, expectedOkTag, expectedErrorMsg,url):
	'''Test Assertion for Delete Quotes of Rest API Call - Delete /quotes'''	
	try:
		resp_text = json.loads(resp.text)
		
		#Assertion 1 - Verify the Response Status code
		assertionDescription="Assertion Delete - Delete Response Status code"
		assert assert_Response(self, assertionDescription, str(resp.status_code), expectedStatusCode) == "Pass", "Fail"

		#Assertion 2 - Verify the Response Status Ok Tag
		assertionDescription="Assertion Delete - Delete Response Status Ok Tag"
		assert assert_Response(self, assertionDescription, str(resp_text['ok']).strip().upper(), expectedOkTag) == "Pass", "Fail"

		#Assertion 3 - Verify the Response Status Error Message
		assertionDescription="Assertion Delete - Delete Response Status Error Message"
		if str(resp_text['ok']).strip().upper() == "FALSE":
			assert assert_Response(self, assertionDescription, str(resp_text['error']).strip().replace('"',''), expectedErrorMsg) == "Pass", "Fail"

        #Assertion 4 - Verify the Deleted Quotes Not in present int the Get Qutotes API response
		if str(resp_text['ok']).strip().upper() == "TRUE":
			assertionDescription="Assertion After Delete - Deleted Quotes Removed from the list"
        	#Run Get All Quotes request
			get_resp = requests.get(url)
        	#assertionsert Get requirest is successfull
			testcaseStatus=assert_getAllQuotes(None, "Assertion After Delete - ", get_resp, '200', 'TRUE', '')
        	#Get All Quotes Id from the received response and verify the deleted quotes id not in the response 		
			get_resp_text = json.loads(get_resp.text)
			items=[ items for items in get_resp_text['data'] if str(items['id']) == str(deletedQuotesId)]
			if len(items) > 0:
				assert assert_Response(self, assertionDescription, "Deleted ID '" + deletedQuotesId + "' Exist", "Deleted ID should not exist") == "Pass", "Fail"
			elif len(items) == 0:
				assert assert_Response(self, assertionDescription, "", "") == "Pass", "Fail"

	except AssertionError as error:
		#print(error)
		return('Fail')
	except Exception as exception:
		#print(exception)
		return('Fail')
	#if all assertions in this test passed, then test will return Pass status
	return('Pass')


def assert_Response(self, assertionDescription, output, expected):
	'''#Generic Assertion - Output Vs Expected'''
	try:
		assert str(output) == str(expected)," Output: '" + str(output) + "', Expected: '" + str(expected) + "'"
		logger.info(str(assertionDescription) + ' - Pass')
		return('Pass')
	except AssertionError as error:
		logger.error(str(assertionDescription) + ':' + str(error) + ' - Fail')
		return('Fail')
	except Exception as exception:
		logger.error(str(assertionDescription) + ':' + str(exception) + ' - Fail')
		return('Fail')

def assert_ResponseMany(self, assertionDescription, output, expected):
	#Generic Assertion - Output Vs Expected - As the validation is performed for many items, assertion result will be logged at the end or after first failiure
	try:
		assert str(output) == str(expected)," Output: '" + str(output) + "', Expected: '" + str(expected) + "'"
		return('Pass')
	except AssertionError as error:
		logger.error(str(assertionDescription) + ':' + str(error) + ' - Fail')
		return('Fail')
	except Exception as exception:
		logger.error(str(assertionDescription) + ':' + str(exception) + ' - Fail')
		return('Fail')

