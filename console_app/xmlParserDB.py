import xml.etree.ElementTree as ET
import pprint

import psycopg2
import sys

from console_app.jsonEntities.Workflow import *


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

    cursor.execute("select owf.name, jwf.descriptor from os_wfentry owf "
                   "inner join jiraissue ji on owf.id = ji.workflow_id "
                   "INNER JOIN jiraworkflows jwf on owf.name = jwf.workflowname "
                   "where ji.id = 19677")

    # wfname = cursor.fetchall()
    #
    # pprint.pprint(wfname)
    #
    # cursor.execute("select * from jiraworkflows where workflowname=%s", (wfname))

    wfinfo = cursor.fetchall()

    pprint.pprint(wfinfo[0][1])

    # return wfinfo[0][1]


if __name__ == "__main__":
    # main()
    # Define our connection string
    conn_string = "host='jira-lab.bars.group' port='5432' dbname='jiradb' user='postgres' password='jstyJZAwFAo9'"

    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    cursor.execute("select owf.name, jwf.descriptor from os_wfentry owf "
                   "inner join jiraissue ji on owf.id = ji.workflow_id "
                   "INNER JOIN jiraworkflows jwf on owf.name = jwf.workflowname "
                   "where ji.id = 19677")

    # wfname = cursor.fetchall()
    #
    # pprint.pprint(wfname)
    #
    # cursor.execute("select * from jiraworkflows where workflowname=%s", (wfname))

    wfinfo = cursor.fetchall()

    root = ET.fromstring(wfinfo[0][1])


    # root = tree.getroot()
    #
    # steps = tree.getiterator("step")
    #
    jswf = Workflow(wfinfo[0][0])

    for step in root.iter("step"):
        wf_step = Step(step.attrib['id'], step.attrib['name'])
        print '%s (%s)' % (step.attrib['name'], step.attrib['id'])
        # actions = step.find('actions').findall('action')
        for action in step.iter('action'):
            step_action = Action(action.attrib['id'], action.attrib['name'], action.find('results').find('unconditional-result').attrib['step'])
            wf_step.add_action(step_action)

            # results = action.iter('result')
            print '\t%s -> %s' % (action.attrib['name'], action.find('results').find('unconditional-result').attrib['step'])
        jswf.add_step(wf_step)



    print json.dumps(jswf, cls=MyEncoder, ensure_ascii=False).encode('utf8')





