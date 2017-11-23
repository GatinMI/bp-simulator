from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import base64
from urllib.parse import urlparse
from tlslite.utils import keyfactory
import oauth2 as oauth
import json

from bpsimulator.serialize import IssueSerialize


class SignatureMethod_RSA_SHA1(oauth.SignatureMethod):
    name = 'RSA-SHA1'

    def signing_base(self, request, consumer, token):
        if not hasattr(request, 'normalized_url') or request.normalized_url is None:
            raise ValueError("Base URL for request is not set.")

        sig = (
            oauth.escape(request.method),
            oauth.escape(request.normalized_url),
            oauth.escape(request.get_normalized_parameters()),
        )

        key = '%s&' % oauth.escape(consumer.secret)
        if token:
            key += oauth.escape(token.secret)
        raw = '&'.join(sig)
        return key, raw

    def sign(self, request, consumer, token):
        """Builds the base signature string."""
        key, raw = self.signing_base(request, consumer, token)

        data = "-----BEGIN PRIVATE KEY-----MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALmssc2MMXdJ7sg6b+eb2jqU4PfDrc2DA0h/UXLu8aTczNLMmHnR4dZ8RJ6/5fjyIVJ3B3SY/7RBKz8Ufl6OcayEK44NsLNyHkz/J2qV+34F/+E+XdhCLPQagYh7Ev0bSncITJ09sk03y7NaN7w9zakzFGvkM6j4gR8nTjwIuvhxAgMBAAECgYAUBNSeztC+hdAi8noCRMGAs3CWBhkFIW0HMgL8G1seZVgIGlsON1zcHUXgv9vxvVluZLr/DUf0jVo2UOVXGJCU0/Rl2u54jdJNOT/CKtvMZnA4vCdEFrdWQBvMeCsfn9s+v09iCW3l/zADdEjIjmtyh68P38vnIL1NLlgkc9zgYQJBAO1cHHxwgp4HVioMzbEqKvg/CiNJsQ7UXDpV69No5Ik52Y9myc8oK8CHGnioTdIBIPQO7/STk+1wZTsigz2q4SUCQQDIQYCEtBKHnR8i49rAhEETPNlEF0KXSevgYs4lZY5/2JT5b72FASFapWFLMqcKfEjyqek/HySZScFA+R26thZdAkEA1nWZT14gxkP+uDOlTeO5u17J/CRDFBEP261yTCvEAbEBP64xvTigf24Snt4CojJe4eT1LdiBmdEpxgpi5j8U+QJALm7hueN3GHLaMWDb7B++ZxOI3Tz3d9TwGItQeWNe803o3R2HuDtW3InUUXdhPBEtaPb02moCNnjfko0w04Y9EQJAdYqSXUDqNDwouEF/c+GO9UEj0w6lf4TCSU0hLBalIjNXnxaWCBZwfORG12T5SKyi0sVAX72aB6NJoIUDq3ZWhQ==-----END PRIVATE KEY-----"
        privateKeyString = data.strip()

        privatekey = keyfactory.parsePrivateKey(privateKeyString)
        signature = privatekey.hashAndSign(raw)

        return base64.b64encode(signature)


jira_url = ""
access_token = ""
resp = ""
content = ""
client = ""
consumer = ""
fields = ""
parsed_fields = ""
JIRA_HOME = "http://jira-lab.bars.group:8080"
access_token_url = JIRA_HOME + '/plugins/servlet/oauth/access-token'
request_token_url = JIRA_HOME + '/plugins/servlet/oauth/request-token'


def index(request):
    global jira_url, access_token, resp, content, client, consumer, parsed_fields, JIRA_HOME, access_token_url, request_token_url
    consumer_key = 'oauth-sample-consumer'
    consumer_secret = 'dont_care'
    authorize_url = JIRA_HOME + '/plugins/servlet/oauth/authorize'
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    client.set_signature_method(SignatureMethod_RSA_SHA1())

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain
    # said access token.

    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s: %s" % (resp['status'], content))

    request_token = dict(urlparse.parse_qsl(content))

    jira_url = "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

    if ("jira_url" != ""):
        return render(request, "index.html", {"url": jira_url});


def signin(request):
    global jira_url, access_token, resp, content, client, consumer, fields, parsed_fields

    JIRA_HOME = "http://jira-lab.bars.group:8080"

    access_token_url = JIRA_HOME + '/plugins/servlet/oauth/access-token'

    data_url = JIRA_HOME + '/rest/auth/1/session'

    if resp['status'] != '200':
        raise Exception("Invalid response %s: %s" % (resp['status'], content))

    request_token = dict(urlparse.parse_qsl(content))

    token = oauth.Token(request_token['oauth_token'],
                        request_token['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    client.set_signature_method(SignatureMethod_RSA_SHA1())

    access_token = dict(urlparse.parse_qsl(content))
    # Waiting for Jira submitting from user
    while (len(access_token) != 5):
        resp, content = client.request(access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))

    accessToken = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
    client = oauth.Client(consumer, accessToken)
    client.set_signature_method(SignatureMethod_RSA_SHA1())
    resp, content = client.request(data_url, "GET")
    link = json.loads(content)
    data, fields = client.request(link["self"], "GET")
    parsed_fields = json.loads(fields)
    key = parsed_fields[u'key']
    name = parsed_fields[u'name']
    emailAddress = parsed_fields[u'emailAddress']
    displayName = parsed_fields[u'displayName']
    avatar_link = parsed_fields[u'avatarUrls'][u'16x16']
    resp, content = client.request(data_url, "GET")
    if resp['status'] != '200':
        raise Exception("Should have access!")
    else:
        return render_to_response("signin.html",
                                  {"key": key, "name": name, "emailAddress": emailAddress, "displayName": displayName,
                                   "avatar_link": avatar_link});





from console_app.models import JiraIssue


def get_issue(request, issue_id):
    try:
        issue = JiraIssue.objects.get(jira_id=issue_id)
    except JiraIssue.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IssueSerialize(issue, context={'request': request})
        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, encoding="utf-8"),
                            content_type="application/json; encoding=utf-8")