import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, ArrowLeft, CheckCircle, AlertCircle } from 'lucide-react';

interface ContractAnalysisLauncherProps {
  onBack: () => void;
}

export function ContractAnalysisLauncher({ onBack }: ContractAnalysisLauncherProps) {
  const [isLaunching, setIsLaunching] = useState(false);
  const [serverStatus, setServerStatus] = useState<'checking' | 'ready' | 'starting' | 'error'>('checking');
  const [launchUrl, setLaunchUrl] = useState<string>('');

  useEffect(() => {
    checkServerStatus();
  }, []);

  const checkServerStatus = async () => {
    try {
      const response = await fetch('/api/health_check');
      if (response.ok) {
        setServerStatus('ready');
        setLaunchUrl('/contract-analysis');
      } else {
        setServerStatus('starting');
        startContractAnalysisServer();
      }
    } catch (error) {
      setServerStatus('starting');
      startContractAnalysisServer();
    }
  };

  const startContractAnalysisServer = async () => {
    try {
      // Server is already running on same port, just need to wait a moment
      setTimeout(() => {
        setServerStatus('ready');
        setLaunchUrl('/contract-analysis');
      }, 2000);
    } catch (error) {
      setServerStatus('error');
    }
  };

  const handleLaunchApp = () => {
    setIsLaunching(true);
    // Navigate to contract analysis page on same server
    window.location.href = launchUrl;
    setTimeout(() => setIsLaunching(false), 1000);
  };

  const StatusIcon = () => {
    switch (serverStatus) {
      case 'checking':
      case 'starting':
        return <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />;
      case 'ready':
        return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-6 h-6 text-red-500" />;
    }
  };

  const getStatusMessage = () => {
    switch (serverStatus) {
      case 'checking':
        return 'Checking server status...';
      case 'starting':
        return 'Starting Contract Analysis Server...';
      case 'ready':
        return 'Contract Analysis Server is ready!';
      case 'error':
        return 'Error starting server. Please try again.';
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="bg-gradient-to-br from-gray-900 to-black p-8 rounded-xl max-w-2xl w-full border border-gray-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <button
            onClick={onBack}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-gray-400" />
          </button>
          <h2 className="text-2xl font-bold text-white">
            Premium Contract Analysis Platform
          </h2>
        </div>

        <div className="text-center mb-8">
          <div className="bg-gradient-to-br from-indigo-600 to-purple-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
            <StatusIcon />
          </div>
          
          <h3 className="text-xl font-semibold text-white mb-2">
            {getStatusMessage()}
          </h3>
          
          <p className="text-gray-300">
            Advanced AI-powered contract analysis with CUAD + Groq integration
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="bg-gray-800/50 p-4 rounded-lg">
            <h4 className="text-white font-semibold mb-2">🚀 Features Available:</h4>
            <ul className="text-gray-300 space-y-1 text-sm">
              <li>• Single Contract Analysis with Risk Scoring</li>
              <li>• Batch Processing for Multiple Contracts</li>
              <li>• Contract Comparison and Recommendations</li>
              <li>• App Store Compliance Checking</li>
              <li>• Advanced Risk Assessment with AI Insights</li>
            </ul>
          </div>

          <div className="bg-gray-800/50 p-4 rounded-lg">
            <h4 className="text-white font-semibold mb-2">🤖 AI Technologies:</h4>
            <ul className="text-gray-300 space-y-1 text-sm">
              <li>• CUAD (Contract Understanding Attentive Dataset)</li>
              <li>• Groq API for Advanced Analysis</li>
              <li>• Multi-Model Validation</li>
              <li>• Specialized Contract Type Detection</li>
            </ul>
          </div>
        </div>

        <div className="flex gap-4">
          {serverStatus === 'ready' ? (
            <button
              onClick={handleLaunchApp}
              disabled={isLaunching}
              className="flex-1 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg flex items-center justify-center gap-2 hover:from-indigo-700 hover:to-purple-700 transition-all disabled:opacity-50"
            >
              <ExternalLink className="w-5 h-5" />
              {isLaunching ? 'Launching...' : 'Launch Contract Analysis Platform'}
            </button>
          ) : serverStatus === 'error' ? (
            <button
              onClick={startContractAnalysisServer}
              className="flex-1 bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry
            </button>
          ) : (
            <div className="flex-1 bg-gray-600 text-white px-6 py-3 rounded-lg text-center">
              Please wait...
            </div>
          )}
          
          <button
            onClick={onBack}
            className="px-6 py-3 text-gray-400 hover:text-white transition-colors"
          >
            Back
          </button>
        </div>

        {serverStatus === 'ready' && (
          <div className="mt-4 p-3 bg-green-900/20 border border-green-500/30 rounded-lg">
            <p className="text-green-400 text-sm text-center">
              ✅ Server is running at {launchUrl}
            </p>
          </div>
        )}
      </motion.div>
    </div>
  );
}
