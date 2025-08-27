"""Result formatting module."""

from typing import List, Dict, Any


class ResultFormatter:
    """Handles formatting of search results for display."""
    
    @staticmethod
    def format_search_results(results: List[Dict[str, Any]], query: str = "") -> str:
        """Format search results for display."""
        if not results:
            return ResultFormatter._format_no_results(query)
        
        formatted = f"🔍 **Found {len(results)} result(s) for:** '{query}'\n\n"
        
        for i, result in enumerate(results, 1):
            similarity_percent = int(result['similarity'] * 100)
            
            tool = str(result['tool']).strip()
            action = str(result['action']).strip()
            summary = str(result['summary']).strip()
            link = str(result['link']).strip()
            
            formatted += f"**{i}. {tool} - {action}** ({similarity_percent}% match)\n"
            formatted += f"📝 **Summary:** {summary}\n"
            formatted += f"🔗 **Documentation:** [{link}]({link})\n\n"
        
        return formatted
    
    @staticmethod
    def _format_no_results(query: str) -> str:
        """Format message when no results are found."""
        return (f"🔍 No relevant results found for: '{query}'\n\n"
               "💡 **Tips:**\n"
               "- Try different keywords\n"
               "- Use tool names (GitLab, Jira, SonarQube, etc.)\n"
               "- Search for actions (setup, configure, deploy, etc.)")
    
    @staticmethod
    def format_status_message(record_count: int) -> str:
        """Format status message for UI display."""
        status_emoji = "✅" if record_count > 0 else "❌"
        return f"**{status_emoji} Data Status:** {record_count} records loaded from data/ folder"