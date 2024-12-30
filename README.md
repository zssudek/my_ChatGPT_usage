# my_ChatGPT_usage
Desperately searching for why do I pay 20$ each month to this tool...

# README: ChatGPT Usage Analysis Project

## Overview
This project analyzes ChatGPT usage based on categorized and processed conversation data. The aim is to understand how ChatGPT has been utilized, focusing on different application categories, message trends over time, and the sentiment of user interactions.

## Key Features
- **Categorization**: Messages are categorized into various groups such as Homework/Projects, Learning, Technical Help, and more.
- **Sentiment Analysis**: Determines the emotional tone of messages across categories.
- **Correlation Analysis**: Identifies relationships between variables such as message length and sentiment, or hour of day and sentiment.
- **Visualizations**: Provides insightful charts to display usage patterns and trends.

## Visualizations
The project generates the following visualizations:
1. Final Categories Pie Chart: Displays the distribution of all messages across categories.
2. Short Messages Pie Chart: Shows subcategories for short messages.
3. Messages Over Time Line Chart: Highlights daily activity trends.
4. Hourly Message Activity Bar Chart: Illustrates message activity by hour.
5. Sentiment Distribution Bar Chart: Represents the polarity of sentiment in messages.
6. Average Sentiment by Category Bar Chart: Shows average sentiment for each category.
7. Correlation Scatter Plots:
   - Hour of Day vs Sentiment
   - Message Length vs Sentiment

## Processed Data
The processed conversation data is saved in a CSV file:
- **File**: `categorized_homework_analysis.csv`
- **Content**:
  - Categorized messages
  - Sentiment scores
  - Additional metadata such as timestamps, message length, and categories

## Installation
To run this project, follow the steps below:

1. Clone the repository: git clone <repository_url>
2. Navigate to the project directory
3. Install the required dependencies: pip install -r requirements.txt

## How to Run
1.Run the analysis script:
python setup.py

2. View the generated charts and the saved CSV file in the project folder.

## Requirements
The project uses the following Python libraries:
- `pandas`
- `matplotlib`
- `seaborn`
- `textblob`
- `fpdf`

Install all dependencies using the provided `requirements.txt` file.

## Outputs
1. Charts: PNG files for all visualizations mentioned above.
2. Data File: A categorized CSV file (`categorized_homework_analysis.csv`) containing the processed data.
3. PDF Report: A comprehensive report summarizing the analysis and including visualizations.

## Future Work
Possible enhancements include:
- Dynamic dashboards using tools like `Streamlit` or `Dash`.
- Advanced sentiment analysis using a pre-trained language model.
- Integration with real-time data sources for continuous analysis.

## License
This project is open-source and available under the MIT License.



