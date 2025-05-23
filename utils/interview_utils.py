import os
import pandas as pd
from pathlib import Path
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv('KEY'))

def rephrase_question(question):
    """Rephrase a technical question into a conversational interview style"""
    try:
        prompt = f"""Convert this technical question into a natural, conversational interview style while maintaining its professional tone:
Original: {question}
Make it sound like a senior data scientist asking a candidate during an interview."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error rephrasing question: {str(e)}")
        return question

def get_random_question(category="All"):
    """Get a random question from the dataset and rephrase it"""
    try:
        current_dir = Path(__file__).parent.parent
        data_path = current_dir / 'interview_qa_combined.csv'

        if not data_path.exists():
            return None, None

        df = pd.read_csv(data_path)
        if df.empty:
            return None, None

        if category != "All":
            df = df[df['Category'] == category]

        if df.empty:
            return None, None

        question = df.sample(n=1).iloc[0]
        rephrased_question = rephrase_question(question['Question'])
        return rephrased_question, question['Answer']
    except Exception as e:
        print(f"Error getting random question: {str(e)}")
        return None, None

def evaluate_answer(question, user_answer, ideal_answer):
    """Evaluate user's answer using TF-IDF and cosine similarity"""
    try:
        # Calculate similarity between user answer and ideal answer
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([user_answer, ideal_answer])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        # Convert similarity to score (0-10) and round to integer
        score = int(round(similarity * 10))
        
        # Extract key points from answers using simple text analysis
        user_keywords = set(word.lower() for word in user_answer.split())
        ideal_keywords = set(word.lower() for word in ideal_answer.split())
        
        # Find matching and missing keywords
        matches = user_keywords.intersection(ideal_keywords)
        missing = ideal_keywords - user_keywords
        
        # Generate feedback
        feedback = "Key Points Covered:\n"
        feedback += "\n".join(f"✓ '{word}'" for word in list(matches)[:3])
        feedback += "\n\nMissing Key Points:\n"
        feedback += "\n".join(f"• '{word}'" for word in list(missing)[:3])

        return f"Score: {score}/10\n\n{feedback}\n\nIdeal Response:\n{ideal_answer}"
    except Exception as e:
        print(f"Error in answer evaluation: {str(e)}")
        return "Error evaluating answer. Please try again."

def get_ai_response(question):
    """Get AI response for user's question using Replit AI"""
    try:
        prompt = f"""As an expert data scientist, provide a detailed answer to this interview question: {question}"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Error getting response. Please try again."

def get_question_categories():
    """Get list of available question categories"""
    df = load_questions()
    if df is None:
        return ["All"]
    return ["All"] + sorted(df['Category'].unique().tolist())

def load_questions():
    """Load interview questions from CSV file"""
    try:
        current_dir = Path(__file__).parent.parent
        data_path = current_dir / 'interview_qa_combined.csv'

        if not data_path.exists():
            st.error(f"Data file not found at {data_path}")
            return None

        df = pd.read_csv(data_path)
        if df.empty:
            st.error("The dataset is empty")
            return None

        return df
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return None