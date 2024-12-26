import json
import pandas as pd
import matplotlib.pyplot as plt

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

# Exploratory Data Analysis
# Distribution of roles
author_role_counts = conversation_df['author_role'].value_counts()
plt.figure(figsize=(8, 5))
author_role_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution of Author Roles')
plt.xlabel('Author Role')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

# Save cleaned DataFrame
conversation_df.to_csv('cleaned_conversations.csv', index=False)
print("Exploratory Data Analysis Complete. Cleaned data saved to 'cleaned_conversations.csv'.")
