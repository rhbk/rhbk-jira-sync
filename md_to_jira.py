#!/usr/bin/env python3

# Author: Elijah Shackelford (eshack94)

# Description:
#
# This script converts a markdown file to Jira/Confluence markup syntax.
# It will write to stdout, so you can redirect the output to a file if desired.
#
# The original markdown file will not be modified unless you redirect the output
# to the same file.

# Usage:
# python3 md_to_jira.py <markdown_file>
# python3 md_to_jira.py <markdown_file> > <jira_file>
# python3 md_to_jira.py <markdown_file> | pbcopy

import sys
import re


def convert_line(line):
    # Convert headers
    line = re.sub(r'^#{6}\s*(.+)', r'h6. \1', line)
    line = re.sub(r'^#{5}\s*(.+)', r'h5. \1', line)
    line = re.sub(r'^#{4}\s*(.+)', r'h4. \1', line)
    line = re.sub(r'^#{3}\s*(.+)', r'h3. \1', line)
    line = re.sub(r'^#{2}\s*(.+)', r'h2. \1', line)
    line = re.sub(r'^#\s*(.+)', r'h1. \1', line)

    # Convert bold and italic
    line = re.sub(r'\*\*(.+?)\*\*', r'*\1*', line)
    line = re.sub(r'__(.+?)__', r'*\1*', line)
    line = re.sub(r'\*(.+?)\*', r'_\1_', line)
    line = re.sub(r'_(.+?)_', r'_\1_', line)

    # Convert inline code
    line = re.sub(r'`([^`]+)`', r'{{\1}}', line)

    # Convert strikethrough
    line = re.sub(r'~~(.+?)~~', r'-\1-', line)

    # Convert links
    line = re.sub(r'\[(.*?)\]\((.+?)\)', r'[\1|\2]', line)

    # Convert unordered lists
    line = re.sub(r'^\*\s+', r'- ', line)

    # Convert GFM task lists
    line = re.sub(r'^\s*-\s*\[(x|X| )\]', lambda match: f'[{match.group(1)}]', line)

    return line


def convert_multiline_elements(content):
    # Convert multiline fenced code blocks
    content = re.sub(r'```(\w+)?\n(.*?)\n```', process_code_block, content, flags=re.MULTILINE | re.DOTALL)

    # Convert indented code blocks
    content = re.sub(r'((?:^ {4}.*\n?)+)', process_indented_code_block, content, flags=re.MULTILINE)

    return content


def process_code_block(match):
    lang = match.group(1)
    code = match.group(2)
    if lang:
        return f'{{code:{lang}}}\n{code}\n{{code}}'
    else:
        return f'{{code}}\n{code}\n{{code}}'


def process_indented_code_block(match):
    code = match.group(1)
    # Remove the leading 4 spaces or tab from each line
    code = re.sub(r'^ {4}|\t', '', code, flags=re.MULTILINE)
    return f'{{code}}\n{code}{{code}}\n'


def markdown_to_jira(content):

    # Convert multiline elements
    content = convert_multiline_elements(content)

    # Process the lines
    # add toggle flag to keep track of whether we're in a code block or not
    # so we don't convert # characters in code blocks
    # toggles on when we enter a code block and toggles off when we exit
    # toggle state determines whether we convert the line or not
    in_code_block = False
    jira_lines = []
    for line in content.splitlines():
        if line.startswith("```") or line.startswith("{code"):
            in_code_block = not in_code_block

        if not in_code_block:
            line = convert_line(line)
        jira_lines.append(line)
    formated_body = ""
    # Print the converted lines
    for jira_line in jira_lines:
        formated_body = formated_body + jira_line + "\n"

    return formated_body
