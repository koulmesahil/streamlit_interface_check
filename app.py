import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Sports Ball Classifier",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject the animated background using HTML component
background_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        #defaultCanvas0 {
            position: fixed;
            top: 0;
            left: 0;
            z-index: -1;
        }
    </style>
</head>
<body>
    <script>
    let particles = [];
    let sports = ['⚽', '🏀', '⚾', '🏈', '🎾', '🏐', '🎱', '🏉', '🏓'];
    
    function setup() {
        createCanvas(windowWidth, windowHeight);
        
        // Create initial particles
        for (let i = 0; i < 30; i++) {
            particles.push(new Particle());
        }
    }
    
    function draw() {
        // Gradient background
        let c1 = color(15, 32, 39);
        let c2 = color(32, 58, 67);
        let c3 = color(44, 83, 100);
        
        for (let y = 0; y < height; y++) {
            let inter = map(y, 0, height, 0, 1);
            let c;
            if (inter < 0.5) {
                c = lerpColor(c1, c2, inter * 2);
            } else {
                c = lerpColor(c2, c3, (inter - 0.5) * 2);
            }
            stroke(c);
            line(0, y, width, y);
        }
        
        // Update and display particles
        for (let particle of particles) {
            particle.update();
            particle.display();
        }
    }
    
    function windowResized() {
        resizeCanvas(windowWidth, windowHeight);
    }
    
    class Particle {
        constructor() {
            this.x = random(width);
            this.y = random(height);
            this.vx = random(-0.5, 0.5);
            this.vy = random(-0.5, 0.5);
            this.size = random(20, 40);
            this.symbol = random(sports);
            this.alpha = random(100, 200);
            this.rotation = random(TWO_PI);
            this.rotationSpeed = random(-0.02, 0.02);
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.rotation += this.rotationSpeed;
            
            // Wrap around edges
            if (this.x < -50) this.x = width + 50;
            if (this.x > width + 50) this.x = -50;
            if (this.y < -50) this.y = height + 50;
            if (this.y > height + 50) this.y = -50;
        }
        
        display() {
            push();
            translate(this.x, this.y);
            rotate(this.rotation);
            textSize(this.size);
            textAlign(CENTER, CENTER);
            fill(255, 255, 255, this.alpha);
            text(this.symbol, 0, 0);
            pop();
        }
    }
    </script>
</body>
</html>
"""

# Display background in an iframe that covers the page
components.html(
    background_html,
    height=0,
    scrolling=False,
)

# Custom CSS
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full page styling with gradient fallback */
    .stApp {
        background: linear-gradient(180deg, 
            rgb(15, 32, 39) 0%, 
            rgb(32, 58, 67) 50%, 
            rgb(44, 83, 100) 100%);
    }
    
    /* Main content container */
    .main {
        padding-top: 8vh;
    }
    
    /* Title styling */
    .minimal-title {
        font-size: 3.5rem;
        font-weight: 300;
        letter-spacing: 0.3rem;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    .emoji-row {
        font-size: 1.8rem;
        letter-spacing: 0.8rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Info icon styling */
    .info-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .info-icon {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        width: 32px;
        height: 32px;
        line-height: 32px;
        text-align: center;
        cursor: help;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .info-icon:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: scale(1.1);
    }
    
    .info-icon:hover .tooltip {
        opacity: 1;
        visibility: visible;
        transform: translateX(-50%) translateY(-10px);
    }
    
    .tooltip {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%) translateY(0);
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(20px);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 300;
        letter-spacing: 0.05rem;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        line-height: 1.6;
        text-align: left;
    }
    
    .tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 8px solid transparent;
        border-top-color: rgba(0, 0, 0, 0.9);
    }
    
    /* Upload area styling */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* File uploader text */
    [data-testid="stFileUploader"] label {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 300 !important;
        letter-spacing: 0.05rem;
    }
    
    [data-testid="stFileUploader"] section {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"] section:hover {
        border-color: rgba(255, 255, 255, 0.5);
        background: rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stFileUploader"] small {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Image preview */
    [data-testid="stImage"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Success message */
    [data-testid="stAlert"] {
        background: rgba(76, 175, 80, 0.2) !important;
        backdrop-filter: blur(20px);
        border-radius: 12px;
        border: 1px solid rgba(76, 175, 80, 0.4) !important;
        color: white !important;
    }
    
    [data-testid="stAlert"] svg {
        color: rgba(76, 175, 80, 1) !important;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 4rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="minimal-title">CLASSIFY</h1>', unsafe_allow_html=True)

# Emoji row with all 15 sports balls
st.markdown('''
    <div class="emoji-row">
        🏈 ⚾ 🏀 🎱 🎳 🏏 ⚽ ⛳ 🏑 🏒 🏉 🏸 🏓 🎾 🏐
    </div>
''', unsafe_allow_html=True)

# Info icon with hover tooltip
st.markdown('''
    <div class="info-container">
        <div class="info-icon">
            ℹ️
            <div class="tooltip">
                <strong>Upload a sports ball image</strong><br>
                and we'll see if it's one of these:<br><br>
                🏈 American Football • ⚾ Baseball • 🏀 Basketball<br>
                🎱 Billiard Ball • 🎳 Bowling Ball • 🏏 Cricket Ball<br>
                ⚽ Football • ⛳ Golf Ball • 🏑 Field Hockey Ball<br>
                🏒 Hockey Puck • 🏉 Rugby Ball • 🏸 Shuttlecock<br>
                🏓 Table Tennis Ball • 🎾 Tennis Ball • 🏐 Volleyball
            </div>
        </div>
    </div>
''', unsafe_allow_html=True)

# Create centered column for upload
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=['png', 'jpg', 'jpeg', 'gif'],
        help="Upload a sports ball image for classification"
    )
    
    if uploaded_file is not None:
        # Display success message
        st.success("✓ Image uploaded successfully")
        
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Classifying your sports ball...")
        
        # Optional: Display image info
        st.markdown(f"""
            <div style='text-align: center; color: rgba(255, 255, 255, 0.6); 
                        font-size: 0.9rem; margin-top: 1rem; letter-spacing: 0.05rem;'>
                {uploaded_file.name} • {image.size[0]} × {image.size[1]}
            </div>
        """, unsafe_allow_html=True)
