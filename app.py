import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="SmartChef AI | Zero-Waste & Health Engine",
    page_icon="🥑",
    layout="wide"
)

# Global Variables Initialization
allow_missing = False

# 2. Responsive UI Styling
st.markdown("""
    <style>
    .hero-banner {
        background: linear-gradient(135deg, #0d5c46 0%, #11998e 50%, #38ef7d 100%);
        padding: 24px 16px;
        border-radius: 18px;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(17, 153, 142, 0.2);
    }
    .hero-banner h1 {
        color: #ffffff !important;
        font-weight: 800;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        margin-bottom: 6px;
    }
    .hero-banner p {
        color: #f0fdf4 !important;
        font-size: clamp(0.85rem, 2.5vw, 1.1rem);
        margin: 0;
    }
    .metric-card {
        background: #ffffff;
        padding: 16px 12px;
        border-radius: 14px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 10px;
    }
    .metric-card h3 {
        margin: 0;
        color: #0d5c46;
        font-size: clamp(1.1rem, 3vw, 1.35rem);
        font-weight: 700;
    }
    .metric-card p {
        margin: 4px 0 0 0;
        color: #64748b;
        font-size: 0.8rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0d5c46 0%, #11998e 100%);
        color: #ffffff !important;
        font-size: 1.15rem;
        font-weight: 700;
        border-radius: 12px;
        padding: 12px 20px;
        border: none;
        box-shadow: 0 4px 14px rgba(13, 92, 70, 0.25);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(13, 92, 70, 0.35);
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
        <p>Interactive Leftover Recipe & Health Engine | Supporting SDG 3 & SDG 12</p>
    </div>
""", unsafe_allow_html=True)

# 5. Impact Metrics Header
m1, m2, m3 = st.columns([1, 1, 1])
with m1:
    st.markdown("""<div class="metric-card"><h3>🌐 SDG 3 & 12</h3><p>Aligned Global Goals</p></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><h3>⚖️ ~400g / Meal</h3><p>Avg Benchmark Waste Saved</p></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><h3>🍃 ~1.2 kg CO₂e</h3><p>Average Footprint Reduction</p></div>""", unsafe_allow_html=True)

st.write("")

# 6. Main Interface Layout
col1, col2 = st.columns([1.3, 0.7], gap="large")

with col1:
    st.markdown("### 🧺 1. Smart Ingredient Selector")
    
    input_method = st.radio(
        "Choose Input Pipeline:", 
        ["Interactive Pantry Drawers", "Fridge Vision Scanner", "Voice Pantry Assistant"], 
        horizontal=True
    )
    
    selected_ingredients = []
    ingredients_text = ""
    uploaded_image = None
    audio_file = None

    if input_method == "Interactive Pantry Drawers":
        st.caption("Select available ingredients from the options below:")
        
        veg = st.multiselect("🥦 Fresh Produce & Greens:", ["Spinach", "Tomatoes", "Onions", "Bell Peppers", "Carrots", "Broccoli", "Garlic", "Cucumber", "Zucchini"])
        grains = st.multiselect("🌾 Grains, Staples & Bakery:", ["Cooked Rice", "Pasta / Noodles", "Bread", "Oats", "Quinoa", "Flour"])
        protein = st.multiselect("🍗 Proteins, Meat & Seafood:", ["Cooked Chicken", "Ground Beef", "Canned Tuna", "Salmon", "Eggs", "Shrimp"])
        dairy = st.multiselect("🧀 Dairy, Cheese & Alternatives:", ["Milk", "Greek Yogurt", "Cheddar / Cheese", "Butter", "Tofu", "Heavy Cream"])
        pantry = st.multiselect("🥫 Legumes, Spices & Pantry Goods:", ["Canned Chickpeas", "Lentils", "Olive Oil", "Soy Sauce", "Mushrooms", "Tomato Paste"])
        
        extra_text = st.text_input("✍️ Additional items (comma-separated):", placeholder="e.g., half lemon, fresh basil")
        
        all_items = veg + grains + protein + dairy + pantry
        if extra_text:
            all_items.extend([item.strip() for item in extra_text.split(",") if item.strip()])
            
        ingredients_text = ", ".join(all_items)
        
        if ingredients_text:
            st.success(f"Active Pantry Payload ({len(all_items)} items): **{ingredients_text}**")

    elif input_method == "Fridge Vision Scanner":
        uploaded_file = st.file_uploader("📸 Upload clear image of fridge shelf:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Vision Stream Feed", use_container_width=True)

    elif input_method == "Voice Pantry Assistant":
        st.caption("Press the microphone icon below and speak your leftover ingredients out loud:")
        audio_file = st.audio_input("Record your leftover ingredients")
        if audio_file:
            st.success("🎤 Audio recorded! Click 'Generate Culinary & Health Analysis' below to proceed.")

    st.markdown("### 🛰️ Pantry Expiration Radar")
    expiring_items = st.text_input("Items reaching end-of-life TODAY/TOMORROW:", placeholder="e.g., open yogurt, fresh spinach")
    
    if expiring_items:
        st.warning(f"🚨 **Expiration Risk Alert:** System will prioritize using: **{expiring_items}**")

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

st.divider()

# 7. Execution Logic
if st.button("🔮 Generate Culinary & Health Analysis", type="primary"):
    if input_method == "Interactive Pantry Drawers" and not ingredients_text:
        st.warning("Please select or specify at least one ingredient to proceed.")
        st.stop()
    elif input_method == "Fridge Vision Scanner" and not uploaded_image:
        st.warning("Please upload a fridge image to proceed.")
        st.stop()
    elif input_method == "Voice Pantry Assistant" and not audio_file:
        st.warning("Please record a voice input to proceed.")
        st.stop()
        
    with st.spinner("Synthesizing low-GI culinary plan & waste mitigation data..."):
        system_instruction = f"""
        You are an elite nutritionist and zero-waste chef expert.
        Generate a delicious, healthy, low-waste recipe based ONLY on the provided leftover ingredients.
        
        User Rules:
        - Health Profile: {health_profile}
        - Servings Required: {family_size}
        - Expiring Priority Ingredients: {expiring_items}
        
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
        
        # Robust execution function using retries for gemini-3.6-flash
        def generate_with_retries(contents_payload, max_attempts=3):
            for attempt in range(1, max_attempts + 1):
                try:
                    return client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=contents_payload
                    )
                except Exception as e:
                    # If server is overloaded (503 / UNAVAILABLE), pause briefly and retry
                    if any(err_code in str(e) for err_code in ["503", "UNAVAILABLE"]) and attempt < max_attempts:
                        time.sleep(2)
                        continue
                    raise e

        try:
            if input_method == "Fridge Vision Scanner" and uploaded_image:
                payload = [uploaded_image, system_instruction + "\nFirst, identify the leftover ingredients in the photo, then build the recipe."]
            elif input_method == "Voice Pantry Assistant" and audio_file:
                audio_bytes = audio_file.read()
                audio_part = types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=audio_file.type or "audio/wav"
                )
                payload = [
                    audio_part,
                    system_instruction + "\nListen to the audio recording to extract all mentioned ingredients, then generate the recipe."
                ]
            else:
                payload = f"{system_instruction}\nLeftover Ingredients Provided: {ingredients_text}"

            response = generate_with_retries(payload)
            
            st.success("Analysis Complete!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
