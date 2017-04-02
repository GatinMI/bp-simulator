import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from jira import JIRA, JIRAError
from models import *
from pony.orm import *
from datetime import datetime
from django.utils.dateparse import parse_datetime


def init():
    jira_server = "http://jira-lab.bars.group:8080"
    jira_user = raw_input("User: ")
    jira_password = raw_input("Password: ")
    jira_server = {'server': jira_server}
    jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))
    return jira


jira = init()





# jira.project_components('project=NIALPHABI')

# json = jira._get_json()
# print json

@db_session
def create_user(key):
    user = JiraUser.get(key=key)
    if (user == None):
        user_json = jira.user(key)
        user = JiraUser(key=key)
        user.name = user_json.name
        user.displayName = user_json.displayName
        user.emailAddress = user_json.emailAddress
        user.active = bool(user_json.active)
    return user


@db_session
def create_project(id):
    project = Project.get(project_id=id)
    if (project == None):
        project_json = jira.project(id)
        project = Project(project_id=id)
        if hasattr(project_json, 'url'):
            project.url = project_json.url
        project.description  = project_json.description
        project.key = project_json.key
        project.name = project_json.name
        project.lead = create_user(project_json.lead.key)
    return project


def get_projects():
    projects = jira.projects()
    for project in projects:
        create_project(int(project.id))


@db_session
def create_link_type(id):
    link_type = IssueLinkType.get(link_id=id)
    if (link_type == None):
        link_type_json = jira.issue_link_type(id)
        link_type = IssueLinkType(link_id=id)
        link_type.inward = link_type_json.inward
        link_type.outward = link_type_json.outward
        link_type.name = link_type_json.name
    return link_type


def get_link_types():
    link_types = jira.issue_link_types()
    for link_type in link_types:
        create_link_type(link_type.id)


@db_session
def create_issue_type(id):
    issue_type = IssueType.get(type_id=id)
    if (issue_type == None):
        issue_type_json = jira.issue_type(id)
        issue_type = IssueType(type_id=id)
        issue_type.name = issue_type_json.name
        issue_type.description = issue_type_json.description
    return issue_type


def get_issue_types():
    create_issue_type(id)
    issue_types = jira.issue_types()
    for issue_type in issue_types:
        create_issue_type(issue_type.id)


@db_session
def create_priority(id):
    priority = Priority.get(priority_id=id)
    if (priority == None):
        priority_json = jira.priority(id)
        priority = Priority(priority_id=priority_json.id)
        priority.name = priority_json.name
        priority.description = priority_json.description
        priority.statusColor = priority_json.statusColor
        priority.iconUrl = priority_json.iconUrl
    return priority


def get_priorities():
    priorities = jira.priorities()
    for priority in priorities:
        create_priority(priority.id)


@db_session
def create_component(id):
    component = Component.get(component_id=id)
    if component == None:
        component_json = jira.component(id)
        component = Component(component_id=id)
        component.name = component_json.name
        if 'lead' in component_json.__dict__:
            component.lead = component_json.lead
        else:
            component.lead = None
        component.assigneeType = component_json.assigneeType
        component.project = create_project(component_json.project.id)
    return component


def get_components(project):
    components = jira.project_components(project)
    for component in components:
        create_component(component.id)


def get_statuses():
    statuses = jira.statuses()
    for status in statuses:
        create_status(status.id)


@db_session
def create_status(id):
    status = IssueStatus.get(stat_id=id)
    if status == None:
        status_json = jira.status(id)
        status = IssueStatus(stat_id=id)
        status.name = status_json.name
        status.description = status_json.description
        status.icon_url = status_json.iconUrl
        # status.status_category = create_status_category(status.statusCategory) ???
    return status


@db_session
def create_status_category(status_category_json):
    status_category = StatusCategory.get(stat_cat_id=status_category_json.id)
    if status_category == None:
        status_category = StatusCategory()
        status_category.name = status_category_json.name
        status_category.stat_cat_id = id
        status_category.key = status_category_json.key
        status_category.color_name = status_category_json.colorName
        status_category.save()
    return status_category


# TODO
def get_issues(project_id):
    issues = jira.search_issues('project=' + project_id)
    for issue in issues:
        create_issue(issue.key)


# TODO
def get_version_projects(project):
    project_versions = jira.project_versions(project)
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


# TODO
@db_session
def create_issue(key):
    # issue = jira.issue('BIALPHASP-1027')
    issue = JiraIssue.get(key=key)
    if (issue == None):
        issue_json = jira.issue(key)
        issue = JiraIssue(key=issue_json.key)
        issue.project = create_project(issue_json.fields.project.id)
        if issue_json.fields.assignee and len(issue_json.fields.assignee.key) > 0:
            issue.assignee = create_user(issue_json.fields.assignee.key)
        if issue_json.fields.issuetype:
            issue.issue_type = create_issue_type(issue_json.fields.issuetype.id)
        if issue_json.fields.summary:
            issue.summary = issue_json.fields.summary
        if issue_json.fields.description:
            issue.description = issue_json.fields.description
        if issue_json.fields.environment:
            issue.environment = issue_json.fields.environment
        if issue_json.fields.priority:
            issue.priority = create_priority(issue_json.fields.priority.id)
        if issue_json.fields.resolution:
            issue.resolution = issue_json.fields.resolution.name
        if issue_json.fields.status:
            issue.issue_status = create_status(issue_json.fields.status.id)
        issue.created = parse_datetime(issue_json.fields.created)
        issue.updated = parse_datetime(issue_json.fields.updated)
        if issue_json.fields.duedate:
            issue.due_time = parse_datetime(issue_json.fields.duedate)
        issue.votes = issue_json.fields.votes.votes
        issue.watches = issue_json.fields.watches.watchCount
        issue.time_original_estimate = issue_json.fields.timeoriginalestimate
        issue.time_estimate = issue_json.fields.timeestimate
        issue.time_spent = issue_json.fields.timespent
        # issue_json.raw['fields']['creator']
        # print issue_json.raw['fields']['reporter']
        # issue_json.raw['fields']['progress']
        # print issue_json.raw['fields']['comment']
    return issue


# issue = jira.issue('BIALPHABI-3024')
# issue = jira.issue('BIALPHASP-1061')
# issue = jira.issue('BIMONEU-1174')
# print issue.raw["fields"]["watches"]

# print issue.raw

# print issue.fields.assignee

# print issue.raw["fields"]["project"]
# print issue.raw["fields"]

# print issue.raw["fields"]["assignee"]
# create_issue(issue.key)
#
projects = jira.projects()
for project in projects:
    print project
    try:
        issues = jira.search_issues('project=%s' % project)

        for issue in issues:
            print issue
            ji = create_issue(issue.key)
            print ji

    except JIRAError:
        print "Can't connect"



# with db_session:
#     jira_issue = JiraIssue.get(key="BIALPHABI-3024")
#     print jira_issue.project.name

