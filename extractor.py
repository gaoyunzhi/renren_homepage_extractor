#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from pypinyin import lazy_pinyin

FILE_DIR = "/Users/yunzhi_gao/Google Drive/download/renren"
RENREN_ID_LOCATOR = "var profileOwnerId = '"
RENREN_ID_ENDER = "'"
RENREN_NAME_LOCATOR = "profileOwnerName = '"
RENREN_NAME_ENDER = "'"
HOME_TOWN_LOCATOR = '<li class="hometown">'
HOME_TOWN_ENDER = '</li>'
LOCATION_LOCATOR = '<li class="address">'
LOCATION_ENDER = '</li>'
SCHOOL_LOCATOR = '<li class="school">'
SCHOOL_ENDER = '</li>'
BIRTHDAY_LOCATOR = '<li class="birthday">'
BIRTHDAY_ENDER = '</li>'
SCHOOL_DETAIL_LOCATOR = '就读于'
SCHOOL_DETAIL_ENDER = '</span>'
BIRTHDAY_DETAIL_LOCATOR = '<span>，'
BIRTHDAY_DETAIL_ENDER = '</span>'

MAX_MATCH_LEN = 100

def clean_text(text):
    return ''.join(text.split('\n'))

def find_with_locator(content, locator, ender, start_index):
    if not content:
        return None, None
    locator_index = content.find(locator, start_index)
    result_start_index = locator_index + len(locator)
    result_end_index = content.find(ender, result_start_index)
    if result_start_index == -1 or result_end_index == -1 or \
        result_end_index - result_start_index > MAX_MATCH_LEN:
        return None, len(content)
    return (clean_text(content[result_start_index: result_end_index]), result_end_index)

def format_birthday_western(birthday):
    if not birthday:
        return None
    day, _ = find_with_locator(birthday, '月', '日', 0)
    month = birthday[:birthday.find('月')]
    return month + '/' + day

def to_pinyin(text):
    if not text:
        return None
    text = text.decode('utf-8')
    return ''.join(lazy_pinyin(text))

def get_profile_link(id):
    if not id:
        return None
    return "http://www.renren.com/" + id + "/profile"

for filename in os.listdir(FILE_DIR):
    with open(os.path.join(FILE_DIR, filename)) as f:
        content = f.read()
        renren_id, next_index = find_with_locator(content, RENREN_ID_LOCATOR, RENREN_ID_ENDER, 0)
        renren_name, next_index = find_with_locator(content, RENREN_NAME_LOCATOR, RENREN_NAME_ENDER, next_index)
        school, next_index = find_with_locator(content, SCHOOL_LOCATOR, SCHOOL_ENDER, next_index)
        birthday, next_index = find_with_locator(content, BIRTHDAY_LOCATOR, BIRTHDAY_ENDER, next_index)
        hometown, next_index = find_with_locator(content, HOME_TOWN_LOCATOR, HOME_TOWN_ENDER, next_index)
        location, next_index = find_with_locator(content, LOCATION_LOCATOR, LOCATION_ENDER, next_index)
        school, _ = find_with_locator(school, SCHOOL_DETAIL_LOCATOR, SCHOOL_DETAIL_ENDER, 0)
        birthday, _ = find_with_locator(birthday, BIRTHDAY_DETAIL_LOCATOR, BIRTHDAY_DETAIL_ENDER, 0)
        birthday_western_format = format_birthday_western(birthday)
        renren_profile = get_profile_link(renren_id)
        pinyin_name = to_pinyin(renren_name)
        if location:
            print pinyin_name, renren_profile, renren_id, renren_name, school, birthday, birthday_western_format
