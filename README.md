# 🌿 LittleSteps Childcare Hub

LittleSteps is a premium, modern **Python Streamlit** childcare and parenting platform. It features pediatrician-approved insights, custom styling guidelines, interactive trackers, and personalization tools designed to bridge the gap between developmental science and everyday parenting.

---

## ✨ Features

- **🏠 Articles & Insights (Home Feed)**
  - Responsive search bar and interactive category filter chips.
  - Featured Article Hero highlighting the latest clinical advice.
  - Glassmorphic article cards with hover-lift animations.
  - Interactive newsletter sign-up circle.

- **📖 Immersive Article Reader**
  - Styled typography utilizing Google Fonts (*Lora* and *Inter*) for a premium reading feel.
  - Real-time post likes and persistent comments dashboard (persisted in SQLite).

- **👶 Child Profiles (Sidebar Navigation)**
  - Add/delete child profiles with date-of-birth inputs.
  - Dynamic age calculator showing age in months/years.

- **🧩 Milestone Tracker & Play Planner**
  - Personalizes recommendations automatically based on the selected child's age in months.
  - Checkable milestone timeline showing progress bars and clinical parenting advice.
  - Screens-free daily activities schedules (Infant, Toddler, Preschooler).

- **💉 Immunization Tracker**
  - Tracks pediatric vaccine completions from Birth to 6 Years.
  - Dynamic completion progress bar.
  - Color-coded highlighting flagging current due/upcoming vaccinations.

- **✍️ Content Creator Admin Console**
  - Unlocked via the passcode: `admin`.
  - Add new articles dynamically with categories, tags, images, read times, and authors.
  - Delete posts option to clean up custom additions.

---

## 🛠️ Tech Stack & Requirements

- **Backend Logic**: Python 3.8+
- **Framework**: Streamlit
- **Persistence**: SQLite (native DB file `littlesteps.db` initialized on startup)
- **Styling**: Pure CSS (`styles.css` injected through HTML/Markdown container hooks)

---

## 🚀 Running the App Locally

### 1. Setup the Environment
We recommend creating a virtual environment:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

### 2. Install Dependencies
Install all package requirements:

```bash
pip install -r requirements.txt
```

### 3. Run the App
Start the Streamlit local server:

```bash
streamlit run app.py
```

The application will launch on your browser at [http://localhost:8501](http://localhost:8501).

> [!NOTE]
> The admin passcode to publish new articles is **`admin`**.
