# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests movies similar to the user's favorite based on features like genres, keywords, cast, director, and more. This project uses natural language processing and machine learning to find similarities between movies and provide personalized suggestions.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Tech Stack](#tech-stack)
- [Dataset Used](#dataset-used)
- [Approach](#approach)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Sample Output](#sample-output)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)
- [License](#license)

---

## 📖 About the Project

The aim of this project is to help users discover movies they are likely to enjoy based on a given input movie. Unlike collaborative filtering which depends on user ratings, this system uses **content-based filtering** where recommendations are made by analyzing the features of the movies themselves.

---

## 🛠️ Tech Stack

- **Language**: Python 🐍
- **Libraries**:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `nltk`
  - `ast`
- **IDE**: VS Code / Jupyter Notebook
- **Data Source**: TMDB (The Movie Database)

---

## 🎞️ Dataset Used

Two CSV files from [Kaggle's TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata):
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

After preprocessing, columns like **genres, keywords, overview, cast, and crew** were merged and transformed into a single tag to extract meaningful similarity.

---

## 🧠 Approach

1. **Data Merging & Cleaning**:
   - Merged `movies` and `credits` datasets on `title`.
   - Extracted relevant features: `genres`, `keywords`, `cast`, `crew`, and `overview`.

2. **Feature Engineering**:
   - Extracted top 3 actors and director.
   - Combined all textual features into one string ("tags").

3. **Text Preprocessing**:
   - Converted all text to lowercase.
   - Removed spaces, punctuation.
   - Used `nltk`'s `PorterStemmer` to reduce words to their root form.

4. **Vectorization**:
   - Used `CountVectorizer` (Bag of Words model) to convert text to numerical vectors.
   - Removed stopwords and limited to top 5000 words.

5. **Similarity Calculation**:
   - Computed **cosine similarity** between movie vectors.

6. **Recommendation Function**:
   - When a user enters a movie, the function returns top 5 similar movies based on cosine similarity scores.

---

## 🧩 System Architecture

Raw Data (CSV) 
     ↓
Data Cleaning & Feature Extraction
     ↓
Text Preprocessing (NLP)
     ↓
Vectorization using CountVectorizer
     ↓
Cosine Similarity Matrix
     ↓
User Input → Movie Title
     ↓
Top 5 Similar Movies as Output

✨ Features
Input any movie title and get 5 similar movie recommendations.

Uses content features, not ratings.

Clean and understandable code with comments.

Easy to extend into a web app using Streamlit or Flask.

🚀 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
Install the required packages:

bash
Copy
Edit
pip install -r requirements.txt
If you're using Jupyter Notebook:

bash
Copy
Edit
jupyter notebook
▶️ How to Run
Run the notebook or script file:

bash
Copy
Edit
python recommend.py
OR open Movie_Recommendation_System.ipynb in Jupyter.

Call the recommendation function:

python
Copy
Edit
recommend('Avatar')
🖼️ Sample Output
bash
Copy
Edit
Recommendations for: Avatar

1. John Carter
2. Guardians of the Galaxy
3. Star Trek
4. Star Wars: The Force Awakens
5. Interstellar
🔮 Future Enhancements
Build a frontend using Streamlit or Flask.

Deploy the model using Heroku or Render.

Add collaborative filtering (user behavior-based recommendations).

Include movie posters and ratings in output.

Build a search bar with autocomplete.

