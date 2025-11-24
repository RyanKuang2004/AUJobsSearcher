import unittest
import os
from dotenv import load_dotenv
from analyzers.job_analyzer import JobAnalyzer

# Load environment variables
load_dotenv()

class TestLLMIntegration(unittest.TestCase):
    def test_analyze_job_description(self):
        """
        Tests that the JobAnalyzer can successfully call the OpenAI API
        and return a structured response without temperature errors.
        """
        # Ensure API key is present
        if not os.environ.get("OPENAI_API_KEY"):
            print("Skipping LLM test: OPENAI_API_KEY not found.")
            return

        analyzer = JobAnalyzer()
        
        description = """
        Company Description
About SEEK
SEEK’s portfolio of diverse businesses make a positive impact on a truly global scale. Our purpose is to help people live more fulfilling and productive working lives and help organisations succeed. We create world-class technology solutions to connect more people to relevant employment, education, small business and volunteer opportunities. We have a culture of high-performance in our workplaces and celebrate the diversity of our employees who contribute to the success of our organisation.
Life at SEEK
SEEK’s purpose is at the centre of everything we do.
Our SEEK
, which defines the way we work, is all about what makes us unique and a little bit different. Passion, Team, Delivery and Future are our principles that drive innovation and creativity. SEEK strives to support employee wellbeing by providing an amazing experience at work which led us to being named AFR BOSS Top 10 Best Places to Work in Technology (
2021-2024
). We are proud to work in an environment that's inclusive where everyone's unique ideas, experiences and perspectives are valued.
Our award-winning head office in Cremorne (just a 4 min walk from Richmond station) provides an exceptional space to collaborate with colleagues. The building provides sweeping views of the city, a games area, sit and stand desks at every workstation, modern end-of-trip facilities and Thursday night drinks which gives our people an opportunity to connect in a social setting.
Job Description
The Team
The Candidate Quality team consists of Data Scientists, AI Engineers, and Product Managers, operating as a specialized unit within SEEK’s broader Artificial Intelligence & Analytics division. We follow a quarterly planning cycle in pursuit of our mission: helping hirers connect with quality candidates. Our work encompasses developing machine learning models for candidate quality scoring, leveraging AI to enhance role requirements,
selection criteria, and candidate matching, and supporting candidate discovery.
The Role
As a Data Scientist at SEEK, you’ll be part of a fast-paced, supportive environment where you can make a real difference. You’ll work on complex challenges that have a direct impact on people’s lives, helping us evolve our business and reach new heights.
Successful performance in this role will be demonstrated through the business value contributed by developed and supported products. Further, the successful candidate will be expected to stay up to date with emerging techniques in natural language processing and machine learning, and be deeply involved in a culture of continual improvement.
This role will report to a Senior Data Scientist / Principal Data Scientist within AIPS. AIPS has a matrix structure where your direct line manager will act as a coach and technical mentor but your day-to-day activity will be determined by the squad priorities.
Key Responsibilities
Forming clear data addressable problem statements related to candidate-job matching and  qualification identification
Gathering, validating and understanding data relevant to job requirements and candidate qualifications
Designing and building data transformation pipelines and machine learning algorithms to improve matching accuracy and relevance
Working with product management and other business stakeholders to review and iterate data products to better serve both hirers and job seekers
Developing models that can effectively identify and highlight relevant skills and qualifications from  unstructured text data
Evangelising appropriate ML methods and explaining them, and their associated benefits and limitations to team members from Engineering and Strategy.
Qualifications
Essential Qualifications, Skills and Experience
Post graduate qualification in a quantitative field (e.g. Physics, Mathematics, Bioinformatics, Computer Science)
Advanced data extraction and processing skills using SQL, Spark, etc
Familiarity with S3, EC2 and/or EMR in AWS
Deep knowledge of machine learning algorithms focused on classification, ranking and recommendation systems
Experience with NLP, particularly information extraction and semantic similarity
Able to write serviceable code (e.g. Python, Scala) and comfortable working with and around a professional software development team
Good communication and interpersonal skills with the ability to communicate complex technical concepts to business key decision makers and product owners
Ability to adapt quickly and thrive in an ambiguous and rapidly changing environment
Other Qualifications, Skills and Experience
Experience with Deep Learning (particularly Transformers and other modern NLP architectures)
Experience with large language models and their application to information extraction
Track record in working independently within an agile team environment, scoping work, making and keeping commitments to deliver against a shared agenda
Experience working with datasets which do not fit within memory on a single machine
Experience developing systems that operate at scale in production environments
Additional Information
Permanent Perks
At SEEK we offer:
Annual Performance Bonus Plan
Support of flexible working, including a mix of office and work from home days depending on your role.
Paid and unpaid leave benefits including Personal Flexi Days and Volunteer Days, as well as the opportunity to purchase additional leave
Support for parents with 14 weeks paid primary carers leave and 2 weeks paid leave for partners
SEEK is committed to operating sustainably and is preparing for the impacts of climate change and the transition to a low-carbon future, and is working to minimise its environmental impacts which includes a long-term emissions reduction target of net zero by FY2050
The opportunity to work from anywhere for up to 4 weeks per financial year
SEEKer Support, a confidential service that offers employees up to six sessions with a mental health professional of your choice
Tailored career development planning (including Education Assistance Program)
Professional development sessions with industry leading guest speakers
Free income protection insurance
Access to a wide range of discounts on things such as health insurance, fitness, food, travel, accommodation plus many more
Frequent events including sports days, annual Christmas party, hackathon, and trivia
Free kick-start breakfast every morning and fresh fruit available all day in our offices
Casual dress – every day
At SEEK, we are passionate about fostering a culture of inclusion and wellbeing that embraces and values the diversity of our people. We are a purpose driven business that works with heart.
We know teams with diverse ideas, experiences and perspectives are more creative and are critical to ensuring effective delivery and innovating to enable our future success. As such, we welcome applications from people with diverse backgrounds and life experiences, especially as they relate to gender, sexual identity, culture, faith, disability and life stages. If you have the skills, curiosity and an adaptable mindset but don't meet every responsibility or qualification listed in this advertisement, please still get in touch with us.
Should you require any specific support or adjustments throughout the recruitment process and beyond, please advise us and we will be happy to assist.
For this role, only those candidates with the eligible right to work will be considered.
SEEK kindly requests no unsolicited resumes or approaches from recruitment agencies and will not be responsible for any associated fees.
        """
        
        print(f"Testing with model: {analyzer.llm.model_name}")
        
        result = analyzer.analyze_job_description(description)
        
        print("LLM Result:", result)


if __name__ == "__main__":
    unittest.main()
