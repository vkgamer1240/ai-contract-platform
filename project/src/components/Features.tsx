import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { Shield, Brain, Zap, AlertTriangle } from 'lucide-react';

export function Features() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const features = [
    {
      icon: Shield,
      title: "Advanced Protection",
      description: "Our AI system provides comprehensive protection against potential contract vulnerabilities and loopholes."
    },
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "State-of-the-art machine learning algorithms analyze contracts for potential risks and ambiguities."
    },
    {
      icon: Zap,
      title: "Real-time Detection",
      description: "Instant identification of problematic clauses and potential legal exposure in your contracts."
    },
    {
      icon: AlertTriangle,
      title: "Risk Assessment",
      description: "Detailed risk scoring and analysis of each contract section with actionable insights."
    }
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-black to-indigo-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-white mb-4">
            Powerful Features for Contract Analysis
          </h2>
          <p className="text-xl text-gray-300">
            Leverage AI technology to protect your business interests
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-white"
            >
              <div className="h-12 w-12 text-indigo-400 mb-4">
                <feature.icon size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-300">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}