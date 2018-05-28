# log_analysis

## Introduction
This is a python module that uses information of large database named newsdata.sql and draws conclusions from that information.The database includes three tables:
* The **authors** table includes information about the authors of articles.
* The **articles** table includes the articles themselves.
* The **log** table includes one entry for each time a user has accessed the site.

#### Conclusions:
* Top 3 articles of all time.
* Top authors of all time.
* Days with more than 1% of bad requests.

### Functions in news.py:
* **connect():** Connects to the PostgreSQL database and returns a database connection.
* **access_articles():** Prints Top 3 articles of all time.
* **access_authors():** Prints Top authors of all time.
* **access_errors():** Print Days with more than 1% of bad requests.

### Queries Made:
* <h4>access_articles</h4>
```select articles.title, count(*) as num
            from log, articles
            where log.status='200 OK'
            and articles.slug = substr(log.path, 10)
            group by articles.title
            order by num desc
            limit 3;
 ```           
* <h4>access_authors</h4>
```select authors.name, count(*) as num
            from articles, authors, log
            where log.status='200 OK'
            and authors.id = articles.author
            and articles.slug = substr(log.path, 10)
            group by authors.name
            order by num desc;
 ```
* <h4>access_errors</h4>
```select * from (
    select a.day,
    round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
    as errp from
        (select date(time) as day, count(*) as hits from log group by day)
        as a inner join
        (select date(time) as day, count(*) as hits from log where status
        like '%404%' group by day) as b
    on a.day = b.day)
as t where errp > 1.0;
```
## Steps to follow:

* First create one seperate folder for vagrant.

* From the vagrant folder open the terminal emulator.

* Install vagrant using command( sudo apt-get install vagrant).

* Install virtualbox using command( sudo apt-get install virtualbox).

* Initialize current directory to vagrant environment using command( vagrant init hashicorp/precise64).

* Now type (vagrant up).

* Then (vagrant ssh) to go to vagrant environment.

* sudo apt-get install python-psycopg2.

* Create database name as news.

* Download the datafile from this link https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip and place in vagrant folder.

* Type the command (cd /vagrant ) to make it into vagrant path.

* Now access the sql file with command ( psql -d news -f newsdata.sql).

* Now run the python file with command (python filename.py).

### Output:
![log.png](https://github.com/gunturusaikrishna/log_analysis/blob/master/log.png)

```
