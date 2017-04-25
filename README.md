# Investigating customer transactions

Analyzing customer transactions is crucial for every business. How often they shop? What's their average spending? Does enrollment in a loyalty program influence their spending habits? These are some of the questions I attempted to answer here. 

## Creating the ETL pipeline

First, my goal was to write a script that __extracts__ the data from the provided CSV files and __uploads__ it to a local database.

### Data

Data consists of two .csv files, <code>customers.csv</code> and <code>transactions.csv</code> which I uploaded into a local database using SQLite, joined and performed basic aggregation to fill in missing colums. 

__customers.csv__: The customer CSV file provides a list of customer data, where each row represents a unique customer. Each column represents an attribute or value associated with the customer. The columns include:

1. <code>id</code>: unique user identification number

2. <code>date</code>: date the user signed up for the service

3. <code>loyalty</code>: Whether the user is enrolled in the program (enrolled) or part of the control group (control)

4. <code>location</code>: Location attribute

5. <code>age</code>: Age attribute

6. <code>favorite_movie_line</code>: Favorite movie line of all time

7. <code>number_of_purchases</code>: Total number of purchases

8. <code>value_of_purchases</code>: Total value of purchases (in cents)

9. <code>total_standard_points</code>: Total standard points earned from purchases (if enrolled in loyalty)

10. <code>total_points_redeemed</code>: Total points redeemed for purchase discount

__transactions.csv__: The transaction CSV file provides a list of all transactions completed over a 2 year time period. Each column represents an attribute or value associated with a transaction.

1. <code>date</code>: date the transaction was completed
2. <code>user_id</code>: The id of the user that completed the transaction
3. <code>value</code>: The value of the transaction (in cents)
4. <code>point_differential</code>: The difference between points earned and points redeemed (i.e. pointsdifferential = standardpointsearned - pointsredeemed)

## Creating the database

I created a local database with the following commands:

<pre>
try:
    # Open the connection
    conn = sqlite3.connect('customers_transactions.db')
    # Write the customers and transactions data frames to a local database
    transactions.to_sql("Transactions", conn, flavor='sqlite',index=False)
    customers.to_sql("Customers", conn, flavor='sqlite',index=False)
    # Close the connection
    conn.close()
except ValueError:
    print 'Database already in the current directory, move on.'
</pre>

If the database already exists, it will raise an error and move on.

## Join & Aggregate

With the data loaded into my database, I wrote a script that extracts the data from local database and fills in the missing values in the following columns:

<code>number_of_purchases</code>
<code>value_of_purchases</code>
<code>total_standard_points</code>
<code>total_points_redeemed</code>

With the following SQLite query:

<pre>
# Open the connection
conn = sqlite3.connect('customers_transactions.db')
a = conn.cursor()

# Write the SQLite query executed in the next step
sql_query = "SELECT user_id, loyalty, signup_date, location,\
            gender, age, favorite_movie_line,\
            count(user_id) as number_of_purchases,\
            sum(value) as value_of_purchases,\
            CASE loyalty\
                WHEN 'control' THEN\
                    0\
                ELSE\
                    sum(round((value/100)*100)/10)\
                END total_standard_points,\
            CASE loyalty\
                WHEN 'control' THEN\
                    0\
                ELSE\
                    sum(round((round((Transactions.value/100)*100)/10 - \
            Transactions.point_differential)/1000)*1000)\
                END total_points_redeemed\
            FROM Transactions JOIN Customers on user_id = id\
            GROUP BY user_id ORDER BY user_id"

df = pd.read_sql_query(sql_query, conn)

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()
</pre>

In the .pynb file you will find an alternative analysis using <code>pandas</code> package. The advantage of using the SQL database is that it runs __much__ faster.

## Insights about the loyalty program

Next, my goal was to investigate the efficacy of the loyalty program. I grouped the conclusions of my analysis into executive summary below:

- Customers who are in the loyaty program tend to spend on average more money every time they shop (*t* = 4.85, *p* < 0.001) and they also shop more often. However, the loyalty program also costs money - with every applied discount the company spends 500 cents. It seems reasonable to take that into account and adjust the calculations.

![mean_purchase_value](images/mean_purchase_value.png)

- After adjusting for the cost of the discounts redeemed by the customers the difference in the average purchase value is no longer significant, *t* = -1.67, *p* > 0.05. If I had more time, I would look at the number of purchases - it is possible that since enrolled customers on average shop more often the total net revenue might still be higher.

![net_mean_purchase](images/net_mean_purchase.png)

- Most customers make their first purchase shortly after signing up for the loyalty program. Enrolled customers tend to spend more money on the purchase soon after becoming members, as indicated by a negative correlation *r* = -0.13, *p* < 0.001. The correlation is weak, but highly significant. 

![time_to_first_purchase](images/time_to_first_purchase.png)
![time_to_first_purchase_purchase_value_outlier](images/time_to_first_purchase_purchase_value_outlier.png)

# Testing

To test the code to make sure it works run the following command in your terminal shell from the <code>/Loyalty-Program-ETL/</code>directory:

    python code/test_utilities.py    

You will then see a report on the testing results.

# Requirements:

1. <a href="https://www.python.org/"> Python</a> (2.7)
2. <a href="http://jupyter.org/">Jupyter Notebook</a>
3. <a href="http://www.numpy.org/">NumPy</a>
4. <a href="http://www.scipy.org/">SciPy</a>
5. <a href="http://matplotlib.org/">matplotlib</a>
6. <a href="http://pandas.pydata.org">Pandas</a>
7. <a href="http://scikit-learn.org/stable/">scikit learn</a>
8. <a href="http://seaborn.pydata.org">seaborn</a>
9. <a href="https://www.sqlite.org">SQLite</a>

To install all of them (except Python) using pip run:
<pre>
 pip install -r requirements.txt
</pre>

