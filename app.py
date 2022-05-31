from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

app = FastAPI()

# This will be used as DB
expense_tracker = dict()

# Model classes for API
class Item(BaseModel):
    name: str
    members: list[str] = []

class Expense(BaseModel):
    name: str
    items: list[dict] = []

class Balance(BaseModel):
    name: str
    balances: dict = None

class DeleteExpense(BaseModel):
    expense_name: str


# API endpoints

@app.get('/')
def docs_redirect():
    return RedirectResponse(url='/docs')

@app.post('/create-group')
def create_expense(item: Item):
    if item.name in expense_tracker:
        raise HTTPException(status_code=400, detail="Group already exists")
    else:
        expense_tracker[item.name] = {"members": item.members}

    expense_tracker[item.name]["expenses"] = dict()
    return expense_tracker

@app.get('/group-details/{group_name}')
def get_group_details(group_name: str):
    if group_name in expense_tracker:
        return expense_tracker[group_name]
    else:
        raise HTTPException(status_code=404, detail="Group doesn't exist")

@app.patch('/add-expense/{group_name}')
def add_expense(group_name: str, item: Expense):
    
    expense_tracker[group_name]["expenses"][item.name] = item.items
    
    # Adding new members to the members list
    members = expense_tracker[group_name]["members"]
    expenses_dict = expense_tracker[group_name]["expenses"]
    for v in expenses_dict.values():
        for i in v:
            paidlist = list(i["paid_by"][0].keys())
            owedlist = list(i["owed_by"][0].keys())
            newlist = list(set(paidlist + owedlist))

            if newlist != members: 
                expense_tracker[group_name]["members"] = list(set(expense_tracker[group_name]["members"] + newlist))
                expense_tracker[group_name]["members"].sort()

    return expense_tracker[group_name]

@app.patch('/update-expense/{group_name}')
def update_expense(group_name: str, item: Expense):
    if group_name in expense_tracker:
        expense_tracker[group_name]["expenses"][item.name] = item.items

    # Adding new members to the members list
    members = expense_tracker[group_name]["members"]
    expenses_dict = expense_tracker[group_name]["expenses"]
    for v in expenses_dict.values():
        for i in v:
            paidlist = list(i["paid_by"][0].keys())
            owedlist = list(i["owed_by"][0].keys())
            newlist = list(set(paidlist + owedlist))

            if newlist != members: 
                expense_tracker[group_name]["members"] = list(set(expense_tracker[group_name]["members"] + newlist))
                expense_tracker[group_name]["members"].sort()

        return expense_tracker[group_name]
    else:
        raise HTTPException(status_code=404, detail="Group not found")

@app.patch('/add-balances')
def add_balance(item: Balance):
    expense_tracker[item.name]["balances"] = item.balances
    return expense_tracker[item.name]

@app.get('/balance-summary/{group_name}')
def balance_summary(group_name: str):
    balances = expense_tracker[group_name]["balances"]
    for k,v in balances.items():
        if len(v["owes_to"]):
            people = {}
            for dct in v["owes_to"]: 
                people = people | dct

            return {"summary": f"{k} owes {key}: {value} " for key, value in people.items()}


@app.delete('/delete-expense/{group_name}')
def delete_expense(group_name: str, item: DeleteExpense):
    if group_name in expense_tracker:
        if item.expense_name in expense_tracker[group_name]["expenses"]:
                expense_tracker[group_name]["expenses"].pop(item.expense_name, None)
                raise HTTPException(status_code=200, detail="Expense deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Expense not found")
    else:
        raise HTTPException(status_code=404, detail="Group not found")