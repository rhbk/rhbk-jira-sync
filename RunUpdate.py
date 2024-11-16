import requests
from requests.auth import HTTPDigestAuth
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
import re
import json
from GitHubIssueObject import IntegratedIssue
from GitHubIssueObject import ConfigDigest
import logging
import datetime
import sys
import md_to_jira

# Loading configuration for the run
config = ConfigDigest()
# Configuring logging to GitToJira.log with level set in the config file (ERROR, WARN, INFO, DEBUG)
# TODO: Add configuration of the name of the logging file
logging.basicConfig(filename='GitToJira.log', encoding='utf-8', level=config.logLevel)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
try:
    # Connecting to the configured JIRA instance
    jira = JIRA(config.jiraBaseUrl, token_auth=config.jiraToken)
    logging.info("Integration run at {}".format(datetime.datetime.now()))
    #Search for issues in desired project, the search is trying to find the prefixes
    search = jira.search_issues(config.jiraUpdateQuery.format(config.jiraProject, config.jiraGitPrefix), maxResults=False)
    # Iterating thru found issues
    for issue in search:
        firstIndex = issue.fields.summary.find(config.jiraGitPrefix) + len(config.jiraGitPrefix)
        lastIndex = issue.fields.summary.find("]", firstIndex)
        response = requests.get("{}{}{}/issues/{}".format(config.gitBaseUrl, config.gitHubOrgName, "/keycloak", issue.fields.summary[firstIndex:lastIndex]), headers={'Accept':'application/vnd.github.full+json'})
        if response.status_code != 200:
            logging.error("GitHub Issue #{} not updated. Check the GitHub issue number if correct. Error message : {}".format(issue.fields.summary[firstIndex:lastIndex], response.text))
        else:
            logging.debug("GitHub Issue found")
            data = json.loads(response.text)
            if (data["body"] != None):
                body = md_to_jira.markdown_to_jira(data["body"])
            else:
                body=data["body"]
            # Processing response to the defined Python object for further processing
            ghIssue = IntegratedIssue(data["id"], data["title"], body, data["number"], data["labels"], data["state"], data["assignee"], data["assignees"], data["html_url"], config.areaMappers)
            #Preparing JIRA object for update
            jiraIssue = {
                            'project': {'key':config.jiraProject},
                            'summary': "{} [{}{}{}]".format(ghIssue.title, config.jiraGitPrefix, ghIssue.number, config.jiraGitSuffix),
                            'description' : str(ghIssue.body),
                            'labels' : ghIssue.resolveLabels([]),
                        }
            jiraIssue['customfield_12313240'] = str(ghIssue.team)
            jiraIssue["labels"] = ghIssue.resolveLabels(issue.fields.labels)
            # Checking, if the link to the original GitHub Issue is already in JIRA, otherwise adding it. This needs to be done to avoiding duplicated links
            issueGitHubLink = config.gitHubLinkBaseUrl.format(config.gitHubOrgName, config.gitHubRepository, ghIssue.number)
            links = jira.remote_links(issue)
            hasLink = False
            for link in links:
                if link.object.url == issueGitHubLink:
                    hasLink = True
            if not hasLink:
                jira.add_simple_link(issue, {"url":issueGitHubLink, "title":"Link to original GitHub issue"})
            #Updating JIRA issue
            issue.update(jiraIssue)
            issue.update(fields={"components": ghIssue.resolveTeamComponents(issue.fields.components, config.teamToComponentMapper)})
            if (issue.fields.status.name != "Closed" and ghIssue.status == "closed"):
                jira.transition_issue(issue, "Closed")
            logging.info("GitHub issue number {} succesfully updated under JIRA issue {}".format(ghIssue.number, issue.key))
    jira.close()
    logging.info("Integration run succesfull!")

except Exception as error:
    logging.error(error)
    jira.close()
    sys.exit(1)
