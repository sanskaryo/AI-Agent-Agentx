import pytest
from src.agent.workflow import WebpageMaintenanceAgent
from src.agent.llm import LLMHandler
from src.agent.webpage_analyzer import WebpageAnalyzer
from src.utils.monitoring import MetricsCollector
from src.utils.mcp import MCPHandler

@pytest.fixture
def agent():
    return WebpageMaintenanceAgent()

@pytest.fixture
def llm():
    return LLMHandler()

@pytest.fixture
def analyzer():
    return WebpageAnalyzer()

@pytest.fixture
def metrics():
    return MetricsCollector()

@pytest.fixture
def mcp():
    return MCPHandler()

def test_agent_initialization(agent):
    assert agent.llm is not None
    assert agent.analyzer is not None
    assert agent.metrics is not None

def test_llm_text_generation(llm):
    prompt = "Test prompt"
    response = llm.generate_text(prompt)
    assert isinstance(response, str)
    assert len(response) > 0

def test_webpage_analysis(analyzer):
    url = "https://example.com"
    analysis = analyzer.analyze_page(url)
    assert isinstance(analysis, dict)
    assert "url" in analysis
    assert "title" in analysis
    assert "meta_description" in analysis

def test_metrics_collection(metrics):
    test_data = {
        "seo_score": 85,
        "performance_metrics": {
            "load_time": 1.5
        }
    }
    metrics.record_analysis(test_data)
    current_metrics = metrics.get_metrics()
    assert current_metrics["seo_score"] == 85
    assert current_metrics["performance_score"] > 0

def test_mcp_requests(mcp):
    url = "https://example.com"
    seo_data = mcp.get_seo_data(url)
    assert isinstance(seo_data, dict)
    
    performance_data = mcp.get_performance_data(url)
    assert isinstance(performance_data, dict)

def test_agent_workflow(agent):
    url = "https://example.com"
    result = agent.run(url)
    assert isinstance(result, dict)
    assert "status" in result
    assert "analysis" in result
    assert "plan" in result
    assert "execution_steps" in result
    assert "verification" in result 