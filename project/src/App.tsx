import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { Features } from './components/Features';
import { Process } from './components/Process';
import { Benefits } from './components/Benefits';
import { Footer } from './components/Footer';
import { LoginModal } from './components/LoginModal';
import { Chatbot } from './components/Chatbot';
import { ServiceSelection } from './components/ServiceSelection';
import { ContractAnalysisLauncher } from './components/ContractAnalysisLauncher';
import { Dashboard } from './pages/Dashboard';
import { authService } from './lib/auth';

function App() {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showChatbot, setShowChatbot] = useState(false);
  const [showServiceSelection, setShowServiceSelection] = useState(false);
  const [showContractAnalysis, setShowContractAnalysis] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const user = authService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
      setIsAuthenticated(true);
    }
  }, []);

  const handleGetStarted = () => {
    if (isAuthenticated) {
      setShowServiceSelection(true);
    } else {
      setShowLoginModal(true);
    }
  };

  const handleLogin = async (email: string, password: string) => {
    const result = await authService.login(email, password);
    if (result.success && result.user) {
      setCurrentUser(result.user);
      setIsAuthenticated(true);
      setShowLoginModal(false);
      setShowServiceSelection(true);
    } else {
      alert(result.message);
    }
  };

  const handleSignup = async (email: string, password: string, name: string) => {
    const result = await authService.signup(name, email, password);
    if (result.success) {
      alert('Account created successfully! Please login.');
    } else {
      alert(result.message);
    }
  };

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthenticated(false);
    setShowChatbot(false);
    setShowServiceSelection(false);
    setShowContractAnalysis(false);
  };

  const handleSelectContractAnalysis = () => {
    setShowServiceSelection(false);
    setShowContractAnalysis(true);
  };

  const handleSelectEducationBot = () => {
    setShowServiceSelection(false);
    setShowChatbot(true);
  };

  const handleBackToServiceSelection = () => {
    setShowContractAnalysis(false);
    setShowChatbot(false);
    setShowServiceSelection(true);
  };

  const handleCloseServiceSelection = () => {
    setShowServiceSelection(false);
  };

  if (isAuthenticated && showChatbot) {
    return (
      <Dashboard user={currentUser} onLogout={handleLogout} />
    );
  }

  return (
    <div className="bg-black">
      <Navbar />
      <Hero onGetStarted={handleGetStarted} />
      <Features />
      <Process />
      <Benefits />
      <Footer />
      
      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLogin={handleLogin}
        onSignup={handleSignup}
      />
      
      {showServiceSelection && (
        <ServiceSelection
          onClose={handleCloseServiceSelection}
          onSelectContractAnalysis={handleSelectContractAnalysis}
          onSelectEducationBot={handleSelectEducationBot}
        />
      )}
      
      {showContractAnalysis && (
        <ContractAnalysisLauncher
          onBack={handleBackToServiceSelection}
        />
      )}
      
      <Chatbot
        isOpen={showChatbot}
        onClose={() => setShowChatbot(false)}
      />
    </div>
  );
}

export default App;