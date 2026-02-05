import { motion } from "framer-motion";

const InventoryTable = ({ products }) => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-slate-800 rounded-xl shadow-xl overflow-hidden border border-slate-700 mb-6"
        >
            <div className="p-4 border-b border-slate-700">
                <h2 className="text-lg font-semibold text-white">Live Inventory</h2>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-slate-300">
                    <thead className="bg-slate-900 text-xs uppercase text-slate-400">
                        <tr>
                            <th className="px-6 py-3">Product Name</th>
                            <th className="px-6 py-3">SKU</th>
                            <th className="px-6 py-3">Category</th>
                            <th className="px-6 py-3 text-right">Stock</th>
                            <th className="px-6 py-3 text-right">Reorder Pt</th>
                            <th className="px-6 py-3">Supplier</th>
                            <th className="px-6 py-3 text-center">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                        {products.map((product) => (
                            <tr key={product.product_id} className="hover:bg-slate-700/50 transition-colors">
                                <td className="px-6 py-4 font-medium text-white">{product.name}</td>
                                <td className="px-6 py-4">{product.sku}</td>
                                <td className="px-6 py-4">
                                    <span className="px-2 py-1 rounded-full text-xs font-semibold bg-slate-700 text-slate-300">
                                        {product.category}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right font-mono">{product.stock_level}</td>
                                <td className="px-6 py-4 text-right font-mono text-slate-500">{product.reorder_point}</td>
                                <td className="px-6 py-4">{product.supplier_name}</td>
                                <td className="px-6 py-4 text-center">
                                    {product.stock_level <= product.reorder_point ? (
                                        <span className="text-rose-400 font-bold text-xs flex items-center justify-center gap-1">
                                            ⚠️ Low Stock
                                        </span>
                                    ) : (
                                        <span className="text-emerald-400 font-bold text-xs">Ok</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                        {products.length === 0 && (
                            <tr>
                                <td colSpan="7" className="px-6 py-8 text-center text-slate-500">
                                    No products found in database.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </motion.div>
    );
};

export default InventoryTable;
