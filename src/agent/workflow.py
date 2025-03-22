from langgraph.graph import StateGraph
from typing import Dict, Any
from .llm import LLMHandler
from .webpage_analyzer import WebpageAnalyzer
from ..utils.monitoring import MetricsCollector

class WebpageMaintenanceAgent:
    def __init__(self):
        self.llm = LLMHandler()
        self.analyzer = WebpageAnalyzer()
        self.metrics = MetricsCollector()
    
    def create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for webpage maintenance."""
        workflow = StateGraph()
        
        # Add nodes
        workflow.add_node("analyze", self.analyze_node)
        workflow.add_node("plan", self.plan_node)
        workflow.add_node("execute", self.execute_node)
        workflow.add_node("verify", self.verify_node)
        
        # Add edges
        workflow.add_edge("analyze", "plan")
        workflow.add_edge("plan", "execute")
        workflow.add_edge("execute", "verify")
        workflow.add_edge("verify", "analyze")  # Cyclical loop
        
        return workflow
    
    def analyze_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the webpage and collect metrics."""
        url = state.get("url")
        if not url:
            return {"error": "No URL provided", "status": "failed"}
        
        # Analyze webpage
        analysis = self.analyzer.analyze_page(url)
        
        # Get LLM analysis
        llm_analysis = self.llm.analyze_content(analysis.get("content", ""))
        
        # Collect metrics
        self.metrics.record_analysis(analysis)
        
        return {
            **state,
            "analysis": analysis,
            "llm_analysis": llm_analysis,
            "status": "analyzed"
        }
    
    def plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create a maintenance plan based on analysis."""
        analysis = state.get("analysis", {})
        llm_analysis = state.get("llm_analysis", {})
        
        # Generate maintenance plan using LLM
        prompt = f"""Based on the following analysis, create a detailed maintenance plan:
        
        Technical Analysis:
        {analysis}
        
        LLM Analysis:
        {llm_analysis}
        
        Please provide:
        1. Priority tasks
        2. Required changes
        3. Implementation steps
        4. Expected outcomes
        """
        
        plan = self.llm.generate_text(prompt)
        
        return {
            **state,
            "plan": plan,
            "status": "planned"
        }
    
    def execute_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the maintenance plan."""
        plan = state.get("plan")
        if not plan:
            return {"error": "No plan provided", "status": "failed"}
        
        # Generate execution steps using LLM
        prompt = f"""Based on the following plan, generate specific execution steps:
        
        Plan:
        {plan}
        
        Please provide:
        1. Step-by-step implementation
        2. Required tools/technologies
        3. Potential challenges
        4. Success criteria
        """
        
        execution_steps = self.llm.generate_text(prompt)
        
        # Record execution metrics
        self.metrics.record_execution(execution_steps)
        
        return {
            **state,
            "execution_steps": execution_steps,
            "status": "executed"
        }
    
    def verify_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Verify the execution results."""
        execution_steps = state.get("execution_steps")
        if not execution_steps:
            return {"error": "No execution steps provided", "status": "failed"}
        
        # Generate verification steps using LLM
        prompt = f"""Based on the following execution steps, create verification criteria:
        
        Execution Steps:
        {execution_steps}
        
        Please provide:
        1. Verification checklist
        2. Success metrics
        3. Potential issues
        4. Improvement suggestions
        """
        
        verification = self.llm.generate_text(prompt)
        
        # Record verification metrics
        self.metrics.record_verification(verification)
        
        return {
            **state,
            "verification": verification,
            "status": "verified"
        }
    
    def run(self, url: str) -> Dict[str, Any]:
        """Run the complete workflow."""
        workflow = self.create_workflow()
        agent_executor = workflow.compile()
        
        # Initialize state
        initial_state = {
            "url": url,
            "status": "initialized"
        }
        
        # Run the workflow
        try:
            result = agent_executor.invoke(initial_state)
            return result
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
        finally:
            self.analyzer.close() 