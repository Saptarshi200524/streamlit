# mental_health_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, date, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="MindCare - AI Mental Health Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
    }
    .positive {
        color: #4CAF50;
    }
    .negative {
        color: #F44336;
    }
    .neutral {
        color: #FF9800;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    .chat-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        height: 400px;
        overflow-y: scroll;
    }
    .user-message {
        background-color: #1E88E5;
        color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: right;
        max-width: 80%;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #E3F2FD;
        color: black;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: left;
        max-width: 80%;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = pd.DataFrame(columns=['date', 'mood', 'energy', 'sleep', 'notes'])
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'resources' not in st.session_state:
    st.session_state.resources = {
        'Anxiety': ['Breathing exercises', 'Grounding techniques', 'Progressive muscle relaxation'],
        'Depression': ['Behavioral activation', 'Thought challenging', 'Gratitude journaling'],
        'Stress': ['Time management', 'Mindfulness meditation', 'Physical exercise']
    }

# Mock AI response generator
def get_ai_response(user_input, mood_data):
    # This is a simplified version - in a real app, you'd connect to an AI API
    user_input = user_input.lower()
    
    if any(word in user_input for word in ['anxious', 'anxiety', 'nervous', 'worry']):
        return "I understand you're feeling anxious. Have you tried any breathing exercises? They can help calm your nervous system. Would you like me to guide you through one?"
    elif any(word in user_input for word in ['sad', 'depressed', 'down', 'hopeless']):
        return "I'm sorry to hear you're feeling down. Remember that feelings are temporary, and it's okay to not be okay. Would talking about what's bothering you help?"
    elif any(word in user_input for word in ['stress', 'stressed', 'overwhelmed']):
        return "It sounds like you're feeling stressed. Breaking tasks into smaller steps can make them more manageable. Would you like to try a quick mindfulness exercise?"
    elif any(word in user_input for word in ['happy', 'good', 'great', 'better']):
        return "I'm glad to hear you're feeling good! It's wonderful that you're experiencing positive emotions. What do you think contributed to this mood?"
    elif any(word in user_input for word in ['sleep', 'tired', 'exhausted', 'energy']):
        return "Sleep issues can significantly impact mental health. Maintaining a consistent sleep schedule and creating a relaxing bedtime routine can help. Would you like some sleep hygiene tips?"
    else:
        return "Thank you for sharing. I'm here to support you. Would you like to talk more about what you're experiencing, or perhaps try a coping strategy?"

# App header
st.markdown('<h1 class="main-header">🧠 MindCare AI</h1>', unsafe_allow_html=True)
st.markdown("### Your Personal Mental Health Assistant")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/mental-health.png", width=80)
    st.title("MindCare Navigation")
    
    page = st.radio("Go to", ["Dashboard", "Mood Tracker", "Chat with AI", "Resources", "Progress Analytics"])
    
    st.markdown("---")
    st.markdown("### Emergency Resources")
    st.info("""
    If you're in crisis, please contact:
    - National Suicide Prevention Lifeline: 988
    - Crisis Text Line: Text HOME to 741741
    - Emergency Services: 911
    """)

# Dashboard page
if page == "Dashboard":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="sub-header">Welcome to MindCare</h2>', unsafe_allow_html=True)
        st.write("""
        Your AI-powered mental health companion. This application helps you:
        - Track your mood and emotional patterns
        - Provide AI-guided support through chat
        - Offer personalized coping strategies
        - Monitor your mental health progress over time
        """)
        
        st.markdown("---")
        st.markdown("### Today's Check-in")
        
        if st.button("Quick Mood Log"):
            with st.expander("Log Your Mood"):
                today = date.today().strftime("%Y-%m-%d")
                mood = st.select_slider("How are you feeling today?", 
                                       options=["😢", "😔", "😐", "🙂", "😄"])
                energy = st.slider("Energy Level (1-10)", 1, 10, 5)
                sleep = st.slider("Hours of sleep last night", 0.0, 12.0, 7.0, 0.5)
                notes = st.text_input("Brief notes (optional)")
                
                if st.button("Save Entry"):
                    new_entry = pd.DataFrame({
                        'date': [today],
                        'mood': [mood],
                        'energy': [energy],
                        'sleep': [sleep],
                        'notes': [notes]
                    })
                    st.session_state.mood_data = pd.concat([st.session_state.mood_data, new_entry], ignore_index=True)
                    st.success("Mood logged successfully!")
    
    with col2:
        st.markdown("### Your Mental Health Overview")
        
        if not st.session_state.mood_data.empty:
            # Calculate some basic stats
            avg_mood = st.session_state.mood_data['mood'].iloc[-1] if not st.session_state.mood_data.empty else "No data"
            avg_energy = st.session_state.mood_data['energy'].mean() if not st.session_state.mood_data.empty else "No data"
            avg_sleep = st.session_state.mood_data['sleep'].mean() if not st.session_state.mood_data.empty else "No data"
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Current Mood", avg_mood)
            with col_b:
                st.metric("Avg. Energy", f"{avg_energy:.1f}/10" if isinstance(avg_energy, float) else avg_energy)
            with col_c:
                st.metric("Avg. Sleep", f"{avg_sleep:.1f} hrs" if isinstance(avg_sleep, float) else avg_sleep)
            
            # Recent entries
            st.markdown("#### Recent Entries")
            st.dataframe(st.session_state.mood_data.tail(3), hide_index=True)
        else:
            st.info("No mood data yet. Start tracking to see your insights here!")

# Mood Tracker page
elif page == "Mood Tracker":
    st.markdown('<h2 class="sub-header">Mood & Wellness Tracking</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("mood_entry_form"):
            st.subheader("New Entry")
            entry_date = st.date_input("Date", value=date.today())
            mood = st.select_slider("Mood", options=["😢", "😔", "😐", "🙂", "😄"])
            energy = st.slider("Energy Level (1-10)", 1, 10, 5)
            sleep = st.slider("Hours of sleep", 0.0, 12.0, 7.0, 0.5)
            stress = st.slider("Stress Level (1-10)", 1, 10, 5)
            notes = st.text_area("Notes about your day")
            
            submitted = st.form_submit_button("Save Entry")
            if submitted:
                new_entry = pd.DataFrame({
                    'date': [entry_date.strftime("%Y-%m-%d")],
                    'mood': [mood],
                    'energy': [energy],
                    'sleep': [sleep],
                    'stress': [stress],
                    'notes': [notes]
                })
                st.session_state.mood_data = pd.concat([st.session_state.mood_data, new_entry], ignore_index=True)
                st.success("Mood entry saved!")
    
    with col2:
        st.subheader("Why Track Your Mood?")
        st.info("""
        Regular mood tracking can help you:
        - Identify patterns and triggers
        - Recognize early warning signs
        - Track the effectiveness of coping strategies
        - Better communicate with healthcare providers
        """)
        
        if not st.session_state.mood_data.empty:
            st.subheader("Quick Stats")
            st.metric("Days Tracked", len(st.session_state.mood_data))
            last_mood = st.session_state.mood_data['mood'].iloc[-1]
            st.metric("Latest Mood", last_mood)

# Chat with AI page
elif page == "Chat with AI":
    st.markdown('<h2 class="sub-header">Chat with MindCare AI</h2>', unsafe_allow_html=True)
    st.write("Talk about what you're experiencing. I'm here to listen and provide support.")
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Type your message here...", key="chat_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Send"):
            if user_input:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("Thinking..."):
                    ai_response = get_ai_response(user_input, st.session_state.mood_data)
                    time.sleep(1)  # Simulate processing time
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "ai", "content": ai_response})
                
                # Rerun to update chat display
                st.rerun()
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Suggested conversation starters
    st.markdown("---")
    st.markdown("**Not sure what to say? Try these:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("I'm feeling anxious today"):
            st.session_state.chat_input = "I'm feeling anxious today"
            st.rerun()
    with col2:
        if st.button("I've been feeling down"):
            st.session_state.chat_input = "I've been feeling down"
            st.rerun()
    with col3:
        if st.button("I'm having trouble sleeping"):
            st.session_state.chat_input = "I'm having trouble sleeping"
            st.rerun()

# Resources page
elif page == "Resources":
    st.markdown('<h2 class="sub-header">Mental Health Resources</h2>', unsafe_allow_html=True)
    
    # Personalized recommendations based on mood data
    if not st.session_state.mood_data.empty:
        st.subheader("Personalized Recommendations")
        
        # Simple logic to determine recommendations - in a real app, this would be more sophisticated
        last_mood = st.session_state.mood_data['mood'].iloc[-1]
        avg_stress = st.session_state.mood_data['stress'].mean() if 'stress' in st.session_state.mood_data.columns else 5
        
        if last_mood in ["😢", "😔"] or avg_stress > 7:
            st.warning("Based on your recent entries, you might find these resources particularly helpful:")
            st.info("""
            - **Cognitive Behavioral Therapy (CBT) exercises**: Challenge negative thought patterns
            - **Behavioral activation**: Schedule enjoyable activities to improve mood
            - **Mindfulness meditation**: Practice staying present without judgment
            """)
        elif last_mood in ["🙂", "😄"]:
            st.success("It's great to see you're doing well! These resources can help maintain positive mental health:")
            st.info("""
            - **Gratitude journaling**: Regularly note things you're thankful for
            - **Preventive practices**: Build resilience through regular self-care
            - **Community connection**: Engage with supportive communities
            """)
        else:
            st.info("These general resources might be helpful for you:")
            st.info("""
            - **Stress management techniques**: Breathing exercises, time management
            - **Mood tracking**: Continue monitoring patterns
            - **Self-compassion practices**: Be kind to yourself during difficult times
            """)
    
    st.markdown("---")
    
    # Resource library
    st.subheader("Resource Library")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Anxiety", "Depression", "Stress", "Mindfulness"])
    
    with tab1:
        st.markdown("### Anxiety Resources")
        st.write("""
        - **Deep Breathing Exercise**: Inhale for 4 counts, hold for 7, exhale for 8
        - **Grounding Technique**: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste
        - **Progressive Muscle Relaxation**: Tense and release each muscle group from toes to head
        """)
        
    with tab2:
        st.markdown("### Depression Resources")
        st.write("""
        - **Behavioral Activation**: Schedule pleasurable activities even when you don't feel like it
        - **Thought Records**: Identify and challenge negative automatic thoughts
        - **Gratitude Journal**: Write down three good things each day
        """)
        
    with tab3:
        st.markdown("### Stress Management")
        st.write("""
        - **Time Management**: Break tasks into smaller steps, prioritize
        - **Physical Activity**: Regular exercise reduces stress hormones
        - **Social Support**: Connect with understanding friends or family
        """)
        
    with tab4:
        st.markdown("### Mindfulness Practices")
        st.write("""
        - **Body Scan Meditation**: Focus attention on different parts of your body
        - **Mindful Breathing**: Pay attention to the sensation of breathing
        - **Loving-Kindness Meditation**: Send wishes for happiness to yourself and others
        """)

# Progress Analytics page
elif page == "Progress Analytics":
    st.markdown('<h2 class="sub-header">Your Progress Analytics</h2>', unsafe_allow_html=True)
    
    if st.session_state.mood_data.empty:
        st.info("No data yet. Start tracking your mood to see analytics here.")
    else:
        # Convert mood to numerical values for plotting
        mood_mapping = {"😢": 1, "😔": 2, "😐": 3, "🙂": 4, "😄": 5}
        plot_data = st.session_state.mood_data.copy()
        plot_data['mood_numeric'] = plot_data['mood'].map(mood_mapping)
        plot_data['date'] = pd.to_datetime(plot_data['date'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Mood trend chart
            st.subheader("Mood Trend")
            fig = px.line(plot_data, x='date', y='mood_numeric', 
                         title='Your Mood Over Time',
                         labels={'mood_numeric': 'Mood Level', 'date': 'Date'})
            fig.update_yaxis(tickvals=list(mood_mapping.values()), 
                            ticktext=list(mood_mapping.keys()))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Energy and sleep chart
            st.subheader("Energy & Sleep")
            if 'energy' in plot_data.columns and 'sleep' in plot_data.columns:
                fig = px.scatter(plot_data, x='sleep', y='energy', 
                                color='mood',
                                title='Sleep vs Energy Correlation',
                                labels={'sleep': 'Hours of Sleep', 'energy': 'Energy Level'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Additional metrics
        st.subheader("Pattern Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_mood = plot_data['mood_numeric'].mean()
            st.metric("Average Mood", f"{avg_mood:.1f}/5")
        
        with col2:
            if 'stress' in plot_data.columns:
                avg_stress = plot_data['stress'].mean()
                st.metric("Average Stress", f"{avg_stress:.1f}/10")
        
        with col3:
            if 'sleep' in plot_data.columns:
                avg_sleep = plot_data['sleep'].mean()
                st.metric("Average Sleep", f"{avg_sleep:.1f} hours")
        
        # Mood distribution
        st.subheader("Mood Distribution")
        mood_counts = plot_data['mood'].value_counts()
        fig = px.pie(values=mood_counts.values, names=mood_counts.index, 
                    title='Distribution of Your Mood States')
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>MindCare AI is designed to support your mental health journey, but it's not a replacement for professional help.</p>
    <p>If you're experiencing a mental health emergency, please contact a healthcare provider or emergency services.</p>
</div>
""", unsafe_allow_html=True)
