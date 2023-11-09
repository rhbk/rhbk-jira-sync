import json
import os

class IntegratedIssue:
    def __init__(self, id, title, body, number, labels, state, assignee, assignees, url, mapper):
        self.id = id
        self.title = title
        self.body = body
        self.number = number
        self.labels = []
        self.url = url
        self.team = ""
        self.resolveStatus(assignee, assignees, state)
        for x in labels:
            self.labels.append(x["name"])
        self.resolveTeam(mapper)

    def resolveTeam(self, mapper):
        for label in self.labels:
            if label in mapper.keys():
                self.team = mapper[label]
    
    def resolveStatus(self, assignee, assignees, state):
        if state == "Closed":
            self.status = "Closed"
            return
        elif assignee or assignees:
            self.status = "In Progress"
        else:
            self.status = "To Do"

    def resolveLabels(self, currentLabels):
        labels = []
        for label in currentLabels:
            if "GHI/" not in label:
                labels.append(label)
        for label in self.labels:
            labels.append("GHI/{}".format(label))
        return labels

# Helper class to consume Configuration file called config.json
class ConfigDigest:
    def __init__(self):
        # TODO: Secure exception handling, if the config file is not present in the folder with the script
        configFile = open('config.json')
        config = json.loads(configFile.read())
        self.areaMappers = config["areaMapper"]
        self.jiraBaseUrl = config["jiraBaseUrl"]
        self.gitBaseUrl = config["gitHubBaseUrl"]
        self.gitHubOrgName = config["gitHubOrgName"]
        self.jiraToken = os.getenv('JIRA_PAT')
        self.jiraQuery = "project = '{}' and summary ~ '{}{}{}'"
        self.jiraGitPrefix = config["jiraGitPrefix"]
        self.jiraGitSuffix = config["jiraGitSuffix"]
        self.jiraProject = config["jiraProject"]
        self.statusMapper = config["statusMapper"]
        self.logLevel = config["loggingLevel"]
        self.jiraUpdateQuery = config["jiraUpdateQuery"]
        self.gitHubLinkBaseUrl = config["gitHubLinkBaseUrl"]
        self.gitHubRepository = config["gitHubRepository"]

