# A Django rest api for Vending Machine #
-----------------------------------------
Language: Python 3.6
Framework: Django 2.1
Package: Djangorestframework 3.8
Testing: pytest 3.8
-----------------------------------------


#########################################
Quick Start
Install all required packages from the requirements.txt
Run: pip install -r requirements.txt
Next, run the following commands on the terminal
python manage.py makemigrations vendingmachine
python manage.py createsuperuse
python manage.py manage.py runserver

#########################################
TESTING
To test please use the following command
python manage.py test

#########################################
URLs
Homepage
http://127.0.0.1:8000/ 
Admin panel
http://127.0.0.1:8000/admin/

#########################################
API URLs

-----------------------------------------
/api/create-machine/
To create a new vending machine
Method: POST
{
	"name": "Machine 1",
	"password": "test123"
}

-----------------------------------------
To set a password
/api/set-password/
Method: POST
{"password": "test123"}

-----------------------------------------

To check a password
Method: POST
/api/check-password/
{"password": "test123"}

-----------------------------------------

To create a token for the required machine
Method: POST
{"name": "Machine 1", "password": "test123"}` 

-----------------------------------------

To update wallet on the machine
Method: POST
{
    "1 pence": 10,
    "2 pence": 20,
    "5 pence": 30,
    "50 pound": 120
}

-----------------------------------------

To get and send money to a wallet

Method: GET

Return info from the required wallet

/api/send-money/
{
    "sent_money": {
        "50 pence": 1,
        "10 pence": 5,
        "5 pence": 3,
        "2 pence": 6,
        "1 pence": 12
    }
}

Method : POST

/api/send-money/ 
{
    "sent_money": {
        "50 pence": 1,
        "10 pence": 5,
        "5 pence": 3,
        "2 pence": 6,
        "1 pence": 12
    }
}


#########################################
EXTRA INFORMATIONS
To start using a new machine please create a new machine from the 
following urls using HTTP POST method.
URL
http://127.0.0.1:8000/api/create-machine/ 

You MUST add a token to header with the following data
KEY: Authorization
VALUE: "JWT <token> "

To request data and send money please use the following available units on the system.
http://127.0.0.1:8000/api/update-wallet/ 
http://127.0.0.1:8000/api/send-money/ 

#########################################

AVAILABLE CURRENCY UNITS

* '1 pence'
* '2 pence'
* '5 pence'
* '10 pence'
* '20 pence'
* '50 pence'
* '1 pound'
* '2 pound'
* '5 pound'
* '10 pound'
* '20 pound'
* '50 pound'



