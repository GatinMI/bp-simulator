import xml.etree.ElementTree as ET

tree = ET.parse('../Bars Epic Workflow.xml')

root = tree.getroot()

steps = tree.getiterator("step")

for step in steps:
    actions = step.find('actions').findall('action')
    for action in actions:
        print '%s %s' % (step.attrib['id'], action.attrib['name'])
        fields = action.findall('meta')
        for field in fields:
            if field.attrib['name'] == 'jira.fieldscreen.id':
                print field.text