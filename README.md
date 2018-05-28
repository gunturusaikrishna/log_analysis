# log_analysis

## Introduction
This is a python module that uses information of large database of a web server and draw business conclusions from that information. The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. The database includes three tables:
* The **authors** table includes information about the authors of articles.
* The **articles** table includes the articles themselves.
* The **log** table includes one entry for each time a user has accessed the site.

#### The project drives fconclusions:
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
### Output:
![log.png](https://github.com/gunturusaikrishna/log_analysis/blob/master/log.png)

```
