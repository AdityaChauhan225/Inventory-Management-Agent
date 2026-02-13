"""
Flexible CSV Data Processor with Intelligent Column Detection
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import re


class DataProcessor:
    """Handles CSV loading and preprocessing with flexible column detection"""
    
    # Column name mappings for intelligent detection
    COLUMN_PATTERNS = {
        'sku': ['sku', 'id', 'product_id', 'item_id', 'code', 'product_code'],
        'product_name': ['name', 'product', 'item', 'product_name', 'item_name', 'description'],
        'stock': ['stock', 'quantity', 'qty', 'inventory', 'available', 'on_hand', 'current_stock'],
        'sales': ['sales', 'sold', 'units_sold', 'demand', 'sales_30', 'monthly_sales'],
        'reorder_point': ['reorder', 'min_stock', 'safety_stock', 'threshold', 'reorder_point'],
    }
    
    def __init__(self):
        self.detected_columns = {}
        
    def load_csv(self, uploaded_file) -> pd.DataFrame:
        """Load CSV file from Streamlit uploader with automatic encoding detection"""
        encodings = ['utf-8', 'cp1252', 'latin1', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding=encoding)
                return df
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise ValueError(f"Error loading CSV: {str(e)}")
        
        # If all encodings fail
        raise ValueError("Unable to decode CSV file. Please ensure it's a valid CSV file.")
    
    def detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Auto-detect relevant columns using fuzzy matching
        Returns mapping of standard names to actual column names
        """
        detected = {}
        # Clean column names for matching: lowercase, strip whitespace, replace spaces with underscores
        df_columns_clean = {col: col.lower().strip().replace(' ', '_') for col in df.columns}
        
        for standard_name, patterns in self.COLUMN_PATTERNS.items():
            for col, col_clean in df_columns_clean.items():
                for pattern in patterns:
                    # Check for exact match or if pattern is part of the name
                    if pattern == col_clean or pattern in col_clean:
                        detected[standard_name] = col
                        break
                if standard_name in detected:
                    break
        
        self.detected_columns = detected
        return detected
    
    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate inventory metrics if columns are available
        """
        result_df = df.copy()
        cols = self.detected_columns
        
        # Calculate run rate if sales column exists
        if 'sales' in cols and 'stock' in cols:
            sales_col = cols['sales']
            stock_col = cols['stock']
            
            # Fill NaN values with 0 to prevent calculation errors
            result_df[sales_col] = pd.to_numeric(result_df[sales_col], errors='coerce').fillna(0)
            result_df[stock_col] = pd.to_numeric(result_df[stock_col], errors='coerce').fillna(0)
            
            # Assume sales are for 30 days if not specified
            result_df['run_rate'] = result_df[sales_col] / 30
            
            # Calculate days left (avoid division by zero)
            # Use a large number (999) for infinite days when run_rate is 0
            result_df['days_left'] = result_df.apply(
                lambda row: row[stock_col] / row['run_rate'] if row['run_rate'] > 0 else 999.0,
                axis=1
            )
            
            # Calculate estimated restock date
            result_df['restock_date'] = result_df['days_left'].apply(
                lambda days: (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d') if days < 999 else 'N/A'
            )
            
            # Determine urgency level
            result_df['urgency'] = result_df['days_left'].apply(self._calculate_urgency)
        
        return result_df
    
    def _calculate_urgency(self, days_left: float) -> str:
        """Calculate urgency level based on days left"""
        # Centralized constants for urgency thresholds
        CRITICAL_THRESHOLD = 7
        WARNING_THRESHOLD = 30
        MONITOR_THRESHOLD = 60
        
        if days_left < CRITICAL_THRESHOLD:
            return 'CRITICAL'
        elif days_left < WARNING_THRESHOLD:
            return 'WARNING'
        elif days_left < MONITOR_THRESHOLD:
            return 'MONITOR'
        else:
            return 'OK'
    
    def format_for_ai(self, df: pd.DataFrame, max_rows: int = 1000) -> str:
        """
        Convert DataFrame to compact text format for AI processing
        """
        # Limit rows to avoid token overflow
        df_sample = df.head(max_rows).copy()
        
        # Clean data: replace NaN with empty string
        df_sample = df_sample.fillna('')
        
        # Convert to CSV string using pandas (more robust)
        # index=False to exclude row numbers, quoting=None for minimal quotes unless needed
        output = "INVENTORY DATA (CSV Format):\n\n"
        output += df_sample.to_csv(index=False)
        
        # Limit total output size to prevent API issues - increased to 50k chars
        if len(output) > 50000:
            output = output[:50000] + "\n[Data truncated for API compatibility]"
        
        return output
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics"""
        stats = {
            'total_items': len(df),
            'columns_detected': self.detected_columns,
        }
        
        # Add urgency breakdown if available
        if 'urgency' in df.columns:
            stats['urgency_breakdown'] = df['urgency'].value_counts().to_dict()
        
        return stats
