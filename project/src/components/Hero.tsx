import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { ContractModel } from './ContractModel';
import { motion } from 'framer-motion';
import { SearchCode } from 'lucide-react';

interface HeroProps {
  onGetStarted: () => void;
}

export function Hero({ onGetStarted }: HeroProps) {
  return (
    <div className="relative h-screen bg-gradient-to-b from-indigo-900 to-black overflow-hidden">
      <div className="absolute inset-0">
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <ContractModel />
          <OrbitControls enableZoom={false} />
        </Canvas>
      </div>
      
      <div className="relative z-10 h-full flex items-center justify-center">
        <div className="text-center px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              AI Contract Loophole Detection
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Advanced AI technology to identify and protect against contract vulnerabilities
            </p>
            <div className="flex justify-center gap-4">
              <button 
                onClick={onGetStarted}
                className="bg-indigo-600 text-white px-8 py-3 rounded-lg flex items-center gap-2 hover:bg-indigo-700 transition-colors"
              >
                <SearchCode className="w-5 h-5" />
                Get Started
              </button>
              <button className="border border-white text-white px-8 py-3 rounded-lg hover:bg-white/10 transition-colors">
                Learn More
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}