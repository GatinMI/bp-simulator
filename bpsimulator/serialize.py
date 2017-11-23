from rest_framework import serializers

from console_app.models import JiraIssue, JiraWorkflow


class WorkflowSerialize(serializers.ModelSerializer):
    class Meta:
        model = JiraWorkflow
        fields = 'name', 'type', 'descriptor'


class IssueSerialize(serializers.ModelSerializer):
    animals = serializers.StringRelatedField(many=True)
    project = serializers.StringRelatedField(many=True)
    assignee = serializers.StringRelatedField(many=True)
    issue_type = serializers.StringRelatedField(many=True)
    priority = serializers.StringRelatedField(many=True)
    issue_status = serializers.StringRelatedField(many=True)
    create = serializers.StringRelatedField(many=False)
    updated = serializers.StringRelatedField(many=False)
    due_time = serializers.StringRelatedField(many=False)
    resolution_date = serializers.StringRelatedField(many=False)

    class Meta:
        model = JiraIssue
        fields = 'key', 'name', 'project', 'assignee', 'issue_type', 'summary', 'description', 'enviroment', 'priority', \
                 'resolution', 'issue_status', 'create', 'updated', 'due_time', 'votes', 'watches', \
                 'time_original_estimate', 'time_estimate', 'time_spent', 'resolution_date', 'jira_id', 'workflow_id'
