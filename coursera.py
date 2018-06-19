from lxml import etree
import requests


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


def get_course_info(course_slug):
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    print(get_courses_list())
