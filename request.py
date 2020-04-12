import requests
from config import HOST
url = f'http://{HOST}:8080/'

job_post = '''

Title: Senior iOS Developer

Vacancy:
01

Job Context:
We are looking for a Senior iOS Developer who is motivated to combine the art of design with the art of programming.

Job Responsibilities:
● Online Portfolio or example of live work is MUST.
● Excellent design and color thinking.
● Taking responsibilities to develop and maintain a small or large scale project.
● Revision, modification, and integration of existing projects.
● Good problem solving and programming skills.
● Candidate must be able to lead the team and provide solutions.
● Familiarity with RESTful APIs to connect iOS applications to back-end services
● Develop new mobile applications according to clients/management requirements.
● Manage projects, maintain documentation on different phases of projects.
● Respond promptly and fix the issues/bugs identified by clients/QC.
● Must have hands-on experience on using Auto Layout to support adaptive layouts
● Knows how to handle both XIB files and storyboard
● Extensive experience in developing high performance Enterprise iOS applications with multilingual support
● Push notifications using APNS and Firebase, camera UI handling etc.
● Must have very good Object Oriented Concepts
● Hands-on experience on publishing iOS app in apple app store is a must
● Comfortable working through the entire stack from user interface through the systems levels
● Experience on web service or Web API integration and consuming XML or JSON is a must
● Database programming skills on SQLite, MySQL or PostgreSql
● Hard working, Innovative, Quality Conscious, Self-motivated
● Keep skills current with new technologies
● Has to work on multiple projects
● Have to use the version controlling system (git).
● Follows iOS best practices according to community rules.
● Maintains proper iOS coding convention.
● Writes readable and easy codes.
● Must be a team player.
● Should be comfortable using SwiftLint and Objective-Clean.

Employment Status:
Full-time

Educational Requirements:
● We don't care about your academic qualifications.
● If you are a smart developer, eager to work from home, join with us.

Experience Requirements:
● At least 4 year(s)
● The applicants should have experience in the following area(s):
iOS Application Development, Mobile apps developer

Additional Requirements:
● Age 24 to 36 years
● Both males and females are allowed to apply
● Required to communicate effectively with development team.
● Must have capability to adapt new technology and if necessary switch to new technology
● With the QA team, jointly develop strategies for automating testing across multiple platforms.
● Perform detailed requirement, time estimation, analysis and contribute to the design of the architecture
● Highly motivated, enthusiastic, and self-driven. Strong desire to learn new technologies.

Job Location:
Remote (any location)

Salary:
60k-100k

Compensation & Other Benefits:
• 2 Annual Festival Bonuses
• Salary Review: Yearly
• Necessary Public holidays and casual leaves

Read Before Apply:
Must Follow the Format, otherwise it would go to spam box.
Send your CV using subject 'Your name – IOS x Yrs Exp' , replace x with number 2,3,4,5 etc, with body copy year of experience, experience summary & Expected salary to hr@technovicinity.com. CV file name format must be 'Name_IOS_Experience_year'.
If you feel you are smart & meet these requirements and have the quality & dream to be the market leader in your profession - feel free to email your detailed resume to hr@technovicinity.com
Special note: Technovicinity Limited is based at Dhaka, Bangladesh, but this is a purely remote based job. But applicant should be mentally prepared to work in office environment if needed. There is going to be fixed office hours(with flexibility to set the hours). You need to have the mindset to work remotely, but as a team member with others. It could be good, as you work at your home comfort. But need to have a plan to manage professional and personal life well.


'''
data = {'desc':job_post}
response = requests.post(url, json=data)

info = response.json()['extracted_info']

for key in info.keys():
    print(f'{key} =  {info[key]}')
