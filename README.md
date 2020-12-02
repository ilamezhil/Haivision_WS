Haivision Assignment
#Prerequisite
#Start Service Running the Quotes API
In Command Prompt Navigate Quotes server exe dist folder - .\Haivision_WS\quotes_server\dist\quotes_server
Run .\Haivision_WS\quotes_server\dist\quotes_server> quotes_server.exe in command prompt
visit http://127.0.0.1:6543/quotes in a browser to ensure it functions. You should see a JSON structure similar to this:
{ "ok": true, "data": [ { "id": 1, "text": "We have nothing to fear but fear itself!" }, { "id": 2, "text": "All work and no play makes Jack a dull boy." }, { "id": 3, "text": "Travel is fatal to prejudice, bigotry, and narrow-mindedness." } ] }

#This package is used to test below requirements
1. POST /reset - Reset the quotes and ID sequence to their original values.
2. GET /quotes - Output data is sorted by id. Test that this is true for at least 12 quotes; There are no duplicate IDs.
3. POST /quotes - Accepts a string as the "text" field, e.g. {"text": "I have a dream"}; The response data contains a new ID and the text as provided in the request; Rejects (with HTTP code 400) objects missing the text field, and when the text field is not a string, e.g. {}  and  {"text": 123};Storing at least 20 quotes is supported;After adding a new quote, it should appear in a subsequent GET /quotes request.
4. GET /quotes/<id> - All quotes objects from GET /quotes are retrievable individually based on their ID, and that the text matches; Nonexistant quote IDs provoke an HTTP code 404.
5. DELETE /quotes/<id> - Deleting a quote succeeds, and subsequent attempts to delete that quote reply with HTTP code 404; Once a quote is deleted, it no longer shows up in the data for GET /quotes.
 
#All Test cases can be configured in input.csv file; resetflag - True/False will decide the reset prerequisite step
Note: Formatting errors in input.csv file not handled. Ensure the the inputs entered correctly. Refer sample input.csv scenarios attached.
 
#Command to Run the test script 
Navigate to .\Haivision_WS\dist\test_quotes_api in command prompt
Run .\Haivision_WS\dist\test_quotes_api>test_quotes_api.exe  - in command prompt

Input file location - .\Haivision_WS\dist\test_quotes_api\data ; File Name: input.csv
log files location - .\Haivision_WS\dist\test_quotes_api\log ; File Names: Haivision_Test_Summary.log' & Haivision_Test_Detail.log

#python execution file created using pyinstaller

###################################################################################

#You can run actual pytest with below installations
install python 3.6 or higher, set required paths in environment variables.
Verify the python installed version using below 
C:\>py -m pip --version
pip 20.2.3 from C:\Users\***\AppData\Local\Programs\Python\Python39\lib\site-packages\pip (python 3.9)

#Command to Run the pytest script 
Navigate to .\Haivision_WS - in command prompt
Run .\Haivision_WS>>py.test test_quotes_api.py  - in command prompt


#Creating a virtual environment in Project Directory (Below steps are optional as the repo already updated with 'env' folder
cd C:\HaiVision
C:\HaiVision>py -m venv env

#Activating a virtual environment
C:\HaiVision>.\env\Scripts\activate
(env) C:\HaiVision>where python
C:\HaiVision\env\Scripts\python.exe
C:\Users\***\AppData\Local\Programs\Python\Python39\python.exe
C:\Users\***\AppData\Local\Microsoft\WindowsApps\python.exe

#Installing webserrvice and pytest packages 

pip install -U requests
pip install -U pytest
pip install pyinstaller
