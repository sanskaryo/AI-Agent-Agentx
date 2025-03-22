import streamlit as st
import subprocess
import time
from src.agent.workflow import WebpageMaintenanceAgent
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def start_test_server():
    """Start the test HTTP server."""
    server_process = subprocess.Popen(['python', 'serve_test.py'])
    time.sleep(2)  # Wait for server to start
    return server_process

def run_agent_analysis(url):
    """Run the agent analysis."""
    try:
        agent = WebpageMaintenanceAgent()
        result = agent.run(url)
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return {"error": str(e), "status": "failed"}

def format_analysis_results(results):
    """Format analysis results for display."""
    if not results:
        return "No results available."
    
    formatted = "### Analysis Results\n\n"
    
    # Status
    formatted += f"**Status:** {results.get('status', 'Unknown')}\n\n"
    
    # Analysis
    if 'analysis' in results:
        formatted += "#### Technical Analysis\n"
        analysis = results['analysis']
        formatted += f"- Title: {analysis.get('title', 'N/A')}\n"
        formatted += f"- Meta Description: {analysis.get('meta_description', 'N/A')}\n"
        formatted += f"- Broken Links: {len(analysis.get('broken_links', []))}\n"
        formatted += f"- Content Issues: {len(analysis.get('content_issues', []))}\n"
        formatted += f"- SEO Issues: {len(analysis.get('seo_issues', []))}\n\n"
    
    # Plan
    if 'plan' in results:
        formatted += "#### Maintenance Plan\n"
        formatted += f"```\n{results['plan']}\n```\n\n"
    
    # Execution Steps
    if 'execution_steps' in results:
        formatted += "#### Execution Steps\n"
        formatted += f"```\n{results['execution_steps']}\n```\n\n"
    
    # Verification
    if 'verification' in results:
        formatted += "#### Verification\n"
        formatted += f"```\n{results['verification']}\n```\n"
    
    return formatted

def main():
    st.title("AI Webpage Maintenance Agent")
    st.write("This tool helps you analyze and maintain webpages using AI.")
    
    # Sidebar
    st.sidebar.title("Options")
    test_url = st.sidebar.text_input(
        "Test URL",
        value="http://localhost:8000/test_website/index.html",
        help="URL of the webpage to analyze"
    )
    
    # Main content
    st.write("### Test Website")
    st.write("The test website contains various issues that the AI agent can detect and fix:")
    st.markdown("""
    - Duplicate H1 tags
    - Empty paragraphs
    - Missing alt text in images
    - Broken links
    - Performance issues
    - SEO issues
    - Accessibility issues
    - Content issues
    """)
    
    # Analysis button
    if st.button("Run Analysis"):
        with st.spinner("Running analysis..."):
            # Start test server
            server_process = start_test_server()
            
            try:
                # Run analysis
                results = run_agent_analysis(test_url)
                st.session_state.analysis_results = results
                
                # Display results
                st.markdown(format_analysis_results(results))
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Analysis completed. Here are the results:\n\n" + format_analysis_results(results)
                })
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })
            finally:
                # Clean up
                server_process.terminate()
                server_process.wait()
    
    # Chat interface
    st.write("### Chat with the Agent")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            st.info(message["content"])
        else:
            st.write(message["content"])
    
    # Chat input
    user_input = st.text_input("Ask the agent a question:", key="user_input")
    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Process user input
            if "analyze" in user_input.lower():
                with st.spinner("Running analysis..."):
                    results = run_agent_analysis(test_url)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "I've analyzed the webpage. Here are the results:\n\n" + format_analysis_results(results)
                    })
            elif "fix" in user_input.lower():
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "I can help you fix the issues found in the webpage. Would you like me to generate a maintenance plan?"
                })
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "I can help you analyze the webpage, fix issues, or answer questions about the analysis. What would you like me to do?"
                })
            
            # Clear input
            st.session_state.user_input = ""

if __name__ == "__main__":
    main() 