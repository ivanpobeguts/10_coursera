from lxml import etree
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse


def get_courses_list(keyword):
    courses_list = []
    courses_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses = requests.get(courses_url)
    bytes_courses_list = bytes(courses.text, 'utf-8')
    root = etree.fromstring(bytes_courses_list)
    for url in root.getchildren():
        for loc in url.getchildren():
            if keyword in loc.text:
                courses_list.append(loc.text)
    return courses_list


def get_course_info(course_url):
    course_info_dict = {}
    course_html = requests.get(course_url)
    course_html.encoding = 'utf-8'
    soup = BeautifulSoup(course_html.text, 'html.parser')
    course_info_dict['name'] = soup.find('h1', {"class": "title display-3-text"}).text
    course_info_dict['language'] = soup.find('div', {"class": "rc-Language"}).text
    rating = soup.find('div', {"class": "ratings-text bt3-visible-xs"})
    if rating:
        course_info_dict['rating'] = rating.text[:3]
    else:
        course_info_dict['rating'] = '-'
    course_info_dict['start_date'] = soup.find('div', {"class": "startdate rc-StartDateString caption-text"}).text
    course_info_dict['weeks'] = len(soup.findAll('div', {"class": "week"}))
    return course_info_dict


def output_courses_info_to_xlsx(course_info, sheet):
    sheet.append({
        1: course_info['name'],
        2: course_info['language'],
        3: course_info['rating'],
        4: course_info['start_date'],
        5: course_info['weeks']
    })


def get_workbook():
    wb = Workbook(encoding='utf-8')
    sheet = wb.active
    sheet.title = "python_courses"
    header = ['Name', 'Language', 'Rating', 'Start date', 'Weeks Ammount']
    sheet.append(header)
    return wb


def save_excel_workbook(excel_workbook, xlsx_filepath):
    try:
        excel_workbook.save(xlsx_filepath)
        return True
    except PermissionError:
        return False


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--filename',
        help='output path',
        default='python_courses.xlsx',
    )
    parser.add_argument(
        '--keyword',
        help='searching keyword',
        default='python',
    )
    if not parser.parse_args().filename.endswith('.xlsx'):
        parser.error(
            ".xlsx file expected!"
        )
    return parser.parse_args()


if __name__ == '__main__':
    output_path = get_parser_args().filename
    search_keyword = get_parser_args().keyword
    courses_list = get_courses_list(search_keyword)
    workbook = get_workbook()
    for course in courses_list:
        course_info = get_course_info(course)
        output_courses_info_to_xlsx(course_info, workbook.active)
    if not save_excel_workbook(workbook, output_path):
        print('Close your file before running script!')
    else:
        print('Successfully saved to', output_path)
