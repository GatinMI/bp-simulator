import pprint

import psycopg2
import sys


def main():
    # Define our connection string
    conn_string = "host='jira-lab.bars.group' port='5432' dbname='jiradb' user='postgres' password='jstyJZAwFAo9'"

    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    cursor.execute("select owf.name from os_wfentry owf "
                   "inner join jiraissue ji on owf.id = ji.workflow_id "
                   "where ji.id = 19605")

    wfname = cursor.fetchall()

    pprint.pprint(wfname)

    cursor.execute("select * from jiraworkflows where workflowname=%s", (wfname))

    wfinfo = cursor.fetchall()

    pprint.pprint(wfinfo)


if __name__ == "__main__":
    main()
