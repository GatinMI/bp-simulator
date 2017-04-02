# coding=utf-8
from __future__ import unicode_literals

from pony.orm import *

from datetime import datetime, time

jira_db = Database()


class StatusCategory(jira_db.Entity):
    # stat_cat_id = models.IntegerField(default=0)
    # name = models.CharField(max_length=255)
    # key = models.CharField(max_length=60)
    # color_name = models.CharField(max_length=60)
    stat_cat_id = Required(int)
    name = Optional(str)
    key = Optional(str)
    color_name = Optional(str)
    issueStatusSet = Set('IssueStatus')

class IssueStatus(jira_db.Entity):
    # stat_id = models.IntegerField(default=0)
    # name = models.CharField(max_length=60)
    # description = models.TextField()
    # icon_url = models.CharField(max_length=255)
    # status_category = models.ForeignKey(StatusCategory)
    # sequence = models.IntegerField(default=0)
    stat_id = Required(int)
    name = Optional(str)
    description = Optional(str)
    icon_url = Optional(str)
    status_category = Optional(StatusCategory)
    sequence = Optional(int)
    jiraIssueSet = Set('JiraIssue')


class Priority(jira_db.Entity):
    # sequence = models.IntegerField(default=0)
    # name = models.CharField(max_length=60)
    # description = models.TextField()
    # icon_url = models.CharField(max_length=255)
    # status_color = models.CharField(max_length=60)
    # priority_id = models.IntegerField(default=0)
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
    # name = models.CharField(max_length=255)
    # description = models.CharField(max_length=255)
    # type_id = models.IntegerField(default=0)
    type_id = Required(int)
    name = Optional(str)
    description = Optional(str)
    jiraIssueSet = Set('JiraIssue')

class IssueLinkType(jira_db.Entity):
    # link_name = models.CharField(max_length=255)
    # inward = models.CharField(max_length=255)
    # outward = models.CharField(max_length=255)
    # link_id = models.IntegerField(default=0)
    # style = models.CharField(max_length=60)
    link_id = Required(int)
    link_name = Optional(str)
    inward = Optional(str)
    outward = Optional(str)
    style = Optional(str)


# доделать
class JiraUser(jira_db.Entity):
    # name = models.CharField(max_length=255)
    # key = models.CharField(max_length=60)
    # emailAddress = models.CharField(max_length=255)
    # displayName = models.CharField(max_length=255)
    # active = models.BinaryField()
    # uri = models.CharField(max_length=255)
    # avatarUrls = None
    key = Required(str)
    name = Optional(str)
    emailAddress = Optional(str)
    displayName = Optional(str)
    active = Optional(bool)
    uri = Optional(str)
    leadSet = Set('Project')
    assigneedIssues = Set('JiraIssue')


class Project(jira_db.Entity):
    # name = models.CharField(max_length=255)
    # url = models.CharField(max_length=255)
    # lead = models.ForeignKey(JiraUser)
    # description = models.TextField(blank=True)
    # key = models.CharField(max_length=255)
    # project_id = models.IntegerField(default=0)
    # counter = models.IntegerField(default=0)
    # assignee_type = models.IntegerField(default=0)
    # avatar = models.ForeignKey(Avatar)
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
    # component_id = models.IntegerField(default=0)
    # name = models.CharField(max_length=255)
    # lead = models.CharField(max_length=255)
    # assignee_type = models.IntegerField(default=0)
    # project = models.ForeignKey(Project)
    # description = models.TextField(blank=True)
    # url = models.CharField(max_length=255)
    component_id = Required(int)
    name = Required(str)
    lead = Required(str)
    assignee_type = Required(int)
    project = Required(Project)
    description = Optional(str)
    url = Optional(str)


class ProjectVersion(jira_db.Entity):
    # proj_id = models.IntegerField(default=0)
    # name = models.CharField(max_length=255)
    # project = models.ForeignKey(Project)
    # realised = models.CharField(max_length=10)
    # archived = models.CharField(max_length=10)
    # realise_date = models.DateTimeField()
    # start_date = models.DateTimeField()
    # url = models.CharField(max_length=255)
    # sequence = models.IntegerField(default=0)
    # description = models.TextField(blank=True)
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
    # key = models.CharField(max_length=255)
    # project = models.ForeignKey(Project)
    # assignee = models.CharField(max_length=255)
    # issue_type = models.ForeignKey(IssueType)
    # summary = models.CharField(max_length=255)
    # description = models.TextField(blank=True)
    # environment = models.TextField()
    # priority = models.ForeignKey(Priority)
    # resolution = models.CharField(max_length=255)
    # issue_status = models.ForeignKey(IssueStatus)
    # created = models.DateTimeField()
    # updated = models.DateTimeField()
    # due_time = models.DateTimeField()
    # votes = models.IntegerField(default=0)
    # watches = models.IntegerField(default=0)
    # time_original_estimate = models.IntegerField(default=0)
    # time_estimate = models.IntegerField(default=0)
    # time_spent = models.IntegerField(default=0)
    # resolution_date = models.DateTimeField()
    # workflow = models.ForeignKey(Workflow)
    # security = models.IntegerField(default=0)
    # issue_sum = models.IntegerField(default=0)
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
    # workflow - Required()


# class IssueLink(models.Model):
#     link_type = models.ForeignKey(IssueLinkType)
#     source = models.ForeignKey(JiraIssue)
#     destination = models.ForeignKey(JiraIssue)
#     sequence = models.IntegerField(default=0)

# class Workflow(models.Model):
#     author = models.CharField(max_length=255)
#     group_level = models.CharField(max_length=255)
#     role_level = models.CharField(max_length=255)
#     work_log_body = models.TextField()
#     created = models.DateTimeField()
#     update_author = models.CharField(max_length=255)
#     updated = models.DateTimeField()
#     start_date = models.DateTimeField()
#     time_worked = models.IntegerField(default=0)


jira_db.bind('sqlite', 'jira_db.sqlite', create_db=True)
jira_db.generate_mapping(create_tables=True)
