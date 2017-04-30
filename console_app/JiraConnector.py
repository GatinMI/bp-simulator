import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from jira import JIRA, JIRAError
from models import *
from pony.orm import *
from datetime import datetime
from django.utils.dateparse import parse_datetime

class JiraConnector:
    jira = None
    server = ''
    user = ''
    password = ''


    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.jira = JIRA(options={'server': server}, basic_auth=(user, password))

    @db_session
    def create_user(self, key):
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
    def create_project(self, id):
        project = Project.get(project_id=id)
        if (project == None):
            project_json = self.jira.project(id)
            project = Project(project_id=id)
            if hasattr(project_json, 'url'):
                project.url = project_json.url
            project.description  = project_json.description
            project.key = project_json.key
            project.name = project_json.name
            project.lead = self.create_user(project_json.lead.key)
        return project


    def get_projects(self):
        projects = self.jira.projects()
        for project in projects:
            self.create_project(int(project.id))


    @db_session
    def create_link_type(self, id):
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
            self.create_link_type(link_type.id)


    @db_session
    def create_issue_type(id):
        issue_type = IssueType.get(type_id=id)
        if (issue_type == None):
            issue_type_json = jira.issue_type(id)
            issue_type = IssueType(type_id=id)
            issue_type.name = issue_type_json.name
            issue_type.description = issue_type_json.description
        return issue_type


    def get_issue_types(self):
        self.create_issue_type(id)
        issue_types = self.jira.issue_types()
        for issue_type in issue_types:
            self.create_issue_type(issue_type.id)


    @db_session
    def create_priority(self, id):
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
            self.create_priority(priority.id)


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
            component.project = self.create_project(component_json.project.id)
        return component


    def get_components(self, project):
        components = self.jira.project_components(project)
        for component in components:
            self.create_component(component.id)


    def get_statuses(self):
        statuses = self.jira.statuses()
        for status in statuses:
            self.create_status(status.id)


    @db_session
    def create_status(self, id):
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
    def create_status_category(self, status_category_json):
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
    def get_issues(self, project_id):
        issues = self.jira.search_issues('project=' + project_id)
        for issue in issues:
            self.create_issue(issue.key)


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


    # TODO
    @db_session
    def create_issue(self,key):
        issue = JiraIssue.get(key=key)
        if (issue == None):
            issue_json = self.jira.issue(key)
            issue = JiraIssue(key=issue_json.key)
            issue.project = self.create_project(issue_json.fields.project.id)
            if issue_json.fields.assignee and len(issue_json.fields.assignee.key) > 0:
                issue.assignee = self.create_user(issue_json.fields.assignee.key)
            if issue_json.fields.issuetype:
                issue.issue_type = self.create_issue_type(issue_json.fields.issuetype.id)
            if issue_json.fields.summary:
                issue.summary = issue_json.fields.summary
            if issue_json.fields.description:
                issue.description = issue_json.fields.description
            if issue_json.fields.environment:
                issue.environment = issue_json.fields.environment
            if issue_json.fields.priority:
                issue.priority = self.create_priority(issue_json.fields.priority.id)
            if issue_json.fields.resolution:
                issue.resolution = issue_json.fields.resolution.name
            if issue_json.fields.status:
                issue.issue_status = self.create_status(issue_json.fields.status.id)
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



if __name__ == "__main__":
    accessor = JiraConnector('http://jira-lab.bars.group:8080', 'ext_i.nasibullin', 'jstyJZAwFAo9')

    issue = accessor.jira.issue('BIMONEU-1174')


    print issue.raw

