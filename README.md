# Expense Tracker App
Expense Tracker app for the SDE-Intern task. This app is made using Python and FastAPI

## Installation  
Python 3.9+ required. Install FastAPI and Uvicorn ASGI Web server using pip:  

```pip install -r requirements.txt```
## API Guide
Well, FastAPI documents pretty much everything about the API endpoints with an nteractive UI to test the APIs. The API endpoints are in accordance with the project specification.

### API Endpoints
* ```/create-group```  
Creates a group. Structure for which is :
```
{
  "name": "string",
  "members": []
}
```

* ```/group-details/{group_name}```  
Displays a group  

* ```/add-expense/{group_name}```  
Adds expense to an existing group. Structure for which is:
```
 {
   "name": "Fruits and Milk",
   "items": [{"name": "milk", "value": 50, "paid_by": [{"A": 40, "B": 10}], "owed_by": [{"A": 20,"B": 20, "C": 10}]},
             {"name": "fruits", "value": 50, "paid_by": [{"A": 50}], "owed_by": [{"A": 10,"B": 30, "C": 10}]}]
 }
 ```
 
* ```/update-expense/{group_name}```  
Updates a expense of a group. Structure for which is:
```
 {
   "name": "Fruits and Milk",
   "items": [{"name": "milk", "value": 50, "paid_by": [{"A": 40, "B": 10}], "owed_by": [{"A": 20,"B": 20, "C": 10}]},
             {"name": "fruits", "value": 50, "paid_by": [{"A": 50}], "owed_by": [{"A": 10,"B": 30, "C": 10}]}]
 }
```
* ```/add-balances```  
API Endpoint to add balances to a group. Structure for which is:
```
  {
  "name": "Home",
  "balances": {
    "A": {
      "total_balance": -100.0,
      "owes_to": [{"C": 100}],
      "owed_by": []
    },
    "B": {
      "total_balance": 0.0,
      "owes_to": [],
      "owed_by": []
    },
    "C": {
      "total_balance": 100.0,
      "owes_by": [{"A": 100}],
      "owed_to": []
    }
  }
  }
```

* ```/balance-summary/{group_name}```  
Displays simplified balance summary of a group  

* ```/delete-expense/{group_name}```  
Deletes an expense of a group. Structure for which is:
```
{
  "expense_name": "string"
}
```
