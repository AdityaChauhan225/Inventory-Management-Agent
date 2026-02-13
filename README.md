# IMA-V3 - Inventory Management & AI Forecasting

A minimalistic inventory management system powered by AI for demand forecasting and intelligent restock recommendations.

## 🌟 Features

- **📊 Flexible CSV Upload**: Works with any CSV format - intelligent column detection
- **🤖 AI-Powered Analysis**: Uses Ollama (glm5:cloud) for insights
- **⚡ Smart Compression**: ScaleDown API integration for efficient token usage
- **📈 Demand Forecasting**: Automatic calculation of run rates and restock dates
- **⚠️ Urgency Detection**: Automatic prioritization of critical items
- **📥 Export Reports**: Download detailed markdown reports and processed CSV

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed and running
- (Optional) ScaleDown API key

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "e:\code\GENAI ScaleDown\IMA-V3"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OLLAMA_API_BASE=http://localhost:11434
   OLLAMA_MODEL=glm5:cloud
   SCALEDOWN_API_KEY=your_api_key_here
   ```

4. **Ensure Ollama is running**
   ```bash
   ollama serve
   ```

5. **Pull the required model**
   ```bash
   ollama pull glm5:cloud
   ```

## 🎯 Usage

### Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Upload Your CSV

1. Click "Browse files" to upload your inventory CSV
2. The system will automatically detect relevant columns (stock, sales, product names, etc.)
3. View the data preview and detected column mappings
4. Click "Generate AI Analysis" for insights
5. Download reports in Markdown or CSV format

### CSV Format

Your CSV can have any structure! The system intelligently detects columns like:

- **Product identifiers**: sku, id, product_id, code
- **Product names**: name, product, item, description
- **Stock levels**: stock, quantity, qty, inventory, available
- **Sales data**: sales, sold, units_sold, demand
- **Reorder points**: reorder, min_stock, safety_stock

Example CSV:
```csv
SKU,Product Name,Stock Qty,Sales (30 Days),Reorder Point
SKU001,Widget A,150,60,50
SKU002,Gadget B,25,112,40
```

## 📋 System Architecture

```
IMA-V3/
├── src/
│   ├── data_processor.py      # Flexible CSV loading & column detection
│   ├── scaledown_client.py    # ScaleDown API integration
│   ├── ollama_agent.py        # Ollama AI agent
│   └── forecaster.py          # Demand forecasting & reporting
├── app.py                     # Streamlit application
├── requirements.txt           # Python dependencies
└── .env                       # Environment configuration
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OLLAMA_API_BASE` | Ollama API endpoint | `http://localhost:11434` | Yes |
| `OLLAMA_MODEL` | Ollama model to use | `glm5:cloud` | Yes |
| `SCALEDOWN_API_KEY` | ScaleDown API key | - | No* |

*ScaleDown is optional - the system will work without it using uncompressed prompts

### Ollama Models

If `glm5:cloud` is not available, you can use alternatives:
```bash
# Use a different model
ollama pull llama3
```

Then update your `.env`:
```env
OLLAMA_MODEL=llama3
```

## 📊 How It Works

1. **CSV Upload**: User uploads any inventory CSV file
2. **Column Detection**: System auto-detects relevant columns using pattern matching
3. **Metric Calculation**: Computes run rates, days left, restock dates, urgency levels
4. **Compression**: (Optional) ScaleDown API compresses data for token efficiency
5. **AI Analysis**: Ollama analyzes compressed data and generates insights
6. **Reporting**: System generates downloadable reports with recommendations

## 🛠️ Troubleshooting

### Ollama Connection Error

**Problem**: `Error communicating with Ollama`

**Solutions**:
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_API_BASE` in `.env` matches your Ollama instance
- Verify the model is installed: `ollama list`

### Model Not Found

**Problem**: Model 'glm5:cloud' not found

**Solutions**:
- Pull the model: `ollama pull glm5:cloud`
- Or use an alternative model (see Configuration section)

### ScaleDown API Error

**Problem**: ScaleDown API fails

**Solution**: The system automatically falls back to using uncompressed data. Set `SCALEDOWN_API_KEY` in `.env` if you have an API key.

### CSV Loading Error

**Problem**: Error loading CSV

**Solutions**:
- Ensure CSV is properly formatted (no corrupted data)
- Check encoding (should be UTF-8)
- Verify file has at least one column

## 📝 Example Workflow

1. **Start the app**: `streamlit run app.py`
2. **Upload CSV**: Click "Browse files" and select your inventory CSV
3. **Review Detection**: Check that columns were detected correctly
4. **View Metrics**: See urgency levels (Critical/Warning/Monitor/OK)
5. **Get AI Insights**: Click "Generate AI Analysis"
6. **Export**: Download the markdown report or processed CSV

## 🎨 Design Philosophy

**Minimalistic**: Clean, focused UI with only essential features
**Flexible**: Works with any CSV structure
**Intelligent**: Auto-detects columns and calculates metrics
**Actionable**: Provides clear, prioritized recommendations

## 📄 License

This project is part of an internship assignment demonstrating ScaleDown API integration.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review your `.env` configuration
3. Ensure Ollama is running and model is available

---

**Built with**: Python • Streamlit • Ollama • ScaleDown API
