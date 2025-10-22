import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
        /* Fallback for browsers that don't support background-clip */
        color: #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    
    .uploaded-file {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">💬 WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.markdown("## 📁 Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file", type=['txt'], help="Upload your exported WhatsApp chat file")
if uploaded_file is not None:
    # Show file upload success
    st.sidebar.markdown(f"""
    <div class="uploaded-file">
        <h4>✅ File Uploaded Successfully!</h4>
        <p><strong>File:</strong> {uploaded_file.name}</p>
        <p><strong>Size:</strong> {len(uploaded_file.getvalue())} bytes</p>
    </div>
    """, unsafe_allow_html=True)
    
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    st.sidebar.markdown("## 👤 Select User")
    selected_user = st.sidebar.selectbox("Choose user for analysis", user_list, help="Select a specific user or 'Overall' for group analysis")
    
    st.sidebar.markdown("## 🎯 Analysis Options")
    show_analysis = st.sidebar.button("🚀 Start Analysis", type="primary", use_container_width=True)
    
    if show_analysis:

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        
        st.markdown('<h2 class="section-header">📊 Key Statistics</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">📨 {num_messages:,}</div>
                <div class="metric-label">Total Messages</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">📝 {words:,}</div>
                <div class="metric-label">Total Words</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">📎 {num_media_messages:,}</div>
                <div class="metric-label">Media Shared</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🔗 {num_links:,}</div>
                <div class="metric-label">Links Shared</div>
            </div>
            """, unsafe_allow_html=True)

        # Timeline Analysis
        st.markdown('<h2 class="section-header">📈 Timeline Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📅 Monthly Activity")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots(figsize=(10, 6))
            ax.plot(timeline['time'], timeline['message'], color='#667eea', linewidth=3, marker='o', markersize=8)
            ax.fill_between(timeline['time'], timeline['message'], alpha=0.3, color='#667eea')
            ax.set_xlabel('Month', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.markdown("### 📆 Daily Activity")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#764ba2', linewidth=2, marker='s', markersize=6)
            ax.fill_between(daily_timeline['only_date'], daily_timeline['message'], alpha=0.3, color='#764ba2')
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        # Activity Analysis
        st.markdown('<h2 class="section-header">🗓️ Activity Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📅 Most Active Days")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(busy_day.index, busy_day.values, color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b'])
            ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.set_title('Weekly Activity Pattern', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.markdown("### 📆 Most Active Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(busy_month.index, busy_month.values, color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#fa709a'])
            ax.set_xlabel('Month', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.set_title('Monthly Activity Pattern', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        st.markdown("### 🔥 Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        if not user_heatmap.empty:
            fig,ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(user_heatmap, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Messages'})
            ax.set_title('Hour vs Day Activity Heatmap', fontsize=14, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
            ax.set_ylabel('Day of Week', fontsize=12, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No activity data available for heatmap")

        # User Analysis (only for Overall)
        if selected_user == 'Overall':
            st.markdown('<h2 class="section-header">👥 User Analysis</h2>', unsafe_allow_html=True)
            x,new_df = helper.most_busy_users(df)
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🏆 Top Active Users")
                fig, ax = plt.subplots(figsize=(10, 8))
                bars = ax.barh(x.index, x.values, color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'])
                ax.set_xlabel('Number of Messages', fontsize=12, fontweight='bold')
                ax.set_title('Most Active Users', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                
            with col2:
                st.markdown("### 📊 User Statistics")
                st.dataframe(new_df, use_container_width=True)

        # Content Analysis
        st.markdown('<h2 class="section-header">📝 Content Analysis</h2>', unsafe_allow_html=True)
        
        # WordCloud
        st.markdown("### ☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        if df_wc is not None:
            fig,ax = plt.subplots(figsize=(12, 8))
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Most Frequent Words', fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No text data available for wordcloud generation")

        # Most Common Words and Emoji Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Most Common Words")
            most_common_df = helper.most_common_words(selected_user,df)
            if not most_common_df.empty:
                fig,ax = plt.subplots(figsize=(10, 8))
                bars = ax.barh(most_common_df[0], most_common_df[1], color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#ffecd2', '#fcb69f'])
                ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
                ax.set_title('Top 20 Most Common Words', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No common words data available")

        with col2:
            st.markdown("### 😀 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user,df)
            if not emoji_df.empty:
                fig,ax = plt.subplots(figsize=(10, 8))
                colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#ffecd2', '#fcb69f']
                wedges, texts, autotexts = ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%1.1f%%", colors=colors[:10])
                ax.set_title('Top 10 Most Used Emojis', fontsize=14, fontweight='bold')
                plt.tight_layout()
                st.pyplot(fig)
                
                st.markdown("#### 📋 Emoji Statistics")
                st.dataframe(emoji_df.head(10), use_container_width=True)
            else:
                st.info("No emoji data available")

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-top: 2rem;'>
            <h3>🎉 Analysis Complete!</h3>
            <p>Your WhatsApp chat has been thoroughly analyzed. Explore the insights above to understand your chat patterns better.</p>
            <p><strong>Built with ❤️ using Streamlit</strong></p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome message when no file is uploaded
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin: 2rem 0;'>
        <h2>🚀 Welcome to WhatsApp Chat Analyzer!</h2>
        <p style='font-size: 1.2rem; margin: 1rem 0;'>Upload your WhatsApp chat file to get started with comprehensive analysis</p>
        <div style='margin: 2rem 0;'>
            <h3>📊 What you'll get:</h3>
            <ul style='text-align: left; display: inline-block;'>
                <li>📈 Message statistics and trends</li>
                <li>📅 Timeline analysis (daily/monthly)</li>
                <li>🗓️ Activity patterns and heatmaps</li>
                <li>👥 User engagement analysis</li>
                <li>☁️ Word clouds and common words</li>
                <li>😀 Emoji usage statistics</li>
            </ul>
        </div>
        <p><strong>Upload a file from the sidebar to begin! 📁</strong></p>
    </div>
    """, unsafe_allow_html=True)







