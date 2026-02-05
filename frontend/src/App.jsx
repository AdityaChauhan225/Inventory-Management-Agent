import { useState, useEffect } from "react";
import axios from "axios";
import InventoryTable from "./components/InventoryTable";
import ChatInterface from "./components/ChatInterface";
import StatsCard from "./components/StatsCard";

function App() {
  const [products, setProducts] = useState([]);
  const [metrics, setMetrics] = useState({ original_tokens: 0, compressed_tokens: 0 });

  useEffect(() => {
    // Fetch products on mount
    axios.get("http://localhost:8000/api/products")
      .then(res => setProducts(res.data))
      .catch(err => console.error("Failed to fetch products", err));
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 p-6 md:p-12 font-sans selection:bg-blue-500/30">
      <div className="max-w-7xl mx-auto">
        <header className="mb-10 text-center md:text-left">
          <h1 className="text-4xl font-extrabold text-white tracking-tight mb-2">
            Smart Inventory <span className="text-blue-500">Agent</span>
          </h1>
          <p className="text-slate-400">
            Powered by ScaleDown Context Optimization & AI
          </p>
        </header>

        {/* Metrics Section */}
        <StatsCard
          original={metrics.original_tokens}
          compressed={metrics.compressed_tokens}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Inventory Data (2/3 width) */}
          <div className="lg:col-span-2">
            <InventoryTable products={products} />
          </div>

          {/* Right Column: Chat Interface (1/3 width) */}
          <div className="lg:col-span-1">
            <ChatInterface onMetricsUpdate={setMetrics} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
