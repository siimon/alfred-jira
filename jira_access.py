# -*- coding: utf-8 -*-
import oauth2 as oauth
import json
from signature_method import SignatureMethod_RSA_SHA1
import argparse
from helper import WorkflowHelper

class JIRA_Client:
  def __init__(self):
    settings = None
    with open('settings.txt', 'r') as f:
      settings = json.loads(f.readlines()[0])

    self.consumer_key = settings['consumer_key']
    self.consumer_secret = settings['consumer_secret']
    self.base_url =  settings['base_url']
    self.access_token = settings['access_token']
    self.access_token_secret = settings['access_token_secret']
    self.key_path = settings['key_path']

  def search(self, query):
    data_url = "%s/rest/api/2/search?jql=%s&maxResults=10" % (self.base_url, query)
    result = self.execute_request(data_url)
    print self.convert_to_xml_list(result)
  def browse(self, issue):
    url = "%s/rest/api/2/issue/%s" % (self.base_url, issue);
    result = self.execute_request(url)
    print self.convert_to_xml_single(result)

  def execute_request(self, request):
    consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
    token = oauth.Token(self.access_token, self.access_token_secret)
    client = oauth.Client(consumer, token)
    client.set_signature_method(SignatureMethod_RSA_SHA1(self.key_path))

    resp, content = client.request(request, 'GET')
    content_json = json.loads(content)
    return content_json

  def convert_to_xml_list(self, json):
    if('issues' in json):
      issues = json['issues']
      helper = WorkflowHelper(self.base_url)
      alfred_xml = helper.convert_to_alfred_valid_xml_list(issues)
      return alfred_xml
    return ""
  def convert_to_xml_single(self, json):
    helper = WorkflowHelper(self.base_url)
    alfred_xml = helper.convert_to_alfred_valid_xml_single(json)
    return alfred_xml

  def help(self):
    return """
\033[1mNAME\033[0m
    JIRA Access , JIRA API for Alfred Workflow

\033[1mDESCRIPTION\033[0m
    Handle requests to JIRA REST API

\033[1mOPTIONS\033[0m

  -q, --query
   Argument to use in search. Could be a JQL query or a JIRA key

  -o, --operation
    [browse , search]
    Sets the current operation

"""



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-q', '--query')
  parser.add_argument('-o', '--operation')
  args = parser.parse_args()

  client = JIRA_Client()
  if(args.operation == 'search'):
    client.search(args.query)
  elif (args.operation == 'browse'):
    client.browse(args.query)
  else:
    print client.help()

