import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="🏟️ Sports Arena Simulator",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sports-themed styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stadium-header {
        text-align: center;
        color: white;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
        padding: 20px;
        background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
        border-radius: 15px;
        margin-bottom: 30px;
    }
    
    .scoreboard {
        background: #1a1a1a;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 2em;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 3px solid #ffcc00;
        box-shadow: 0 0 20px rgba(255, 204, 0, 0.5);
    }
    
    .game-action {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-size: 1.2em;
        margin: 10px 0;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .crowd-meter {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        height: 30px;
        border-radius: 15px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.home_score = 0
    st.session_state.away_score = 0
    st.session_state.quarter = 1
    st.session_state.crowd_energy = 50
    st.session_state.game_events = []
    st.session_state.player_stats = {
        'Player A': {'points': 0, 'assists': 0, 'rebounds': 0},
        'Player B': {'points': 0, 'assists': 0, 'rebounds': 0},
        'Player C': {'points': 0, 'assists': 0, 'rebounds': 0},
    }

# Header
st.markdown('<div class="stadium-header">🏟️ ULTIMATE SPORTS ARENA SIMULATOR 🏟️</div>', unsafe_allow_html=True)

# Sidebar - Stadium Controls
with st.sidebar:
    st.header("🎮 Arena Controls")
    
    stadium_name = st.text_input("Stadium Name", "Thunder Dome")
    sport_type = st.selectbox("Sport Type", ["Basketball", "Football", "Soccer", "Hockey"])
    
    st.divider()
    
    home_team = st.text_input("Home Team", "Warriors")
    away_team = st.text_input("Away Team", "Titans")
    
    st.divider()
    
    st.subheader("🎪 Stadium Features")
    pyrotechnics = st.checkbox("Pyrotechnics 🎆", value=True)
    jumbotron = st.checkbox("Jumbotron Display 📺", value=True)
    music = st.checkbox("Victory Music 🎵", value=True)
    
    st.divider()
    
    weather = st.select_slider(
        "Weather Condition",
        options=["☀️ Sunny", "⛅ Cloudy", "🌧️ Rainy", "❄️ Snowy"]
    )

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.metric("🏠 Home Team", home_team, st.session_state.home_score)
    st.metric("📊 Quarter", st.session_state.quarter, "In Progress" if st.session_state.game_started else "Not Started")

with col2:
    st.markdown(f"""
        <div class="scoreboard">
            {home_team} {st.session_state.home_score} - {st.session_state.away_score} {away_team}
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.metric("✈️ Away Team", away_team, st.session_state.away_score)
    st.metric("🔥 Crowd Energy", f"{st.session_state.crowd_energy}%")

# Crowd Energy Meter
st.progress(st.session_state.crowd_energy / 100)

# Game Controls
st.divider()
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    if st.button("🎬 Start Game", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.game_events.append(f"⚡ Game Started! {home_team} vs {away_team}")
        st.rerun()

with col_b:
    if st.button("⚡ Simulate Play", disabled=not st.session_state.game_started, use_container_width=True):
        # Simulate a random play
        actions = [
            f"🏀 {home_team} scores 3 points!",
            f"🎯 {away_team} scores 2 points!",
            f"🔥 Amazing assist by Player A!",
            f"🛡️ Defensive block!",
            f"⭐ Steal and fast break!",
            f"🎪 Crowd goes wild!",
            f"💪 Rebound battle!"
        ]
        
        action = np.random.choice(actions)
        st.session_state.game_events.insert(0, action)
        
        # Update scores randomly
        if "3 points" in action and home_team in action:
            st.session_state.home_score += 3
        elif "2 points" in action:
            if home_team in action:
                st.session_state.home_score += 2
            else:
                st.session_state.away_score += 2
        
        # Update crowd energy
        st.session_state.crowd_energy = min(100, st.session_state.crowd_energy + np.random.randint(-5, 15))
        
        # Update player stats
        player = np.random.choice(list(st.session_state.player_stats.keys()))
        stat = np.random.choice(['points', 'assists', 'rebounds'])
        st.session_state.player_stats[player][stat] += np.random.randint(1, 4)
        
        st.rerun()

with col_c:
    if st.button("⏭️ Next Quarter", disabled=not st.session_state.game_started, use_container_width=True):
        st.session_state.quarter = min(4, st.session_state.quarter + 1)
        st.session_state.game_events.insert(0, f"🔔 Quarter {st.session_state.quarter} begins!")
        st.rerun()

with col_d:
    if st.button("🔄 Reset Game", use_container_width=True):
        st.session_state.game_started = False
        st.session_state.home_score = 0
        st.session_state.away_score = 0
        st.session_state.quarter = 1
        st.session_state.crowd_energy = 50
        st.session_state.game_events = []
        for player in st.session_state.player_stats:
            st.session_state.player_stats[player] = {'points': 0, 'assists': 0, 'rebounds': 0}
        st.rerun()

# Game Events Feed
st.divider()
st.subheader("📢 Live Game Feed")

events_col1, events_col2 = st.columns([2, 1])

with events_col1:
    if st.session_state.game_events:
        for event in st.session_state.game_events[:10]:  # Show last 10 events
            st.markdown(f'<div class="game-action">{event}</div>', unsafe_allow_html=True)
    else:
        st.info("🎮 Start the game and simulate plays to see live action!")

with events_col2:
    st.subheader("⭐ Player Stats")
    stats_df = pd.DataFrame(st.session_state.player_stats).T
    st.dataframe(stats_df, use_container_width=True)

# Visualizations
st.divider()
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("📊 Score Progression")
    # Create a simple score chart
    quarters = list(range(1, st.session_state.quarter + 1))
    home_scores = [st.session_state.home_score // st.session_state.quarter * q for q in quarters]
    away_scores = [st.session_state.away_score // st.session_state.quarter * q for q in quarters]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quarters, y=home_scores, mode='lines+markers', name=home_team, line=dict(color='#FF512F', width=3)))
    fig.add_trace(go.Scatter(x=quarters, y=away_scores, mode='lines+markers', name=away_team, line=dict(color='#3a7bd5', width=3)))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title="Quarter",
        yaxis_title="Score"
    )
    st.plotly_chart(fig, use_container_width=True)

with viz_col2:
    st.subheader("🎯 Player Performance")
    if any(sum(stats.values()) > 0 for stats in st.session_state.player_stats.values()):
        player_totals = {player: sum(stats.values()) for player, stats in st.session_state.player_stats.items()}
        fig2 = px.bar(
            x=list(player_totals.keys()),
            y=list(player_totals.values()),
            labels={'x': 'Player', 'y': 'Total Stats'},
            color=list(player_totals.values()),
            color_continuous_scale='sunset'
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Simulate plays to see player performance!")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: white; padding: 20px;'>
        🏆 Welcome to the Ultimate Sports Arena Experience! 🏆<br>
        Built with ❤️ for sports fans everywhere
    </div>
""", unsafe_allow_html=True)
