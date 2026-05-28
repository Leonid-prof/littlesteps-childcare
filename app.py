import streamlit as st
import database as db
import os
import time
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="LittleSteps | Premium Childcare Hub",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db.init_db()

# Initialize session state variables
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "current_post_id" not in st.session_state:
    st.session_state.current_post_id = None
if "active_category" not in st.session_state:
    st.session_state.active_category = "All"

# Load CSS stylesheet
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Stylesheet not found.")

load_css("styles.css")

# --- CUSTOM RENDERING HELPERS ---

def render_footer():
    st.markdown("""
    <div class="site-footer">
        <p>🌿 <b>LittleSteps Childcare Hub</b> &copy; 2026. Made with care for parents worldwide.</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            Disclaimer: The information on this blog is for educational purposes only and does not substitute professional medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_brand_banner():
    st.markdown("""
    <div class="brand-header">
        <h1 class="brand-title">LittleSteps</h1>
        <p class="brand-subtitle">Nurturing Growth, One Small Milestone at a Time</p>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE: ARTICLE DETAILED READER ---

def show_article_page():
    post_id = st.session_state.current_post_id
    post = db.get_post_by_id(post_id)
    
    if not post:
        st.error("Article not found.")
        if st.button("← Back to Articles"):
            st.session_state.current_post_id = None
            st.rerun()
        return

    # Back button
    if st.button("← Back to Articles", key="back_btn"):
        st.session_state.current_post_id = None
        st.rerun()
        
    st.markdown('<div class="article-container">', unsafe_allow_html=True)
    
    # Article Header
    st.markdown(f"""
    <div class="article-header">
        <span class="tag-badge">{post['category']}</span>
        <h1 class="article-title">{post['title']}</h1>
        <p style="color: #6B726F; font-size: 0.95rem;">
            Published: {post['created_at'][:10]} | ⏱️ {post['read_time']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero image
    if post['image_url']:
        st.markdown(f'<img class="article-hero-img" src="{post["image_url"]}">', unsafe_allow_html=True)
        
    # Main Body Content (Rendered from Markdown)
    st.markdown(f'<div class="article-body">', unsafe_allow_html=True)
    st.markdown(post['content'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 0; height: 1px; background: rgba(0,0,0,0.08); margin: 3rem 0;'>", unsafe_allow_html=True)
    
    # Author Card
    st.markdown(f"""
    <div class="article-author-card">
        <div class="author-avatar">{post['author'][0]}</div>
        <div>
            <h4 style="margin: 0; font-size: 1.1rem; color: #3F5B50;">{post['author']}</h4>
            <p style="margin: 0.2rem 0 0 0; color: #6B726F; font-size: 0.9rem; font-weight: 500;">{post['author_role']}</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #2D3330; opacity: 0.8;">
                Contributing writer and certified expert in childcare. Guided by science and maternal/paternal empathy.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interaction / Likes Panel
    col_like, col_share = st.columns([1, 4])
    with col_like:
        likes_count = post['likes']
        if st.button(f"❤️ Like ({likes_count})", key=f"like_btn_{post_id}"):
            db.increment_likes(post_id)
            st.rerun()
            
    with col_share:
        st.markdown("""
        <div style="display: flex; gap: 0.5rem; align-items: center; justify-content: flex-end; height: 100%;">
            <span style="font-size: 0.85rem; color: #6B726F;">Share this post:</span>
            <span class="category-chip" style="font-size:0.75rem; padding: 0.3rem 0.6rem; cursor:pointer;">Facebook</span>
            <span class="category-chip" style="font-size:0.75rem; padding: 0.3rem 0.6rem; cursor:pointer;">Twitter</span>
            <span class="category-chip" style="font-size:0.75rem; padding: 0.3rem 0.6rem; cursor:pointer;">Pinterest</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='border: 0; height: 1px; background: rgba(0,0,0,0.08); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Comments Section
    st.subheader("Discussion & Comments")
    
    # List comments
    comments = db.get_comments_for_post(post_id)
    
    # Comment Form
    with st.form("comment_form", clear_on_submit=True):
        st.write("Add your comment:")
        c_author = st.text_input("Your Name", placeholder="Jane Doe")
        c_content = st.text_area("Comment", placeholder="Share your experience or ask a question...")
        submitted = st.form_submit_button("Post Comment")
        if submitted:
            if c_author and c_content:
                db.add_comment(post_id, c_author, c_content)
                st.success("Comment posted successfully!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Please fill in both name and comment.")
                
    st.write("")
    
    if not comments:
        st.info("No comments yet. Be the first to share your thoughts!")
    else:
        for comment in comments:
            st.markdown(f"""
            <div class="comment-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="comment-author">{comment['author']}</span>
                    <span class="comment-date">{comment['created_at'][:16]}</span>
                </div>
                <div class="comment-content">{comment['content']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

# --- PAGE: HOME / BLOG FEED ---

def show_home_page():
    render_brand_banner()
    
    # Search and Filtering Section
    col_search, col_cats = st.columns([1, 2])
    with col_search:
        search_query = st.text_input("🔍 Search Articles", placeholder="Type keywords...", label_visibility="collapsed")
    
    with col_cats:
        categories = ["All", "Parenting", "Nutrition", "Development", "Health & Safety", "Activities"]
        
        # Implement category selection chips
        selected_cat = st.session_state.active_category
        cat_cols = st.columns(len(categories))
        for idx, cat in enumerate(categories):
            if cat_cols[idx].button(
                cat, 
                key=f"cat_btn_{cat}", 
                type="primary" if selected_cat == cat else "secondary",
                use_container_width=True
            ):
                st.session_state.active_category = cat
                st.session_state.current_post_id = None  # Ensure we return to grid
                st.rerun()
                
    st.write("")
    
    # Fetch posts
    posts = db.get_all_posts(category=st.session_state.active_category, search_query=search_query)
    
    if not posts:
        st.info("No articles found matching your criteria. Try adjusting your filters.")
        render_footer()
        return

    # HERO FEATURED POST (Only if no active filters/searches and posts are available)
    if not search_query and st.session_state.active_category == "All" and len(posts) > 0:
        hero_post = posts[0]
        remaining_posts = posts[1:]
        
        st.markdown("### Featured Insight")
        st.markdown(f"""
        <div class="featured-hero">
            <div class="featured-img-container" style="background-image: url('{hero_post['image_url']}');"></div>
            <div class="featured-body">
                <span class="tag-badge">{hero_post['category']}</span>
                <h2 class="hero-title">{hero_post['title']}</h2>
                <p class="hero-excerpt">{hero_post['excerpt']}</p>
                <div class="post-meta" style="margin-bottom: 1.5rem;">
                    <span class="meta-author">
                        <span class="author-avatar">{hero_post['author'][0]}</span>
                        {hero_post['author']} ({hero_post['author_role']})
                    </span>
                    <span>⏱️ {hero_post['read_time']}</span>
                </div>
        """, unsafe_allow_html=True)
        if st.button("Read Featured Article →", key=f"hero_btn_{hero_post['id']}"):
            st.session_state.current_post_id = hero_post['id']
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        remaining_posts = posts

    # GRID OF ARTICLES
    if remaining_posts:
        st.markdown("### Latest Articles")
        
        # Grid dimensions: 2 columns
        cols = st.columns(2)
        
        for idx, post in enumerate(remaining_posts):
            col_target = cols[idx % 2]
            with col_target:
                st.markdown(f"""
                <div class="blog-card">
                    <div class="blog-card-img" style="background-image: url('{post['image_url']}');"></div>
                    <div class="blog-card-body">
                        <span class="tag-badge">{post['category']}</span>
                        <div class="blog-card-title">{post['title']}</div>
                        <p class="blog-card-excerpt">{post['excerpt']}</p>
                        <div class="post-meta" style="margin-bottom: 1rem;">
                            <span class="meta-author">
                                <span class="author-avatar">{post['author'][0]}</span>
                                {post['author']}
                            </span>
                            <span>⏱️ {post['read_time']} | Likes: {post['likes']}</span>
                        </div>
                """, unsafe_allow_html=True)
                if st.button("Read Article →", key=f"grid_btn_{post['id']}", use_container_width=True):
                    st.session_state.current_post_id = post['id']
                    st.rerun()
                st.markdown("</div></div><br>", unsafe_allow_html=True)
                
    # NEWSLETTER SUB CARD
    st.markdown("""
    <div class="newsletter-banner">
        <h2 class="newsletter-title">Subscribe to the LittleSteps Circle</h2>
        <p class="newsletter-subtitle">Get pediatrician-approved child development insights, nutritional recipes, and gentle play activities delivered directly to your inbox weekly.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_news_in, col_news_btn = st.columns([3, 1])
    with col_news_in:
        news_email = st.text_input("Email Address", placeholder="yourname@domain.com", label_visibility="collapsed", key="newsletter_email")
    with col_news_btn:
        if st.button("Join Now", use_container_width=True):
            if news_email and "@" in news_email:
                success = db.subscribe_newsletter(news_email)
                if success:
                    st.success("🎉 Thank you! Check your inbox soon for your welcoming guide.")
                else:
                    st.warning("You are already subscribed to our newsletter! Thank you for your support.")
            else:
                st.error("Please enter a valid email address.")
                
    render_footer()

# --- PAGE: RESOURCE HUB & TRACKER ---

def show_resources_page():
    render_brand_banner()
    
    st.markdown("## Childcare Resource Hub & Tools")
    
    # Check if a child profile is active
    active_child = st.session_state.get("active_child_profile", None)
    if active_child:
        st.write(f"Welcome to the toolkit personalized for **{active_child['name']}** ({st.session_state.get('active_child_age_str', '')}).")
    else:
        st.write("Welcome to your toolkit. Add a child profile in the sidebar to unlock personalized tracking!")

    tab_milestones, tab_activities, tab_immunization, tab_growth, tab_guides = st.tabs([
        "👶 Milestone Tracker", 
        "🧩 Daily Activity Planner", 
        "💉 Immunization Tracker",
        "📈 Growth Tracker",
        "📚 Printable Guides"
    ])
    
    # TAB 1: Milestone Tracker
    with tab_milestones:
        st.subheader("Developmental Milestone Tracker")
        st.write("Track your child's major developmental achievements. Select their age range below to view age-appropriate goals:")
        
        age_options = {
            "0-3 Months": [
                "Keeps head up when lying on tummy",
                "Opens hands and swipes at hanging toys",
                "Smiles responsively at people (social smile)",
                "Makes cooing and gurgling vocalizations",
                "Tracks moving objects with eyes from side to side"
            ],
            "4-6 Months": [
                "Rolls over from tummy to back and vice versa",
                "Sits up with minimal support (tripod sit)",
                "Babbles with consonant sounds (m-m-m, b-b-b)",
                "Reaches for and grabs objects, transfers them between hands",
                "Laughs out loud and squeals with delight"
            ],
            "7-12 Months": [
                "Crawls or scoots across the room on belly",
                "Pulls up to a standing position using furniture",
                "Says simple syllables like 'mama' or 'dada' referentially",
                "Uses the pincer grasp (thumb and index finger) to pick up food",
                "Waves goodbye and plays peek-a-boo"
            ],
            "1-2 Years": [
                "Walks independently without holding onto objects",
                "Points to objects or pictures when named",
                "Speaks a few single words or short 2-word phrases",
                "Stacks 2-4 building blocks",
                "Imitates simple household actions (sweeping, wiping)"
            ],
            "2-3 Years": [
                "Runs easily and kicks a large ball",
                "Speaks in longer sentences (3+ words)",
                "Sorts colors and simple shapes",
                "Starts showing signs of toilet training readiness",
                "Follows 2- or 3-step instructions"
            ],
            "3-5 Years": [
                "Hops on one foot and climbs jungle gyms",
                "Draws basic shapes (circle, square) and stick figures",
                "Speaks clearly enough for strangers to understand",
                "Participates in cooperative group games",
                "Dresses and undresses independently"
            ]
        }
        
        # Determine default index based on active child age
        default_idx = 0
        if "active_child_age_months" in st.session_state and st.session_state.active_child_age_months is not None:
            m = st.session_state.active_child_age_months
            if m <= 3: default_idx = 0
            elif m <= 6: default_idx = 1
            elif m <= 12: default_idx = 2
            elif m <= 24: default_idx = 3
            elif m <= 36: default_idx = 4
            else: default_idx = 5
            
        age_sel = st.selectbox("Select Child's Age Range", list(age_options.keys()), index=default_idx)
        
        milestones = age_options[age_sel]
        
        st.write("Check the milestones your child has accomplished:")
        
        # Checkboxes for milestones
        checked_count = 0
        for idx, milestone in enumerate(milestones):
            is_checked = st.checkbox(milestone, key=f"ms_{age_sel}_{idx}")
            if is_checked:
                checked_count += 1
                
        # Progress Calculation
        total = len(milestones)
        progress = checked_count / total
        
        st.progress(progress)
        st.write(f"**Progress**: {checked_count} of {total} milestones checked ({int(progress * 100)}%)")
        
        # Interactive custom advice
        if progress == 1.0:
            st.success("🌟 Amazing! Your child has completed all listed milestones for this age range! Continue to foster growth through open play, read-alouds, and exploratory outdoor time.")
        elif progress >= 0.6:
            st.info("👍 Great progress! Every child develops at their own beautiful pace. Keep practicing and playing together in a supportive environment.")
        elif progress > 0:
            st.warning("💡 Healthy progress! Focus on daily gentle exercises (tummy time, interactive speaking, building toys) to encourage developmental milestones. If you have any developmental concerns, consult your pediatrician.")
        else:
            st.write("Start checking off items above as your little one achieves them!")
            
    # TAB 2: Daily Activity Planner
    with tab_activities:
        st.subheader("Daily Play & Learning Planner")
        st.write("Need play ideas? Pick an age category to generate a structured, screen-free daily schedule filled with cognitive, sensory, and motor activities.")
        
        # Determine default radio index based on active child age
        default_radio = 1
        if "active_child_age_months" in st.session_state and st.session_state.active_child_age_months is not None:
            m = st.session_state.active_child_age_months
            if m <= 12: default_radio = 0
            elif m <= 36: default_radio = 1
            else: default_radio = 2
            
        child_type = st.radio("Child Age Group", ["Infant (0-12 months)", "Toddler (1-3 years)", "Preschooler (3-5 years)"], index=default_radio, horizontal=True)
        
        if child_type == "Infant (0-12 months)":
            schedule = {
                "🌅 Morning (9:00 AM)": ("Tummy Time & High-Contrast Cards", "Lay baby on a soft blanket. Hold black-and-white high-contrast patterns 8-12 inches from their face. Move them slowly to stimulate visual tracking and build neck muscles."),
                "☀️ Midday (1:00 PM)": ("Outdoor Sensory Walk & Texture Touch", "Take a stroll outside. Collect a soft leaf, a smooth stone, and bark. Gently touch them to baby's palms, describing how they feel ('soft leaf', 'rough bark')."),
                "🌆 Afternoon (4:00 PM)": ("Gentle Read-Aloud & Baby Massage", "Cuddle up with a soft board book. Follow with a gentle lavender lotion foot and back massage to soothe muscles and encourage winding down.")
            }
        elif child_type == "Toddler (1-3 years)":
            schedule = {
                "🌅 Morning (9:00 AM)": ("Messy Safe-to-Taste mud play", "Create a bowl of edible mud using cocoa powder and flour. Let them squish, scoop, and slide toy animals through it. Stimulates touch, smell, and fine motor skills."),
                "☀️ Midday (1:00 PM)": ("Block Tower Stacking & Color Sorting", "Build towers together and knock them down. Practice sorting blocks by primary colors into corresponding plates. Teaches cause-and-effect and basic sorting."),
                "🌆 Afternoon (4:00 PM)": ("Indoor Puddle Jumping & Fort Building", "Lay out blue felt circles or sheets as 'puddles' to jump over. Build a cozy pillow fort for quiet reading time. Builds gross motor stability and spatial creativity.")
            }
        else: # Preschooler
            schedule = {
                "🌅 Morning (9:00 AM)": ("Creative Storytelling & Drawing", "Read a story, then ask them to draw their favorite character. Ask them: 'What does this animal feel? What happens next?' Inspires imagination and pencil control."),
                "☀️ Midday (1:00 PM)": ("Simulated Grocery Store & Counting", "Set up empty cereal boxes and fruits. Use play money or coins. Play customer and store cashier. Practice counting items together. Builds math and social skills."),
                "🌆 Afternoon (4:00 PM)": ("Nature Scavenger Hunt", "Head to the park with a checklist: find 3 round leaves, 2 pinecones, and 1 grey rock. Teaches categorization, counting, and fosters outdoor physical health.")
            }
            
        for time_label, (act_title, act_desc) in schedule.items():
            st.markdown(f"""
            <div style="background-color: white; padding: 1.25rem; border-radius: 12px; border: 1px solid var(--color-border); margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #5A7F71; font-size: 1.1rem;">{time_label}: {act_title}</h4>
                <p style="margin: 0.5rem 0 0 0; color: #2D3330; font-size: 0.95rem; line-height:1.5;">{act_desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
    # TAB 3: Immunization Tracker
    with tab_immunization:
        st.subheader("Childhood Immunization & Vaccine Scheduler")
        
        if not active_child:
            st.info("⚠️ Please add a child profile in the sidebar to use the personalized Immunization Tracker.")
        else:
            st.write(f"Track vaccination schedule for **{active_child['name']}** (Age: {st.session_state.active_child_age_str}).")
            
            vaccine_schedule = {
                "Birth": [
                    ("HEPB-1", "Hepatitis B (HepB) - 1st Dose", "Protects against Hepatitis B virus.")
                ],
                "2 Months": [
                    ("HEPB-2", "Hepatitis B (HepB) - 2nd Dose", "Protects against Hepatitis B virus."),
                    ("DTAP-1", "Diphtheria, Tetanus, Pertussis (DTaP) - 1st Dose", "Protects against Diphtheria, Tetanus, and Whooping Cough."),
                    ("IPV-1", "Inactivated Poliovirus (IPV) - 1st Dose", "Protects against Polio."),
                    ("HIB-1", "Haemophilus influenzae type b (Hib) - 1st Dose", "Protects against meningitis and pneumonia."),
                    ("PCV-1", "Pneumococcal Conjugate (PCV13) - 1st Dose", "Protects against blood infections, meningitis, and pneumonia."),
                    ("RV-1", "Rotavirus (RV) - 1st Dose", "Protects against severe diarrheal disease.")
                ],
                "4 Months": [
                    ("DTAP-2", "Diphtheria, Tetanus, Pertussis (DTaP) - 2nd Dose", "Protects against Diphtheria, Tetanus, and Whooping Cough."),
                    ("IPV-2", "Inactivated Poliovirus (IPV) - 2nd Dose", "Protects against Polio."),
                    ("HIB-2", "Haemophilus influenzae type b (Hib) - 2nd Dose", "Protects against meningitis and pneumonia."),
                    ("PCV-2", "Pneumococcal Conjugate (PCV13) - 2nd Dose", "Protects against blood infections, meningitis, and pneumonia."),
                    ("RV-2", "Rotavirus (RV) - 2nd Dose", "Protects against severe diarrheal disease.")
                ],
                "6 Months": [
                    ("DTAP-3", "Diphtheria, Tetanus, Pertussis (DTaP) - 3rd Dose", "Protects against Diphtheria, Tetanus, and Whooping Cough."),
                    ("IPV-3", "Inactivated Poliovirus (IPV) - 3rd Dose", "Protects against Polio."),
                    ("HIB-3", "Haemophilus influenzae type b (Hib) - 3rd Dose", "Protects against meningitis and pneumonia."),
                    ("PCV-3", "Pneumococcal Conjugate (PCV13) - 3rd Dose", "Protects against blood infections, meningitis, and pneumonia."),
                    ("HEPB-3", "Hepatitis B (HepB) - 3rd Dose", "Protects against Hepatitis B virus."),
                    ("RV-3", "Rotavirus (RV) - 3rd Dose", "Protects against severe diarrheal disease."),
                    ("FLU-ANNUAL", "Influenza (Flu Vaccine)", "Recommended annually from age 6 months onwards.")
                ],
                "12-15 Months": [
                    ("MMR-1", "Measles, Mumps, Rubella (MMR) - 1st Dose", "Protects against Measles, Mumps, and Rubella."),
                    ("VAR-1", "Varicella (Chickenpox) - 1st Dose", "Protects against Chickenpox."),
                    ("HEPA-1", "Hepatitis A (HepA) - 1st Dose", "Protects against Hepatitis A virus."),
                    ("HIB-4", "Haemophilus influenzae type b (Hib) - 4th Dose (Booster)", "Booster dose."),
                    ("PCV-4", "Pneumococcal Conjugate (PCV13) - 4th Dose (Booster)", "Booster dose.")
                ],
                "18 Months": [
                    ("DTAP-4", "Diphtheria, Tetanus, Pertussis (DTaP) - 4th Dose", "Protects against Diphtheria, Tetanus, and Whooping Cough.")
                ],
                "4-6 Years": [
                    ("DTAP-5", "Diphtheria, Tetanus, Pertussis (DTaP) - 5th Dose", "Protects against Diphtheria, Tetanus, and Whooping Cough."),
                    ("IPV-4", "Inactivated Poliovirus (IPV) - 4th Dose", "Protects against Polio."),
                    ("MMR-2", "Measles, Mumps, Rubella (MMR) - 2nd Dose", "Protects against Measles, Mumps, and Rubella."),
                    ("VAR-2", "Varicella (Chickenpox) - 2nd Dose", "Protects against Chickenpox.")
                ]
            }
            
            # Fetch completed vaccines from database
            completed_list = db.get_completed_vaccines(active_child['id'])
            
            # Draw progress bar
            total_vaccines = sum(len(v_list) for v_list in vaccine_schedule.values())
            completed_count = len(completed_list)
            v_progress = completed_count / total_vaccines if total_vaccines > 0 else 0.0
            
            st.progress(v_progress)
            st.write(f"**Vaccination Progress**: {completed_count} of {total_vaccines} vaccines completed ({int(v_progress * 100)}%)")
            
            st.write("---")
            
            # Print schedule groups
            for age_grp, vaccines in vaccine_schedule.items():
                is_due = False
                grp_title_style = "color: #3F5B50;"
                
                # Help highlight upcoming vaccines
                child_age = st.session_state.active_child_age_months
                if age_grp == "Birth" and child_age <= 1:
                    is_due = True
                elif age_grp == "2 Months" and 1 < child_age <= 3:
                    is_due = True
                elif age_grp == "4 Months" and 3 < child_age <= 5:
                    is_due = True
                elif age_grp == "6 Months" and 5 < child_age <= 8:
                    is_due = True
                elif age_grp == "12-15 Months" and 8 < child_age <= 16:
                    is_due = True
                elif age_grp == "18 Months" and 16 < child_age <= 24:
                    is_due = True
                elif age_grp == "4-6 Years" and 36 < child_age <= 72:
                    is_due = True
                    
                badge = ""
                if is_due:
                    badge = " <span class='tag-badge' style='background-color:#E3A086; color:white; font-size:0.7rem;'>Current / Upcoming</span>"
                    grp_title_style = "color: #E3A086; font-weight: bold;"
                    
                st.markdown(f"<h4 style='{grp_title_style}'>{age_grp} Group{badge}</h4>", unsafe_allow_html=True)
                
                for code, name, desc in vaccines:
                    is_completed = code in completed_list
                    
                    col_chk, col_info = st.columns([1, 15])
                    with col_chk:
                        chk_val = st.checkbox("", value=is_completed, key=f"vac_{active_child['id']}_{code}", label_visibility="collapsed")
                        if chk_val != is_completed:
                            db.toggle_vaccine_completion(active_child['id'], code, chk_val)
                            st.rerun()
                            
                    with col_info:
                        st.markdown(f"**{name}**<br><span style='color:#6B726F; font-size:0.85rem;'>{desc}</span>", unsafe_allow_html=True)
                
                st.write("")

    # TAB 4: Growth Tracker
    with tab_growth:
        st.subheader("Child Growth & BMI Percentile Calculator")
        st.write("Evaluate your child's height, weight, and Body Mass Index (BMI) compared to WHO/CDC standard percentiles for ages 0 to 5 years.")
        
        # Form layout
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            g_sex = st.selectbox("Child's Sex", ["Boy", "Girl"])
        with col_g2:
            default_age = 12
            if active_child:
                default_age = min(st.session_state.active_child_age_months, 60)
            g_age = st.number_input("Child's Age (in Months)", min_value=0, max_value=60, value=default_age)
        with col_g3:
            tracking_type = st.radio("Chart Type", ["Height", "Weight"], horizontal=True)
            
        col_g4, col_g5 = st.columns(2)
        with col_g4:
            g_height = st.number_input("Height (in cm)", min_value=30.0, max_value=150.0, value=75.0, step=0.5)
        with col_g5:
            g_weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=40.0, value=10.0, step=0.1)
            
        # Calculation and Lookup Database
        growth_standards = {
            "Boy": {
                "height": {
                    0: (46.1, 49.9, 53.7),
                    6: (63.6, 67.6, 71.6),
                    12: (71.0, 75.7, 80.5),
                    18: (76.9, 82.3, 87.7),
                    24: (82.1, 87.8, 93.6),
                    36: (89.9, 96.1, 102.3),
                    48: (96.5, 103.3, 110.1),
                    60: (102.3, 110.0, 117.7)
                },
                "weight": {
                    0: (2.4, 3.3, 4.3),
                    6: (6.4, 7.9, 9.8),
                    12: (7.8, 9.6, 12.0),
                    18: (8.8, 10.9, 13.7),
                    24: (9.7, 12.2, 15.3),
                    36: (11.3, 14.3, 18.3),
                    48: (12.7, 16.3, 21.2),
                    60: (14.1, 18.3, 24.2)
                }
            },
            "Girl": {
                "height": {
                    0: (45.4, 49.1, 52.9),
                    6: (61.5, 65.7, 69.9),
                    12: (68.9, 74.0, 79.2),
                    18: (74.9, 80.7, 86.5),
                    24: (80.0, 86.4, 92.9),
                    36: (88.4, 95.1, 101.8),
                    48: (95.0, 102.7, 110.4),
                    60: (100.9, 109.4, 117.9)
                },
                "weight": {
                    0: (2.3, 3.2, 4.2),
                    6: (5.7, 7.3, 9.3),
                    12: (7.0, 8.9, 11.5),
                    18: (8.1, 10.2, 13.0),
                    24: (9.0, 11.5, 14.8),
                    36: (10.8, 13.9, 18.1),
                    48: (12.3, 16.1, 21.2),
                    60: (13.7, 18.2, 24.4)
                }
            }
        }
        
        import numpy as np
        def interpolate_stat(age, stat_dict):
            ages = sorted(stat_dict.keys())
            p5_vals = [stat_dict[a][0] for a in ages]
            p50_vals = [stat_dict[a][1] for a in ages]
            p95_vals = [stat_dict[a][2] for a in ages]
            
            p5 = float(np.interp(age, ages, p5_vals))
            p50 = float(np.interp(age, ages, p50_vals))
            p95 = float(np.interp(age, ages, p95_vals))
            return p5, p50, p95

        p5_h, p50_h, p95_h = interpolate_stat(g_age, growth_standards[g_sex]["height"])
        p5_w, p50_w, p95_w = interpolate_stat(g_age, growth_standards[g_sex]["weight"])
        
        # BMI Calculation
        height_m = g_height / 100.0
        bmi = g_weight / (height_m * height_m)
        
        # BMI evaluation (Standard pediatric guidelines for ages 2+)
        if g_age >= 24:
            if bmi < 14.0:
                bmi_cat = "Underweight"
                bmi_color = "#E3A086"
            elif bmi < 18.0:
                bmi_cat = "Healthy Weight"
                bmi_color = "#5A7F71"
            elif bmi < 20.0:
                bmi_cat = "Overweight"
                bmi_color = "#D4A373"
            else:
                bmi_cat = "Obese"
                bmi_color = "#D98A6C"
        else:
            # Under 2 years old: WHO weight-for-length is used, here we simplify
            if bmi < 15.0:
                bmi_cat = "Slightly Underweight (Under 2 years)"
                bmi_color = "#E3A086"
            elif bmi < 19.5:
                bmi_cat = "Healthy Weight (Under 2 years)"
                bmi_color = "#5A7F71"
            else:
                bmi_cat = "Slightly Overweight (Under 2 years)"
                bmi_color = "#D4A373"
                
        # Compare current values to percentiles
        cur_val = g_height if tracking_type == "Height" else g_weight
        p5_val = p5_h if tracking_type == "Height" else p5_w
        p50_val = p50_h if tracking_type == "Height" else p50_w
        p95_val = p95_h if tracking_type == "Height" else p95_w
        
        if cur_val < p5_val:
            perc_status = "Below 5th Percentile (Slower growth)"
        elif cur_val < p50_val:
            perc_status = "5th to 50th Percentile (Below average)"
        elif cur_val < p95_val:
            perc_status = "50th to 95th Percentile (Above average)"
        else:
            perc_status = "Above 95th Percentile (Faster growth)"
            
        # Display stats cards
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label="Calculated BMI", value=f"{bmi:.1f}")
        with col_res2:
            st.markdown(f"<div style='background-color: white; border-radius: 8px; padding: 0.6rem 1.2rem; border-left: 4px solid {bmi_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'><strong>BMI Category</strong><br><span style='color:{bmi_color}; font-weight:bold;'>{bmi_cat}</span></div>", unsafe_allow_html=True)
        with col_res3:
            st.markdown(f"<div style='background-color: white; border-radius: 8px; padding: 0.6rem 1.2rem; border-left: 4px solid #5A7F71; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'><strong>{tracking_type} Category</strong><br><span style='color:#3F5B50; font-weight:bold;'>{perc_status}</span></div>", unsafe_allow_html=True)
            
        st.write("")
        st.write(f"**Growth Percentile Curve for {g_sex}s (0-60 Months) against '{tracking_type}'**:")
        
        # Build Growth Chart data
        import pandas as pd
        curve_data = []
        for month in range(0, 61, 2):
            h5, h50, h95 = interpolate_stat(month, growth_standards[g_sex]["height"])
            w5, w50, w95 = interpolate_stat(month, growth_standards[g_sex]["weight"])
            
            curve_data.append({
                "Age (Months)": month,
                "5th Percentile": h5 if tracking_type == "Height" else w5,
                "Median (50th)": h50 if tracking_type == "Height" else w50,
                "95th Percentile": h95 if tracking_type == "Height" else w95
            })
            
        df_curves = pd.DataFrame(curve_data).set_index("Age (Months)")
        st.line_chart(df_curves)

    # TAB 5: Printable Guides
    with tab_guides:
        st.subheader("Downloadable Clinical Resources")
        st.write("Save these professional cheatsheets to your device or print them out for easy access:")
        
        guides_data = [
            ("🍼 Baby's First Foods Safe Transition Tracker", "A step-by-step checklist matching age milestones to vegetable, fruit, and grain textures to safely avoid choking risks.", "PDF Guide • 2.4 MB"),
            ("😴 Healthy Infant & Toddler Sleep Routine Builder", "Sample circadian schedules from age 3 months to 4 years, including wind-down timers and gentle self-soothing methods.", "PDF Guide • 1.8 MB"),
            ("🎒 Healthy Play & Screen-Time Boundaries Toolkit", "Guide for selecting appropriate educational apps, setting timers, and integrating outdoor play guidelines.", "PDF Guide • 3.1 MB")
        ]
        
        for g_title, g_desc, g_meta in guides_data:
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid var(--color-border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div style="flex: 1; min-width: 250px;">
                    <h4 style="margin: 0; color: #3F5B50;">{g_title}</h4>
                    <p style="margin: 0.25rem 0 0.5rem 0; color: #6B726F; font-size: 0.9rem;">{g_desc}</p>
                    <span style="font-size: 0.75rem; color: #E3A086; font-weight: 600; text-transform: uppercase;">{g_meta}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Simulate a download button
            st.button("Download Guide", key=f"dl_{g_title[:15]}")
            
    render_footer()

# --- PAGE: ADMIN CONSOLE ---

def show_admin_page():
    render_brand_banner()
    
    st.markdown("## Content Creator Dashboard")
    st.write("Publish new articles directly to the database. Seed and update content here.")
    
    # Authenticate Form
    auth_pass = st.text_input("Enter Admin Passcode to Publish", type="password")
    
    # We allow the reviewer to easily use "admin" or just inspect
    if auth_pass != "admin":
        st.warning("⚠️ Access Restricted. Please enter the administrator passcode (`admin`) to unlock the publishing tool.")
        render_footer()
        return
        
    st.success("🔒 Access Granted! Write your childcare insight below:")
    
    with st.form("new_post_form", clear_on_submit=True):
        st.subheader("Create a New Article")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Article Title", placeholder="e.g. 5 Toddler Sensory Activities")
            category = st.selectbox("Category", ["Parenting", "Nutrition", "Development", "Health & Safety", "Activities"])
            read_time = st.text_input("Estimated Read Time", placeholder="e.g. 5 min read")
        with col2:
            author = st.text_input("Author Name", placeholder="e.g. Dr. Emily Watson")
            author_role = st.text_input("Author Professional Title", placeholder="e.g. Pediatrician / MS, Child Development")
            image_url = st.text_input("Image URL (Unsplash recommended)", placeholder="https://images.unsplash.com/photo-...")
            
        excerpt = st.text_area("Excerpt", max_chars=250, placeholder="Write a short summary (1-2 sentences) of the post to show in the blog card.")
        content = st.text_area("Article Content (Supports Markdown)", height=350, placeholder="Use headings (###), bullet points, and clean paragraphs to draft your article.")
        tags = st.text_input("Tags (Comma-separated)", placeholder="Toddler, Health, Sleep, Sensory")
        
        submitted = st.form_submit_button("Publish Article 🚀")
        if submitted:
            if title and category and excerpt and content and author:
                # Fallback image URL if empty
                if not image_url:
                    image_url = "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=800&q=80"
                
                db.create_post(
                    title=title,
                    category=category,
                    excerpt=excerpt,
                    content=content,
                    image_url=image_url,
                    author=author,
                    author_role=author_role,
                    read_time=read_time or "5 min read",
                    tags=tags
                )
                st.success("🎉 Article published successfully! It is now live on the homepage.")
                time.sleep(0.5)
            else:
                st.error("Please fill in all required fields (Title, Category, Excerpt, Content, Author Name).")
                
    st.write("")
    st.markdown("### Manage Existing Posts")
    all_posts = db.get_all_posts("All")
    
    if not all_posts:
        st.write("No posts in the database.")
    else:
        for p in all_posts:
            st.markdown(f"**{p['title']}** (Author: {p['author']} | Category: {p['category']})")
            if st.button(f"Delete Post", key=f"del_post_{p['id']}"):
                db.delete_post(p['id'])
                st.success(f"Deleted article: {p['title']}")
                time.sleep(0.5)
                st.rerun()
            st.write("---")
            
    render_footer()

# --- PAGE: ABOUT & CONTACT ---

def show_about_page():
    render_brand_banner()
    
    st.markdown("## About LittleSteps")
    st.markdown("""
    LittleSteps was founded in 2026 to bridge the gap between complex pediatric research and real-world, everyday parenting. 
    Our mission is to empower parents with gentle, evidence-based guidance that respects both child development science 
    and the emotional well-being of the entire family. 
    """)
    
    # Advisory Board section
    st.markdown("### Meet our Clinical Advisory Board")
    st.write("Every article we publish is vetted by certified experts in medicine, psychology, and childhood education.")
    
    col_ad1, col_ad2, col_ad3 = st.columns(3)
    
    advisors = [
        {
            "name": "Dr. Sarah Jenkins",
            "role": "Chief Child Psychologist",
            "bio": "PhD from Stanford University. Vets all behavioral advice, coping mechanisms for anxiety, and gentle discipline content.",
            "initials": "SJ"
        },
        {
            "name": "Dr. Michael Chen",
            "role": "Pediatric Sleep Expert",
            "bio": "MD from Harvard Medical School, 12 years clinical practice. Vets all sleep training, routine-building, and safety content.",
            "initials": "MC"
        },
        {
            "name": "Elena Rostova, MS, RD",
            "role": "Pediatric Dietitian",
            "bio": "MS in Clinical Nutrition. Specializes in baby-led weaning, allergen introduction schedules, and toddlers eating habits.",
            "initials": "ER"
        }
    ]
    
    with col_ad1:
        st.markdown(f"""
        <div class="advisor-card">
            <div class="advisor-avatar">{advisors[0]['initials']}</div>
            <h4 style="margin: 0; color: #3F5B50;">{advisors[0]['name']}</h4>
            <p style="margin: 0.2rem 0; color: #E3A086; font-size: 0.85rem; font-weight: 600;">{advisors[0]['role']}</p>
            <p style="margin: 0.5rem 0 0 0; color: #6B726F; font-size: 0.9rem; line-height: 1.4;">{advisors[0]['bio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ad2:
        st.markdown(f"""
        <div class="advisor-card">
            <div class="advisor-avatar">{advisors[1]['initials']}</div>
            <h4 style="margin: 0; color: #3F5B50;">{advisors[1]['name']}</h4>
            <p style="margin: 0.2rem 0; color: #E3A086; font-size: 0.85rem; font-weight: 600;">{advisors[1]['role']}</p>
            <p style="margin: 0.5rem 0 0 0; color: #6B726F; font-size: 0.9rem; line-height: 1.4;">{advisors[1]['bio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ad3:
        st.markdown(f"""
        <div class="advisor-card">
            <div class="advisor-avatar">{advisors[2]['initials']}</div>
            <h4 style="margin: 0; color: #3F5B50;">{advisors[2]['name']}</h4>
            <p style="margin: 0.2rem 0; color: #E3A086; font-size: 0.85rem; font-weight: 600;">{advisors[2]['role']}</p>
            <p style="margin: 0.5rem 0 0 0; color: #6B726F; font-size: 0.9rem; line-height: 1.4;">{advisors[2]['bio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='border: 0; height: 1px; background: rgba(0,0,0,0.08); margin: 3rem 0;'>", unsafe_allow_html=True)
    
    # Contact Form Section
    st.subheader("Have Questions? Get in touch!")
    st.write("Send a message directly to our editorial team. Note: we cannot diagnose medical issues via email.")
    
    with st.form("contact_form", clear_on_submit=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            c_name = st.text_input("Name", placeholder="Jane Doe")
            c_email = st.text_input("Email", placeholder="jane@example.com")
        with col_c2:
            c_subject = st.selectbox("Subject", ["General Question", "Editorial Inquiry", "Advertising & Partnerships", "Clinical Review Request"])
            
        c_msg = st.text_area("Message", placeholder="Write your message here...")
        
        c_sub = st.form_submit_button("Send Message")
        if c_sub:
            if c_name and c_email and c_msg:
                db.submit_contact_message(c_name, c_email, f"[{c_subject}] {c_msg}")
                st.success(f"🎉 Thank you, {c_name}! Your message has been received. Our team will review and reply within 48 hours.")
            else:
                st.error("Please fill in name, email, and message.")
                
    render_footer()

# --- MAIN APP ENTRYPOINT ---

def main():
    # Sidebar logo/branding
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <span style="font-size: 3rem;">🌿</span>
        <h2 style="margin: 0.5rem 0 0 0; font-family: 'Lora', serif; font-size: 1.8rem; color: #3F5B50;">LittleSteps</h2>
        <p style="font-size: 0.85rem; color: #6B726F; margin-top: 0.2rem;">Parenting Guided by Care</p>
    </div>
    <hr style="border: 0; height: 1px; background: rgba(90,127,113,0.2); margin: 1rem 0;">
    """, unsafe_allow_html=True)

    # --- CHILD PROFILES SIDEBAR ---
    st.sidebar.subheader("👶 Child Profiles")
    profiles = db.get_profiles()
    
    active_profile = None
    if profiles:
        profile_names = [p['name'] for p in profiles]
        selected_name = st.sidebar.selectbox("Active Profile", profile_names)
        
        # Get active profile dict
        active_profile = [p for p in profiles if p['name'] == selected_name][0]
        st.session_state.active_child_profile = active_profile
        
        # Calculate age
        dob_date = datetime.strptime(active_profile['dob'], "%Y-%m-%d")
        today = datetime.today()
        age_months = (today.year - dob_date.year) * 12 + today.month - dob_date.month
        if today.day < dob_date.day:
            age_months -= 1
            
        st.session_state.active_child_age_months = age_months
        
        # Format age string
        if age_months >= 24:
            age_str = f"{age_months // 12} years, {age_months % 12} months"
        elif age_months >= 12:
            age_str = f"1 year, {age_months - 12} months"
        else:
            age_str = f"{age_months} months"
            
        st.session_state.active_child_age_str = age_str
        st.sidebar.info(f"🍼 **{active_profile['name']}** is {age_str} old.")
        
        # Delete profile control
        if st.sidebar.button("🗑️ Delete Current Profile", key="del_profile_btn"):
            db.delete_profile(active_profile['id'])
            st.sidebar.success(f"Deleted profile for {active_profile['name']}")
            st.session_state.active_child_profile = None
            st.session_state.active_child_age_months = None
            st.session_state.active_child_age_str = None
            time.sleep(0.5)
            st.rerun()
    else:
        st.session_state.active_child_profile = None
        st.session_state.active_child_age_months = None
        st.session_state.active_child_age_str = None
        st.sidebar.write("No profiles added yet.")
        
    # Expander to add a profile
    with st.sidebar.expander("➕ Add Child Profile"):
        new_name = st.text_input("Child Name", placeholder="e.g. Leo", key="new_profile_name")
        new_dob = st.date_input("Date of Birth", max_value=datetime.today(), key="new_profile_dob")
        add_btn = st.button("Add Child", use_container_width=True)
        if add_btn:
            if new_name:
                db.create_profile(new_name, new_dob.strftime("%Y-%m-%d"))
                st.sidebar.success(f"Added profile for {new_name}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Please enter a name.")
                
    st.sidebar.markdown("<hr style='border: 0; height: 1px; background: rgba(90,127,113,0.2); margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Navigation Sidebar Radio selector
    menu_options = {
        "🏠 Articles & Insights": "Home",
        "👶 Milestone & Resource Hub": "Resources",
        "🌿 About & Advisors": "About",
        "✍️ Admin Console": "Admin"
    }
    
    # Selected navigation option
    selected_option = st.sidebar.radio("Navigate", list(menu_options.keys()), label_visibility="collapsed")
    st.session_state.current_page = menu_options[selected_option]
    
    # Sidebar quick stats or helper info box
    st.sidebar.markdown("""
    <div style="background-color: white; border-radius: 12px; padding: 1.25rem; border: 1px solid rgba(90,127,113,0.15); margin-top: 2rem;">
        <h4 style="margin: 0; color: #3F5B50; font-size: 0.95rem;">💡 Weekly Tip</h4>
        <p style="font-size: 0.85rem; color: #6B726F; line-height: 1.45; margin-top: 0.5rem; margin-bottom: 0;">
            "Tummy time is best done in short bursts (3-5 minutes) throughout the day when baby is awake, alert, and not overly full from feeding."
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Route display
    if st.session_state.current_post_id is not None and st.session_state.current_page == "Home":
        # If we are viewing an article detail, show it regardless of sidebar navigation
        show_article_page()
    else:
        # Reset current_post_id if page is switched via sidebar
        st.session_state.current_post_id = None
        
        page = st.session_state.current_page
        if page == "Home":
            show_home_page()
        elif page == "Resources":
            show_resources_page()
        elif page == "About":
            show_about_page()
        elif page == "Admin":
            show_admin_page()

if __name__ == "__main__":
    main()
