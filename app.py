#!/usr/bin/python
from __future__ import print_function # works in python 2.6 and higher
import psycopg2,os

# Executes a read on the database, and prints the results to screen
def exec_query(query):
    print()
    # Connect to the db
    db = psycopg2.connect(database="news")
    c = db.cursor()
    # execute select statement!
    c.execute(query)
    # print the results to screen
    results = c.fetchall()
    for r in results:
        for i in range(len(r)):
            print(r[i], end='')
            if len(r) - i > 1:
                print(" - ", end='')
        print()
    print()

# Executes the Top 3 Articles query, printing results to screen.
def find_top_articles():
    # Look at SUCCESSFUL GETs only
    # match the URL slug to the article record
    query = """
        select articles.title, count(log.id) Total from log, articles
        where status='200 OK' and method='GET' and path like '/article/%'
              and substring(path from 10 for 999) = articles.slug
        group by articles.title
        order by Total desc
        limit 3;
    """
    exec_query(query)


# Executes the Top Authors query, printing results to screen.
#  hat off to Marc at SO for concatenation in join:
#  https://stackoverflow.com/questions/13274679/like-with-on-column-names
def find_top_authors():
    # we can use article slug in a like comparison with the path
    # we look at *SUCCESSFUL* GETs for authors' articles.
    # We return the author's name, and the number of views.
    query = """
        select authors.name Author, count(log.id) Number_Views from log
        left join articles on log.path like '/article/' || articles.slug
        join authors on articles.author = authors.id
        where method='GET' and status='200 OK' and path like '/article/%'
        group by authors.name
        order by Number_Views desc;
    """
    exec_query(query)

# Executes the "Days with >1% Web Server Errors" query,
#  printing results to screen.
def find_error_days():
    # Here I'm using substring():
    #  https://www.postgresql.org/docs/9.1/static/functions-string.html
    # I'm also converting timestamps to strings:
    #  https://www.postgresql.org/docs/9.1/static/functions-formatting.html
    # Finally, we need to only count values with a 404 error
    #  This can be done in many different ways:
    #  https://stackoverflow.com/questions/5396498/postgresql-sql-count-of-true-values
    #  I use some of the ideas from the post above, as well as a subselect
    query = """
    select err_date, round(pct_with_error, 2) from
        (select COALESCE(100.0 * sum(case when status='404 NOT FOUND' then 1 else 0 end), 0) / count(*) as pct_with_error,
                substring(to_char(time, 'YYYY-MM-DD') from 1 for 10) err_date
        from log
        group by err_date) summary
    where pct_with_error > 1.0
    """
    exec_query(query)

# Main loop. Lets user choose a query from a list of options.
if __name__ == "__main__":
    done = False
    while (not done):
        print("Reporting Utilities")
        print(" 1) Find Three Most Popular Articles of All Time")
        print(" 2) Find Most Popular Article Authors of All Time")
        print(" 3) Display Days Where >1% of Requests Errored Out")
        print(" 4) Quit")
        try:
            my_choice = int(raw_input("Select an option: "))
        except:
            print("Oops. Something went wrong! Please try again")
            continue
        if my_choice==1:
            find_top_articles()
        elif my_choice==2:
            find_top_authors()
        elif my_choice==3:
            find_error_days()
        else:
            done=True
