import requests
from config import HOST
url = f'http://{HOST}:8080/'

job_post = '''
Title: Senior Front End Developer

Vacancy:
01

Job Context:
We are looking for a Front-End Web Developer who is motivated to combine the art of design with the art of programming. Responsibilities will include translation of the UI/UX design wireframes to actual code that will produce visual elements of the application.

Job Responsibilities:
• You will implement beautiful layouts using CSS and HTML.
• Familiarity common JavaScript Plugins or API(youtube, google map,html to canvas).
• Developing web application with cross-browser support, and with fluid, elastic or responsive designs.
• Build reusable code and libraries for future use.

Technical Requirements:
• Excellent critical thinking skills.
• Extensive experience in HTML5 & CSS Coding.
• Ability to write oriented and reusable CSS code is must.
• Knowledge on PHP, MySQL, Wordpress, XML
• Knowledge on SVG, Canvas etc
• Excellent design and color thinking.
• Knowledge of graphics software such as Adobe Suite, Photoshop etc.
• Must have the mentality of always using the correct dummy text.
• Highly organized, detail oriented, and able to work autonomously with minimal direction as well as in a team.
• Solution driven with ability to understand the big picture.
• Optimize application for maximum speed and scalability.
• Proficient understanding of web markup, including HTML5, CSS3, Bootstrap.
• Should have strong knowledge of Javascript, Ajax, JQuery.
• Must be able to handle & fix problem from Cpanel, FTP, Web Server, etc.
• Cross Browser Compatibility with most common browsers (Chrome, Firefox, IE, Safari, Opera).
• Knowledge on common project automation tools like grunt, gulp, webpack etc.
• Should have the basic knowledge of at least few of the advanced JavaScript libraries and frameworks, such as AngularJS, ReactJS, VueJS, NodeJS, etc.
• Experience in using CSS pre-processors such as LESS, SASS or Stylus etc
• Experience in using image/component lazy loading.
• Understanding of assets compression.

Employment Status:
Full-time

Educational Requirements:
• Design skills and creativity that matters. There is no strict requirement for educational qualification.

Experience Requirements:
• 2 to 4 year(s)
• The applicants should have experience in the following area(s):
Web Designer
• The applicants should have experience in the following
business area(s):
Software Company

Additional Requirements:
• Both males and females are allowed to apply.
• Must have a “can-do” attitude.
• Can think out of the box.
• You are a lifelong learner and passionate about learning new things and taking on new challenges.
• Ability to work under pressure.
• Problem-solving skill.
• Hard-working.
• Team player.
• Mindset to work at home with dedication.
• Strong internet connection with good backup plan.

Job Location:
Remote (any location)

Salary:
30k-40k

Compensation & Other Benefits:
• 2 Annual Festival Bonuses
• Salary Review: Yearly
• Necessary Public holidays and casual leaves

Read Before Apply:
Must Follow the Format, otherwise it would go to spam box.
Send your CV using subject 'Your name – FED x Yrs Exp' , replace x with number 2,3,4,5 etc, with body copy year of experience, experience summary & Expected salary to hr@technovicinity.com. CV file name format must be 'Name_FED_Experience_year'.
If you feel you are smart & meet these requirements and have the quality & dream to be the market leader in your profession - feel free to email your detailed resume to hr@technovicinity.com

Special note: Technovicinity Limited is based at Dhaka, Bangladesh, but this is a purely remote based job. But applicant should be mentally prepared to work in office environment if needed. There is going to be fixed office hours(with flexibility to set the hours). You need to have the mindset to work remotely, but as a team member with others. It could be good, as you work at your home comfort. But need to have a plan to manage professional and personal life well.
'''
data = {'desc':job_post}
response = requests.post(url, json=data)

print(response.json())