import pandas as pd
from pathlib import Path
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('KEY')
if not api_key or api_key == 'your_KEY_here':
    print("Warning: Invalid OpenAI API key")
    client = None
else:
    client = OpenAI(api_key=api_key)

def rephrase_with_fallback(question):
    """Attempt to rephrase, fall back to original if API unavailable"""
    if not client:
        print("OpenAI client not initialized - using original question")
        return question
    try:
        return rephrase_question(question)
    except Exception as e:
        print(f"Rephrasing failed: {e}")
        return question

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

def rephrase_question(question):
    """Rephrase a technical question into a conversational interview style"""
    try:
        prompt = f"""Convert this technical question into a natural, conversational interview style while maintaining its professional tone:
Original: {question}
Make it sound like a senior data scientist asking a candidate during an interview."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an experienced data science interviewer."},
                     {"role": "user", "content": prompt}],
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
        rephrased_question = rephrase_with_fallback(question['Question'])
        return rephrased_question, question['Answer']
    except Exception as e:
        print(f"Error getting random question: {str(e)}")
        return None, None

def evaluate_answer(question, user_answer, ideal_answer):
    """Evaluate user's answer using local model comparison"""
    try:
        # Calculate similarity between user answer and ideal answer
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([user_answer, ideal_answer])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert similarity to score (0-10) and round to integer
        score = int(round(similarity * 10))
        
        # Generate evaluation based on similarity
        if similarity >= 0.8:
            strengths = ["Good coverage of key points", "Well-structured response", "Clear explanation"]
            improvements = ["Consider adding more specific examples", "Could elaborate on some points"]
        elif similarity >= 0.5:
            strengths = ["Partial coverage of key points", "Basic understanding shown"]
            improvements = ["Missing several key points from ideal answer", "Need more detailed explanation"]
        else:
            strengths = ["Attempted to address the question"]
            improvements = ["Significant gaps in coverage", "Consider reviewing the topic"]
        
        # Format response
        response = f"""Score: {score}/10
Strengths:
{chr(10).join(['- ' + s for s in strengths])}

Improvements:
{chr(10).join(['- ' + i for i in improvements])}

Ideal Response:
{ideal_answer}"""
        
        return response
    except Exception as e:
        print(f"Error in answer evaluation: {str(e)}")
        return "Error evaluating answer. Please try again."

def get_ai_response(question):
    """Get AI response for user's question using OpenAI"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert data scientist providing detailed answers to interview questions."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Error getting response. Please try again."

def get_question_categories():
    """Get list of available question categories"""
    df = load_questions()
    if df is None:
        return ["All"]
    
    return ["All"] + sorted(df['Category'].unique().tolist())
