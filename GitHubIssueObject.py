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
        self.status = state
        for x in labels:
            self.labels.append(x["name"].replace(" ","-"))
        self.resolveTeam(mapper)

    def resolveTeam(self, mapper):
        for label in self.labels:
            if label in mapper.keys():
                self.team = mapper[label]

    def resolveLabels(self, currentLabels):
        labels = []
        for label in currentLabels:
            if "GHI/" not in label:
                labels.append(label)
        for label in self.labels:
            labels.append("GHI/{}".format(label))
        return labels
    
    def resolveTeamComponents(self, currentComps, teamMapper):
        newComponents = []
        for comps in currentComps:
            if "team/" not in comps.name:
                newComponents.append(comps)
        for label in self.labels:
            if label in teamMapper.keys():
                for team in teamMapper[label]:
                    newComponents.append({"name" : team})
        return newComponents


# Helper class to consume Configuration file called config.json
class ConfigDigest:
    def __init__(self):
        # TODO: Secure exception handling, if the config file is not present in the folder with the script
        configFile = open('config.json')
        config = json.loads(configFile.read())
        self.areaMappers = config["areaMapper"]
        self.teamToComponentMapper = config["teamToComponentMapper"]
        self.jiraBaseUrl = config["jiraBaseUrl"]
        self.gitBaseUrl = config["gitHubBaseUrl"]
        self.gitHubOrgName = config["gitHubOrgName"]
        self.jiraToken = os.getenv('JIRA_PAT')
        self.ghToken = os.getenv('GH_PAT')
        self.jiraQuery = "project = '{}' and summary ~ '{}{}{}'"
        self.jiraGitPrefix = config["jiraGitPrefix"]
        self.jiraGitSuffix = config["jiraGitSuffix"]
        self.jiraProject = config["jiraProject"]
        self.logLevel = config["loggingLevel"]
        self.jiraUpdateQuery = config["jiraUpdateQuery"]
        self.gitHubLinkBaseUrl = config["gitHubLinkBaseUrl"]
        self.gitHubRepository = config["gitHubRepository"]
        self.jiraRateLimitSecondsTimeout = config["jiraRateLimitSecondsTimeout"]
    

