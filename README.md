# Easy News Website Reports

This provides a framework for allowing non-report writers to run useful queries on the Udacity news database. By using a simple menu-based interface, users can find out the most popular news articles and authors, and when the web server was underperforming.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run this project, you must be running [Postgres](https://www.postgresql.org/download/) and [Python 3](https://www.python.org/downloads/) (both available for Windows, Max OS X, and Linux).

Your local database must be a Postgres database named `news`, and must conform to the schema in the schema section below.

### Installing

Follow the links above to download Postgres and Python 3.

Alternatively, [this Udacity page](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91) has links to download a virtual machine that contains Python and Postgres, and a link to an example SQL database that you can import for use on your development machine.

Regardless, be sure to visit the Udacity site to download the newsdata.zip file.

Next, clone the git repo
```
git clone https://github.com/victor-pan/udacity-web-log-analysis.git
```

Ensure the app.py file is in the same directory as the .sql file.

Now, you are finally ready to use the application
```
$ ./python app.py
TODO -- more details
```
See the output.txt file for a complete sample output.

### Database Schema
This project was designed to work with a local test database, however it could work with a live webserver log database if it conforms to the following schema. For full details, install the example newsdata.sql file and view the data definitions from Postgres.

## Relations
```
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | articles | table | vagrant
 public | authors  | table | vagrant
 public | log      | table | vagrant
```

### articles
 Column |           Type           |                       Notes            
--------+--------------------------+--------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null, replaces whitespace with dashes, should be unique
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null, sequential

### authors
```
 Column |  Type   |                      Notes
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null, sequential
```

### log
```
 Column |           Type           |                    Notes               
--------+--------------------------+--------------------------------------------
 path   | text                     | ex. /article/balloon-goons-doomed, notice the final piece is the article slug
 ip     | inet                     |
 method | text                     |
 status | text                     | status code with name of status, ex. '202 OK'
 time   | timestamp with time zone | default now()
 id     | integer                  | not null, sequential
```

## Running the tests

### End to End Tests
Run the application
```
$ python ./app.py
```
Select whichever queries you want to run. Validate the query results by manual inspection on small datasets.

### Coding style tests
Use pep257 and pycodestyle to test the app's PEP compliance.

To install pep257
```
pip install 257
```
To run pep257
```
pep257 app.py
```

To install pycodestyle (which has replaced pep8)
```
pip install pycodestyle
```
To run pycodestyle
```
pycodestyle app.py
```

## Deployment

To deploy this to a live system, it is recommended you add the ability for the user to enter a username and password and compile the Python code.

## Built With

* [Python](https://www.python.org/) - Application code, DB-API
* [PostgreSQL](https://www.postgresql.org/) - Relational database

## Contributing

Please read [CONTRIBUTING.md](https://github.com/victor-pan/udacity-web-log-analysis/blob/master/CONTRIBUTING.md) for the process for submitting pull requests.

## Versioning

We use [Git](https://git-scm.com/) for versioning. For the versions available, see the [tags on this repository](https://github.com/victor-pan/udacity-web-log-analysis/tags). 

## Authors

* **Victor Pan** - *Initial work* - [victor-pan](https://github.com/victor-pan)

Also thanks to [Udacity](https://classroom.udacity.com) for the idea for and input on this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
[Udacity](https://classroom.udacity.com) for the idea for and input on this project.