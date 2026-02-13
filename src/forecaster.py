"""
Demand Forecasting and Report Generation
"""
import pandas as pd
from datetime import datetime
from typing import Dict


class Forecaster:
    """Handles demand forecasting and report generation"""
    
    @staticmethod
    def forecast_demand(df: pd.DataFrame, days_ahead: int = 30) -> pd.DataFrame:
        """
        Simple demand forecasting based on historical run rate
        
        Args:
            df: DataFrame with calculated metrics
            days_ahead: Number of days to forecast
            
        Returns:
            DataFrame with forecast columns added
        """
        forecast_df = df.copy()
        
        if 'run_rate' in forecast_df.columns:
            forecast_df['forecasted_demand'] = forecast_df['run_rate'] * days_ahead
            forecast_df['recommended_order'] = forecast_df.apply(
                lambda row: max(0, row['forecasted_demand'] - row.get('stock', 0))
                if 'stock' in df.columns else 0,
                axis=1
            )
        
        return forecast_df
    
    @staticmethod
    def calculate_restock_urgency(days_left: float) -> int:
        """
        Calculate urgency score (1-10) aligned with DataProcessor thresholds
        """
        if days_left < 7:  # CRITICAL
            return 10
        elif days_left < 14: # High WARNING
            return 8
        elif days_left < 30: # WARNING
            return 6
        elif days_left < 60: # MONITOR
            return 4
        else:
            return 1
    
    @staticmethod
    def format_report(analysis: str, df: pd.DataFrame, stats: Dict) -> str:
        """
        Generate markdown report
        
        Args:
            analysis: AI-generated analysis
            df: Processed DataFrame
            stats: Summary statistics
            
        Returns:
            Markdown-formatted report
        """
        report = f"""# 📦 Inventory Analysis Report
> *Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}*
> **CONFIDENTIAL**

---

## 📊 Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Items** | {stats.get('total_items', 0)} |
| **Columns Detected** | {', '.join(stats.get('columns_detected', {}).keys())} |

"""
        
        # Add urgency breakdown if available
        if 'urgency_breakdown' in stats:
            report += "### Urgency Breakdown\n\n"
            report += "| Status | Count | Status |\n| :--- | :---: | :--- |\n"
            for urgency, count in stats['urgency_breakdown'].items():
                emoji = {
                    'CRITICAL': '🔴',
                    'WARNING': '🟡',
                    'MONITOR': '🟠',
                    'OK': '🟢'
                }.get(urgency, '⚪')
                report += f"| {emoji} **{urgency}** | {count} | {urgency} |\n"
            report += "\n"
        
        # Add AI analysis
        report += f"""---

## 🤖 AI Analysis & Recommendations

{analysis}

---

## 📋 Detailed Actions Required

"""
        
        # Add top items needing attention
        if 'urgency' in df.columns:
            urgent = df[df['urgency'].isin(['CRITICAL', 'WARNING'])].head(15)
            if not urgent.empty:
                report += "### ⚠️ Critical Restock List (Top 15)\n\n"
                # Select only relevant columns for the report to keep it clean
                cols = [c for c in urgent.columns if c in ['sku', 'product_name', 'stock', 'days_left', 'urgency', 'restock_date']]
                if not cols: 
                    cols = urgent.columns
                report += urgent[cols].to_markdown(index=False)
                report += "\n\n"
        
        report += f"""
---

**IMA-V3 Inventory Management System**  
*Forecasts are estimates based on available historical data.*
"""
        
        return report
    
    @staticmethod
    def get_key_metrics(df: pd.DataFrame) -> Dict:
        """Extract key metrics for dashboard display"""
        metrics = {}
        
        if 'urgency' in df.columns:
            metrics['critical_items'] = len(df[df['urgency'] == 'CRITICAL'])
            metrics['warning_items'] = len(df[df['urgency'] == 'WARNING'])
            metrics['total_items'] = len(df)
        
        if 'days_left' in df.columns:
            # Filter out infinite values (999) for average calculation
            valid_days = df[df['days_left'] < 900]['days_left']
            if not valid_days.empty:
                metrics['avg_days_left'] = valid_days.mean()
                metrics['min_days_left'] = valid_days.min()
            else:
                metrics['avg_days_left'] = 0
                metrics['min_days_left'] = 0
        
        if 'stock' in df.columns:
            # Try to find stock column dynamically if 'stock' key isn't standard
            # But DataProcessor standardizes it to 'stock' key in detected_columns
            # heuristic: check for column containing 'stock'
            stock_cols = [c for c in df.columns if 'stock' in c.lower() and 'days' not in c.lower()]
            if stock_cols:
                 metrics['total_stock_value'] = df[stock_cols[0]].sum()
        
        return metrics
