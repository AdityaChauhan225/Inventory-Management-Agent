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
    
    def format_for_ai(self, df: pd.DataFrame, max_chars: int = 15000) -> str:
        """
        Convert DataFrame to compact text format for AI processing.
        Prioritizes Critical/Warning items and includes a summary.
        """
        # 1. Create a high-level summary
        total_items = len(df)
        urgency_counts = df['urgency'].value_counts().to_dict() if 'urgency' in df.columns else {}
        
        summary = f"""
INVENTORY SUMMARY:
- Total Items: {total_items}
- Critical Items (Restock Now): {urgency_counts.get('CRITICAL', 0)}
- Warning Items (Monitor): {urgency_counts.get('WARNING', 0)}
- OK Items: {urgency_counts.get('OK', 0)}
"""

        # 2. Filter and Prioritize Data
        # We want to send ALL Critical and Warning items, but only a sample of others if space permits.
        
        if 'urgency' in df.columns:
            # Split dataframe
            critical_df = df[df['urgency'] == 'CRITICAL'].copy()
            warning_df = df[df['urgency'] == 'WARNING'].copy()
            other_df = df[~df['urgency'].isin(['CRITICAL', 'WARNING'])].copy()
            
            # Combine back with priority
            # Critical -> Warning -> Others
            prioritized_df = pd.concat([critical_df, warning_df, other_df])
        else:
            prioritized_df = df.copy()
            
        # 3. Trim Columns
        # Keep only essential columns to save tokens
        essential_cols = []
        for col_type in ['sku', 'product_name', 'stock', 'sales', 'days_left', 'urgency']:
            if col_type in self.detected_columns:
                essential_cols.append(self.detected_columns[col_type])
            elif col_type in prioritized_df.columns: # fallback if column name is standard
                 essential_cols.append(col_type)
                 
        # If we found essential columns, use only those. Otherwise use all.
        if len(essential_cols) >= 3:
            export_df = prioritized_df[essential_cols]
        else:
            export_df = prioritized_df

        # 4. Convert to CSV string until limit is reached
        csv_string = export_df.to_csv(index=False)
        
        # 5. Construct Final Prompt
        final_output = summary + "\nDETAILED DATA (Sorted by Urgency):\n" + csv_string
        
        # 6. Strict Length Limiting
        if len(final_output) > max_chars:
            final_output = final_output[:max_chars] + "\n... [Data Truncated for Speed] ..."
            
        return final_output
    
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
