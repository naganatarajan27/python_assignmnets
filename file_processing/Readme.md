## Project 1 - filereader.py
### Read a pdf file from a folder. Refer to the PDF file Chemistry Questions.pdf
### Requirements
1. Store a PDF file in a folder called “/content”
2. Read PDF file from the folder
3. Write the content to a text file called “output.txt”
4. Store this file under the “/content” folder
### Error Handling
1. Take care of case where folder is not available
2. Take care of case where PDF file is not present in the content folder
3. Take care of case where the output.txt file is not available

## Project 2 - traversefolder.py
### Traverse through folder tree and filter pdf files
### Requirements
1. Add sub-folders called “One”, “Two”, “Three” under the folder called “/content”
2. Add PDF files under each of the sub-folders
3. Load all PDF files under the sub-folders and load the PDF content
4. Write the content to a text file called “output.txt” under each sub-folder respectively
### Error Handling
1. Take care of case where folder is not available
2. Take care of case where PDF file is not present in a sub-folder
3. Take care of case where the output.txt file is not available in a sub-folder

## Project 3 - filereaderperpage.py
## Read content from a particular page
### Requirements
1. Update project 1 and update the reading of content 
2. Take a page number as an input from command prompt
3. Read content of the page number provided and write to the output file
### Error Handling
1. Take care of case where folder is not available
2. Take care of case where PDF file is not present in a sub-folder
3. Take care of case where the output.txt file is not available in a sub-folder

## Project 4 - regexUsage.py
## Read regular expression from a config file and extract content
### Requirements
1. Update project 3
2. Add support for a configuration file 
3. In the configuration file set a config with key “regex” and value some regular expression that will match a part of the content in the PDF
4. Update code to extract only the content matching the regular expression 
5. Write to the output file
### Error Handling
1. Take care of case where folder is not available
2. Take care of case where PDF file is not present in a sub-folder
3. Take care of case where the output.txt file is not available in a sub-folder
4. Take care of case where no configuration file is available
5. Take care of the case where configuration file does not have the regular expression
