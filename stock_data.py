import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    """Class to fetch and process stock data from Yahoo Finance"""
    
    def __init__(self):
        pass
    
    def get_stock_data(self, symbol, period="1y"):
        """
        Fetch comprehensive stock data for a given symbol
        
        Args:
            symbol (str): Stock ticker symbol
            period (str): Time period for historical data
            
        Returns:
            dict: Dictionary containing stock info and price data
        """
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get basic company info
            info = ticker.info
            
            # Validate that we have valid company data
            if not info or 'symbol' not in info:
                return None
            
            # Get historical price data
            hist_data = ticker.history(period=period)
            
            if hist_data.empty:
                return None
            
            # Get additional financial data
            try:
                # Get quarterly financials
                quarterly_financials = ticker.quarterly_financials
                
                # Get balance sheet
                balance_sheet = ticker.balance_sheet
                
                # Get cash flow
                cash_flow = ticker.cashflow
            except:
                # If financial data is not available, continue without it
                quarterly_financials = pd.DataFrame()
                balance_sheet = pd.DataFrame()
                cash_flow = pd.DataFrame()
            
            return {
                'info': info,
                'price_data': hist_data,
                'quarterly_financials': quarterly_financials,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow
            }
            
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {str(e)}")
            return None
    
    def validate_symbol(self, symbol):
        """
        Validate if a stock symbol exists and has data
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Check if we have basic company information
            return bool(info and 'symbol' in info and info.get('longName'))
            
        except:
            return False
    
    def get_company_name(self, symbol):
        """
        Get the full company name for a given symbol
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            str: Company name or None if not found
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('longName')
        except:
            return None
    
    def get_sector_and_industry(self, symbol):
        """
        Get sector and industry information for a company
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            tuple: (sector, industry) or (None, None) if not found
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('sector'), info.get('industry')
        except:
            return None, None
    
    def calculate_technical_indicators(self, price_data):
        """
        Calculate basic technical indicators
        
        Args:
            price_data (pd.DataFrame): Historical price data
            
        Returns:
            dict: Dictionary with technical indicators
        """
        if price_data.empty:
            return {}
        
        try:
            # Calculate moving averages
            sma_20 = price_data['Close'].rolling(window=20).mean()
            sma_50 = price_data['Close'].rolling(window=50).mean()
            
            # Calculate RSI (simplified)
            delta = price_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Current values
            current_price = price_data['Close'].iloc[-1]
            current_sma_20 = sma_20.iloc[-1] if not sma_20.empty else None
            current_sma_50 = sma_50.iloc[-1] if not sma_50.empty else None
            current_rsi = rsi.iloc[-1] if not rsi.empty else None
            
            return {
                'current_price': current_price,
                'sma_20': current_sma_20,
                'sma_50': current_sma_50,
                'rsi': current_rsi,
                'volume_avg': price_data['Volume'].tail(20).mean(),
                'price_change_30d': ((current_price - price_data['Close'].iloc[-30]) / price_data['Close'].iloc[-30] * 100) if len(price_data) >= 30 else None
            }
            
        except Exception as e:
            print(f"Error calculating technical indicators: {str(e)}")
            return {}
