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

def find_course_by_number(course_name:str) -> BeautifulSoup:
    # clean up course name
    course_name=re.split('[- \n]',course_name.strip().lower())
    course_name.append(''.join(x for x in course_name[1] if x.isnumeric()))
    

    # get the right url from website
    if int(course_name[2])<500:
        url=f"https://bulletins.psu.edu/university-course-descriptions/undergraduate/{course_name[0]}/"
    elif int(course_name[2])<=799 and int(course_name[2])>=700:
        url=f"https://bulletins.psu.edu/university-course-descriptions/medicine/{course_name[0]}/"
    elif (int(course_name[2])<=699 and int(course_name[2])>=500) or (int(course_name[2])<=899 and int(course_name[2])>=800):
        url=f"https://bulletins.psu.edu/university-course-descriptions/graduate/{course_name[0]}/"
    elif int(course_name[2])<=999 and int(course_name[2])>=900:
        try:
            url=f"https://bulletins.psu.edu/university-course-descriptions/dickinsonlaw/{course_name[0]}/"
        finally:
            url=f"https://bulletins.psu.edu/university-course-descriptions/pennstatelaw/{course_name[0]}/"
    
    soup=read_page(url)
    # look for the right course
    courses=soup.find_all(class_="courseblock")
    for p in courses:
        course=p.find(class_="course_code").contents
        if course[2].contents[0].lower()==course_name[1]:
            return p
    
    return None

def get_course_name(soup:BeautifulSoup) -> str:
    try:
        return soup.find(class_="course_codetitle").contents[0]
    except AttributeError:
        return None

def get_course_credits(soup:BeautifulSoup) -> str:
    try:
        credit_string=soup.find(class_="course_credits").contents[0].strip()
        credit_number=credit_string.split(" ")[0]
        return credit_string
    except AttributeError:
        return None

def get_course_desc(soup:BeautifulSoup) -> str:
    try:
        return soup.find(class_="courseblockdesc").find("p").get_text().strip()
    except AttributeError:
        return None

def get_course_extras(soup:BeautifulSoup) -> list:
    try:
        res=[]
        
        if soup.find_all(class_="noindent courseblockextra") :
            for i in soup.find_all(class_="noindent courseblockextra"):
                res.append(i.get_text().strip().replace("\n\t\t\t\n\n\t\t\t\t","\n"))
        
        return res
    except AttributeError:
        return [None]

def get_all_info(soup:BeautifulSoup) -> list:
    
    name=get_course_name(soup)
    credits=get_course_credits(soup)
    desc=get_course_desc(soup)
    res=[name,credits,desc]

    extras=get_course_extras(soup)
    res+=extras

    return res

def find_by_attribute(attribute:str) -> list:
    d={
        "arts":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/arts/",
        "health":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/health-wellness/",
        "humanities":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/humanities/",
        "science":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/natural-sciences/",
        "quantification":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/quantification/",
        "social":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/quantification/",
        "writing":"https://bulletins.psu.edu/undergraduate/general-education/course-lists/writing-speaking/"
    }

    if attribute in d:
        
        url=d[attribute]
        soup=read_page(url)
        courses=[]
        for i in soup.find_all(class_="even"):
            res=[]
            #courses.append(i.find(class_="code").get_text())
            course=i.find_all("td")
            for j in course:
                res.append(j.get_text())
            courses.append(res)
        return courses
    else:
        return [None]
        
def get_by_attribute(attribute:str) -> list :
    pass

def run_tests():
    import doctest
    # Run tests in all docstrings
    doctest.testmod(verbose=True)

if __name__== "__main__":
    #print(find_by_attribute(i))
    #run_tests()
    pass