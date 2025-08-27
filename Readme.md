# Semantic search based gradio application run locally
##Purpose: 
Team: The application is a semantic search based chat interface  being offered by tools support team who support all the sdlc tools , this application is going to be used by users of these sdlc tools. where the users input the query, The chat interface will find the relevant semantic keywords


##End Goal: 
UI: Use Gradio to give in a chat interface
Logic layer: Simple SLM/ Transfer to do only semantic search. No Need for context as of now. 
DB layer : In memory vector DB or whichever is relevant. 
I need to be able to run the application locally preferably via docker with necessary resource constraints to be able to run in laptop <4GB ram and also share the setting up instructions.

###Preparation 1:
1.Random test data and links ~100 links to be created around Gitlab, Cloudbees, Nexus,Sonarqube,Q whisperer, Atlassian tools.

####Action Item 1: 
Write a Class/Function where Input data source An excel file shared by Tools support team, which consists of  relevant content  which consists of 4 columns, 
columnA: Tool
columnB:Action
ColumnC:Summary of page
ColumnD: Confluence Link



###Preparation 2 (Inactive): 
2. Random XML data which follow exact structure of confluence around wiki links which are created.


####Action Item 1:
Action item: Write a inactive  Class/Function where the data source is an XML file of confluence dump  which has 2 labels "relevant""most-asked" keep it in inactive stage which is going to be released as iteration2


The UI interface should be able to understand the user query and respond to the relevant all matched keywords as an output.No need for context management as a part of Beta Release.

