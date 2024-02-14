#! /usr/bin/env python3

import os
import yaml
import shutil
from datetime import datetime

YAML_FILE_PATH = 'source/talks.yml'
ARCHIVE_DIR = 'archive'

def md_link(name, link, bold=False):
    if bold: name = f'**{name}**'
    return f'[{name}]({link})'

def reender(yaml_record):
    md_title = md_link(
        name = yaml_record['title'],
        link = yaml_record['video'],
        bold = True
    )

    title_line = f'- {md_title}  '
    if 'resources' in yaml_record:
        if yaml_record['resources']:
            for resource_name, resource_link in yaml_record['resources'].items():
                title_line += f'\[[{resource_name.capitalize()}]({resource_link})\]  '

    tags = yaml_record['tags']
    tags_line = '  '.join (
        [f'`🏷️ {tag}`' for tag in tags]
    )

    md_summary = yaml_record['summary']
    summary_line = f'{md_summary}'

    md_conference_name = yaml_record['conference']['name']
    if 'event' in yaml_record['conference']:
        md_event_name = yaml_record['conference']['event']
        md_conference_name += f' {md_event_name}'

    conference_line = f'🎙️  **{md_conference_name}** '
    if 'website' in yaml_record['conference']:
        conference_line += md_link("Website", yaml_record['conference']['website']) + " "
    if 'channel' in yaml_record['conference']:
        conference_line += md_link("Youtube", yaml_record['conference']['channel']) + " "
    if 'socials' in yaml_record['conference']:
        for social_network_name, social_network_link in yaml_record['conference']['socials'].items():
            conference_line += f'[{social_network_name.capitalize()}]({social_network_link})  '

    return f'{title_line}  \n{tags_line}  \n{summary_line}  \n{conference_line}  \n'

def main():
    with open(YAML_FILE_PATH) as f:
        talks_from_yml = yaml.safe_load(f.read())

    if not talks_from_yml:
        if ARCHIVE_DIR in os.listdir():
            shutil.rmtree(ARCHIVE_DIR)
        return

    markdown_dict = {}

    for tfy in talks_from_yml:
        pub_date_dt = datetime.strptime(tfy['pub_date'], '%Y-%m-%d')

        pub_date_year = str(pub_date_dt.year)
        if pub_date_year not in markdown_dict.keys():
            markdown_dict[pub_date_year] = {}

        pub_date_week = str(pub_date_dt.isocalendar().week)
        if pub_date_week not in markdown_dict[pub_date_year].keys():
            markdown_dict[pub_date_year][pub_date_week] = {}

        category = tfy['category']
        if category not in markdown_dict[pub_date_year][pub_date_week].keys():
            markdown_dict[pub_date_year][pub_date_week][category] = {}

        subcategory = tfy.get('subcategory', None)
        if subcategory not in markdown_dict[pub_date_year][pub_date_week][category].keys():
            markdown_dict[pub_date_year][pub_date_week][category][subcategory] = {}

        title = tfy.get('title', None)
        markdown_dict[pub_date_year][pub_date_week][category][subcategory][title] = tfy

    for pub_date_year in markdown_dict.keys():
        if ARCHIVE_DIR not in os.listdir():
            os.mkdir(ARCHIVE_DIR)

        if pub_date_year not in os.listdir(ARCHIVE_DIR):
            os.mkdir(f'{ARCHIVE_DIR}/{pub_date_year}')

        for pub_date_week in markdown_dict[pub_date_year]:
            week_markdown_file = f'{ARCHIVE_DIR}/{pub_date_year}/week{pub_date_week}.md'
            with open(week_markdown_file, 'w') as wmf:
                for category in markdown_dict[pub_date_year][pub_date_week]:
                    wmf.write(f'# {category}\n')
                    for subcategory in markdown_dict[pub_date_year][pub_date_week][category]:
                        wmf.write(f'## {subcategory}\n')
                        for title in markdown_dict[pub_date_year][pub_date_week][category][subcategory]:
                            yaml_record = markdown_dict[pub_date_year][pub_date_week][category][subcategory][title]
                            md_record = reender(yaml_record)
                            wmf.write(md_record)

main()