import { useState } from 'react';
import { Menu, X, FileText } from 'lucide-react';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed w-full z-50 bg-black/80 backdrop-blur-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-indigo-500" />
            <span className="ml-2 text-xl font-bold text-white">ContractAI</span>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <a href="#features" className="text-gray-300 hover:text-white px-3 py-2">Features</a>
              <a href="#process" className="text-gray-300 hover:text-white px-3 py-2">How it Works</a>
              <a href="#benefits" className="text-gray-300 hover:text-white px-3 py-2">Benefits</a>
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                Get Started
              </button>
            </div>
          </div>
          
          <div className="md:hidden">
            <button onClick={() => setIsOpen(!isOpen)} className="text-gray-300">
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
        
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <a href="#features" className="text-gray-300 hover:text-white block px-3 py-2">Features</a>
              <a href="#process" className="text-gray-300 hover:text-white block px-3 py-2">How it Works</a>
              <a href="#benefits" className="text-gray-300 hover:text-white block px-3 py-2">Benefits</a>
              <button className="w-full bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                Get Started
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}