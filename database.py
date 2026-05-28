import sqlite3
import os

DB_NAME = "littlesteps.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create posts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        excerpt TEXT NOT NULL,
        content TEXT NOT NULL,
        image_url TEXT,
        author TEXT NOT NULL,
        author_role TEXT,
        read_time TEXT,
        likes INTEGER DEFAULT 0,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create comments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
    )
    """)
    
    # Create newsletter table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS newsletter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create messages table (contact form)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dob TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create completed_vaccines table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed_vaccines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        vaccine_code TEXT NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (child_id) REFERENCES profiles(id) ON DELETE CASCADE,
        UNIQUE(child_id, vaccine_code)
    )
    """)
    
    conn.commit()
    
    # Seed data if posts table is empty
    cursor.execute("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        conn.commit()
        
    conn.close()

def seed_data(cursor):
    posts_data = [
        (
            "The Art of Gentle Parenting: Coping with Toddler Tantrums",
            "Parenting",
            "Understand the neuroscience behind toddler meltdowns and discover proactive strategies to guide them through big emotions with empathy.",
            """### Understanding the Toddler Brain
When a toddler has a meltdown, it is not a calculated attempt to manipulate you. From a neurological standpoint, their prefrontal cortex—the area of the brain responsible for logic, self-regulation, and reasoning—is still under heavy construction. When they are overwhelmed by big emotions (frustration, fatigue, hunger), their amygdala takes over. This triggers a full "fight or flight" response.

### Shift from Reacting to Connecting
Gentle parenting isn't about letting your child do whatever they want. It is about maintaining firm boundaries while validating their emotional state.

1. **Acknowledge and Validate**: Instead of saying *"Stop crying, it's not a big deal,"* try saying *"You really wanted that cookie. It is hard when we can't have what we want."* This labels their emotion and helps them feel heard.
2. **Co-Regulate**: A toddler cannot calm down alone. They need to "borrow" your calm. Take deep breaths, lower your voice, and get down to their eye level.
3. **Establish Clear Boundaries**: Validation doesn't mean giving in. *"I see you are angry, but I cannot let you hit me. I am going to move over here to keep us both safe."*

### Proactive Strategies for the Future
- **Create Routine**: Toddlers thrive on predictability. Use visual schedules to help them understand what comes next.
- **Provide Controlled Choices**: Boost their autonomy by giving choices: *"Do you want to wear the blue socks or the red socks today?"*
- **Prioritize Connection**: Spending just 10-15 minutes of uninterrupted, one-on-one play time daily can significantly reduce attention-seeking behavioral challenges.

Remember, parenting is a marathon, not a sprint. Be gentle with your child, and equally gentle with yourself!""",
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=800&q=80",
            "Dr. Sarah Jenkins",
            "Child Psychologist",
            "6 min read",
            "Toddler, Behavior, Gentle Parenting, Psychology"
        ),
        (
            "Nourishing Tiny Tummies: A Beginner's Guide to Baby-Led Weaning",
            "Nutrition",
            "Transitioning your baby to solid foods? Here is everything you need to know about baby-led weaning, including safe first foods and nutrient needs.",
            """### What is Baby-Led Weaning (BLW)?
Baby-Led Weaning is an approach to introducing solid foods where babies skip purees and spoon-feeding entirely, moving straight to self-feeding finger foods from about six months of age. It encourages autonomy, develops fine motor skills (like the pincer grasp), and allows babies to explore textures and flavors at their own pace.

### Signs of Readiness
Before starting BLW, make sure your baby meets the following developmental milestones (typically around 6 months):
- Can sit up independently with little to no support.
- Has good head and neck control.
- Reaches for food and brings it to their mouth.
- Has lost the tongue-thrust reflex (which pushes food out of the mouth).

### Safe First Foods
When preparing foods for BLW, a general rule of thumb is to cut food into pieces the size and shape of an adult pinky finger. This makes it easy for the baby to hold and chew from the top. The food should be soft enough to mash between your thumb and forefinger.

*   **Avocado**: Cut into long wedges. You can leave some skin at the bottom or coat it in crushed oats to make it less slippery.
*   **Steamed Broccoli**: Large florets make perfect handles for tiny hands.
*   **Sweet Potato**: Roasted or steamed wedges.
*   **Soft Fruits**: Ripe banana halves, soft pear, or strawberries.
*   **Meat**: Slow-cooked, tender strips of beef or chicken that they can suck on.

### Choking vs. Gagging: The Crucial Difference
It is completely natural to feel anxious about choking. However, understanding the gag reflex is reassuring.
- **Gagging**: A normal safety mechanism. The baby may cough, sputter, turn slightly red, and make gagging sounds. This means their body is pushing food forward. Keep calm, watch, and let them work through it.
- **Choking**: A quiet and life-threatening emergency. The airway is blocked. The baby will be silent, unable to cough or make sound, and may turn blue. *Ensure you take an infant CPR and first-aid course before starting solids.*

### Key Nutrients to Focus On
By 6 months, a baby’s iron stores naturally begin to deplete. Prioritize iron-rich foods like cooked lentils, eggs, fortified cereals, and ground meats. Pair them with Vitamin C sources (like bell peppers or citrus) to enhance absorption!""",
            "https://images.unsplash.com/photo-1596464716127-f2a82984de30?auto=format&fit=crop&w=800&q=80",
            "Elena Rostova, MS, RD",
            "Pediatric Dietitian",
            "8 min read",
            "Baby Food, Weaning, Nutrition, Milestones"
        ),
        (
            "Setting the Stage for Sweet Dreams: Tear-Free Sleep Routines",
            "Health & Safety",
            "Sleep is crucial for developmental growth. Explore our evidence-based, tear-free nighttime routines that promote long, restorative sleep.",
            """### The Importance of Child Sleep
During sleep, a child's brain processes the day's experiences, consolidates memory, and releases growth hormones. A well-rested child is more emotionally resilient, has a stronger immune system, and learns more effectively. Conversely, chronic sleep deprivation can lead to mood swings, behavioral problems, and difficulty concentrating.

### Designing the Perfect Sleep Sanctuary
To set your child up for sleep success, their environment needs to signal to their circadian rhythm that it's time to rest:
- **Temperature**: Keep the room cool, ideally between 18°C and 20°C (65°F to 68°F).
- **Light**: Use blackout curtains to block out early morning sun or street lights.
- **Sound**: A white noise machine can drown out disruptive household or street sounds. Use a consistent, low, static sound.
- **Screens**: Keep all screens (tablets, TVs, phones) out of the bedroom. Avoid screen time for at least 1 hour before bed, as blue light inhibits melatonin production.

### The 4-Step Bedtime Routine
Consistency is key. Performing the exact same sequence of events every night programs your child's body to wind down.

1. **Warm Bath**: The warm water relaxes muscles. When they step out of the bath, their body temperature drops slightly, mimicking the natural drop in temperature that happens before sleep, inducing sleepiness.
2. **Pajamas & Massage**: Dress them in comfortable, breathable organic cotton pajamas. A gentle lavender lotion massage can be deeply soothing.
3. **Dim-Light Reading**: Read 2-3 books in a dimly lit room. Keep your voice quiet, slow, and melodic.
4. **Cuddle & Lullaby**: Spend 5 minutes in a quiet cuddle, singing a consistent song or talking about their favorite part of the day. Place them in their crib or bed while they are *drowsy but awake* to help them learn to fall asleep independently.

### Handling Night Wakings
When your child wakes up at night, respond calmly and boringly. Keep lights off or very dim. Speak in soft whispers. Avoid turning it into play time. Reassure them with a hand on their chest: *"You are safe. It is time for sleep. I love you."* then gradually exit the room. Consistent boundaries build trust and security.""",
            "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80",
            "Dr. Michael Chen",
            "Pediatrician",
            "5 min read",
            "Sleep, Health, Infant Care, Routines"
        ),
        (
            "Sensory Play: Why Mess and Mud are Essential for Brain Development",
            "Development",
            "Sensory play is not just about making a mess—it builds neural connections in the brain's pathways. Learn simple, low-cost activities.",
            """### What is Sensory Play?
Sensory play includes any activity that stimulates a child's senses: touch, smell, taste, sight, and hearing, as well as balance (vestibular) and body awareness (proprioception). When kids engage multiple senses simultaneously, they are actively building cognitive networks.

### The Developmental Benefits
- **Neural Connections**: Sensation signals the brain to strengthen pathways that are crucial for complex learning tasks later in life.
- **Language Skills**: Describing textures, temperatures, and actions (e.g., *"slippery," "cold," "squishy," "pouring"*) expands their vocabulary.
- **Fine and Gross Motor Skills**: Pouring, scooping, pinching, squeezing, and balancing build muscle strength and hand-eye coordination.
- **Emotional Regulation**: Squishing clay or playing with water has an incredibly grounding, therapeutic, and calming effect on overstimulated children.

### 3 Easy, Mess-Friendly Activities to Try at Home

#### 1. The Classic Sensory Bin
*   **What you need**: A large plastic tub, a dry base (uncooked rice, dried beans, or oats), scoopers, measuring cups, and small toys (like plastic dinosaurs or trucks).
*   **How it works**: Let them scoop, pour, bury, and excavate. It teaches spatial awareness and basic math concepts (volume, weight).

#### 2. Safe-to-Taste Mud Play
*   **What you need**: Ground cocoa powder, flour, water, and toy plastic farm animals.
*   **How it works**: Mix the ingredients to create a realistic, chocolate-scented "mud." Children can make the animals walk through the mud, wash them in a tub of warm soapy water next to it, and experience rich textures without parents worrying about ingestion.

#### 3. Rainbow Bubble Foam
*   **What you need**: 2 tbsp dish soap or baby body wash, 1/2 cup water, food coloring, and a hand mixer.
*   **How it works**: Whisk on high speed until stiff peaks form. Scoop the colorful foam into a bath or sensory table. The fluffy, airy texture is delightful to squeeze and stack.

### Embracing the Mess
It can be hard to watch your living room turn into a sensory lab. To manage the clean-up:
- Lay down a large plastic shower curtain or tablecloth on the floor before play.
- Take sensory play outdoors! Grass, mud, and water are the ultimate sensory tools.
- Involve your child in the cleanup process, teaching them responsibility as part of the fun.""",
            "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=800&q=80",
            "Clara Vance",
            "Early Childhood Educator",
            "4 min read",
            "Sensory Play, Development, Activities, Motor Skills"
        )
    ]
    cursor.executemany("""
    INSERT INTO posts (title, category, excerpt, content, image_url, author, author_role, read_time, tags)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, posts_data)

# --- POST OPERATIONS ---

def get_all_posts(category=None, search_query=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM posts"
    params = []
    
    conditions = []
    if category and category != "All":
        conditions.append("category = ?")
        params.append(category)
        
    if search_query:
        conditions.append("(title LIKE ? OR excerpt LIKE ? OR content LIKE ? OR tags LIKE ?)")
        search_wild = f"%{search_query}%"
        params.extend([search_wild, search_wild, search_wild, search_wild])
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post

def create_post(title, category, excerpt, content, image_url, author, author_role, read_time, tags):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO posts (title, category, excerpt, content, image_url, author, author_role, read_time, tags)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, category, excerpt, content, image_url, author, author_role, read_time, tags))
    conn.commit()
    conn.close()

def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

def increment_likes(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

# --- COMMENT OPERATIONS ---

def add_comment(post_id, author, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO comments (post_id, author, content)
    VALUES (?, ?, ?)
    """, (post_id, author, content))
    conn.commit()
    conn.close()

def get_comments_for_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC", (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

# --- NEWSLETTER OPERATIONS ---

def subscribe_newsletter(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO newsletter (email) VALUES (?)", (email,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # Already subscribed
        success = False
    conn.close()
    return success

# --- CONTACT MESSAGES ---

def submit_contact_message(name, email, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO messages (name, email, message)
    VALUES (?, ?, ?)
    """, (name, email, message))
    conn.commit()
    conn.close()

# --- PROFILE OPERATIONS ---

def create_profile(name, dob):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (name, dob) VALUES (?, ?)", (name, dob))
    conn.commit()
    conn.close()

def get_profiles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles ORDER BY created_at DESC")
    profiles = cursor.fetchall()
    conn.close()
    return profiles

def delete_profile(profile_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    conn.commit()
    conn.close()

# --- VACCINE OPERATIONS ---

def get_completed_vaccines(child_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT vaccine_code FROM completed_vaccines WHERE child_id = ?", (child_id,))
    vaccines = [row['vaccine_code'] for row in cursor.fetchall()]
    conn.close()
    return vaccines

def toggle_vaccine_completion(child_id, vaccine_code, completed):
    conn = get_db_connection()
    cursor = conn.cursor()
    if completed:
        try:
            cursor.execute("INSERT OR IGNORE INTO completed_vaccines (child_id, vaccine_code) VALUES (?, ?)", (child_id, vaccine_code))
            conn.commit()
        except sqlite3.Error:
            pass
    else:
        cursor.execute("DELETE FROM completed_vaccines WHERE child_id = ? AND vaccine_code = ?", (child_id, vaccine_code))
        conn.commit()
    conn.close()
