# veloria-tech-ml-intern-assignment
Task 1
Data Collection Using Web Scraping
1)Problem understanding:  
what does scraping means : One is writing the logic that tells the code how to scrape that website.
Scraping IS: website-specific ,structure-based ,requires inspection

2) input :
1. Where to go
requests.get("website link")
2. What to look for
links (<a> tags)
tables
divs
spans

3)output: ( of 10 companies)
* Match date
• Team 1 name and Team 2 name
• Venue (stadium name)
• Match result (which team won)
• Top scorer of the match and their score

What to do with howstat.com
STEP 1: Open the website( (https://www.howstat.com)
STEP 2: Understand what you are looking at
STEP 3: Inspect the page ( for example :"https://www.howstat.com/cricket/Statistics/Matches/MatchList.asp")


Flow of the code:
Import tools
      ↓
Open howstat
      ↓
Find match links
      ↓
Take first 10
      ↓
Open each match
      ↓
Extract details
      ↓
Store in list
      ↓
Convert to table
      ↓
Save CSV

Problem faced :I faced a 403 Forbidden error while scraping the HowStat website because the site uses Cloudflare protection, which blocks automated Python requests made using requests.get(). Initially, the scraper returned 0 match links because the website was not sending actual HTML content to the script. To identify the issue, I checked the status code (403) and printed the response HTML, which showed “Just a moment…”, confirming Cloudflare blocking. To solve this, I replaced requests with the cloudscraper library, which can bypass basic Cloudflare protection and access the real webpage HTML. After that, the scraper successfully fetched the page content and was able to proceed with extracting match data

## File Included

- `scraper.py` → Python script used to scrape cricket match data
- `match_data.csv` → Output CSV file containing scraped match information

---

## Libraries to Install

Install required libraries before running the script:

```bash
pip install pandas beautifulsoup4 cloudscraper
```

---

## How to Run the Script

Run the scraper using:
python scraper.py


Task 2:

Prediction Model for Winning of Cricket Matches

Algorithm Used:
For this assignment, I have used the Random Forest Classifier algorithm. The reason behind using Random Forest is that it has better performance on structured data, whereas Logistic Regression can't perform that well. Also, it works efficiently in case of multiple features effecting the output/result.

Features Used:
Following features were used to train the prediction model:
1. Team Strength – determined through historical wins of a particular team.
2. Home Advantage – the feature is used to find whether a team is playing at home or not.
3. Head to Head Strength – historical record of two teams in past matches.

The features used above will assist the model in learning about historical performance trends.

Model Evaluation:
Accuracy Score & F1 score were used for evaluating the prediction model performance.
- Accuracy Score: measures the accuracy percentage of correct results.
- F1 Score: evaluates both precision and recall.

Results:
Following results were obtained after running the predictive model:
- Accuracy Score: 56%
- F1 Score: 0.47

Conclusion:
It has been observed that this predictive model is successfully predicting winners in cricket matches using historical data of previous matches. Accuracy can be further increased by using features like player performance, team ranking, weather condition etc.    
## Files in Project
### `model.py`
Main machine learning script.

Functions:
- Loads and cleans cricket match data
- Performs feature engineering
- Trains the machine learning model
- Evaluates prediction performance
- Prints Accuracy Score, F1 Score, and Confusion Matrix

### `matches.csv`
Dataset containing historical cricket match information.


## Libraries Used

Install the required libraries before running the project.

Run this command:
pip install pandas scikit-learn


Required libraries:

- pandas
- scikit-learn

---

## How to Run the Project

### Step 1: Open terminal in project folder

### Step 2: Run the Python script
python model.py

Task 3:
 ## rag_search.py — Semantic Search Using Vector Embeddings (RAG)

### Brief Description

I built a semantic search system for cricket match data using vector embeddings and ChromaDB. Instead of performing simple keyword matching, the system understands the meaning of user queries and retrieves the most relevant cricket matches.

The project follows a Retrieval-Augmented Generation (RAG) approach:

1. Cricket match records are converted into natural language sentences.
2. Sentences are converted into vector embeddings using `sentence-transformers`.
3. Embeddings are stored in ChromaDB.
4. User queries are converted into embeddings.


Example query:

`"Show me matches where Mumbai won"`

The system returns the 3 most relevant match records based on semantic similarity.

---

### How to Run `rag_search.py`

#### Step 1 — Install required libraries

Run the following command:

```bash
pip install pandas sentence-transformers chromadb
```

#### Step 2 — Run the script

```bash
python rag_search.py
```

### Libraries Used

* `pandas` — for reading and processing CSV data
* `sentence-transformers` — for generating vector embeddings
* `chromadb` — for storing and retrieving embeddings


---

### Results

* Embedding Model Used: `all-MiniLM-L6-v2`
* Embedding Dimension: 384
* Retrieval Type: Semantic similarity search



### Challenges Faced

* Understanding how vector embeddings represent text meaning
* Converting tabular cricket match data into meaningful sentences
* Setting up ChromaDB correctly for vector storage
* Debugging missing columns and variable errors
* Ensuring the correct flow:
  CSV → Text Sentences → Embeddings → Vector Storage

