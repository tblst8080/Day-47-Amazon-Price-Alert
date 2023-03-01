# Day-47-Amazon-Price-Alert
Day 47 of 100 days of python by Angela Yu.


1) Obtains Amazon url's from google doc via Sheety APi. 
2) Checks Amazon url's for price changes. 
3) After 7 days of observation, alert notifications are sent via email if price is 2 standard deviations below historical average.

To-Do's
1) Create a google doc with a single column of Amazon url's under column name: "url"
2) Connect google doc to Sheety, generate token, and enable retrieval permission
3) Insert personalized info in the .env file
4) Run code daily for at least 7 days
