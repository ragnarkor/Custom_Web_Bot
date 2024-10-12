# Flow chart of Hikiniku_To_Come_Bot

1. Input Data
    - url
    - driver setting
    - party size
    - time slot

2. Check if input data valid
    - check party size range
        - Range: 1 - 4
    - check time slot range and format
        - Range: 11:00 - 21:15
        - Format: HHMM

3. Booker info loader
    - load booker_info.yml

4. Try each time slot
    - load driver access to the url
    - loop each time slot to a function
        - select party size
        - select date
        - select time slot
        - input booker info and credit card info

## Code template
```Python
driver = uc.Chrome(options=options)
driver.get(url)

booker_info = _load_yml()

try:
    bot = Booking(driver)

    bot.select_partysize(party_size)

    bot.select_date(date)

    for time_slot in time slot:
        bot.select_time_slot(time_slot)

        bot.payment(booker_info)
