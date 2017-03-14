# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class StatusCategory(models.Model):
    stat_cat_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=60)
    color_name = models.CharField(max_length=60)


class IssueStatus(models.Model):
    stat_id = models.IntegerField(default=0)
    name = models.CharField(max_length=60)
    description = models.TextField()
    icon_url = models.CharField(max_length=255)
    status_category = models.ForeignKey(StatusCategory)
    # sequence = models.IntegerField(default=0)


class Priority(models.Model):
    # sequence = models.IntegerField(default=0)
    name = models.CharField(max_length=60)
    description = models.TextField()
    icon_url = models.CharField(max_length=255)
    status_color = models.CharField(max_length=60)
    priority_id = models.IntegerField(default=0)


class Avatar(models.Model):
    pass


class IssueType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type_id = models.IntegerField(default=0)


class IssueLinkType(models.Model):
    link_name = models.CharField(max_length=255)
    inward = models.CharField(max_length=255)
    outward = models.CharField(max_length=255)
    link_id = models.IntegerField(default=0)
    # style = models.CharField(max_length=60)


# доделать
class JiraUser(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=60)
    emailAddress = models.CharField(max_length=255)
    displayName = models.CharField(max_length=255)
    active = models.BinaryField()
    # uri = models.CharField(max_length=255)
    # avatarUrls = None


class Project(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    lead = models.ForeignKey(JiraUser)
    description = models.TextField(blank=True)
    key = models.CharField(max_length=255)
    project_id = models.IntegerField(default=0)
    # counter = models.IntegerField(default=0)
    # assignee_type = models.IntegerField(default=0)
    # avatar = models.ForeignKey(Avatar)


class Component(models.Model):
    component_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    lead = models.CharField(max_length=255)
    assignee_type = models.IntegerField(default=0)
    project = models.ForeignKey(Project)
    # description = models.TextField(blank=True)
    # url = models.CharField(max_length=255)


class ProjectVersion(models.Model):
    proj_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project)
    realised = models.CharField(max_length=10)
    archived = models.CharField(max_length=10)
    realise_date = models.DateTimeField()
    start_date = models.DateTimeField()
    # url = models.CharField(max_length=255)
    # sequence = models.IntegerField(default=0)
    # description = models.TextField(blank=True)


class JiraIssue(models.Model):
    key = models.CharField(max_length=255)
    project = models.ForeignKey(Project)
    assignee = models.CharField(max_length=255)
    issue_type = models.ForeignKey(IssueType)
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    environment = models.TextField()
    priority = models.ForeignKey(Priority)
    resolution = models.CharField(max_length=255)
    issue_status = models.ForeignKey(IssueStatus)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    due_time = models.DateTimeField()
    votes = models.IntegerField(default=0)
    watches = models.IntegerField(default=0)
    time_original_estimate = models.IntegerField(default=0)
    time_estimate = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    # resolution_date = models.DateTimeField()
    # workflow = models.ForeignKey(Workflow)
    # security = models.IntegerField(default=0)
    # issue_sum = models.IntegerField(default=0)

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
