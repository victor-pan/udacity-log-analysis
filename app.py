#!/usr/bin/env python3

"""Code for the news data utilities.

This module defines methods for interesting queries on the news database.

The main method allows users to choose a query from a list of options.

More queries can be added here in the future.
"""

import psycopg2
import os


def exec_query(query):
    """Execute a read on the database, and print the results to screen."""
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
            print(r[i], end="")
            if len(r) - i > 1:
                print(" - ", end="")
        print()
    print()


def find_top_articles():
    """Execute the Top 3 Articles query, printing results to screen."""
    # Look at SUCCESSFUL GETs only
    # match the URL slug to the article record
    query = """
        SELECT articles.title, count(log.id) Total
        FROM log, articles
        WHERE log.status='200 OK' AND log.method='GET' AND
              log.path LIKE '/article/%'
              AND substring(log.path from 10 for 999) = articles.slug
        GROUP BY articles.title
        ORDER BY Total DESC
        LIMIT 3;
    """
    exec_query(query)


def find_top_authors():
    """Execute the Top Authors query, printing results to screen."""
    # we can use article slug in a like comparison with the path
    # we look at *SUCCESSFUL* GETs for authors' articles.
    # We return the author's name, and the number of views.
    #
    #  hat off to Marc at SO for concatenation in join:
    #  https://stackoverflow.com/questions/13274679/like-with-on-column-names
    query = """
        SELECT authors.name Author, count(log.id) Number_Views
        FROM log LEFT JOIN articles ON
             log.path LIKE '/article/' || articles.slug
        JOIN authors ON articles.author = authors.id
        WHERE method='GET' AND status='200 OK' AND log.path LIKE '/article/%'
        GROUP BY authors.name
        ORDER BY Number_Views DESC;
    """
    exec_query(query)


def find_error_days():
    """Find webserver errors.

    Execute "Days with >1% Web Server Errors" and print results.
    """
    # I'm using the great date_trunc function, courtesy of Clodoaldo:
    #  https://stackoverflow.com/questions/14770829/grouping-timestamps-by-day-not-by-time
    #
    # I was initially using a substrings on each row,
    #  which on the VM took about 9 seconds.
    # Now I only use substring at the end, which takes about 3 seconds.
    #
    # We need to only count values with a 404 error.
    #  The idea of using COALESCE for the roll up comes from:
    #  https://stackoverflow.com/questions/5396498/postgresql-sql-count-of-true-values
    query = """
    SELECT substring(to_char(err_date, 'YYYY-MM-DD') FROM 1 FOR 10),
           round(pct_with_error, 2)
    FROM
        (SELECT date_trunc('day', time) err_date,
        COALESCE(100.0 * SUM(CASE WHEN status='404 NOT FOUND' THEN 1 ELSE 0 END) / COUNT(*), 0.0) as pct_with_error
        FROM log
        GROUP BY err_date) summary
    WHERE pct_with_error > 1.0
    """
    exec_query(query)


if __name__ == "__main__":
    """Main loop. Let user choose a query from a list of options."""
    done = False
    while (not done):
        print("Reporting Utilities")
        print(" 1) Find Three Most Popular Articles of All Time")
        print(" 2) Find Most Popular Article Authors of All Time")
        print(" 3) Display Days Where >1% of Requests Errored Out")
        print(" 4) Quit")
        try:
            my_choice = int(input("Select an option: "))
        except Exception as e:
            print("Oops. Something went wrong! Please try again")
            continue
        if my_choice == 1:
            find_top_articles()
        elif my_choice == 2:
            find_top_authors()
        elif my_choice == 3:
            find_error_days()
        else:
            done = True
