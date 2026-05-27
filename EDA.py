import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# 1. Import the PDF backend
from matplotlib.backends.backend_pdf import PdfPages

# Load data (Fixed variable naming to use 'df' consistently)
df = pd.read_csv("GBvideos.csv")

# trending date to datetime format
df['trending_date']=pd.to_datetime(df['trending_date'], format="%y.%d.%m")

#publish time to datetime format
df['publish_time'] = pd.to_datetime(df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')

# total likes and dislikes
df["total_thumbs"] = df['likes'] + df['dislikes']

# CRITICAL FIX: Calculate missing ratio columns for the final chart
df["like_ratio"] = df["likes"] / (df["total_thumbs"].replace(0, np.nan))
df["dislike_ratio"] = df["dislikes"] / (df["total_thumbs"].replace(0, np.nan))

# Youtube category number to text
youtube_categories = {
    1: "Film & Animation", 2: "Autos & Vehicles", 10: "Music", 15: "Pets & Animals",
    17: "Sports", 18: "Short Movies", 19: "Travel & Events", 20: "Gaming",
    21: "Videoblogging", 22: "People & Blogs", 23: "Comedy", 24: "Entertainment",
    25: "News & Politics", 26: "Howto & Style", 27: "Education", 28: "Science & Technology",
    29: "Nonprofits & Activism", 30: "Movies", 31: "Anime/Animation", 32: "Action/Adventure",
    33: "Classics", 34: "Comedy", 35: "Documentary", 36: "Drama", 37: "Family",
    38: "Foreign", 39: "Horror", 40: "Sci-Fi/Fantasy", 41: "Thriller", 42: "Shorts",
    43: "Shows", 44: "Trailers"
}

df["youtube_category_name"] = df["category_id"].map(youtube_categories)
views_category = df.groupby('youtube_category_name').size().sort_values(ascending=False)


# 2. Open the PDF container
with PdfPages('youtube_analysis_report.pdf') as pdf:


    # --- CHART 1: Views by YouTube Category Over Time ---
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    category_views = (df.groupby(["trending_date", "youtube_category_name"])["views"]
        .sum()
        .unstack(fill_value=0)
        .sort_index()
    )
    category_views.plot(kind="line", linewidth=2, ax=ax1)
    plt.title("Views by YouTube Category Over Time")
    plt.xlabel("Trending Date")
    plt.ylabel("Total Views")
    plt.xticks(rotation=45)
    plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    
    pdf.savefig(fig1, bbox_inches='tight') 
    plt.close(fig1)

    # --- CHART 2: Top 3 Categories ---
    fig2 = plt.figure(figsize=(12, 6))
    category_views = df.groupby(['youtube_category_name', 'trending_date'])['views'].sum()
    entertainment_views = category_views['Entertainment']
    music_views = category_views['Music']
    howto_style_views = category_views['Howto & Style']

    plt.plot(entertainment_views.index, entertainment_views.values, label="Entertainment")
    plt.plot(music_views.index, music_views.values, label="Music")
    plt.plot(howto_style_views.index, howto_style_views.values, label="Howto & Style")

    plt.title("Top 3 Categories")
    plt.xlabel("Date")
    plt.ylabel("Views (Hundreds of Millions)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    pdf.savefig(fig2)
    plt.close(fig2)

    # --- CHART 3: Bottom 3 Categories ---
    fig3 = plt.figure(figsize=(12, 6))
    category_views = df.groupby(['youtube_category_name', 'trending_date'])['views'].sum()
    auto_views = category_views['Autos & Vehicles']
    nonprofit_views = category_views['Nonprofits & Activism']
    shows_views = category_views['Shows']

    plt.plot(auto_views.index, auto_views.values, label="Autos & Vehicles")
    plt.plot(nonprofit_views.index, nonprofit_views.values, label="Nonprofits & Activism")
    plt.plot(shows_views.index, shows_views.values, label="Shows")

    plt.title("Bottom 3 Categories")
    plt.xlabel("Date")
    plt.ylabel("Views (Hundreds of Millions)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    pdf.savefig(fig3)
    plt.close(fig3)

    # --- CHART 4: Reactions per category ---
    fig4, ax4 = plt.subplots(figsize=(14, 6))
    category_reactions = (
        df.groupby("youtube_category_name")[["likes", "dislikes"]].mean().sort_values("likes", ascending=False)
    )
    category_reactions.plot(kind="bar", color=["teal", "coral"], edgecolor="black", ax=ax4)
    plt.title("Average Likes and Dislikes by Category")
    plt.xlabel("Category")
    plt.ylabel("Average Reactions")
    plt.xticks(rotation=45)
    plt.axvspan(-0.5, 0.5, color='green', alpha=0.2)
    plt.legend(["Likes", "Dislikes"])
    plt.tight_layout()
    
    pdf.savefig(fig4)
    plt.close(fig4)

    # --- CHART 5: Likes/dislike ratio ---
    fig5, ax5 = plt.subplots(figsize=(14, 6))
    category_ratios = (
        df.groupby("youtube_category_name")[["like_ratio", "dislike_ratio"]].mean().sort_values("like_ratio", ascending=False)
    )
    category_ratios.plot(kind="bar", color=["teal", "coral"], edgecolor="black", ax=ax5)
    plt.title("Likes/Dislike Ratio")
    plt.xlabel("Category")
    plt.ylabel("Ratio of Reactions")
    plt.axvspan(14.5, 15.5, color='red', alpha=0.2)
    plt.xticks(rotation=45)
    plt.legend(["Likes", "Dislikes"])
    plt.tight_layout()
    
    pdf.savefig(fig5)
    plt.close(fig5)

print("PDF generation complete! Check 'youtube_analysis_report.pdf' in your working directory.")