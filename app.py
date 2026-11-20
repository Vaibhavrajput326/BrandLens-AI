import streamlit as st
import json
from datetime import datetime

import engine

from database import (
    initialize_database,
    initialize_demo_data,
    save_review,
    get_all_reviews,
    get_review_count,
    save_brand,
    get_all_brands,
    get_brand_by_name
)


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="BrandLens AI | Brand Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Initialize database and demo workspace
initialize_database()
initialize_demo_data()

# =====================================================
# 2. PREMIUM DARK THEME CSS
# =====================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(91, 60, 180, 0.15),
            transparent 35%
        ),
        #0B1020;
    color: #F8FAFC;
}

/* Main content */
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #10182B;
    border-right: 1px solid #26334D;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

/* Headings */
h1, h2, h3 {
    color: #F8FAFC !important;
    letter-spacing: -0.5px;
}

p, label, li {
    color: #CBD5E1;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #17233B,
        #111B30
    );
    border: 1px solid #2B3A59;
    padding: 20px;
    border-radius: 16px;
}

[data-testid="stMetricLabel"] {
    color: #A5B4CC !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #151F35 !important;
    color: #F8FAFC !important;
    border: 1px solid #344563 !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        90deg,
        #7048E8,
         #9B5DE5
    );
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(
        90deg,
        #825CF0,
        #B06AF0
    );
    border: none;
    transform: translateY(-2px);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid #283653;
}

.stTabs [data-baseweb="tab"] {
    color: #AAB8D0;
}

.stTabs [aria-selected="true"] {
    color: #C4B5FD !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #121D32;
    border: 1px solid #2B3A59;
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: #293650;
}

/* Custom cards */
.custom-card {
    background: linear-gradient(
        145deg,
        #17233B,
        #111A2D
    );
    border: 1px solid #2B3A59;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
}

.hero-card {
    background: linear-gradient(
        120deg,
        #241C49,
        #17233B 70%
    );
    border: 1px solid #5945A2;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 28px;
}

.muted {
    color: #94A3B8;
    font-size: 14px;
}

.purple-text {
    color: #C4B5FD;
}

.status-pill {
    display: inline-block;
    padding: 5px 12px;
    background: #233A38;
    color: #86EFAC;
    border-radius: 20px;
    font-size: 12px;
}


/* Smart Content Improvement: make disabled result text readable */
[data-testid="stTextArea"] textarea:disabled,
[data-testid="stTextArea"] textarea[disabled],
.stTextArea textarea:disabled {
    background-color: #17243A !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    border: 1px solid #64748B !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    cursor: text !important;
}

/* Keep result labels readable */
[data-testid="stTextArea"] label {
    color: #E2E8F0 !important;
}

/* Improve contrast for text inside disabled text areas */
[data-testid="stTextArea"] textarea:disabled::placeholder {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. HELPER FUNCTIONS
# =====================================================

def read_issues(review):

    try:
        return json.loads(review[2] or "[]")
    except (TypeError, ValueError):
        return []


def get_issue_summary(reviews):

    summary = {
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Suggestion": 0
    }

    for review in reviews:

        for issue in read_issues(review):

            severity = issue.get("severity", "Low")

            if severity not in summary:
                summary[severity] = 0

            summary[severity] += 1

    return summary


# =====================================================
# 4. DATA
# =====================================================

reviews = get_all_reviews()
total_reviews = get_review_count()
brands = get_all_brands()

issue_summary = get_issue_summary(reviews)

total_issues = sum(issue_summary.values())

clean_reviews = sum(
    1 for review in reviews
    if len(read_issues(review)) == 0
)

compliance_score = (
    round((clean_reviews / total_reviews) * 100)
    if total_reviews > 0
    else 0
)


# =====================================================
# 5. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 12px 0 20px 0;">
            <h2 style="margin:0;">🔍 BrandLens</h2>
            <p style="color:#9CAAC3;margin-top:5px;">
                AI Brand Intelligence
            </p>
            <span class="status-pill">● SYSTEM ONLINE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "Content Studio",
            "Review History",
            "Brand Hub",
            "Analytics"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### Workspace Overview")

    st.caption(f"Total brands: {len(brands)}")
    st.caption(f"Total reviews: {total_reviews}")

    st.divider()

    st.markdown(
        """
        <p class="muted">
            BrandLens AI v2.0<br>
            Intelligent Brand Governance
        </p>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 6. HEADER
# =====================================================

st.markdown(
    """
    <div style="display:flex;justify-content:space-between;
                align-items:center;margin-bottom:20px;">
        <div>
            <h1 style="margin-bottom:0;">
                🔍 BrandLens AI
            </h1>
            <p style="color:#94A3B8;">
                Intelligent Brand Governance Platform
            </p>
        </div>
        <div class="status-pill">
            ● LOCAL SYSTEM ACTIVE
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 7. DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero-card">
            <h2>Welcome to your Brand Intelligence Workspace 👋</h2>
            <p style="color:#D5C9FF;">
                Analyze content, maintain brand consistency
                and make every communication count.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 Performance Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Reviews", total_reviews)
    c2.metric("Issues Detected", total_issues)
    c3.metric("Registered Brands", len(brands))
    c4.metric("Clean Reviews", f"{compliance_score}%")

    st.divider()

    left, right = st.columns([1.5, 1])

    with left:

        st.subheader("Issue Distribution")

        if total_issues > 0:

            chart_data = {
                severity: count
                for severity, count in issue_summary.items()
                if count > 0
            }

            st.bar_chart(chart_data)

        else:

            st.info("No issues detected yet.")

    with right:

        st.subheader("Workspace Status")

        st.markdown(
            f"""
            <div class="custom-card">
                <h3>Brand Profiles</h3>
                <h1 class="purple-text">{len(brands)}</h1>
                <p class="muted">Saved brand guidelines</p>
            </div>
            <div class="custom-card">
                <h3>Content Reviews</h3>
                <h1 class="purple-text">{total_reviews}</h1>
                <p class="muted">Stored in local database</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("🕘 Recent Activity")

    if reviews:

        for review in reviews[:5]:

            with st.expander(
                f"Review #{review[0]} | {review[4]}"
            ):

                st.write("**Original content:**")
                st.write(review[1])

                st.write(
                    f"**Issues:** {len(read_issues(review))}"
                )

                st.write("**Suggested correction:**")
                st.write(review[3])

    else:

        st.info(
            "No activity yet. Open Content Studio to analyze your first content."
        )


# =====================================================
# 
# =====================================================
# 8. CONTENT STUDIO — AI + ML INTEGRATION
# =====================================================

elif page == "Content Studio":

    st.subheader("✍️ Content Intelligence Studio")

    st.caption(
        "Analyze content using brand guidelines, NLP rules "
        "and machine learning."
    )

    # Brand selection
    brand_options = ["Generic Review"] + [
        brand[1] for brand in brands
    ]

    selected_brand_name = st.selectbox(
        "Select Brand Profile",
        brand_options
    )

    selected_brand = None

    if selected_brand_name != "Generic Review":

        selected_brand = get_brand_by_name(
            selected_brand_name
        )

        if selected_brand:
             
            st.info(
                f"Active Brand: {selected_brand[1]} | "
                f"Tone: {selected_brand[2]}"
            )

    st.divider()

    # Content editor
    st.markdown("### 📝 Content Editor")

    content = st.text_area(
        "Enter your marketing content",
        height=220,
        placeholder=(
            "Paste your social media post, campaign copy "
            "or marketing content here..."
        )
    )

    st.caption(f"Characters: {len(content)}")

    analyze = st.button(
        "🚀 Analyze with BrandLens AI",
        type="primary",
        use_container_width=True
    )

    if analyze:

        if not content.strip():

            st.error("Please enter some content first.")

        else:

            with st.spinner(
                "Running NLP checks and ML analysis..."
            ):

                # Run complete intelligence engine
                report = engine.analyze_content(
                    content,
                    selected_brand
                )

                issues = report["issues"]

                compliance = report["compliance"]
                
                ml_analysis = report["ml_analysis"]

                corrected_content = report[
                    "suggested_correction"
                ]

                # Save existing review format
                save_review(
                    content,
                    issues,
                    corrected_content
                )

            st.success(
                "BrandLens analysis completed successfully!"
            )

            st.divider()

            # -----------------------------------------
            # COMPLIANCE AND ML SCORE CARDS
            # -----------------------------------------

            st.subheader("📊 Intelligence Overview")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Compliance Score",
                f"{compliance['score']}/100",
                compliance["grade"]
            )

            col2.metric(
                "ML Similarity",
                (
                    f"{ml_analysis['score']}%"
                    if ml_analysis["score"] is not None
                    else "N/A"
                ),
                ml_analysis["status"]
            )

            col3.metric(
                "Total Findings",
                compliance["total_issues"]
            )

            col4.metric(
                "High Severity",
                             compliance["high_issues"]
            )

            # Compliance progress
            st.markdown("### Brand Compliance")

            st.progress(
                compliance["score"] / 100
            )

            st.caption(
                f"Rule-based compliance grade: "
                f"{compliance['grade']}"
            )

            # ML explanation
            with st.expander(
                "🧠 View Machine Learning Analysis"
            ):

                st.write(
                    "**Method:**",
                    ml_analysis["method"]
                )

                st.write(
                    "**Result:**",
                    ml_analysis["status"]
                )

                if ml_analysis["score"] is not None:

                    st.write(
                        f"**Vocabulary similarity:** "
                        f"{ml_analysis['score']}%"
                    )

                st.warning(
                    "TF-IDF similarity measures lexical overlap "
                    "with the saved brand profile. It is not a "
                    "direct measure of brand compliance or "
                    "human-level semantic understanding."
                )

            st.divider()

            # -----------------------------------------
            # ISSUE BREAKDOWN
            # -----------------------------------------
            
            st.subheader("🔍 Detailed Findings")

            severity_cols = st.columns(4)

            severity_cols[0].metric(
                "High",
                compliance["high_issues"]
            )

            severity_cols[1].metric(
                "Medium",
                compliance["medium_issues"]
            )

            severity_cols[2].metric(
                "Low",
                compliance["low_issues"]
            )

            suggestion_count = sum(
                1 for issue in issues
                if issue["severity"] == "Suggestion"
            )

            severity_cols[3].metric(
                "Suggestions",
                suggestion_count
            )

            if issues:

                for index, issue in enumerate(
                    issues,
                    start=1
                ):

                    severity = issue["severity"]

                    with st.expander(
                        f"{index}. {issue['issue']} — {severity}",
                        expanded=True
                    ):

                        st.write(
                            "**Category:**",
                            issue.get("category", "General")
                        )

                        st.write(
                            "**Severity:**",
 severity
                        )

                        st.write(
                            "**Detected Evidence:**"
                        )

                        st.code(
                            issue.get(
                                "evidence",
                                "Evidence not available"
                            )
                        )

                        st.write(
                            "**Recommended Action:**"
                        )

                        st.info(
                            issue["suggestion"]
                        )

            else:

                st.success(
                    "No issues detected by the current review rules."
                )

            st.divider()

            # -----------------------------------------
            # SMART CORRECTION
            # -----------------------------------------

            st.subheader("✨ Smart Content Improvement")

            original_col, improved_col = st.columns(2)

            with original_col:

                st.markdown("**Original Content**")

                st.text_area(
                    "Original",
                    value=content,
                    height=200,
                    disabled=True,
                    key="original_result"
                )

            with improved_col:

                st.markdown("**Suggested Content**")

                st.text_area(
                    "Improved",
                    value=corrected_content,
                    height=200,
                    disabled=True,
                    key="corrected_result"
                )

                st.download_button(
                    "⬇️ Download Improved Content",
                    data=corrected_content,
                    file_name="brandlens_improved_content.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            st.caption(
                "Review all suggested changes before publishing. "
                "Automated corrections may require human editing."
            )

# =====================================================
# 9. REVIEW HISTORY
# =====================================================

elif page == "Review History":

    st.subheader("📚 Review Center")

    st.caption(
        "Access your previously analyzed content."
    )

    if reviews:

        st.write(
            f"Total saved reviews: {len(reviews)}"
        )

        for review in reviews:

            issues = read_issues(review)

            with st.expander(
                f"Review #{review[0]} | {review[4]}"
            ):
                
                st.markdown("**Original Content**")
                st.write(review[1])

                st.markdown(
                    f"**Issues detected: {len(issues)}**"
                )

                for issue in issues:

                    st.write(
                        f"- {issue['issue']} "
                        f"({issue['severity']})"
                    )

                st.markdown("**Suggested Correction**")
                st.write(review[3])

    else:

        st.info("No reviews available yet.")


# =====================================================
# 10. BRAND HUB
# =====================================================

elif page == "Brand Hub":

    st.subheader("🏢 Brand Hub")

    st.caption(
        "Create and manage your organization's brand identities."
    )

    tab1, tab2 = st.tabs(
        ["＋ Create Brand", "▣ Manage Brands"]
    )

    with tab1:

        st.markdown("### Create New Brand Profile")

        with st.form("premium_brand_form"):

            brand_name = st.text_input(
                "Brand Name",
                placeholder="Example: TechNova"
            )

            brand_tone = st.selectbox(
                "Brand Tone",
                [
                    "Professional",
                    "Friendly",
                    "Luxury",
                    "Casual",
                    "Technical",
                    "Inspirational"
                ]
                )

            approved_input = st.text_area(
                "Approved Words",
                placeholder="Innovative, Reliable, Smart"
            )

            prohibited_input = st.text_area(
                "Prohibited Words",
                placeholder="Cheap, Bro, LOL"
            )

            brand_rules = st.text_area(
                "Additional Brand Rules",
                placeholder="Avoid exaggerated claims."
            )

            submitted = st.form_submit_button(
                "💾 Save Brand Profile",
                type="primary"
            )

            if submitted:

                if not brand_name.strip():

                    st.error(
                        "Please enter a brand name."
                    )

                else:

                    approved_words = [
                        word.strip()
                        for word in approved_input.split(",")
                        if word.strip()
                    ]

                    prohibited_words = [
                        word.strip()
                        for word in prohibited_input.split(",")
                        if word.strip()
                    ]

                    result = save_brand(
                        brand_name.strip(),
                        brand_tone,
                        approved_words,
                        prohibited_words,
                        brand_rules.strip()
                    )

                    if result:

                        st.success(
                            "Brand profile saved successfully!"
                        )

                    else:

                        st.error(
                            "Brand already exists or could not be saved."
                        )

    with tab2:

        st.markdown("### Saved Brand Profiles")

        brands = get_all_brands()

        if brands:

            for brand in brands:

                with st.expander(
                    f"🏢 {brand[1]}"
                ):

                    st.write(
                        "**Tone:**",
                        brand[2]
                    )

                    st.write(
                        "**Approved Words:**",
                        ", ".join(
                            json.loads(brand[3] or "[]")
                        )
                    )

                    st.write(
                        "**Prohibited Words:**",
                        ", ".join(
                            json.loads(brand[4] or "[]")
                        )
                    )

                    st.write(
                        "**Additional Rules:**",
                        brand[5]
                                            )

                    st.caption(
                        f"Created: {brand[6]}"
                    )

        else:

            st.info(
                "Create your first brand profile."
            )


# =====================================================
# 11. ANALYTICS
# =====================================================

elif page == "Analytics":

    st.subheader("📈 Brand Analytics")

    st.caption(
        "Understand recurring content problems."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Reviews", total_reviews)
    c2.metric("Total Findings", total_issues)
    c3.metric("Clean Review Rate", f"{compliance_score}%")

    st.divider()

    st.subheader("Severity Breakdown")

    for severity, count in issue_summary.items():

        st.write(
            f"**{severity}:** {count}"
        )

        st.progress(
            count / total_issues if total_issues else 0
        )

    st.divider()

    st.subheader("Brand Portfolio")

    brands = get_all_brands()

    if brands:

        for brand in brands:

            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>{brand[1]}</h3>
                    <p class="muted">
                        Brand tone: {brand[2]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "Add brand profiles to view your portfolio."
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:20px;">
        <p style="color:#A5B4CC;">
            🔍 BrandLens AI
        </p>
        <p style="color:#64748B;font-size:12px;">
            Intelligent Brand Governance Platform
            · Built with Python and Streamlit
        </p>
        </div>
    """,
    unsafe_allow_html=True
)
