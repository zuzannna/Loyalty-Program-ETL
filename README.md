# Data Challenge

In this data challenge my goal was to investigate the efficacy of the loyalty program. My insights are described below:

- Customers who are in the loyaty program tend to spend on average more money every time they shop (*t* = 4.85, *p* < 0.001) and they also shop more often. However, the loyalty program also costs money - with every applied discount the company spends 500 cents. It seems reasonable to take that into account and adjust the calculations.

![mean_purchase_value](mean_purchase_value.png)

- After adjusting for the cost of the discounts redeemed by the customers the difference in the average purchase value is no longer significant, *t* = -1.67, *p* > 0.05. If I had more time, I would look at the number of purchases - it is possible that since enrolled customers on average shop more often the total net revenue might still be higher.

![net_mean_purchase](net_mean_purchase.png)

- Most customers make their first purchase shortly after signing up for the loyalty program. Enrolled customers tend to spend more money on the purchase soon after becoming members, as indicated by a negative correlation *r* = -0.13, *p* < 0.001. The correlation is weak, but highly significant. 

![time_to_first_purchase](time_to_first_purchase.png)
![time_to_first_purchase_purchase_value](time_to_first_purchase_purchase_value.png)
