import pickle
import streamlit as st
import requests
import time
from PIL import Image
from io import BytesIO
import bz2

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean white theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --background: #ffffff;
        --surface: #f8f9fa;
        --primary: #4361ee;
        --accent: #3a0ca3;
        --text: #212529;
        --text-secondary: #6c757d;
    }
    
    /* Base styling */
    .main {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Roboto', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
        color: var(--primary);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--primary);
    }
    
    .header-subtitle {
        color: var(--text-secondary);
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Selectbox styling */
    .stSelectbox > div {
        background-color: var(--background) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        padding: 0.5rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div:hover {
        border: 1px solid var(--primary) !important;
        box-shadow: 0 2px 5px rgba(67, 97, 238, 0.2) !important;
    }
    
    /* Card styling */
    .movie-card {
        background-color: var(--background);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(67, 97, 238, 0.2);
    }
    
    .movie-title {
        font-weight: 600;
        font-size: 1rem;
        margin: 0.75rem 0;
        color: var(--text);
        text-align: center;
        height: 3em;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    .movie-poster {
        border-radius: 8px;
        overflow: hidden;
        transition: all 0.5s ease;
        position: relative;
    }
    
    .movie-poster img {
        width: 100%;
        height: auto;
        transition: all 0.5s ease;
    }
    
    .movie-poster:hover img {
        transform: scale(1.03);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 1.5rem auto !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        background-color: var(--accent) !important;
        box-shadow: 0 2px 10px rgba(67, 97, 238, 0.3) !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: var(--primary) !important;
        border-top-color: transparent !important;
        width: 50px !important;
        height: 50px !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-secondary);
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fadeIn {
        animation: fadeIn 0.6s ease forwards;
    }
    
    .delay-1 { animation-delay: 0.1s; opacity: 0; }
    .delay-2 { animation-delay: 0.2s; opacity: 0; }
    .delay-3 { animation-delay: 0.3s; opacity: 0; }
    .delay-4 { animation-delay: 0.4s; opacity: 0; }
    .delay-5 { animation-delay: 0.5s; opacity: 0; }
    
    /* Recommendation section */
    .recommendations-container {
        margin-top: 2rem;
        opacity: 0;
        animation: fadeIn 0.8s ease forwards;
    }
    
    /* Media queries for responsiveness */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
        .stButton > button {
            padding: 0.5rem 1.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header section with animations
st.markdown("""
<div class="header-container fadeIn">
    <div class="header-title">🎬 Movie Recommender System</div>
    <div class="header-subtitle">Discover your next favorite movie based on your current preferences</div>
</div>
""", unsafe_allow_html=True)

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        poster_path = data.get('poster_path')

        # Return placeholder image if no poster path is found
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image"
        
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    # Log the top 5 movie similarities for debugging
    print(f"Top similarities for {movie}: {distances[:6]}") 
    
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    # Fetch posters in parallel would be ideal, but for simplicity:
    for movie_id in recommended_movie_ids:
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie_names, recommended_movie_posters

@st.cache_resource
def load_data():
    try:
        # Load movies normally
        movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
        
        # Load compressed similarity matrix from .pbz2
        with bz2.BZ2File('artifacts/similarity.pbz2', 'rb') as f:
            similarity = pickle.load(f)
        
        return movies, similarity

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None


# Main content container
with st.container():
    # Load data
    movies, similarity = load_data()
    
    if movies is not None and similarity is not None:
        # Get list of movie titles
        movie_list = movies['title'].values
        
        # Create two columns for layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Movie selection dropdown
            st.markdown('<div class="fadeIn delay-1">', unsafe_allow_html=True)
            selected_movie = st.selectbox(
                "Search or select a movie from the dropdown:",
                movie_list,
                index=0,
                key="movie"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recommendation button
            st.markdown('<div class="fadeIn delay-2">', unsafe_allow_html=True)
            recommend_button = st.button('Get Recommendations')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # When button is clicked, show recommendations
        if recommend_button:
            with st.spinner("Finding the perfect recommendations for you..."):
                # Add a slight delay for dramatic effect
                time.sleep(1.2)
                recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            
            # Display the recommendations
            st.markdown(f"""
            <div class="recommendations-container">
                <h2>Top Recommendations for "{selected_movie}"</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Create columns for movie cards
            cols = st.columns(5)
            
            # Populate columns with movie cards
            for idx, (col, name, poster) in enumerate(zip(cols, recommended_movie_names, recommended_movie_posters)):
                with col:
                    st.markdown(f"""
                    <div class="movie-card fadeIn delay-{idx+1}">
                        <div class="movie-poster">
                            <img src="{poster}" alt="{name}">
                        </div>
                        <div class="movie-title">{name}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="footer fadeIn">
            <p>Built with ❤️ using Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Failed to load movie data. Please check if the pickle files exist in the artifacts directory.")