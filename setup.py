import json
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob, Word
import seaborn as sns
import sys

# Ensure UTF-8 output encoding
sys.stdout.reconfigure(encoding='utf-8')

# Load JSON files
with open('conversations.json', 'r') as file:
    conversations = json.load(file)

# Parse conversations
conversation_data = []
for convo in conversations:
    for key, value in convo.get('mapping', {}).items():
        if value.get('message'):
            message = value['message']
            conversation_data.append({
                'conversation_id': convo.get('id', ''),
                'message_id': message.get('id', ''),
                'author_role': message.get('author', {}).get('role', ''),
                'content': message.get('content', {}).get('parts', [''])[0],
                'timestamp': message.get('create_time', None)
            })

# Create DataFrame
conversation_df = pd.DataFrame(conversation_data)

# Handle missing timestamps
conversation_df['timestamp'] = pd.to_datetime(conversation_df['timestamp'], unit='s', errors='coerce')

# Ensure valid rows with timestamps only
conversation_df = conversation_df.dropna(subset=['timestamp'])

# Extract date and hour for time analysis
conversation_df['date'] = conversation_df['timestamp'].dt.date
conversation_df['hour'] = conversation_df['timestamp'].dt.hour

# Ensure all content is string
conversation_df['content'] = conversation_df['content'].apply(lambda x: str(x) if not isinstance(x, str) else x)

# Correct spelling in messages
# conversation_df['content'] = conversation_df['content'].apply(correct_spelling)

# Enhanced Keyword-based categorization of messages
categories = {
    'homework/projects': [
        'homework', 'assignment', 'project', 'task', 'solution', 'ödev', 'debug', 'kod', 'ders', 'analiz'
    ],
    'learning': ['learn', 'understand', 'explain', 'study', 'öğren', 'çalış', 'açıkla'],
    'general': ['what', 'how', 'why', 'ne', 'nasıl', 'neden'],
    'technical_help': ['setup', 'config', 'install', 'kurulum', 'ayar'],
    'chatgpt_related': ['chatgpt', 'ai', 'openai', 'model'],
    'personal/general': ['günlük', 'kişisel', 'daily', 'advice', 'benim'],
    'text_analysis/translation': ['çevir', 'sentiment', 'dil', 'translate'],
    'start-up': ['startup', 'girişim', 'yatırım', 'gelir']
}

def categorize_message(content):
    if len(content.split()) < 3:  # Short messages category
        return 'short_message'
    if any(token in content for token in ['{', '}', 'def ', 'class ', 'function']):
        return 'homework/projects'
    for category, keywords in categories.items():
        if any(keyword in content.lower() for keyword in keywords):
            return category
    return 'other'

conversation_df['category'] = conversation_df['content'].apply(categorize_message)

# Combine 'other' subcategories into main categories
conversation_df['final_category'] = conversation_df['category']

# Reanalyze uncategorized messages
uncategorized_df = conversation_df[conversation_df['final_category'] == 'other']
print("Sample Uncategorized Messages:")
print(uncategorized_df[['content']].head(10))

# Analyze usage for final categories
final_category_counts = conversation_df['final_category'].value_counts()

# Visualize all categories in a single pie chart with legend showing percentages
if not final_category_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 8))  # Geniş oranlı figür
    wedges, texts = ax.pie(
        final_category_counts,
        labels=None,  # No labels on the pie chart
        startangle=90,
        colors=plt.cm.Paired.colors,
        textprops={'fontsize': 10}
    )
    ax.set_title('GPT Usage by Final Categories', fontsize=14)
    plt.legend(
        wedges, 
        [f"{category}: {percentage:.1f}%" for category, percentage in zip(final_category_counts.index, 100 * final_category_counts / final_category_counts.sum())],
        title="Categories", 
        bbox_to_anchor=(1, 0.5), 
        loc="center left", 
        fontsize=10
    )
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)  # Kenar boşlukları
    plt.axis('equal')
    plt.savefig('final_categories_pie_chart.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available to create a pie chart.")

# Short message alt kategorileri belirleme
def categorize_short_message(content):
    if any(kw in content.lower() for kw in ['ne', 'nasıl', 'neden', 'mi', 'kim']):
        return 'question'
    elif any(kw in content.lower() for kw in ['evet', 'hayır', 'tamam', 'olur', 'ok']):
        return 'response'
    elif any(char in content for char in ['😊', '😂', '👍', '❤️']):
        return 'emoji'
    else:
        return 'other_short'

# Sadece short_message kategorisindeki mesajları analiz et
short_message_df = conversation_df[conversation_df['final_category'] == 'short_message']
short_message_df['short_category'] = short_message_df['content'].apply(categorize_short_message)

# Short message alt kategorilerini say
short_message_counts = short_message_df['short_category'].value_counts()

# Short message alt kategorileri için pie chart oluşturma
if not short_message_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 8))  # Geniş oranlı figür
    wedges, texts = ax.pie(
        short_message_counts,
        labels=None,  # No labels on the pie chart
        startangle=90,
        colors=plt.cm.Paired.colors
    )
    ax.set_title('Short Messages Distribution', fontsize=14)
    plt.legend(
        wedges,
        [f"{category}: {percentage:.1f}%" for category, percentage in zip(short_message_counts.index, 100 * short_message_counts / short_message_counts.sum())],
        title="Short Message Categories",
        bbox_to_anchor=(1, 0.5),
        loc="center left",
        fontsize=10
    )
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)  # Kenar boşlukları
    plt.axis('equal')
    plt.savefig('short_messages_pie_chart.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available to create a pie chart for short messages.")

# Time-based distribution of messages
time_based_counts = conversation_df.groupby('date').size()
if not time_based_counts.empty:
    plt.figure(figsize=(12, 6))
    time_based_counts.plot(kind='line', color='blue')
    plt.title('Number of Messages Over Time', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Message Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('messages_over_time_line_chart.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available for time-based distribution.")

# Hourly message activity
hourly_message_counts = conversation_df.groupby('hour').size()
if not hourly_message_counts.empty:
    plt.figure(figsize=(12, 6))
    hourly_message_counts.plot(kind='bar', color='orange')
    plt.title('Hourly Message Activity', fontsize=14)
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Message Count', fontsize=12)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('hourly_message_activity_bar_chart.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available for hourly message activity.")

# Sentiment Analysis
def analyze_sentiment(content):
    try:
        analysis = TextBlob(content)
        return analysis.sentiment.polarity
    except Exception as e:
        print(f"Error analyzing sentiment for content: {content[:30]}... - {e}")
        return 0

conversation_df['sentiment'] = conversation_df['content'].apply(analyze_sentiment)

# Sentiment distribution
distribution = conversation_df['sentiment'].value_counts(bins=10)
if not distribution.empty:
    plt.figure(figsize=(12, 6))
    distribution.sort_index().plot(kind='bar', color='purple')
    plt.title('Sentiment Distribution of Messages', fontsize=14)
    plt.xlabel('Sentiment Polarity', fontsize=12)
    plt.ylabel('Message Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sentiment_distribution_bar_chart.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available for sentiment analysis distribution.")

# Average sentiment by category
average_sentiments = conversation_df.groupby('final_category')['sentiment'].mean()
if not average_sentiments.empty:
    plt.figure(figsize=(12, 6))
    average_sentiments.sort_values().plot(kind='bar', color='teal')
    plt.title('Average Sentiment by Category', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Average Sentiment Polarity', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('average_sentiment_by_category_bar_chart.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available for average sentiment by category.")

# Correlation Analysis
# 1. Correlation between hour and sentiment
if not conversation_df[['hour', 'sentiment']].empty:
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='hour', y='sentiment', data=conversation_df, alpha=0.5)
    plt.title('Correlation between Hour of Day and Sentiment', fontsize=14)
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Sentiment Polarity', fontsize=12)
    plt.tight_layout()
    plt.savefig('hour_vs_sentiment_scatter.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available for hour vs sentiment correlation.")

# 2. Correlation between message length and sentiment
conversation_df['message_length'] = conversation_df['content'].apply(len)
if not conversation_df[['message_length', 'sentiment']].empty:
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='message_length', y='sentiment', data=conversation_df, alpha=0.5)
    plt.title('Correlation between Message Length and Sentiment', fontsize=14)
    plt.xlabel('Message Length', fontsize=12)
    plt.ylabel('Sentiment Polarity', fontsize=12)
    plt.tight_layout()
    plt.savefig('message_length_vs_sentiment_scatter.png', bbox_inches='tight')
    plt.show()
else:
    print("No data available for message length vs sentiment correlation.")

# Save results
try:
    conversation_df.to_csv('categorized_homework_analysis.csv', index=False)
    print("Categorized and homework-analyzed data saved to 'categorized_homework_analysis.csv'.")
except Exception as e:
    print(f"Error saving categorized homework analysis data: {e}")
