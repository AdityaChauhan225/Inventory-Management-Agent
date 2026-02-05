import { motion } from "framer-motion";

const StatsCard = ({ original, compressed }) => {
    if (!original) return null;

    const saved = original - compressed;
    const percent = original > 0 ? Math.round((saved / original) * 100) : 0;

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-slate-800 p-4 rounded-xl shadow-lg border border-slate-700"
            >
                <h3 className="text-slate-400 text-sm font-medium">Original Tokens</h3>
                <p className="text-2xl font-bold text-white">{original.toLocaleString()}</p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-slate-800 p-4 rounded-xl shadow-lg border border-slate-700"
            >
                <h3 className="text-slate-400 text-sm font-medium">Optimized Tokens</h3>
                <p className="text-2xl font-bold text-blue-400">{compressed.toLocaleString()}</p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="bg-gradient-to-r from-emerald-600 to-teal-600 p-4 rounded-xl shadow-lg"
            >
                <h3 className="text-emerald-100 text-sm font-medium">ScaleDown Savings</h3>
                <div className="flex items-end gap-2">
                    <p className="text-3xl font-bold text-white">{percent}%</p>
                    <span className="text-emerald-100 text-sm mb-1">fewer tokens</span>
                </div>
            </motion.div>
        </div>
    );
};

export default StatsCard;
