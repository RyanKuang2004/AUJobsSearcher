import os
import json
import logging
from typing import Dict, Any, Optional, Literal

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JobAnalyzer")

class JobAnalyzer:
    def __init__(self):
        self.llm = self._initialize_llm()
        self.parser = JsonOutputParser()
        self.prompt = self._create_prompt()

    def _initialize_llm(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found. OpenAI model may fail.")
        return ChatOpenAI(
            model=settings.models.job_analyzer_model,
            temperature=settings.models.job_analyzer_temperature,
            api_key=api_key
        )

    def _create_prompt(self):
        template = """You are an expert job market analyst. Your task is to extract structured information from the job description below.
Only extract information that is explicitly present.
If a field has no data, omit the field entirely (do not include empty lists or nulls).

Output format:
Return valid JSON using the structure below:

{{
  "skills": {{
    "technical_skills": [],
    "soft_skills": [],
    "tools_and_technologies": [],
    "experience_years": [],
    "degrees_and_certifications": []
  }},
  "responsibilities": [],
  "employer_focus": {{
    "values": [],
    "collaboration_expectations": [],
    "domain_knowledge": []
  }}
}}

Field Definitions:
skills
Extract items only if they explicitly appear in the job description.

technical_skills
Programming languages, cloud platforms, data skills, security skills, ML/AI techniques, engineering skills, analytics, infrastructure, etc.

soft_skills
Communication, teamwork, leadership, stakeholder management, organisation, problem-solving, etc.

tools_and_technologies
Frameworks, design tools, dev tools, cloud services, platforms, software packages, libraries, etc.

experience_years
Include any statements like:
“3+ years experience”
“5 years in data engineering”
“Minimum 2 years industry experience”
Extract the text exactly as written.

degrees_and_certifications
Degrees and certs explicitly mentioned:
Bachelor's/Master’s/PhD
PMP, CISSP, AWS, GCP, CPA, etc.

responsibilities
Summarize responsibilities or tasks as short action-oriented bullet-style phrases.
Break long paragraphs into discrete items.

employer_focus
Extract employer preference signals:

values
Things the employer values in candidates:
ownership
attention to detail
initiative
adaptability
problem-solving
customer focus

collaboration_expectations
Explicit statements about working with:
cross-functional teams
product, engineering, design, marketing
stakeholders
executives

domain_knowledge
Industry or domain-specific knowledge:
finance
healthcare
gaming
education
government
ecommerce
Only include if explicitly written.

Rules:
Extract only explicit content — no assumptions or inference.
Omit empty fields entirely.
Keep all items as short, clean phrases.
Ensure JSON is valid.
Make all lists contain unique items.

Job Description:
{description}
"""
        return ChatPromptTemplate.from_template(template)

    def analyze_job_description(self, description: str) -> Dict[str, Any]:
        """
        Analyzes the job description and returns structured data.
        """
        if not description:
            return {}

        try:
            chain = self.prompt | self.llm | self.parser
            result = chain.invoke({"description": description})
            return result
        except OutputParserException as e:
            logger.error(f"Error parsing LLM output: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error during LLM analysis: {e}")
            return {}

    async def analyze_job_description_async(self, description: str) -> Dict[str, Any]:
        """
        Analyzes the job description asynchronously and returns structured data.
        """
        if not description:
            return {}

        try:
            chain = self.prompt | self.llm | self.parser
            result = await chain.ainvoke({"description": description})
            return result
        except OutputParserException as e:
            logger.error(f"Error parsing LLM output: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error during async LLM analysis: {e}")
            return {}

if __name__ == "__main__":
    # Simple test
    analyzer = JobAnalyzer()
    sample_description = """
    We are looking for a Senior Software Engineer with 5+ years of experience in Python and AWS.
    You should have strong communication skills and be able to work in a cross-functional team.
    Responsibilities include building scalable APIs and mentoring junior developers.
    """
    print(json.dumps(analyzer.analyze_job_description(sample_description), indent=2))
