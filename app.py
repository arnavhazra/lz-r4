import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="R4 Promotion Voting",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

# Initialize session state for votes if it doesn't exist
if 'votes' not in st.session_state:
    st.session_state.votes = {candidate['name']: 0 for candidate in candidates_data}

def get_total_votes():
    return sum(st.session_state.votes.values())

def get_vote_percentage(candidate_name):
    total = get_total_votes()
    if total == 0:
        return 0
    return (st.session_state.votes.get(candidate_name, 0) / total * 100)

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
sorted_candidates = sorted(candidates_data, key=lambda c: st.session_state.votes.get(c['name'], 0), reverse=True)

# Display candidates in a responsive grid
cols = st.columns(3)
for i, candidate in enumerate(sorted_candidates):
    with cols[i % 3]:
        with st.container(border=True):
            is_leader = (i == 0 and st.session_state.votes.get(candidate['name'], 0) > 0)
            
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
                <div style="display: flex; justify-content: space-between;"><span>💪 Power:</span> <span style="font-weight: 600;">{candidate['power']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>⚔️ Kills:</span> <span style="font-weight: 600;">{candidate['kills']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>💀 Deaths:</span> <span style="font-weight: 600;">{candidate['deaths']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>❤️ Likes:</span> <span style="font-weight: 600;">{candidate['likes']}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>🎁 Gift Level:</span> <span style="font-weight: 600;">{candidate['giftLevel']}</span></div>
            </div>
            """, unsafe_allow_html=True)

            # Vote handling
            candidate_name = candidate['name']
            percentage = get_vote_percentage(candidate_name)
            
            st.progress(int(percentage))
            st.markdown(f"Votes: **{st.session_state.votes.get(candidate_name, 0)}** ({percentage:.1f}%)")

            # Vote button logic
            if 'voted_for' not in st.session_state:
                st.session_state.voted_for = {}

            has_voted = st.session_state.voted_for.get(candidate_name, False)
            button_text = "✅ Voted" if has_voted else "🗳️ Vote for R4"
            
            if st.button(button_text, key=f"vote_{candidate_name}", use_container_width=True, disabled=has_voted):
                st.session_state.votes[candidate_name] = st.session_state.votes.get(candidate_name, 0) + 1
                st.session_state.voted_for[candidate_name] = True
                st.rerun()

st.divider()

# Current Rankings
with st.container(border=True):
    st.header("📊 Current Rankings")
    
    for i, candidate in enumerate(sorted_candidates):
        candidate_name = candidate['name']
        votes = st.session_state.votes.get(candidate_name, 0)
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
                <div style="font-weight: bold;">{votes} votes</div>
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
