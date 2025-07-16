import { motion } from 'framer-motion';
import { FileText, MessageCircle, ArrowRight, Shield, Brain, PenTool, Edit3, Users } from 'lucide-react';

interface ServiceSelectionProps {
  onClose: () => void;
  onSelectContractAnalysis: () => void;
  onSelectEducationBot: () => void;
  onSelectContractCreation?: () => void;
}

export function ServiceSelection({ onClose, onSelectContractAnalysis, onSelectEducationBot, onSelectContractCreation }: ServiceSelectionProps) {
  
  const handleContractCreation = () => {
    // Redirect to contract creation page
    window.location.href = '/contract-creation';
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="bg-gradient-to-br from-gray-900 to-black p-8 rounded-xl max-w-6xl w-full border border-gray-700"
      >
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-4">
            Welcome to AI Contract Analysis
          </h2>
          <p className="text-gray-300 text-lg">
            Choose your service to get started with AI-powered contract analysis
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Contract Creation Card */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleContractCreation}
            className="bg-gradient-to-br from-orange-600 to-red-600 p-6 rounded-lg cursor-pointer border border-orange-500 hover:border-orange-400 transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <Edit3 className="w-8 h-8 text-white" />
              </div>
              <ArrowRight className="w-6 h-6 text-white/70" />
            </div>
            
            <h3 className="text-xl font-bold text-white mb-3">
              Contract Creation
            </h3>
            
            <p className="text-orange-100 mb-4">
              Generate professional contracts using YOUR fine-tuned RoBERTa model combined with Groq AI for optimal results.
            </p>
            
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-orange-100">
                <Edit3 className="w-4 h-4" />
                <span className="text-sm">AI-Powered Generation</span>
              </div>
              <div className="flex items-center gap-2 text-orange-100">
                <Brain className="w-4 h-4" />
                <span className="text-sm">RoBERTa + Groq Integration</span>
              </div>
              <div className="flex items-center gap-2 text-orange-100">
                <Shield className="w-4 h-4" />
                <span className="text-sm">Legal Structure & Risk Analysis</span>
              </div>
            </div>
            
            <div className="mt-4 bg-white/10 p-3 rounded">
              <p className="text-white font-semibold text-sm">Perfect for:</p>
              <p className="text-orange-100 text-sm">Businesses, legal professionals, startups</p>
            </div>
          </motion.div>

          {/* Contract Analysis Card */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onSelectContractAnalysis}
            className="bg-gradient-to-br from-indigo-600 to-purple-600 p-6 rounded-lg cursor-pointer border border-indigo-500 hover:border-indigo-400 transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <FileText className="w-8 h-8 text-white" />
              </div>
              <ArrowRight className="w-6 h-6 text-white/70" />
            </div>
            
            <h3 className="text-xl font-bold text-white mb-3">
              Contract Analysis
            </h3>
            
            <p className="text-indigo-100 mb-4">
              Advanced AI-powered contract analysis with risk assessment, compliance checking, and detailed insights.
            </p>
            
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-indigo-100">
                <Shield className="w-4 h-4" />
                <span className="text-sm">Risk Assessment & Scoring</span>
              </div>
              <div className="flex items-center gap-2 text-indigo-100">
                <Brain className="w-4 h-4" />
                <span className="text-sm">CUAD + Groq AI Analysis</span>
              </div>
              <div className="flex items-center gap-2 text-indigo-100">
                <FileText className="w-4 h-4" />
                <span className="text-sm">Batch Processing & Comparison</span>
              </div>
            </div>
            
            <div className="mt-4 bg-white/10 p-3 rounded">
              <p className="text-white font-semibold text-sm">Perfect for:</p>
              <p className="text-indigo-100 text-sm">Legal professionals, businesses, app developers</p>
            </div>
          </motion.div>

          {/* Education Chatbot Card */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onSelectEducationBot}
            className="bg-gradient-to-br from-emerald-600 to-teal-600 p-6 rounded-lg cursor-pointer border border-emerald-500 hover:border-emerald-400 transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <MessageCircle className="w-8 h-8 text-white" />
              </div>
              <ArrowRight className="w-6 h-6 text-white/70" />
            </div>
            
            <h3 className="text-xl font-bold text-white mb-3">
              Education for All
            </h3>
            
            <p className="text-emerald-100 mb-4">
              Interactive AI chatbot to learn about contracts, legal terms, and get educational guidance.
            </p>
            
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-emerald-100">
                <MessageCircle className="w-4 h-4" />
                <span className="text-sm">Interactive Learning</span>
              </div>
              <div className="flex items-center gap-2 text-emerald-100">
                <Brain className="w-4 h-4" />
                <span className="text-sm">Contract Law Education</span>
              </div>
              <div className="flex items-center gap-2 text-emerald-100">
                <FileText className="w-4 h-4" />
                <span className="text-sm">Legal Term Explanations</span>
              </div>
            </div>
            
            <div className="mt-4 bg-white/10 p-3 rounded">
              <p className="text-white font-semibold text-sm">Perfect for:</p>
              <p className="text-emerald-100 text-sm">Students, beginners, anyone learning about contracts</p>
            </div>
          </motion.div>
        </div>

        <div className="flex justify-center mt-8">
          <button
            onClick={onClose}
            className="px-6 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
        </div>
      </motion.div>
    </div>
  );
}
