import requests

from bs4 import BeautifulSoup


def retreive_google_career_qualification(url: str) -> dict:
    """
    For the given Google Jobs URL, retrieve all the "qualification" sections.
    This should return a dictionary format of the qualification string (Ex. Minimum qualification) as a key,
    and a list of paragraphs given under the qualifiaction string.
    {'Minimum qualifications:': ['Currently enrolled in or graduated from a degree program within Product Management, Computer Science, Engineering, Data Science, Mathematics, Statistics, or a related technical field, or equivalent practical experience.', 'Internship or Teaching Assistant experience in product management, software development or a similar technical field.', 'Experience leading entrepreneurial efforts or outreach within organizations while building cross-functional relationships.', 'Experience preparing and delivering technical presentations to an audience through internships, coursework, or extracurriculars.'],
     'Preferred qualifications:': ['Experience with methodologies aimed to drive product development and delivery.', 'Experience applying AI/ML concepts to build products or features through relevant internship, capstone projects, or other academic work.', 'Technical experience with programming languages, data analysis, business case/modeling, pricing, or design.', 'Ability to start full-time in the primary cohort onboarding cycle between April and August 2026.', 'Ability to communicate in English fluently to support cross-functional business relationships in the region.', 'Excellent problem-solving, organizational, investigative, and critical thinking skills.']}
    """
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    # Find min qual text and pref qual text
    min_qual_text = soup.find("h3", string="Minimum qualifications:")
    min_qual_html_list = min_qual_text.find_next_sibling("ul")

    min_qual_list = []
    for qual in min_qual_html_list:
        qual = qual.get_text(strip=True)
        if qual != '':
            min_qual_list.append(qual)

    qual_dict = dict()
    qual_dict[min_qual_text.get_text(strip=True)] = min_qual_list    

    pref_qual_text = soup.find("h3", string='Preferred qualifications:')
    pref_qual_html_list = pref_qual_text.find_next_sibling("ul")

    pref_qual_list = []
    for qual in pref_qual_html_list:
        qual = qual.get_text(strip=True)
        if qual != '':
            pref_qual_list.append(qual)
    
    qual_dict[pref_qual_text.get_text(strip=True)] = pref_qual_list

    print(qual_dict)

    return qual_dict
