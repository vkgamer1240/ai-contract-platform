import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

export function Benefits() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const benefits = [
    {
      title: "Risk Mitigation",
      description: "Identify and address potential legal risks before they become problems. Our AI system thoroughly analyzes contract language to spot potential loopholes and vulnerabilities.",
      image: "/Screenshot 2025-06-04 161437.png"
    },
    {
      title: "Time Efficiency",
      description: "Reduce contract review time by up to 90% with our automated AI analysis system. Focus on strategic decisions while our AI handles the detailed review process.",
      image: "/Screenshot 2025-06-04 161450.png"
    },
    {
      title: "Cost Reduction",
      description: "Minimize legal expenses and potential litigation costs by identifying and addressing contract issues early. Our AI helps prevent costly disputes before they arise.",
      image: "/Screenshot 2025-06-04 161503.png"
    }
  ];

  return (
    <section className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => (
            <motion.div
              key={index}
              ref={ref}
              initial={{ opacity: 0, y: 50 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{
                duration: 0.7,
                delay: index * 0.2,
                ease: [0.21, 0.45, 0.32, 0.9]
              }}
              className="relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-b from-indigo-600/20 to-black/20 rounded-xl transform group-hover:scale-105 transition-transform duration-500 ease-out" />
              <div className="relative bg-gradient-to-b from-indigo-900/50 to-black/50 rounded-xl p-6 backdrop-blur-sm transform transition-transform duration-500 ease-out">
                <div className="aspect-video mb-6 overflow-hidden rounded-lg">
                  <motion.img
                    src={benefit.image}
                    alt={benefit.title}
                    className="w-full h-full object-cover"
                    loading="lazy"
                    initial={{ scale: 1.2 }}
                    animate={inView ? { scale: 1 } : {}}
                    transition={{
                      duration: 1.2,
                      delay: index * 0.2,
                      ease: [0.21, 0.45, 0.32, 0.9]
                    }}
                  />
                </div>
                <motion.h3 
                  className="text-2xl font-bold text-white mb-4"
                  initial={{ opacity: 0, x: -20 }}
                  animate={inView ? { opacity: 1, x: 0 } : {}}
                  transition={{
                    duration: 0.7,
                    delay: 0.3 + index * 0.2,
                    ease: [0.21, 0.45, 0.32, 0.9]
                  }}
                >
                  {benefit.title}
                </motion.h3>
                <motion.p 
                  className="text-gray-300"
                  initial={{ opacity: 0 }}
                  animate={inView ? { opacity: 1 } : {}}
                  transition={{
                    duration: 0.7,
                    delay: 0.5 + index * 0.2,
                    ease: [0.21, 0.45, 0.32, 0.9]
                  }}
                >
                  {benefit.description}
                </motion.p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}