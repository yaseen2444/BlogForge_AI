import streamlit as st
import google.generativeai as genai
import requests
import markdown
import os

# Configure Generative AI
genai.configure(api_key="gemeni api key")

def google_fact_check(query):
    try:
        API_KEY = "google api"
        SEARCH_ENGINE_ID = "engine id"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url, timeout=10).json()
        
        if "items" in response:
            return response["items"][0]["snippet"]
        else:
            return "No relevant information found."
    except Exception as e:
        return f"Error during fact checking: {str(e)}"

def generate_blog_with_gemini(input_text, no_words, blog_style, user_name, description, content_type):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        
        prompt = f"""
        You are a professional blog writer. Write a {content_type} blog post for a {blog_style} audience 
        on the topic "{input_text}" within {no_words} words. Include the following description for context: {description}. 
        This blog is written by {user_name}.
        
        Ensure the blog is:
        1. Engaging and informative
        2. SEO-friendly with proper headings (H1, H2, H3)
        3. Well-structured with clear sections
        4. Contains relevant keywords
        5. Has a compelling introduction and conclusion
        
        Format the output in Markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating blog content: {str(e)}"

def generate_project_documentation(code, description):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        
        # Split the code into blocks based on indentation (or a custom rule for block separation)
        code_blocks = code.split("\n\n")  # Splitting by double newlines as an example, you can modify this to suit your needs

        # Generate a detailed explanation for each block
        block_explanations = ""
        for idx, block in enumerate(code_blocks, start=1):
            prompt = f"""
            Explain the following code block in simple terms:

            Code Block {idx}:
            {block}

            Provide an easy-to-understand explanation, including:
            - Purpose of the block
            - Key components
            - How the block fits into the overall functionality
            - Any example use cases or scenarios for this block
            """
            response = model.generate_content(prompt)
            block_explanations += f"### Code Block {idx} Explanation\n{response.text}\n\n"

        # Creating the full documentation prompt
        prompt = f"""
        Create detailed project documentation in Markdown format based on the following information:

        Project Description:
        {description}

        Code Explanations:
        {block_explanations}
        
        Include:
        1. Project Overview
        2. Technical Architecture
        3. Installation Instructions
        4. Usage Guide
        5. Dependencies list
        6. Best practices and recommendations

        Make it engaging and easy to understand.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating documentation: {str(e)}"

def save_as_markdown(content, filename):
    try:
        return content.encode('utf-8')
    except Exception as e:
        st.error(f"Error saving markdown: {str(e)}")
        return None

# Main Streamlit UI
st.set_page_config(
    page_title="Blog Generator Pro",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .medium-btn {
        background-color: #1a8917;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        text-decoration: none;
        display: inline-block;
        text-align: center;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✍️ Professional Blog Generator")

# Sidebar
with st.sidebar:
    st.header("📝 Blog Settings")
    blog_type = st.selectbox(
        "Select Blog Type",
        ["General Blog", "Project Documentation", "Technical Tutorial"]
    )
    
    if blog_type == "Project Documentation":
        project_code = st.text_area("Paste Your Project Code", height=300)

# Main content area
user_name = st.text_input("👤 Author Name")
blog_title = st.text_input("📋 Blog Title")

if blog_type != "Project Documentation":
    input_text = st.text_input("🎯 Blog Topic")
    description = st.text_area("📝 Topic Description")
else:
    description = st.text_area("📝 Project Description")

cols = st.columns(3)
with cols[0]:
    no_words = st.slider("📊 Word Count", 300, 2000, 500)
with cols[1]:
    blog_style = st.selectbox(
        "🎭 Target Audience",
        ["Researchers", "Data Scientists", "General Audience", 
         "Software Engineers", "Product Managers", "Marketing Professionals"]
    )
with cols[2]:
    content_type = st.selectbox(
        "📚 Content Format",
        ["How-to/Tutorial", "Opinion Piece", "Case Study", 
         "Technical Guide", "Problem-Solution", "Comparison"]
    )

# Generate button
if st.button("🚀 Generate Blog"):
    if not blog_title:
        st.warning("Please enter a blog title")
    else:
        with st.spinner("✨ Generating your professional blog..."):
            try:
                if blog_type == "Project Documentation":
                    generated_content = generate_project_documentation(project_code, description)
                else:
                    generated_content = generate_blog_with_gemini(
                        input_text, no_words, blog_style, user_name, description, content_type
                    )
                
                st.markdown("## 📑 Generated Blog")
                st.markdown(generated_content)
                
                # Action buttons
                col_download, col_publish = st.columns(2)
                
                # Download button
                with col_download:
                    markdown_file = save_as_markdown(generated_content, f"{blog_title}.md")
                    if markdown_file:
                        st.download_button(
                            label="⬇️ Download as Markdown",
                            data=markdown_file,
                            file_name=f"{blog_title}.md",
                            mime="text/markdown"
                        )
                
                # Medium publish button
                with col_publish:
                    st.markdown(f"""
                        <a href="https://medium.com/new-story" target="_blank" class="medium-btn">
                            📤 Publish to Medium
                        </a>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Fact-checking section
                if blog_type != "Project Documentation":
                    st.markdown("## 🔍 Fact-Checked Information")
                    fact_checked_info = google_fact_check(input_text)
                    st.write(fact_checked_info)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("### 📝 How to Publish on Medium")
st.markdown("""
1. Click the 'Publish to Medium' button above
2. Sign in to your Medium account if needed
3. Copy the generated content from above
4. Paste the content into Medium's editor
5. Add your cover image directly in Medium's editor
6. Review and format your content
7. Click 'Publish' when ready
""")