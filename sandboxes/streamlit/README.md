# Streamlit Sandbox

Test Streamlit UI components and data visualization for the portfolio tracker.

## What to Test

- Streamlit app interface and layout
- Interactive charts and visualizations
- Data tables and metrics
- User input components
- Real-time data updates

## Commands to Run

```bash
# Navigate to sandbox directory
cd sandboxes/streamlit

# Install dependencies (from main repo)
pip install -r ../../requirements.txt

# Run the Streamlit app
streamlit run streamlit_sandbox.py

# Or run with specific port
streamlit run streamlit_sandbox.py --server.port 8501
```

## Expected Output

The app will open in your browser showing:
- 📈 Portfolio dashboard with metrics
- 📊 Interactive portfolio table with color coding
- 💰 Pie chart of portfolio allocation
- 📈 Bar chart of performance by stock
- 📊 Price history line chart
- 🎯 Interactive features for adding positions

## Features to Test

1. **Portfolio Overview**: View sample portfolio data
2. **Charts**: Interact with pie charts, bar charts, and line charts
3. **Filters**: Select different stocks for price history
4. **Input Forms**: Try adding new positions
5. **Responsive Layout**: Test on different screen sizes

## Play Around Ideas

1. Modify the sample data in `create_sample_data()`
2. Add new chart types (candlestick, heatmap)
3. Create new interactive widgets
4. Add data export functionality
5. Implement real-time data updates
6. Add authentication/login features
7. Create different page layouts

## Troubleshooting

- If charts don't load, check internet connection (Plotly loads from CDN)
- If app is slow, reduce the amount of sample data
- Make sure all dependencies are installed correctly 