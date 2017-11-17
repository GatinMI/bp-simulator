# coding=utf-8
from __future__ import unicode_literals

from pony.orm import *

from datetime import datetime, time

jira_db = Database()

class StatusCategory(jira_db.Entity):
    stat_cat_id = Required(int)
    name = Optional(str)
    key = Optional(str)
    color_name = Optional(str)
    issueStatusSet = Set('IssueStatus')

class IssueStatus(jira_db.Entity):
    stat_id = Required(int)
    name = Optional(str)
    description = Optional(str)
    icon_url = Optional(str)
    status_category = Optional(StatusCategory)
    sequence = Optional(int)
    jiraIssueSet = Set('JiraIssue')


class Priority(jira_db.Entity):
    priority_id = Required(int)
    sequence = Optional(int)
    name = Optional(str)
    description = Optional(str)
    icon_url = Optional(str)
    status_color = Optional(str)
    jiraIssueSet = Set('JiraIssue')

class Avatar(jira_db.Entity):
    pass


class IssueType(jira_db.Entity):
    type_id = Required(int)
    name = Optional(str)
    description = Optional(str)
    jiraIssueSet = Set('JiraIssue')

class IssueLinkType(jira_db.Entity):

    link_id = Required(int)
    link_name = Optional(str)
    inward = Optional(str)
    outward = Optional(str)
    style = Optional(str)


# доделать
class JiraUser(jira_db.Entity):
    key = Required(str)
    name = Optional(str)
    emailAddress = Optional(str)
    displayName = Optional(str)
    active = Optional(bool)
    uri = Optional(str)
    leadSet = Set('Project')
    assigneedIssues = Set('JiraIssue')


class Project(jira_db.Entity):
    project_id = Required(int)
    name = Optional(str)
    url = Optional(str)
    lead = Optional(JiraUser)
    description = Optional(unicode)
    key = Optional(str)
    componentSet = Set('Component')
    projectVersionSet = Set('ProjectVersion')
    jiraIsseuSet = Set('JiraIssue')




class Component(jira_db.Entity):
    component_id = Required(int)
    name = Required(str)
    lead = Required(str)
    assignee_type = Required(int)
    project = Required(Project)
    description = Optional(str)
    url = Optional(str)


class ProjectVersion(jira_db.Entity):
    proj_id = Required(int)
    name = Required(str)
    project = Required(Project)
    realised = Required(str)
    archived = Required(str)
    realise_date = Required(datetime)
    start_date = Required(datetime)
    url = Optional(str)
    sequence = Optional(int)
    description = Optional(str)


class JiraIssue(jira_db.Entity):
    key = Required(str)
    project = Optional(Project)
    assignee = Optional(JiraUser)
    issue_type = Optional(IssueType)
    summary = Optional(str)
    description = Optional(str)
    enviroment = Optional(str)
    priority = Optional(Priority)
    resolution = Optional(str)
    issue_status = Optional(IssueStatus)
    create = Optional(datetime)
    updated = Optional(datetime)
    due_time = Optional(datetime)
    votes = Optional(int)
    watches = Optional(int)
    time_original_estimate = Optional(int)
    time_estimate = Optional(int)
    time_spent = Optional(int)
    resolution_date = Optional(datetime)
    # workflow = Optional(int)


# class IssueLink(models.Model):
#     link_type = models.ForeignKey(IssueLinkType)
#     source = models.ForeignKey(JiraIssue)
#     destination = models.ForeignKey(JiraIssue)
#     sequence = models.IntegerField(default=0)

class Workflow(jira_db.Entity):
    name = Required(str)
    type = Optional(str)
    steps = Set('WorkflowStep')

#
#     author = models.CharField(max_length=255)
#     group_level = models.CharField(max_length=255)
#     role_level = models.CharField(max_length=255)
#     work_log_body = models.TextField()
#     created = models.DateTimeField()
#     update_author = models.CharField(max_length=255)
#     updated = models.DateTimeField()
#     start_date = models.DateTimeField()
#     time_worked = models.IntegerField(default=0)

class JiraAction(jira_db.Entity):
    issue_id = Required(int)
    author = Optional(str)
    created = Optional(datetime)
    updated = Optional(datetime)

class WorkflowStep(jira_db.Entity):
    workflow_id = Required(int)
    name = Optional(str)
    actions = Set('WorkflowAction')

class WorkflowAction(jira_db.Entity):
    step_id = Required(int)
    name = Optional(str)
    result_step_id = Required(int)

class WorkflowIssue(jira_db.Entity):



jira_db.bind('sqlite', 'jira_db.sqlite3', create_db=True)
jira_db.generate_mapping(create_tables=True)
