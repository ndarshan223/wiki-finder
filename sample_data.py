import pandas as pd
import os

def create_sample_data():
    """Create sample Excel data for testing"""
    
    sample_data = [
        # GitLab
        {"Tool": "GitLab", "Action": "Setup CI/CD Pipeline", "Summary": "Configure GitLab CI/CD pipeline for automated testing and deployment", "Confluence Link": "https://confluence.company.com/gitlab-cicd"},
        {"Tool": "GitLab", "Action": "Create Repository", "Summary": "How to create and configure a new GitLab repository with proper permissions", "Confluence Link": "https://confluence.company.com/gitlab-repo"},
        {"Tool": "GitLab", "Action": "Merge Request", "Summary": "Best practices for creating and reviewing merge requests in GitLab", "Confluence Link": "https://confluence.company.com/gitlab-mr"},
        
        # CloudBees
        {"Tool": "CloudBees", "Action": "Jenkins Setup", "Summary": "Install and configure CloudBees Jenkins for enterprise CI/CD", "Confluence Link": "https://confluence.company.com/cloudbees-setup"},
        {"Tool": "CloudBees", "Action": "Pipeline Configuration", "Summary": "Create declarative pipelines in CloudBees Jenkins", "Confluence Link": "https://confluence.company.com/cloudbees-pipeline"},
        
        # Nexus
        {"Tool": "Nexus", "Action": "Repository Management", "Summary": "Configure Nexus repository manager for artifact storage", "Confluence Link": "https://confluence.company.com/nexus-repo"},
        {"Tool": "Nexus", "Action": "Security Configuration", "Summary": "Set up security policies and user management in Nexus", "Confluence Link": "https://confluence.company.com/nexus-security"},
        
        # SonarQube
        {"Tool": "SonarQube", "Action": "Code Quality Analysis", "Summary": "Integrate SonarQube for automated code quality and security scanning", "Confluence Link": "https://confluence.company.com/sonar-analysis"},
        {"Tool": "SonarQube", "Action": "Quality Gates", "Summary": "Configure quality gates and rules in SonarQube projects", "Confluence Link": "https://confluence.company.com/sonar-gates"},
        
        # Atlassian Tools
        {"Tool": "Jira", "Action": "Project Setup", "Summary": "Create and configure Jira projects for agile development", "Confluence Link": "https://confluence.company.com/jira-setup"},
        {"Tool": "Confluence", "Action": "Documentation", "Summary": "Best practices for technical documentation in Confluence", "Confluence Link": "https://confluence.company.com/confluence-docs"},
        {"Tool": "Bitbucket", "Action": "Branch Permissions", "Summary": "Configure branch permissions and workflows in Bitbucket", "Confluence Link": "https://confluence.company.com/bitbucket-permissions"},
    ]
    
    df = pd.DataFrame(sample_data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to Excel
    df.to_excel('data/sample_tools_data.xlsx', index=False)
    print(f"Created sample data with {len(df)} records at data/sample_tools_data.xlsx")

if __name__ == "__main__":
    create_sample_data()