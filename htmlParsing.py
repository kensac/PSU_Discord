
# importing modules
import urllib.request 
from bs4 import BeautifulSoup
import re
  
# providing url
testUrl = "https://bulletins.psu.edu/university-course-descriptions/undergraduate/inart/"


def read_page(url:str)-> BeautifulSoup:
    """
        >>> type(read_page("https://bulletins.psu.edu/university-course-descriptions/undergraduate/inart/"))
        <class 'bs4.BeautifulSoup'>
    """
    # opening the url for reading
    html = urllib.request.urlopen(url)

    # parsing the html file
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def find_course_by_number(course_name:str):
    # clean up course name
    course_name=re.split('[- \n]',course_name.strip().lower())

    # get the right url from website
    url=f"https://bulletins.psu.edu/university-course-descriptions/undergraduate/{course_name[0]}/"
    soup=read_page(url)

    # look for the right course
    courses=soup.find_all(class_="courseblock")
    for p in courses:
        course=p.find(class_="course_code").contents

        if course[2].contents[0]==course_name[1]:
            return p



def run_tests():
    import doctest
    # Run tests in all docstrings
    doctest.testmod(verbose=True)

if __name__== "__main__":
    print(
        find_course_by_number("Math 140 ")
    )
    #run_tests()