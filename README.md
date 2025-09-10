# 🤖 AI Investment Analyzer

A comprehensive AI-powered investment analysis application built with Streamlit that provides intelligent insights for stock investments and 401K benefits analysis.

## ✨ Features

### 📈 Stock Analysis
- **AI-Powered Investment Analysis**: Get detailed AI-generated insights about any stock's investment potential
- **Investment Recommendations**: Receive Buy/Hold/Sell recommendations with reasoning
- **Real-time Data**: Fetch live stock data and financial metrics using Yahoo Finance
- **Interactive Charts**: Visualize stock performance with candlestick charts and volume analysis
- **Flexible Time Periods**: Analyze data across 1 month to 2 years
- **Comprehensive Metrics**: View key financial indicators, market cap, P/E ratios, and more
- **CSV Export**: Download analysis data for further research

### 💼 401K Analysis
- **Company Benefits Analysis**: Analyze 401K plans for any company
- **AI-Powered Insights**: Get detailed breakdowns of company match, vesting schedules, and Roth options
- **Optimization Recommendations**: Receive personalized advice for maximizing 401K benefits
- **Comprehensive Coverage**: Analyze contribution limits, employer matching, and investment options

## 🚀 Technology Stack

- **Frontend**: Streamlit
- **AI Engine**: OpenAI GPT-5
- **Data Source**: Yahoo Finance (yfinance)
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Deployment**: Replit

## 📋 Prerequisites

Before running the application, you need:

1. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Python 3.11+**: For running the application
3. **Replit Account**: For deployment (optional)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/hbasu/ai-investment-analyzer.git
cd ai-investment-analyzer
```

### 2. Install Dependencies
```bash
pip install streamlit pandas plotly yfinance openai
```

### 3. Set Environment Variables
Create a `.env` file or set environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### 4. Run the Application
```bash
streamlit run app.py --server.port 5000
```

The application will be available at `http://localhost:5000`

## 🎯 Usage

### Stock Analysis
1. Navigate to the **Stock Analysis** tab
2. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL)
3. Select your preferred analysis period
4. Click **"🔍 Analyze Stock"**
5. Review the comprehensive AI analysis and recommendations
6. Export results to CSV if needed

### 401K Analysis
1. Switch to the **401K Analysis** tab
2. Enter a company name
3. Click **"Analyze 401K Benefits"**
4. Review detailed benefits breakdown and optimization recommendations

## 📁 Project Structure

```
ai-investment-analyzer/
├── app.py                 # Main Streamlit application
├── ai_analysis.py         # AI analysis engine using OpenAI
├── stock_data.py         # Stock data fetching and processing
├── .streamlit/
│   └── config.toml       # Streamlit server configuration
└── README.md            # Project documentation
```

## 🔧 Configuration

### Streamlit Configuration (`.streamlit/config.toml`)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## 🤖 AI Analysis Capabilities

The application leverages OpenAI's GPT-5 model to provide:

- **Investment Strategy Analysis**: Detailed evaluation of company's AI initiatives and competitive positioning
- **Risk Assessment**: Comprehensive risk analysis including market, technical, and regulatory factors
- **Financial Health**: Analysis of key financial metrics and sustainability
- **Market Trends**: Insights into sector trends and growth potential
- **401K Optimization**: Personalized recommendations for maximizing retirement benefits

## 🛡️ Security Features

- **Unicode Safe Processing**: Robust text sanitization and encoding handling
- **API Key Validation**: Secure validation of OpenAI API keys
- **Error Handling**: Comprehensive error management with fallback responses
- **Safe Logging**: Unicode-safe logging system to prevent encoding errors

## 📊 Sample Analysis Output

### Stock Analysis
- **Company Overview**: Basic company information and market metrics
- **AI Investment Score**: AI-generated rating and recommendation
- **Key Metrics**: Financial ratios, market performance, and technical indicators
- **Investment Recommendation**: Clear Buy/Hold/Sell advice with detailed reasoning
- **Risk Factors**: Identified risks and mitigation strategies

### 401K Analysis
- **Company Match**: Percentage and maximum matching details
- **Vesting Schedule**: Timeline and requirements for benefit vesting
- **Roth Options**: Availability and tax implications
- **Investment Options**: Available funds and fee structures
- **Optimization Tips**: Personalized recommendations for maximizing benefits

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 5000
```

### Replit Deployment
1. Import the repository to Replit
2. Set the `OPENAI_API_KEY` secret in Replit Secrets
3. Configure the workflow to run `streamlit run app.py --server.port 5000`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This application provides AI-generated investment analysis for informational purposes only. It should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/hbasu/ai-investment-analyzer/issues) page
2. Create a new issue with detailed information about your problem
3. Ensure you have the latest version of all dependencies

---

**Built with ❤️ using Streamlit and OpenAI**