![](https://img.shields.io/badge/python-v3.10.1-blue)

- [Solution Tree](#solution-tree)  
- [How To Run Locally](#how-to-run-locally)

# Solution Tree

## The `main.py` module
The runnig process occurs in `main.py`. Module responsible for calling and managing the entire project

The `get_dates` function is reponsible for getting the initial and final date of the cashflow.  
It queries through both `investments` and `installments` list to make this check

The first thing it does is to set default values to the dates. So after that we can keep subbing these values until we get the right one:
```
initial_date = date.max
final_date = date.min
```

After, using `zip_longest`, we can query through both lists in paralel, looking for the dates:
```
for investment, installment in zip_longest(investments, installments,
                                               fillvalue=False):
```

**Obs:** As the list have different lengths, we must check if the iterator has a value before trying to get the dates:
```        
if investment:
    .
    .
    .

if installment:
    .
    .
    .            
```

With everything righ, we now need to transform the string date came from the list into a datetime.date. So we can make some calculations with the dates.  
For making it we call the function `get_current_date()`.  
The function splits the string data and fix it together into a datetime.date variable.  
```
year = int(received_date.split("-")[0])
month = int(received_date.split("-")[1])
day = int(received_date.split("-")[2])

current_date = date(year, month, day)

return current_date
```

Finishing, we use the oldest and most comom way of get min and max values:
```
if current_date < initial_date:
    initial_date = current_date
if current_date > final_date:
    final_date = current_date
```

---

Having initial and final date ready, we now must start to build our cashflow.  
The function responsible for making it is `initiate_cashflow()`.    
This function sets a counter variable equal to the initial date, and go passing day by day until the counter reachs the final date.  
The cashflow is filled as a dictionary. The key is the current_date, and the value is set to 0.0 as default:

```
current_date = initial_date

while current_date <= final_date:
    cashflow[str(current_date)] = 0.0
    current_date += timedelta(days=1)
```

---

After initianting the cashflow, we need to put real values to its correct dates.  
So we must now call the `set_cashflow()` function  
Again we will use `zip_longest` function to query in both lists in paralel, and of course, checking if the iterator has a value:
```
for investment, installment in zip_longest(investments, installments,
                                               fillvalue=False):
    if investment:
    .
    .
    .

    if installment:
    .
    .
    .  
```

With everythin ok, we check if the key with the iterator date exists.  
If exists we store summing(installment) or subtracting(investment) the amount value at this key:
```
if investment["created_at"] in cashflow:
    cashflow[investment["created_at"]] -= \
        float(investment["amount"])
```
```
if installment["due_date"] in cashflow:
    cashflow[installment["due_date"]] += \
        float(installment["amount"])
```

With the cashflow properly setted, we can now calculate the IRR.  
For doing so, we will call the `calculate_irr()` function.  
The function gets all the values present in the cashflow, and uses the `numpy_financial.irr()` function for making the calculation:
```
data = []
for amount in cashflow.values():
    data.append(amount)

irr = round(npf.irr(data), 4)

return irr
```

### Building the extract
For not only returning the IRR, it's nice that we have some other relevant information.
So we have some functions  to get the information and show to the user.

The first two functions are `get_invested_value()` and `get_returned_value()`. Both sum the total amount of the values of its types, investment or installment.  
Querying through the cashflow we can say that if a value is smaller than zero, it's an investiment. If it is bigger than zero it's an installment:
```
def get_invested_value() -> float:
    """Calculate all value invested"""
    invested_value = 0.0
    for amount in cashflow.values():
        if amount < 0:
            invested_value -= amount

    return invested_value
```
```
def get_returned_value() -> float:
    """Calculate all value returned"""
    returned_value = 0.0
    for amount in cashflow.values():
        if amount > 0:
            returned_value += amount

    return round(returned_value, 2)
```

Other function is to get the percetage of the profit.  
Its called `get_profit_percentage()` and it only applies the most common algorithm to discover the percetage with the invested value and the profit value: 
```
profit_percentage = round((profit * 100) / invested_value, 2)

return f"{profit_percentage}%"
```

The last function is the `set_extract()`. It only receives all the information needed and mounts an extract with all the relevant information:
```
def set_extract(irr: float, invested_value: float, returned_value: float,
                profit: float, profit_percentage: str) -> str:
    """Builds an extract with all relevant information"""
    extract = f"""
        IRR: {irr}
        
        INVESTED VALUE: ${invested_value}
        RETURNED VALUE: ${returned_value}
        PROFIT: ${profit} ({profit_percentage})
        CASHFLOW DAYS: {len(cashflow)}
    """

    return extract
```


# How To Run Locally
Requirements:
- [Git](https://git-scm.com/downloads)
- [Python3.10](https://www.python.org/downloads/)

1. Clone the repository  
`https://github.com/salatiel6/TIR-Ulend.git`


2. Open the challenge directory  
Widows/Linux:`cd TIR-Ulend`  
Mac: `open TIR-Ulend`


3. Create virtual environment (recommended)  
`python -m venv ./venv`


4. Activate virtual environment (recommended)  
Windows: `venv\Scripts\activate`  
Linux/Mac: `source venv/bin/activate`


5. Install every dependencies  
`pip install -r requirements.txt`


6. Run the application  
`python main.py`