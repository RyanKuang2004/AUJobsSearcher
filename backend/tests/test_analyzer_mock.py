import os
import json
from analyzers.job_analyzer import JobAnalyzer
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

def test_analyzer_mock():
    print("Testing JobAnalyzer with Mock LLM...")
    
    # Mock response data
    mock_response_data = {
        "skills": {
            "technical_skills": ["Python", "AWS"],
            "soft_skills": ["Communication"],
            "tools_and_technologies": [],
            "experience_years": ["5+ years"],
            "degrees_and_certifications": []
        },
        "responsibilities": ["Build APIs", "Mentor juniors"],
        "employer_focus": {
            "values": ["Ownership"],
            "collaboration_expectations": ["Cross-functional teams"],
            "domain_knowledge": []
        }
    }

    def mock_invoke(input):
        return AIMessage(content=json.dumps(mock_response_data))

    # Set dummy API key to pass initialization validation
    os.environ["OPENAI_API_KEY"] = "dummy-key"
    
    try:
        # Initialize analyzer
        analyzer = JobAnalyzer()
        
        # Replace the LLM with a RunnableLambda
        analyzer.llm = RunnableLambda(mock_invoke)
        
        sample_description = "Test description"
        
        print("\nAnalyzing sample description (Mocked)...")
        result = analyzer.analyze_job_description(sample_description)
        
        print("\nResult:")
        print(json.dumps(result, indent=2))
        
        # Validation
        assert result["skills"]["technical_skills"] == ["Python", "AWS"]
        assert result["responsibilities"] == ["Build APIs", "Mentor juniors"]
        print("\nMock Validation Successful!")
        
    finally:
        # Clean up env var
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

if __name__ == "__main__":
    test_analyzer_mock()
