import streamlit as st

# Apply custom styling
st.markdown("""
<style>
    h1, h2, h3 { color: #52AB98 !important; font-weight: 700 !important; }
    .pillar-card { padding: 25px; border-radius: 12px; height: 100%; transition: transform 0.3s ease; }
    .pillar-card:hover { transform: translateY(-5px); }
</style>
""", unsafe_allow_html=True)
st.title("What If Cairo Had a 311 System?")
st.markdown("### While no open civic data exists for Cairo, NYC provides a powerful framework for what could be possible.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="pillar-card" style='background-color: rgba(82, 171, 152, 0.1); border-left: 5px solid #52AB98;'>
        <h4 style='color: #52AB98;'>NYC Has</h4>
        <ul>
            <li>Open Data Portal</li>
            <li>311 App and phone line</li>
            <li>Anonymous reporting</li>
            <li>Agency accountability metrics</li>
            <li>Real-time complaint tracking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pillar-card" style='background-color: rgba(59, 94, 100, 0.1); border-left: 5px solid #3B5E64;'>
        <h4 style='color: #3B5E64;'>Cairo Gap</h4>
        <ul>
            <li>No civic open data</li>
            <li>No unified complaint line</li>
            <li>Limited digital access</li>
            <li>No public SLA metrics</li>
            <li>No resolution tracking system</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pillar-card" style='background-color: rgba(108, 165, 164, 0.1); border-left: 5px solid #6CA5A4;'>
        <h4 style='color: #6CA5A4;'>What We Would Learn</h4>
        <ul>
            <li>Complaint hotspots by district</li>
            <li>Most under-served areas</li>
            <li>Peak problem periods</li>
            <li>Agency performance gaps</li>
            <li>Reporting channel preferences</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("### Key Takeaway")
st.markdown("""
A successful 311 system is built on three fundamental pillars: **open data infrastructure**, **civic trust**, and **channel accessibility**. 
While technology enables the reporting process, it is the transparency of open data and the accountability of tracking response times that truly empower citizens. 
For a city like Cairo to implement a similar system, the challenge lies not only in deploying a unified call center or app, but in establishing a culture of public accountability where municipal agencies actively measure, report, and improve upon their service delivery metrics in the public eye.
""")