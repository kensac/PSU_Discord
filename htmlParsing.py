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
    if int(course_name[1])<500:
        url=f"https://bulletins.psu.edu/university-course-descriptions/undergraduate/{course_name[0]}/"
    elif int(course_name[1])<=799 and int(course_name[1])>=700:
        url=f"https://bulletins.psu.edu/university-course-descriptions/medicine/{course_name[0]}/"
    elif (int(course_name[1])<=699 and int(course_name[1])>=500) or (int(course_name[1])<=899 and int(course_name[1])>=800):
        url=f"https://bulletins.psu.edu/university-course-descriptions/graduate/{course_name[0]}/"
    elif int(course_name[1])<=999 and int(course_name[1])>=900:
        try:
            url=f"https://bulletins.psu.edu/university-course-descriptions/dickinsonlaw/{course_name[0]}/"
        finally:
            url=f"https://bulletins.psu.edu/university-course-descriptions/pennstatelaw/{course_name[0]}/"
    soup=read_page(url)

    # look for the right course
    courses=soup.find_all(class_="courseblock")
    for p in courses:
        course=p.find(class_="course_code").contents

        if course[2].contents[0]==course_name[1]:
            return p
    
    return None

def get_course_name(soup):
    return soup.find(class_="course_codetitle").contents[0]

def get_course_credits(soup):
    credit_string=soup.find(class_="course_credits").contents[0].strip()
    credit_number=credit_string.split(" ")[0]
    return credit_string

def get_course_desc(soup):
    try:
        return soup.find(class_="courseblockdesc").find("p").get_text().strip()
    finally:
        return None



def run_tests():
    import doctest
    # Run tests in all docstrings
    doctest.testmod(verbose=True)

if __name__== "__main__":
    i=find_course_by_number("AULWR 997 ")
    print(
        get_course_desc(i)
    )
    #run_tests()