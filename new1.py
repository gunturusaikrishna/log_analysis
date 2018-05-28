import psycopg2
import time

# Database queries
# Database question 1: What are the most popular three articles of all time?
access_articles = """select articles.title, count(*) as num
            from log, articles
            where log.status='200 OK'
            and articles.slug = substr(log.path, 10)
            group by articles.title
            order by num desc
            limit 3;"""

# Database question 2: Who are the most popular article authors of all time?
access_authors = """select authors.name, count(*) as num
            from articles, authors, log
            where log.status='200 OK'
            and authors.id = articles.author
            and articles.slug = substr(log.path, 10)
            group by authors.name
            order by num desc;
            """

''' Database question 3:
 On which day did more than 1% of requests lead to errors?'''
access_errors = """select * from (
    select a.day,
    round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
    as errp from
        (select date(time) as day, count(*) as hits from log group by day)
        as a inner join
        (select date(time) as day, count(*) as hits from log where status
        like '%404%' group by day) as b
    on a.day = b.day)
as t where errp > 1.0;
"""
# Query data from the database, open and close the connection


def query_database(sql_request):

    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(sql_request)
    results = cursor.fetchall()
    conn.close()
    return results


# Printing title of the report
def print_as_title(title):
    print ("\n\t\t" + title + "\n")


# Printing the top 3 articles of all time
def topThree_articles():
    topThree_articles = query_database(access_articles)
    print_as_title("---Top 3 articles of all time---")

    for title, num in topThree_articles:
        print(" \"%s\" -- %d views" % (title, num))


# Printing the top authors of all time
def top_authors():
    top_authors = query_database(access_authors)
    print_as_title("---Top authors of all time---")

    for i, j in top_authors:
        print(" %s -- %d views" % (i, j))


# Printing the days in which more than 1% bad requests occured
def most_error_day():
    most_error_day = query_database(access_errors)
    print_as_title("---Days with more than 1% of bad requests---")

    for day, percentagefailed in most_error_day:
        print("""{0:%B %d, %Y} -- {1:.2f} % errors"""
              .format(day, percentagefailed))


if __name__ == '__main__':
    topThree_articles()
    top_authors()
    most_error_day()
