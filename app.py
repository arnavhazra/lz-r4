import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import atexit

# Page configuration
st.set_page_config(
    page_title="R4 Promotion Voting",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Database Setup ---
DB_FILE = "voting.db"

# Close the database connection when the app exits
def close_db_connection(conn):
    print("Closing database connection.")
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    atexit.register(close_db_connection, conn)
    c = conn.cursor()
    # Create votes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            candidate_name TEXT PRIMARY KEY,
            vote_count INTEGER NOT NULL DEFAULT 0
        )
    ''')
    # Create comments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    # Add candidates to votes table if they don't exist
    for candidate in candidates_data:
        c.execute("INSERT OR IGNORE INTO votes (candidate_name, vote_count) VALUES (?, 0)", (candidate['name'],))
    conn.commit()
    return conn

conn = init_db()

# --- Data Loading Functions ---
def load_votes():
    c = conn.cursor()
    c.execute("SELECT candidate_name, vote_count FROM votes")
    votes = {row[0]: row[1] for row in c.fetchall()}
    return votes

def load_comments():
    c = conn.cursor()
    c.execute("SELECT candidate_name, comment FROM comments")
    comments = {candidate['name']: [] for candidate in candidates_data}
    for row in c.fetchall():
        comments[row[0]].append(row[1])
    return comments

# --- Data Saving Functions ---
def save_vote(candidate_name):
    c = conn.cursor()
    c.execute("UPDATE votes SET vote_count = vote_count + 1 WHERE candidate_name = ?", (candidate_name,))
    conn.commit()

def save_comment(candidate_name, comment):
    c = conn.cursor()
    c.execute("INSERT INTO comments (candidate_name, comment) VALUES (?, ?)", (candidate_name, comment))
    conn.commit()

# Load initial data from the database
votes = load_votes()
comments = load_comments()

# Candidate Data
candidates_data = [
    {
        "rank": 2,
        "name": "Glizzy Gobbler",
        "power": "113,987,059",
        "level": 24,
        "country": "🇺🇸",
        "kills": "92.2M",
        "deaths": "512.3K",
        "likes": 900,
        "giftLevel": 4
    },
    {
        "rank": 4,
        "name": "SGunner",
        "power": "99,337,084",
        "level": 26,
        "country": "🇦🇷",
        "kills": "74.2M",
        "deaths": "384.0K",
        "likes": 380,
        "giftLevel": 6
    },
    {
        "rank": 11,
        "name": "Kduss",
        "power": "71,907,600",
        "level": 25,
        "country": "🇺🇳",
        "kills": "49.3M",
        "deaths": "507.9K",
        "likes": 508,
        "giftLevel": 6
    },
    {
        "rank": 12,
        "name": "GG7991",
        "power": "71,338,969",
        "level": 26,
        "country": "🇺🇸",
        "kills": "68.0M",
        "deaths": "530.7K",
        "likes": 614,
        "giftLevel": 4
    },
    {
        "rank": 13,
        "name": "MictlanTecuhtli",
        "power": "70,365,788",
        "level": 26,
        "country": "🇲🇽",
        "kills": "81.5M",
        "deaths": "717.5K",
        "likes": 686,
        "giftLevel": 6
    }
]

def get_total_votes():
    return sum(votes.values())

def get_vote_percentage(candidate_name):
    total = get_total_votes()
    if total == 0:
        return 0
    return (votes.get(candidate_name, 0) / total * 100)

# --- UI ---

st.title("🏆 R4 Promotion Voting")
st.markdown("Vote for alliance members to promote to R4 rank")

total_votes = get_total_votes()

st.markdown(f"""
<div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; padding: 1rem; text-align: center; margin-bottom: 2rem;">
    <h2 style="color: white; font-weight: 600;">
        Total Votes Cast: <span style="color: #FBBF24;">{total_votes}</span>
    </h2>
</div>
""", unsafe_allow_html=True)


# Sorting candidates based on votes
sorted_candidates = sorted(candidates_data, key=lambda c: votes.get(c['name'], 0), reverse=True)

# Display candidates in a responsive grid
cols = st.columns(3)
for i, candidate in enumerate(sorted_candidates):
    with cols[i % 3]:
        with st.container(border=True):
            is_leader = (i == 0 and votes.get(candidate['name'], 0) > 0)
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: white; background: linear-gradient(to right, #FBBF24, #F97316); border-radius: 9999px; width: 2.5rem; height: 2.5rem; display: flex; align-items: center; justify-content: center;">
                        #{candidate['rank']}
                    </div>
                    <div style="font-size: 1.5rem;">{candidate['country']}</div>
                </div>
                {'<div style="font-size: 1.5rem;">👑</div>' if is_leader else ''}
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader(f"Lv.{candidate['level']} {candidate['name']}")

            st.markdown(f"""
            <div style="font-size: 0.875rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between;"><span>💪 AvA points till date (sep 22):</span> <span style="font-weight: 600;">{candidate['power']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>⚔️ HQ Power:</span> <span style="font-weight: 600;">{candidate['kills']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>💀 Kills:</span> <span style="font-weight: 600;">{candidate['deaths']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>❤️ Likes:</span> <span style="font-weight: 600;">{candidate['likes']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>🎁 Gift Level:</span> <span style="font-weight: 600;">{candidate['giftLevel']}</span></div>
            </div>
            """, unsafe_allow_html=True)

            # Vote handling
            candidate_name = candidate['name']
            percentage = get_vote_percentage(candidate_name)
            
            st.progress(int(percentage))
            st.markdown(f"Votes: **{votes.get(candidate_name, 0)}** ({percentage:.1f}%)")

            # Vote and comment section
            if 'voted_for' not in st.session_state:
                st.session_state.voted_for = {}

            has_voted = st.session_state.voted_for.get(candidate_name, False)
            
            if not has_voted:
                comment_text = st.text_area("Add a comment (optional)", key=f"comment_{candidate_name}")
                if st.button("🗳️ Vote for R4", key=f"vote_{candidate_name}", use_container_width=True):
                    save_vote(candidate_name)
                    st.session_state.voted_for[candidate_name] = True
                    if comment_text:
                        save_comment(candidate_name, comment_text)
                    st.rerun()
            else:
                st.button("✅ Voted", key=f"vote_{candidate_name}", use_container_width=True, disabled=True)

            # Display comments
            if comments[candidate_name]:
                with st.expander("View Comments"):
                    for c in comments[candidate_name]:
                        st.info(c)

st.divider()

# Candidate Stats Comparison
st.header("⚔️ Candidate Stats Comparison")

# Data prep for radar chart
def clean_value(value):
    if isinstance(value, str):
        return float(value.replace(',', '').replace('M', 'e6').replace('K', 'e3'))
    return float(value)

stats_df = pd.DataFrame(candidates_data)
stats_to_compare = ['power', 'kills', 'deaths', 'likes', 'giftLevel']
stats_labels = ['AvA points', 'HQ Power', 'Kills', 'Likes', 'Gift Level']
for col in stats_to_compare:
    stats_df[col] = stats_df[col].apply(clean_value)

# Create tabs for different chart types
tab1, tab2, tab3 = st.tabs(["Overall Comparison (Radar)", "Stat Breakdown (Bars)", "Correlation Analysis (Scatter)"])

with tab1:
    # Create radar chart
    fig_radar = go.Figure()
    
    # Normalize data for radar chart
    normalized_stats_df = stats_df.copy()
    for col in stats_to_compare:
        normalized_stats_df[col] = (stats_df[col] - stats_df[col].min()) / (stats_df[col].max() - stats_df[col].min())
    
    for i, row in normalized_stats_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=row[stats_to_compare].values,
            theta=stats_labels,
            fill='toself',
            name=row['name']
        ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title="Candidate Stats Radar Chart"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.subheader("Individual Stat Comparisons")
    
    # Melt the DataFrame to make it suitable for faceting
    stats_melted = stats_df.melt(id_vars='name', value_vars=['power', 'kills', 'deaths'],
                                 var_name='stat', value_name='value')
    
    # Map stat names to the correct labels
    stat_label_map = {'power': 'AvA Points', 'kills': 'HQ Power', 'deaths': 'Kills'}
    stats_melted['stat'] = stats_melted['stat'].map(stat_label_map)

    fig_bar_facet = px.bar(
        stats_melted,
        x='value',
        y='name',
        color='name',
        facet_col='stat',
        orientation='h',
        labels={'value': 'Value', 'name': 'Candidate'},
        text='value'
    )
    fig_bar_facet.update_xaxes(matches=None) # Allow x-axes to have different scales
    fig_bar_facet.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig_bar_facet.update_layout(title="Comparison of Key Stats", showlegend=False)
    st.plotly_chart(fig_bar_facet, use_container_width=True)


with tab3:
    st.subheader("HQ Power vs. Kills")
    fig_scatter = px.scatter(
        stats_df,
        x='kills',
        y='deaths',
        size='power',
        color='name',
        hover_name='name',
        labels={
            'kills': 'HQ Power',
            'deaths': 'Kills',
            'power': 'AvA Points'
        },
        title="Correlation between HQ Power and Kills"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# Vote Distribution
if get_total_votes() > 0:
    st.header("📈 Vote Distribution")
    vote_data = {
        'Candidate': list(votes.keys()),
        'Votes': list(votes.values())
    }
    vote_df = pd.DataFrame(vote_data).sort_values('Votes', ascending=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Votes per Candidate")
        fig_bar = px.bar(
            vote_df,
            x='Votes',
            y='Candidate',
            orientation='h',
            text='Votes',
            color='Votes',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig_bar.update_traces(textposition='inside')
        fig_bar.update_layout(
            xaxis_title="Number of Votes",
            yaxis_title="Candidate",
            showlegend=False,
            height=400,
            uniformtext_minsize=8, 
            uniformtext_mode='hide'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Vote Percentage")
        fig_pie = px.pie(
            vote_df,
            names='Candidate',
            values='Votes',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Viridis_r
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_pie, use_container_width=True)


# Current Rankings
with st.container(border=True):
    st.header("📊 Current Rankings")
    
    for i, candidate in enumerate(sorted_candidates):
        candidate_name = candidate['name']
        vote_count = votes.get(candidate_name, 0)
        percentage = get_vote_percentage(candidate_name)
            
        medal = ""
        if i == 0: medal = "🥇"
        elif i == 1: medal = "🥈"
        elif i == 2: medal = "🥉"
        else: medal = f"{i+1}."

        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; background-color: rgba(255, 255, 255, 0.05); border-radius: 0.5rem; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.5rem;">{medal}</span>
                <div>
                    <span style="font-weight: 600;">{candidate['name']}</span>
                    <span style="font-size: 0.875rem; color: #D1D5DB;">({candidate['power']})</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: bold;">{vote_count} votes</div>
                <div style="font-size: 0.875rem; color: #D1D5DB;">{percentage:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 1.5rem; font-size: 0.875rem; color: #93C5FD;">
    <p>🏰 [HATE]DEATHROW Alliance • Alliance vs Alliance Event Rankings</p>
    <p style="margin-top: 0.5rem;">Vote responsibly - consider power, activity, and contribution to the alliance</p>
</div>
""", unsafe_allow_html=True)
