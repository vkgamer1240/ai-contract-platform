# Security Configuration Guide

## 🔐 Protecting Your API Keys and Sensitive Data

### Important Security Measures

1. **Never commit API keys to GitHub**
   - All API keys should be stored in environment variables
   - Use the `.env.template` file as a guide
   - Create your own `.env` file locally (it's in .gitignore)

2. **Environment Variables Setup**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env with your actual API keys
   nano .env  # or use your preferred editor
   ```

3. **Groq API Key Setup**
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Add it to your `.env` file:
     ```
     GROQ_API_KEY=gsk_your_actual_key_here
     ```

4. **Deployment Environment Variables**
   
   **For Vercel:**
   - Go to your Vercel project dashboard
   - Navigate to Settings → Environment Variables
   - Add your API keys there (they won't be visible in your code)
   
   **For other platforms:**
   - Use the platform's environment variable configuration
   - Never expose keys in your code or config files

### What's Protected

The `.gitignore` file protects:
- ✅ `.env` files (all variants)
- ✅ Large model files (`*.bin`, `*.pt`)
- ✅ API keys and secrets
- ✅ Node modules and build artifacts
- ✅ System files and caches

### Checklist Before Pushing to GitHub

- [ ] All API keys are in environment variables
- [ ] `.env` file exists locally but is NOT committed
- [ ] `.env.template` is committed (without actual keys)
- [ ] Large model files are in .gitignore
- [ ] No hardcoded secrets in Python files

### If You Accidentally Committed Secrets

1. **Immediately revoke the exposed API keys**
2. **Remove the secrets from Git history:**
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path/to/file' --prune-empty --tag-name-filter cat -- --all
   ```
3. **Generate new API keys**
4. **Force push the cleaned repository**

### Production Deployment Notes

- Use environment variables in production
- Enable 2FA on all accounts
- Regularly rotate API keys
- Monitor API key usage
- Use least-privilege access principles
