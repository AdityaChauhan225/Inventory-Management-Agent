import { useState } from "react";
import axios from "axios";
import { Send, Loader2, Cpu } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const ChatInterface = ({ onMetricsUpdate }) => {
    const [query, setQuery] = useState("");
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hello! I am your AI Inventory Assistant provided by ScaleDown. How can I help you optimize your stock today?" }
    ]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        const userMsg = { role: "user", content: query };
        setMessages((prev) => [...prev, userMsg]);
        setQuery("");
        setLoading(true);

        try {
            // Assuming backend is running on port 8000
            const res = await axios.post("http://localhost:8000/api/ask", { query: query });

            const aiResponse = res.data.answer;
            setMessages((prev) => [...prev, { role: "assistant", content: aiResponse }]);

            if (res.data.metrics && onMetricsUpdate) {
                onMetricsUpdate(res.data.metrics);
            }
        } catch (err) {
            setMessages((prev) => [...prev, { role: "assistant", content: "Error: Could not reach the inventory backend." }]);
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[600px] bg-slate-800 rounded-xl shadow-xl border border-slate-700 overflow-hidden">
            <div className="p-4 border-b border-slate-700 bg-slate-900 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                    <Cpu className="text-blue-500" size={20} />
                    AI Assistant
                </h2>
                <span className="text-xs text-slate-500">Powered by ScaleDown API</span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        key={idx}
                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[80%] p-3 rounded-lg text-sm leading-relaxed whitespace-pre-wrap ${msg.role === "user"
                                    ? "bg-blue-600 text-white rounded-br-none"
                                    : "bg-slate-700 text-slate-200 rounded-bl-none"
                                }`}
                        >
                            {msg.content}
                        </div>
                    </motion.div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-slate-700 p-3 rounded-lg rounded-bl-none flex items-center gap-2">
                            <Loader2 className="animate-spin text-blue-400" size={16} />
                            <span className="text-slate-400 text-xs">Analyzing & Compressing Context...</span>
                        </div>
                    </div>
                )}
            </div>

            <div className="p-4 bg-slate-900 border-t border-slate-700">
                <form onSubmit={handleSubmit} className="flex gap-2">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Ask about inventory (e.g. 'What items need restocking?')..."
                        className="flex-1 bg-slate-800 border border-slate-700 text-white text-sm rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors placeholder-slate-500"
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-500 text-white p-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;
