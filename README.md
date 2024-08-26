# OOSC-Hackathon-Overlayy

## Web Scrapping 

The program utilizes Selenium WebDriver, BeautifulSoup, and Requests to automate web scraping efficiently. Selenium manages a Chrome browser to navigate websites and interact with web elements, which is especially useful for sites that load content dynamically. BeautifulSoup facilitates the parsing of HTML content from these sites, streamlining the extraction of data such as URLs and text.

The process begins by ensuring that essential tools like Chrome and ChromeDriver are installed and configured. The program collects links from the website's sitemap or, if unavailable, directly from the homepage. It then analyzes URL path segments to identify the most significant sections of the website. For each of these key sections, the program extracts text, removes any non-text elements, and saves the clean text to files. This approach ensures a targeted and efficient scraping process, effectively capturing the most relevant content from the website.

## Relevance of Link and  Question Generation

The program determines the importance of each link by counting how often its first part appears in the website's structure. For example, on a site like GitHub, if the segment "features" from the URL "github.com/features" is frequently repeated, it shows that "features" is a key area. This method helps identify which parts of the site are considered most important based on their organization.

The Python script leverages the Google Generative AI model "gemini-pro" to generate questions from content found in the five most relevant paths of a website. Once the key segments are identified, the script processes their content and utilizes AI to craft two pertinent questions for each segment. This method facilitates the automatic generation of engaging and relevant content based on the most significant areas of the website.

