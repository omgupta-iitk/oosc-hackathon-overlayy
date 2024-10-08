# OOSC-Hackathon-Overlayy

## Web Scrapping 

The program utilizes Selenium WebDriver, BeautifulSoup, and Requests to automate web scraping efficiently. Selenium manages a Chrome browser to navigate websites and interact with web elements, which is especially useful for sites that load content dynamically. BeautifulSoup facilitates the parsing of HTML content from these sites, streamlining the extraction of data such as URLs and text.

The process begins by ensuring that essential tools like Chrome and ChromeDriver are installed and configured. The program collects links from the website's sitemap or, if unavailable, directly from the homepage. It then analyzes URL path segments to identify the most significant sections of the website. For each of these key sections, the program extracts text, removes any non-text elements, and saves the clean text to files. This approach ensures a targeted and efficient scraping process, effectively capturing the most relevant content from the website.

The webscrapping is done by `scrape_new.py` 

## Relevance of Link and  Question Generation

The program determines the importance of each link by counting how often its first part appears in the website's structure. For example, on a site like GitHub, if the segment "features" from the URL "github.com/features" is frequently repeated, it shows that "features" is a key area. This method helps identify which parts of the site are considered most important based on their organization.

The relevance is also calculated by the `scrape.py` 

The Python script leverages the Google Generative AI model "gemini-pro" to generate questions from content found in the five most relevant paths of a website. Once the key segments are identified, the script processes their content and utilizes AI to craft two pertinent questions for each segment. This method facilitates the automatic generation of engaging and relevant content based on the most significant areas of the website.

The questions are generated by `final_llm.py`


## Usage : 

To generate relevant questions from a website's content , run the `final_pipe.py` and the provide the url of the site along with `http://` .
We will get the final json in `output.json` .

### Our code at work : 
  ![Untitled](https://github.com/user-attachments/assets/ed5b61f6-d345-4caf-9741-fa9544ddd057)
![Untitled](https://github.com/user-attachments/assets/70a8d411-489e-4e7b-9b9e-56d41a52c96b)


[Screencast from 2024-08-26 13-29-57.webm](https://github.com/user-attachments/assets/c3af4b4d-c330-4939-8f19-6bfbc191b201)

**Note : Our code works for Linux OS**
