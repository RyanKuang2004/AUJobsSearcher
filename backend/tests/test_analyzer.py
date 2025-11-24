import os
import json
from analyzers.job_analyzer import JobAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_analyzer():
    print("Testing JobAnalyzer...")
    
    # Check for API keys
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set. Test may fail if using OpenAI.")
    
    analyzer = JobAnalyzer()
    
    sample_description = """
Make an impact in a collaborative, supportive team in an exciting new space focusing on AI!
We're REA
With bold and ambitious goals, REA Group  is changing the way the world experiences property. No matter where you're at on your property journey, we're here to help with every step - whether that's finding or financing your next home.
Our people are the key to our success. At the heart of everything we do, is a thriving culture centred around high performance and care. We are purpose driven and collaborative, which drives innovation and our ability to make a real impact. As such, we’re proud to have been named in Australia’s “Top 5” Best Workplaces two years in a row, as well as being recognised as a Best Workplace for Women.
Day to day of the job
Assist in designing scalable, multi-modal AI solutions (text, image, audio, video) for our web and app platforms.
Utilize Generative AI, LLMs, and VLMs, combining them with traditional ML techniques to deliver impactful solutions.
Build and deploy real-time ML, APIs and batch pipelines using multi-cloud frameworks (AWS/GCP) and tools like SageMaker/VertexAI, Docker, Infrastructure as Code, and Python.
Develop models that enhance property valuations, predict user behaviour, and provide personalised experiences.
Create recommender systems (Collaborative Filtering, Content-Based, Hybrid) using techniques like
Matrix Factorization, Learning to Rank, and Deep Learning.
Extract insights from structured and unstructured data (e.g., text, image, video) for business impact.
Develop visualisation tools to support data and model analytics.
Collaborate with internal stakeholders to design and enhance data products.
Promote REA’s AI, ML, and analytics capabilities both internally and externally.
Who we’re looking for
Practical experience in ML engineering, data science, or related fields.
Skilled in large-scale development with one of the following programming languages: Python or SQL
Competence in one or more of the following areas: Deep Learning / Generative AI, Computer Vision, Recommender Systems, Machine Learning
Experience with key ML libraries such as PyTorch, Keras, HF models, Transformers, XGBoost/LightGBM, and Scikit-learn.
Familiarity with relational databases (e.g., MySQL, PostgreSQL), BigQuery and NoSQL databases (e.g., Redis/DynamoDB, ElasticSearch/Solr, GraphDB).
Experience with cloud platforms: AWS (e.g., EC2, ELB, S3, VPC, Route 53) OR Google Cloud (e.g., Vertex AI, Compute Engine, Pub/Sub, GCS)
Comfortable with containerisation technologies such as Docker.
Some experience deploying AI systems in real-time, production environments.
Familiarity with deployment tools like Terraform, or CloudFormation.
Good communication and interpersonal skills
The REA experience
The physical, mental, emotional and financial health of our people is something we’ll never stop caring about. This is a place to learn and grow.
Some of our
Perks & Benefits
include:
A hybrid and flexible approach to working
Flexible leave options including, birthday leave and purchase additional leave
Flexible parental leave offering for primary and secondary carers
Our Because We Care program offers employees volunteering leave, community grants, matched payroll giving and our Community Café donates 100% of revenue to charity
Hackdays so you can bring your big ideas to life
Our commitment to Diversity, Equity, and Inclusion
We are committed to providing a working environment that embraces and values diversity, equity and inclusion. We believe teams with diverse ideas and experiences are more creative, more eﬀective and fuel disruptive thinking. If you've got the skills, dedication and enthusiasm to learn but don't necessarily meet every single point on the job description, please still get in touch.
Join our Talent Neighbourhood
Keen to be part of REA but didn't find a perfect match with this opportunity? Perhaps the timing isn't right? You should join our Talent Neighbourhood!
#LI-HYBRID
    """
    
    print("\nAnalyzing sample description...")
    try:
        result = analyzer.analyze_job_description(sample_description)
        print("\nResult:")
        print(json.dumps(result, indent=2))
        
        # Basic validation
        assert "skills" in result
        assert "responsibilities" in result
        assert "employer_focus" in result
        print("\nValidation Successful!")
    except Exception as e:
        print(f"\nTest Failed: {e}")

if __name__ == "__main__":
    test_analyzer()
