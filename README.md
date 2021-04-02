# Binance
Order status (status):
Status 	Description
NEW 	The order has been accepted by the engine.
PARTIALLY_FILLED 	A part of the order has been filled.
FILLED 	The order has been completed.
CANCELED 	The order has been canceled by the user.
PENDING_CANCEL 	Currently unused
REJECTED 	The order was not accepted by the engine and not processed.
EXPIRED 	The order was canceled according to the order type's rules (e.g. LIMIT FOK orders with no fill, LIMIT IOC or MARKET orders that partially fill)
or by the exchange, (e.g. orders canceled during liquidation, orders canceled during maintenance)

OCO Status (listStatusType):
Status 	Description
RESPONSE 	This is used when the ListStatus is responding to a failed action. (E.g. Orderlist placement or cancellation)
EXEC_STARTED 	The order list has been placed or there is an update to the order list status.
ALL_DONE 	The order list has finished executing and thus no longer active.
## Sources 

### Postman collection
https://github.com/binance-exchange/binance-api-postman

### Binance lib
https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#new-oco-trade

# Testing

Run all tests

```bash
python -m unittest discover -p "*_test.py"
```

Run specific

```bash
python -m unittest controllers.fileProcessor_test.py
```

### Technical analysis

# MACD

https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_convergence_divergence_macd

#### Pandas-ta

https://reposhub.com/python/deep-learning/twopirllc-pandas-ta.html
https://towardsdatascience.com/technical-analysis-library-to-financial-datasets-with-pandas-python-4b2b390d3543

#### Other lib and sources
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html


#### Pandas samples
https://stackoverflow.com/questions/17071871/how-to-select-rows-from-a-dataframe-based-on-column-values