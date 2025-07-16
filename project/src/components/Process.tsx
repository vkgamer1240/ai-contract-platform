import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { PenTool as Token, FileText, BarChart3, Download, MessageCircle } from 'lucide-react';

export function Process() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const steps = [
    {
      icon: Token,
      title: "Access Tokens",
      description: "Get started with free tokens to analyze your first contracts. Premium plans available for more extensive analysis."
    },
    {
      icon: FileText,
      title: "Upload Document",
      description: "Upload your contract in PDF or text format. Our system supports multiple file formats for your convenience."
    },
    {
      icon: BarChart3,
      title: "AI Analysis",
      description: "Our advanced AI performs deep analysis, identifying potential risks, loopholes, and areas of concern."
    },
    {
      icon: Download,
      title: "Download Report",
      description: "Receive a comprehensive report detailing all findings, risk assessments, and recommended actions."
    },
    {
      icon: MessageCircle,
      title: "Expert Consultation",
      description: "Use your free tokens to consult with legal experts about specific concerns identified in the analysis."
    }
  ];

  return (
    <section id="process" className="py-24 bg-gradient-to-b from-indigo-900 to-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-white mb-4">How It Works</h2>
          <p className="text-xl text-gray-300">Simple steps to secure your contracts</p>
        </motion.div>

        <div className="relative">
          <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-indigo-500/30" />
          
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className={`relative flex items-center gap-8 mb-12 ${
                index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'
              }`}
            >
              <div className={`flex-1 ${index % 2 === 0 ? 'text-right' : 'text-left'}`}>
                <h3 className="text-2xl font-bold text-white mb-2">{step.title}</h3>
                <p className="text-gray-300">{step.description}</p>
              </div>
              
              <div className="relative z-10 flex items-center justify-center w-16 h-16 bg-indigo-600 rounded-full">
                <step.icon className="w-8 h-8 text-white" />
              </div>
              
              <div className="flex-1" />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}