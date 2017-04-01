from jira import JIRA
from models import *


def init():
    jira_server = raw_input("Server: ")
    jira_user = raw_input("User: ")
    jira_password = raw_input("Password: ")
    jira_server = {'server': jira_server}
    jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))
    return jira

jira = init()

def create_user(key):
    user = JiraUser.objects.filter(key=key)
    if len(user) == 0:
        user_json = jira.user(key)
        user = JiraUser()
        user.key = key
        user.name = user_json.name
        user.displayName = user_json.displayName
        user.emailAddress = user_json.emailAddress
        user.active = bool(user_json.active)
        user.save()
    else:
        user = user.get(0)
    return user


def create_project(id):
    project = Project.objects.filter(project_id=id)
    if len(project) == 0:
        project_json = jira.project(id)
        project = Project()
        project.description = project_json.description
        project.project_id = id
        project.key = project_json.key
        project.url = project_json.url
        project.name = project_json.name
        project.lead = create_user(project_json.lead.key)
        project.save()
    else:
        project = project.get(0)
    return project


def get_projects():
    projects = jira.projects()
    for project in projects:
        create_project(int(project.id))


def create_link_type(id):
    link_type = IssueLinkType.objects.filter(link_id=id)
    if len(link_type) == 0:
        link_type_json = jira.issue_link_type(id)
        link_type = IssueLinkType()
        link_type.inward = link_type_json.inward
        link_type.outward = link_type_json.outward
        link_type.name = link_type_json.name
        link_type.link_id = id
    else:
        link_type = link_type.get(0)
    return link_type


def get_link_types():
    link_types = jira.issue_link_types()
    for link_type in link_types:
        create_link_type(link_type.id)


def create_issue_type(id):
    issue_type = IssueType.objects.filter(type_id=id)
    if len(issue_type) == 0:
        issue_type_json = jira.issue_type(id)
        issue_type = IssueType()
        issue_type.name = issue_type_json.name
        issue_type.description = issue_type_json.description
        issue_type.type_id = id
        issue_type.save()
    else:
        issue_type = issue_type.get(0)
    return issue_type


def get_issue_types():
    create_issue_type(id)
    issue_types = jira.issue_types()
    for issue_type in issue_types:
        create_issue_type(issue_type.id)


def create_priority(id):
    priority = Priority.objects.filter(priority_id=id)
    if len(priority) == 0:
        priority_json = jira.issue_type(id)
        priority = Priority()
        priority.name = priority_json.name
        priority.description = priority_json.description
        priority.statusColor = priority_json.statusColor
        priority.iconUrl = priority_json.iconUrl
        priority.priority_id = id
        priority.save()
    else:
        priority = priority.get(0)
    return priority


def get_priorities():
    priorities = jira.priorities()
    for priority in priorities:
        create_priority(priority.id)


def create_component(id):
    component = Component.objects.filter(component_id=id)
    if len(component) == 0:
        component_json = jira.component(id)
        component = Component()
        component.name = component_json.name
        component.component_id = id
        if 'lead' in component_json.__dict__:
            component.lead = component_json.lead
        else:
            component.lead = None
        component.assigneeType = component_json.assigneeType
        component.project = create_project(component_json.project.id)
        component.save()
    else:
        component = component.get(0)
    return component


def get_components(project):
    components = jira.project_components(project)
    for component in components:
        create_component(id)


def get_statuses():
    statuses = jira.statuses()
    for status in statuses:
        create_status(status.id)


def create_status(id):
    status = IssueStatus.objects.filter(stat_id=id)
    if len(status) == 0:
        status_json = jira.status(id)
        status = IssueStatus()
        status.name = status_json.name
        status.stat_id = id
        status.description = status_json.description
        status.icon_url = status_json.iconUrl
        status.status_category = create_status_category(status.statusCategory)
        status.save()
    else:
        status = status.get(0)
    return status


def create_status_category(status_category_json):
    status_category = StatusCategory.objects.filter(stat_cat_id=status_category_json.id)
    if len(status_category) == 0:
        status_category = StatusCategory()
        status_category.name = status_category_json.name
        status_category.stat_cat_id = id
        status_category.key = status_category_json.key
        status_category.color_name = status_category_json.colorName
        status_category.save()
    else:
        status_category = status_category.get(0)
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
def create_issue(key):
    # issue = jira.issue('BIALPHASP-1027')
    issue = JiraIssue.objects.filter(key=key)
    if len(issue) == 0:
        issue = JiraIssue()
        issue_json = jira.issue(key)
        issue.key = issue_json.key
        issue.project = create_project(issue_json.raw['fields']['project']['id'])
        issue.assignee = issue_json.raw['fields']['assignee']
        issue.issue_type = create_issue_type(issue_json.raw['fields']['issuetype']['id'])
        issue.summary = issue_json.raw['fields']['summary']
        issue.description = issue_json.raw['fields']['description']
        issue.environment = issue_json.raw['fields']['environment']
        issue.priority = create_priority(issue_json.raw['fields']['priority']['id'])
        issue.resolution = issue_json.raw['fields']['resolution']
        issue.issue_status = create_status(issue_json.raw['fields']['status']['id'])
        issue.created = issue_json.raw['fields']['created']
        issue.updated = issue_json.raw['fields']['updated']
        issue.due_time = issue_json.raw['fields']['duedate']
        issue.votes = issue_json.raw['fields']['votes']
        issue.watches = issue_json.raw['fields']['watches']
        issue.time_original_estimate = issue_json.raw['fields']['timeoriginalestimate']
        issue.time_estimate = issue_json.raw['fields']['timeestimate']
        issue.time_spent = issue_json.raw['fields']['timespent']
        # issue_json.raw['fields']['creator']
        # print issue_json.raw['fields']['reporter']
        # issue_json.raw['fields']['progress']
        # print issue_json.raw['fields']['comment']
        issue.save()
    else:
        issue = issue.get(0)
    return issue
