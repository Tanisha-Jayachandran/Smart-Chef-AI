import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="SmartChef AI | Zero-Waste & Health Engine",
    page_icon="🥑",
    layout="wide"
)

# 2. Custom CSS Styling (Elevated Aesthetics)
st.markdown("""
    <style>
    /* App Canvas */
    .stApp {
        background-color: #f4f8f6;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0d5c46 0%, #11998e 50%, #38ef7d 100%);
        padding: 32px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(17, 153, 142, 0.2);
    }
    .hero-banner h1 {
        color: #ffffff !important;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .hero-banner p {
        font-size: 1.15rem;
        opacity: 0.92;
        margin: 0;
    }

    /* Modern Impact Cards */
    .metric-card {
        background: #ffffff;
        padding: 20px 15px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #e1ece6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-card h3 {
        margin: 0;
        color: #0d5c46;
        font-size: 1.4rem;
        font-weight: 700;
    }
    .metric-card p {
        margin: 4px 0 0 0;
        color: #617d72;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Primary Action Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0d5c46 0%, #11998e 100%);
        color: white !important;
        font-size: 1.25rem;
        font-weight: 700;
        border-radius: 14px;
        padding: 14px 28px;
        border: none;
        box-shadow: 0 6px 18px rgba(13, 92, 70, 0.25);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(13, 92, 70, 0.35);
    }

    /* Section Styling */
    h3 {
        color: #0d5c46 !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Secure API Key Management
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")

if not api_key:
    st.error("🔒 Backend Authorization Required. Please configure Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# 4. Header Banner
st.markdown("""
    <div class="hero-banner">
        <h1>🥑 SmartChef AI</h1>
        <p>Precision Culinary Intelligence • SDG 3 Good Health & SDG 12 Responsible Consumption</p>
    </div>
""", unsafe_allow_html=True)

# 5. Impact Metrics Header
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""<div class="metric-card"><h3>🌐 SDG 3 & 12</h3><p>Target Framework Alignment</p></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><h3>⚖️ ~400g / Meal</h3><p>Benchmark Landfill Diversion</p></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><h3>🍃 ~1.2 kg CO₂e</h3><p>Average Footprint Reduction</p></div>""", unsafe_allow_html=True)

st.write("")
st.write("")

# 6. Main Interface Layout
col1, col2 = st.columns([1.3, 0.7], gap="large")

with col1:
    st.markdown("### 🧺 1. Ingredient Input Matrix")
    
    input_method = st.radio("Choose Input Pipeline:", ["Interactive Pantry Radar", "Fridge Vision Scanner"], horizontal=True)
    
    selected_ingredients = []
    ingredients_text = ""
    uploaded_image = None

    if input_method == "Interactive Pantry Radar":
        st.caption("Expand drawers below to toggle available household ingredients:")
        
        with st.expander("🥦 Fresh Produce & Greens", expanded=True):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Spinach"): selected_ingredients.append("Spinach")
            if c1.checkbox("Tomatoes"): selected_ingredients.append("Tomatoes")
            if c1.checkbox("Onions"): selected_ingredients.append("Onions")
            if c2.checkbox("Bell Peppers"): selected_ingredients.append("Bell Peppers")
            if c2.checkbox("Carrots"): selected_ingredients.append("Carrots")
            if c2.checkbox("Broccoli"): selected_ingredients.append("Broccoli")
            if c3.checkbox("Garlic"): selected_ingredients.append("Garlic")
            if c3.checkbox("Cucumber"): selected_ingredients.append("Cucumber")
            if c3.checkbox("Zucchini"): selected_ingredients.append("Zucchini")

        with st.expander("🌾 Grains, Staples & Bakery"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Cooked Rice"): selected_ingredients.append("Cooked Rice")
            if c1.checkbox("Pasta / Noodles"): selected_ingredients.append("Pasta")
            if c2.checkbox("Bread"): selected_ingredients.append("Bread")
            if c2.checkbox("Oats"): selected_ingredients.append("Oats")
            if c3.checkbox("Quinoa"): selected_ingredients.append("Quinoa")
            if c3.checkbox("Flour"): selected_ingredients.append("Flour")

        with st.expander("🍗 Proteins, Meat & Seafood"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Cooked Chicken"): selected_ingredients.append("Cooked Chicken")
            if c1.checkbox("Ground Beef"): selected_ingredients.append("Ground Beef")
            if c2.checkbox("Canned Tuna"): selected_ingredients.append("Canned Tuna")
            if c2.checkbox("Salmon"): selected_ingredients.append("Salmon")
            if c3.checkbox("Eggs"): selected_ingredients.append("Eggs")
            if c3.checkbox("Shrimp"): selected_ingredients.append("Shrimp")

        with st.expander("🧀 Dairy, Cheese & Alternatives"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Milk"): selected_ingredients.append("Milk")
            if c1.checkbox("Greek Yogurt"): selected_ingredients.append("Greek Yogurt")
            if c2.checkbox("Cheddar / Cheese"): selected_ingredients.append("Cheese")
            if c2.checkbox("Butter"): selected_ingredients.append("Butter")
            if c3.checkbox("Tofu"): selected_ingredients.append("Tofu")
            if c3.checkbox("Heavy Cream"): selected_ingredients.append("Heavy Cream")

        with st.expander("🥫 Legumes, Spices & Pantry Goods"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Canned Chickpeas"): selected_ingredients.append("Chickpeas")
            if c1.checkbox("Lentils"): selected_ingredients.append("Lentils")
            if c2.checkbox("Olive Oil"): selected_ingredients.append("Olive Oil")
            if c2.checkbox("Soy Sauce"): selected_ingredients.append("Soy Sauce")
            if c3.checkbox("Mushrooms"): selected_ingredients.append("Mushrooms")
            if c3.checkbox("Tomato Paste"): selected_ingredients.append("Tomato Paste")

        extra_text = st.text_input("✍️ Additional items (comma-separated):", placeholder="e.g., half lemon, fresh basil")
        
        all_items = selected_ingredients + ([extra_text] if extra_text else [])
        ingredients_text = ", ".join(all_items)
        
        if ingredients_text:
            st.success(f"Active Pantry Payload ({len(all_items)} items): **{ingredients_text}**")

    else:
        uploaded_file = st.file_uploader("📸 Upload clear image of fridge shelf:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Vision Stream Feed", use_container_width=True)

    st.markdown("### 🛰️ Expiration Radar")
    expiring_items = st.text_input("Items reaching end-of-life TODAY/TOMORROW:", placeholder="e.g., open yogurt, fresh spinach")

with col2:
    st.markdown("### 🧪 2. Health & Target Profile")
    
    health_profile = st.selectbox(
        "Select Health Target:",
        [
            "Standard Healthy Household Mode",
            "🩸 Diabetic & Blood-Sugar Friendly (Low GI / High Fiber)",
            "💪 High-Protein & Fitness Focused",
            "🥗 100% Vegetarian / Plant-Based",
            "🥜 Allergen-Safe (Nut-Free / Gluten-Free)"
        ]
    )
    
    family_size = st.slider("Portion Allocation (Servings):", min_value=1, max_value=6, value=2)
    
    st.markdown("### 📡 AI Engine Modules")
    allow_missing = st.checkbox("Enable 1-Ingredient Smart Fill Suggestion", value=True)

st.divider()

# 7. Execution Logic
if st.button("🔮 Generate Culinary & Health Analysis", type="primary"):
    if input_method == "Interactive Pantry Radar" and not ingredients_text:
        st.warning("Please select or specify at least one ingredient to proceed.")
        st.stop()
        
    with st.spinner("Synthesizing low-GI culinary plan & waste mitigation data..."):
        system_instruction = f"""
        You are an elite nutritionist and zero-waste chef expert.
        Generate a delicious, healthy, low-waste recipe based on leftover ingredients.
        
        User Rules:
        - Health Profile: {health_profile}
        - Servings Required: {family_size}
        - Expiring Priority Ingredients: {expiring_items}
        - Allow Suggesting 1 Missing Core Ingredient: {allow_missing}
        
        If Diabetic/Blood-Sugar Friendly mode is selected:
        1. Prioritize low glycemic index (GI) foods.
        2. Combine high-fiber or protein options to prevent glucose spikes.
        3. Cap simple carbohydrates and explain sugar/carb safety clearly.
        
        Structured Output Format Required:
        ---
        ## 🍲 Recipe Title
        **Preparation Time:** [X] Mins | **Difficulty:** [Easy/Medium]
        
        ### 🛒 Ingredients Required (Using Leftovers First)
        - [List items]
        {'### 💡 Recommended 1 Missing Ingredient to Buy' if allow_missing else ''}
        {'- [Optional 1 missing item]' if allow_missing else ''}
        
        ### 🍳 Step-by-Step Instructions
        1. [Step 1]
        2. [Step 2]
        
        ### 🩸 Glycemic Safety & Health Analysis
        - **Carb & Glycemic Impact:** [Explain glycemic safety]
        - **Nutritional Grade:** [e.g., A+]
        - **Macro Allocation:** [Calories, Protein, Carbs, Fiber per serving]
        
        ### 🌿 Zero-Waste Impact Metrics
        - **Food Waste Prevented:** [Calculate estimated weight in grams based on ingredients provided]
        - **Estimated CO₂ Footprint Saved:** [Calculate estimated CO₂ saved in kg based on ingredients provided]
        ---
        """
        
        try:
            if input_method == "Fridge Vision Scanner" and uploaded_image:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=[uploaded_image, system_instruction + "\nFirst, identify the leftover ingredients in the photo, then build the recipe."]
                )
            else:
                prompt = f"{system_instruction}\nLeftover Ingredients Provided: {ingredients_text}"
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
            
            st.success("Analysis Complete!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
