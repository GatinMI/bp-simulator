from jira import JIRA
from models import *


def init():
    jira_server = "********"
    jira_user = "*********"
    jira_password = "********"
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


# TODO
def get_statuses():
    statuses = jira.statuses
    status = jira.status(1)
    print status.name
    print status.id
    print status.description
    print status.self
    print status.iconUrl
    print status.statusCategory


# TODO
def create_status(id):
    pass


# TODO
def create_status_category(id):
    pass


# TODO
def create_issues():
    pass


# TODO
def get_version_projects(project):
    project_versions = jira.project_versions(project)
    for version in project_versions:
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
def get_issue(key):
    issue = jira.issue('BIALPHASP-1027')
    print issue.key
    print issue.raw['fields']['created']
    print issue.raw['fields']['project']
    print issue.raw['fields']['issuetype']
    print issue.raw['fields']['status']
    print issue.raw['fields']['creator']
    print issue.raw['fields']['reporter']
    print issue.raw['fields']['description']
    print issue.raw['fields']['progress']
    print issue.raw['fields']['comment']
    print issue.raw['fields']['priority']
    print issue.raw['fields']['updated']
    print issue.raw['fields']['duedate']
    print issue.raw['fields']['resolutiondate']
    print issue.raw['fields']['votes']
    print issue.raw['fields']['watches']
    print issue.raw['fields']['timeoriginalestimate']
    print issue.raw['fields']['timeestimate']
    print issue.raw['fields']['timespent']
    print issue.raw['fields']['resolution']
    print issue.raw['fields']['assignee']
    print issue.raw['fields']['summary']
    print issue.raw['fields']['environment']
