# coding: utf-8
import sys
import psycopg2
import xml.etree.ElementTree as ET

from console_app.jsonEntities.Workflow import *

reload(sys)
sys.setdefaultencoding('utf-8')

from jira import JIRA, JIRAError
from models import *
from pony.orm import *
from datetime import datetime
from django.utils.dateparse import parse_datetime
import pytz


class JiraConnector:
    jira = None
    server = ''
    user = ''
    password = ''
    port = '8080'
    db_port = '5432'

    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.jira = JIRA(options={'server': 'http://%s:%s' % (server, self.port)},  basic_auth=(user, password))

    @db_session
    def get_user(self, key):
        user = JiraUser.get(key=key)
        if (user == None):
            user_json = self.jira.user(key)
            user = JiraUser(key=key)
            user.name = user_json.name
            user.displayName = user_json.displayName
            user.emailAddress = user_json.emailAddress
            user.active = bool(user_json.active)
        return user

    @db_session
    def get_project(self, id):
        # нужны ли версии? project.versions
        project = Project.get(project_id=id)
        if (project == None):
            project_json = self.jira.project(id)
            project = Project(project_id=id)
            if hasattr(project_json, 'url'):
                project.url = project_json.url
            project.description = project_json.description
            project.key = project_json.key
            project.name = project_json.name
            project.lead = self.get_user(project_json.lead.key)
        return project

    @db_session
    def get_link_type(self, id):
        link_type = IssueLinkType.get(link_id=id)
        if (link_type == None):
            link_type_json = self.jira.issue_link_type(id)
            link_type = IssueLinkType(link_id=id)
            link_type.inward = link_type_json.inward
            link_type.outward = link_type_json.outward
            link_type.name = link_type_json.name
        return link_type

    def get_link_types(self):
        link_types = self.jira.issue_link_types()
        for link_type in link_types:
            self.get_link_type(link_type.id)

    @db_session
    def get_issue_type(self, id):
        issue_type = IssueType.get(type_id=id)
        if (issue_type == None):
            issue_type_json = self.jira.issue_type(id)
            issue_type = IssueType(type_id=id)
            issue_type.name = issue_type_json.name
            issue_type.description = issue_type_json.description
        return issue_type

    def get_issue_types(self):
        self.get_issue_type(id)
        issue_types = self.jira.issue_types()
        for issue_type in issue_types:
            self.get_issue_type(issue_type.id)

    @db_session
    def get_priority(self, id):
        priority = Priority.get(priority_id=id)
        if (priority == None):
            priority_json = self.jira.priority(id)
            priority = Priority(priority_id=priority_json.id)
            priority.name = priority_json.name
            priority.description = priority_json.description
            priority.statusColor = priority_json.statusColor
            priority.iconUrl = priority_json.iconUrl
        return priority

    def get_priorities(self):
        priorities = self.jira.priorities()
        for priority in priorities:
            self.get_priority(priority.id)

    @db_session
    def create_component(self, id):
        component = Component.get(component_id=id)
        if component == None:
            component_json = self.jira.component(id)
            component = Component(component_id=id)
            component.name = component_json.name
            if 'lead' in component_json.__dict__:
                component.lead = component_json.lead
            else:
                component.lead = None
            component.assigneeType = component_json.assigneeType
            component.project = self.get_project(component_json.project.id)
        return component

    def get_components(self, project):
        components = self.jira.project_components(project)
        for component in components:
            self.create_component(component.id)

    def get_statuses(self):
        statuses = self.jira.statuses()
        for status in statuses:
            self.get_status(status.id)

    @db_session
    def get_status(self, id):
        status = IssueStatus.get(stat_id=id)
        if status == None:
            status_json = self.jira.status(id)
            status = IssueStatus(stat_id=id)
            status.name = status_json.name
            status.description = status_json.description
            status.icon_url = status_json.iconUrl
            # status.status_category = create_status_category(status.statusCategory) ???
        return status

    @db_session
    def get_status_category(self, status_category_json):
        status_category = StatusCategory.get(stat_cat_id=status_category_json.id)
        if status_category == None:
            status_category = StatusCategory()
            status_category.name = status_category_json.name
            status_category.stat_cat_id = id
            status_category.key = status_category_json.key
            status_category.color_name = status_category_json.colorName
            status_category.save()
        return status_category

    def get_issues(self, project_id):
        issues = self.jira.search_issues('project=' + project_id)
        for issue in issues:
            self.create_or_update_issue(issue.key, issue.id)

    # TODO
    def get_version_projects(self, project):
        project_versions = self.jira.project_versions(project)
        for version_json in project_versions:
            pass
            # TODO
            # print version.name
            # print version.self
            # print version.released
            # print version.archived
            # if 'releaseDate' in version.__dict__:
            #     print version.releaseDate
            # if 'startDate' in version.__dict__:
            #     print version.startDate

#Создание или обновление issue
    @db_session
    def create_or_update_issue(self, id, jira_id):
        jira_issue = JiraIssue.get(key=id)
        issue = self.jira.issue(id)
        if (jira_issue == None):
            jira_issue = JiraIssue(key=id)

        utc = pytz.UTC
        issue_updated = parse_datetime(issue.fields.updated)
        if (jira_issue.updated == None or issue_updated > utc.localize(jira_issue.updated)):
            jira_issue.project = self.get_project(issue.fields.project.id)
            jira_issue.jira_id = jira_id
            if issue.fields.assignee and len(issue.fields.assignee.key) > 0:
                jira_issue.assignee = self.get_user(issue.fields.assignee.key)
            if issue.fields.issuetype:
                jira_issue.issue_type = self.get_issue_type(issue.fields.issuetype.id)
            if issue.fields.summary:
                jira_issue.summary = issue.fields.summary
            if issue.fields.description:
                jira_issue.description = issue.fields.description
            if issue.fields.environment:
                jira_issue.environment = issue.fields.environment
            if issue.fields.priority:
                jira_issue.priority = self.get_priority(issue.fields.priority.id)
            if issue.fields.resolution:
                jira_issue.resolution = issue.fields.resolution.name
            if issue.fields.status:
                jira_issue.issue_status = self.get_status(issue.fields.status.id)
            jira_issue.created = parse_datetime(issue.fields.created)
            jira_issue.updated = parse_datetime(issue.fields.updated)
            if issue.fields.duedate:
                jira_issue.due_time = parse_datetime(issue.fields.duedate)
            jira_issue.votes = issue.fields.votes.votes
            jira_issue.watches = issue.fields.watches.watchCount
            jira_issue.time_original_estimate = issue.fields.timeoriginalestimate
            jira_issue.time_estimate = issue.fields.timeestimate
            jira_issue.time_spent = issue.fields.timespent
            wf = self.sync_issue_wf(jira_id)
            jira_issue.workflow_id = wf.id
        return jira_issue

#Синхронизация проектов
    @db_session
    def sync_projects(self):
        projects = self.jira.projects()
        db_projects = select(p.project_id for p in Project)[:]
        projects_id = []
        for project in projects:
            projects_id.append(project.id)
            if project.id not in db_projects:
                self.get_project(int(project.id))
            else:
                self.project_update(int(project.id))
            self.sync_issues(int(project.id))
        drop_projects = set(db_projects).difference(set(projects_id))
        Project.select(lambda p: p.project_id in drop_projects).delete(bulk=True)
        for id in drop_projects:
            self.delete_issues(int(id))

#Синхронизация issue
    @db_session
    def sync_issues(self, project_id):
        issues = self.jira.search_issues('project=' + str(project_id))
        db_issues = select(p.key for p in JiraIssue)[:]
        issues_id = []
        for issue in issues:
            try:
                issues_id.append(issue.key)
                self.create_or_update_issue(issue.key, issue.id)
            except JIRAError as error:
                print "Sorry, but you can't access to issue # "
                print issue
                if error.status_code == 404:
                    print ". Because  you don't have permission"
                else:
                    print ". Because project was deleted"
        drop_issues = set(db_issues).difference(set(issues_id))
        Project.select(lambda p: p.project_id in drop_issues).delete(bulk=True)

    @db_session
    def delete_issues(self, project_id):
        issues = JiraIssue.select(lambda p: p.project.id == project_id)[:]
        for issue in issues:
            issue.delete()

    @db_session
    def delete_issue(self, issue_key):
        issue = JiraIssue.get(key=issue_key)
        issue.delete()

    @db_session
    def project_update(self, project_id):
        project = Project.get(project_id=project_id)
        if (project != None):
            project_json = self.jira.project(id)
            if hasattr(project_json, 'url'):
                project.url = project_json.url
            project.description = project_json.description
            project.key = project_json.key
            project.name = project_json.name
            project.lead = self.get_user(project_json.lead.key)

    @db_session
    def sync_issue_wf(self, issue_key):
        # Define our connection string
        conn_string = "host='%s' port='%s' dbname='jiradb' user='postgres' password='%s'" % (self.server, self.db_port, self.password)

        jira_issue = JiraIssue.get(key=issue_key)

        # print the connection string we will use to connect

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        cursor.execute("select owf.name, jwf.descriptor from os_wfentry owf "
                       "inner join jiraissue ji on owf.id = ji.workflow_id "
                       "INNER JOIN jiraworkflows jwf on owf.name = jwf.workflowname "
                       "where ji.id = %s" % jira_issue.jira_id)

        wfinfo = cursor.fetchall()

        root = ET.fromstring(wfinfo[0][1])

        jswf = Workflow(wfinfo[0][0])

        for step in root.iter("step"):
            wf_step = Step(step.attrib['id'], step.attrib['name'])
            for action in step.iter('action'):
                step_action = Action(action.attrib['id'], action.attrib['name'],
                                     action.find('results').find('unconditional-result').attrib['step'])
                wf_step.add_action(step_action)
            jswf.add_step(wf_step)

        print json.dumps(jswf, cls=MyEncoder, ensure_ascii=False).encode('utf8')

        jira_wf = JiraWorkflow(name=jswf.name)
        jira_wf.descriptor = json.dumps(jswf, cls=MyEncoder)
        return jira_wf

if __name__ == "__main__":
    accessor = JiraConnector("", '', '')

    projects = accessor.jira.projects()

    project = accessor.jira.project(projects[0])

    issue = accessor.jira.search_issues('project=%s' % project)[1]

    print issue

    accessor.create_or_update_issue(issue.key, issue.id)

    # result = accessor.sync_issue_wf(issue.key)

    # print result

    # jira_issue = accessor.create_or_update_issue(issue.id)

    # import json
    # file = open('project.json', 'w')
    # json.dump(project, file)
    # file.close()

    # print project.id
