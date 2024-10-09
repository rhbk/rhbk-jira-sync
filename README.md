
# GitHub to JIRA Integration
*This is a README file for GitHub to JIRA Integration for RHBK and Keycloak*

This script takes information from GitHub issues defined in JIRA by predifined format in config.json and update them into the JIRA. It takes either full ownership of the field or partial ownership of the field.

With the full ownership, whatever will be re-writen in JIRA will be replaced by the information from GitHub Issue by the next run of the script. Please, fill this information directly in GitHub issue.

With the partial ownership of field, GitHub will integrate the information, usually with a prefix (GHI), but user can add his/her own information into JIRA and it will be persisted.

All other field, which this integration doesn't own are fully editable by user in JIRA.

## Integrated fields are:

 - Summary (full ownership) 
 - Description (full ownership) 
 - Team (full
   ownership) 
 - Labels (partial ownership)
 - Componenents (partial ownership, without GHI prefix)
 - Links (partial ownership)

 *Note: For component field, the script updates those with "team/" labels. Others are kept in JIRA only.*
 
 ## Step by step instructions
Here is step by step how to run the integration locally on need basis:

1. Create environment variable JIRA_PAT containing your JIRA token (TBD how to generate JIRA token)

2. Check or alter config.json file in this repository to fit your needs

| Config field           |                 Description                        |
| :--  | :-- |
| areaMapper | Dictionary containing labels from GitHub which are base for determining team in JIRA represented by team id|
| teamToComponentMapper | Mapping GH labels to corresponding components in JIRA. One GH label could add multiple components in JIRA |
| statusMapper | Mapping status codes from your JIRA instance |
| gitHubBaseUrl | URL to GitHub instance |
| gitHubOrgName | Name of the organisation in GitHub, where the repository lies with "/" as prefix |
| gitHubRepository | Name of the repository, which should be used for the integration |
| gitHubLinkBaseUrl | Representation of the URL used for creating links in JIRA to GitHub Issues |
| jiraBaseUrl | URL to JIRA instance, where issues should be integrated |
| jiraGitPrefix | Prefix used in the Summary field in JIRA to signal, that the issue is integrated from GitHub |
| jiraGitSuffix | Suffix used in the Summary field in JIRA to signal, that the issue is integrated from GitHub |
| jiraProject | JIRA project, where GitHub Issues should be integrated into |
| loggingLevel | Level of logging in the integration run. Options are `DEBUG, INFO, WARN, ERROR`|
| jiraUpdateQuery | Query used for searching issues. This is not generaly needed to be changed, since it is filled with previous configs |

3. If not already installed in the system, install two dependencies into Python
- Python Requests by running `python  -m  pip  install  requests` in the terminal
- Python Jira by running `python -m pip install jira` in the terminal

*Note: running on MacOS may require using python3 command. Minimal version of Python in the system is 3.8*

4. Run the script by navigating to the location of the file in Terminal and running `python RunUpdate.py`

5. After the run, you can check log file `GitToJira.log` located in the folder where the main script is