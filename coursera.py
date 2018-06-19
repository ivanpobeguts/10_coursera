from lxml import etree
import requests
from bs4 import BeautifulSoup


def get_courses_list():
    courses_list = []
    courses_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses = requests.get(courses_url)
    bytes_courses_list = bytes(courses.text, 'utf-8')
    root = etree.fromstring(bytes_courses_list)
    for url in root.getchildren():
        for loc in url.getchildren():
            if 'python' in loc.text:
                courses_list.append(loc.text)
    return courses_list


def get_course_info(course_url):
    course_info_dict = {}
    course_html = requests.get(course_url)
    soup = BeautifulSoup(course_html.text, 'html.parser')
    course_info_dict['name'] = soup.find('h1', {"class": "title display-3-text"}).text
    course_info_dict['language'] = soup.find('div', {"class": "rc-Language"}).text
    rating = soup.find('div', {"class": "ratings-text bt3-visible-xs"})
    if rating:
        course_info_dict['rating'] = rating.text[:3]
    else:
        course_info_dict['rating'] = '-'
    course_info_dict['start_date'] = soup.find('div', {"class": "startdate rc-StartDateString caption-text"}).text[7:]
    course_info_dict['weeks'] = len(soup.findAll('div', {"class": "week"}))
    return course_info_dict

def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    courses_list = get_courses_list()
    print(courses_list)
    for course in courses_list:
        print(get_course_info(course))
