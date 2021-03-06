from lxml import etree
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse


def get_data_from_url(url):
    response = requests.get(url)
    return response.content


def get_courses_urls_from_xml(courses_xml, keyword):
    courses_list = []
    root = etree.fromstring(courses_xml)
    for url in root.getchildren():
        for loc in url.getchildren():
            if keyword in loc.text:
                courses_list.append(loc.text)
    return courses_list


def get_course_info(course_html):
    course_info_dict = {}
    soup = BeautifulSoup(course_html, 'html.parser')
    course_info_dict['name'] = soup.find('h1', {'class': 'title display-3-text'})
    course_info_dict['language'] = soup.find('div', {'class': 'rc-Language'})
    course_info_dict['rating'] = soup.find('div', {'class': 'ratings-text bt3-visible-xs'})
    course_info_dict['start_date'] = (
        soup.find('div', {'class': 'startdate rc-StartDateString caption-text'})
    )
    course_info_dict['weeks'] = soup.findAll('div', {'class': 'week'})
    return course_info_dict


def output_courses_info_to_xlsx(course_info, sheet):
    sheet.append({
        1: course_info['name'].text,
        2: course_info['language'].text,
        3: course_info['rating'].text[:3]
            if course_info['rating'] else '-',
        4: course_info['start_date'].text,
        5: len(course_info['weeks'])
    })


def get_workbook():
    wb = Workbook(encoding='utf-8')
    sheet = wb.active
    sheet.title = 'python_courses'
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
        '-f',
        help='output path',
        default='courses.xlsx',
    )
    parser.add_argument(
        '--keyword',
        '-k',
        help='searching keyword',
        default='',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_parser_args()
    output_path = args.filename
    if not output_path.endswith('.xlsx'):
        print('Warning: your file extension is not .xlsx!')
    search_keyword = args.keyword
    courses_urls = get_courses_urls_from_xml(
        get_data_from_url('https://www.coursera.org/sitemap~www~courses.xml'),
        search_keyword
    )
    workbook = get_workbook()
    for course_url in courses_urls:
        course_info = get_course_info(get_data_from_url(course_url))
        output_courses_info_to_xlsx(course_info, workbook.active)
    if not save_excel_workbook(workbook, output_path):
        print('Close your file before running script!')
    else:
        print('Successfully saved to', output_path)
