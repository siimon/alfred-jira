import xml.etree.cElementTree as ET

class WorkflowHelper:
  def __init__(self, base_url):
    self._base_url = base_url

  def convert_to_alfred_valid_xml_list(self,issues):
    root = ET.Element("items")
    for issue in issues:
      key = (issue['key']).encode('utf8')
      fields = issue['fields']
      summary = (fields['summary']).encode('utf8')
      assignee = "Not assigned"
      assigneeFields = fields['assignee']
      if(assigneeFields is not None):
        assignee = assigneeFields['displayName']
      statusFields = fields['status']
      status = statusFields['name']

      titleText = "%s" % ( summary)
      subTitleText = "%s - %s" % (assignee , status)

      item = ET.SubElement(root, "item")
      item.set("valid", "yes")
      item.set("uid", key)
      item.set("arg", "%s/browse/%s" % (self._base_url, key))
      title = ET.SubElement(item, "title")
      title.text = (titleText).decode('utf8')
      subtitle = ET.SubElement(item, "subtitle")
      subtitle.text = (subTitleText).decode('utf8')

      icon = ET.SubElement(item, "icon")
      icon.text = "jira_logo.png"

    return ET.tostring(root, encoding='utf8', method='xml')

  def convert_to_alfred_valid_xml_single(self, issue):
    issues_tuple = [ issue ]
    return self.convert_to_alfred_valid_xml_list(issues_tuple)

