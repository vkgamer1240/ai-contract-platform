"""
WhatsApp Integration for Contract Sharing
=========================================
This module provides functionality to send generated contracts via WhatsApp
"""
import os
import tempfile
import qrcode
from datetime import datetime, timedelta
from typing import Dict, Optional
import io
import base64

class WhatsAppContractSender:
    def __init__(self):
        """Initialize WhatsApp contract sender"""
        self.available = True
        
    def create_contract_message(self, contract_data: Dict, recipient_name: str = "Client") -> str:
        """Create a formatted WhatsApp message with contract details"""
        
        contract_name = contract_data.get('parameters', {}).get('company_a', 'Service Provider')
        client_name = contract_data.get('parameters', {}).get('company_b', 'Client')
        services = contract_data.get('parameters', {}).get('services', 'Professional Services')
        
        # Risk analysis summary
        risk_analysis = contract_data.get('risk_analysis', {}).get('risk_analysis', {})
        risk_score = risk_analysis.get('risk_score', 'N/A')
        risk_level = risk_analysis.get('overall_risk', 'MEDIUM')
        
        message = f"""📄 *CONTRACT READY FOR REVIEW*

🤝 *Service Agreement*
📋 From: {contract_name}
👤 To: {client_name}
🔧 Services: {services}

🤖 *AI Analysis Summary:*
📊 Risk Score: {risk_score}/100
⚠️ Risk Level: {risk_level}
🧠 Generated by: AI Contract Platform

📱 *Next Steps:*
1. Review the contract document
2. Check all terms and conditions  
3. Contact us for any modifications
4. Sign when ready to proceed

⚡ Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Need help? Reply to this message! 💬"""
        
        return message
    
    def create_whatsapp_web_url(self, phone_number: str, message: str) -> str:
        """Create WhatsApp Web URL for sending message"""
        # Clean phone number (remove spaces, dashes, etc.)
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        # Add country code if not present (assuming +1 for US/Canada)
        if len(clean_phone) == 10:
            clean_phone = '1' + clean_phone
        elif len(clean_phone) == 11 and clean_phone[0] == '1':
            pass  # Already has country code
        
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        # Create WhatsApp Web URL
        whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_message}"
        
        return whatsapp_url
    
    def generate_qr_code(self, whatsapp_url: str) -> str:
        """Generate QR code for WhatsApp URL and return as base64 string"""
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(whatsapp_url)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 string
            buffer = io.BytesIO()
            qr_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{qr_base64}"
            
        except Exception as e:
            print(f"QR code generation failed: {str(e)}")
            return None
    
    def create_contract_sharing_options(self, contract_data: Dict, recipient_info: Dict) -> Dict:
        """Create multiple sharing options for the contract"""
        
        phone_number = recipient_info.get('phone', '')
        recipient_name = recipient_info.get('name', 'Client')
        
        # Create WhatsApp message
        message = self.create_contract_message(contract_data, recipient_name)
        
        # Create WhatsApp Web URL
        whatsapp_url = self.create_whatsapp_web_url(phone_number, message)
        
        # Generate QR code
        qr_code = self.generate_qr_code(whatsapp_url)
        
        # Create download link for contract
        contract_text = contract_data.get('contract', '')
        contract_filename = f"contract_{contract_data.get('parameters', {}).get('company_a', 'service')}_{datetime.now().strftime('%Y%m%d')}.txt"
        
        return {
            'whatsapp_url': whatsapp_url,
            'qr_code': qr_code,
            'message': message,
            'contract_filename': contract_filename,
            'recipient_name': recipient_name,
            'phone_number': phone_number,
            'sharing_options': {
                'whatsapp_web': {
                    'title': 'Send via WhatsApp Web',
                    'description': 'Opens WhatsApp Web with pre-filled message',
                    'url': whatsapp_url,
                    'icon': '💬'
                },
                'qr_code': {
                    'title': 'Scan QR Code',
                    'description': 'Scan with phone to open WhatsApp',
                    'qr_data': qr_code,
                    'icon': '📱'
                },
                'copy_message': {
                    'title': 'Copy Message',
                    'description': 'Copy message to send manually',
                    'message': message,
                    'icon': '📋'
                }
            }
        }
    
    def create_contract_file(self, contract_data: Dict) -> str:
        """Create a temporary contract file and return the path"""
        try:
            contract_text = contract_data.get('contract', '')
            contract_params = contract_data.get('parameters', {})
            
            # Create formatted contract content
            formatted_content = f"""
CONTRACT AGREEMENT
==================

Service Provider: {contract_params.get('company_a', 'N/A')}
Client: {contract_params.get('company_b', 'N/A')}
Services: {contract_params.get('services', 'N/A')}
Duration: {contract_params.get('duration', 'N/A')}
Payment Terms: {contract_params.get('payment_terms', 'N/A')}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
AI Model: {contract_data.get('generation_engine', 'AI System')}

CONTRACT DOCUMENT:
==================

{contract_text}

---
Generated by AI Contract Platform
Risk Analysis Included
"""
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(formatted_content)
                return f.name
                
        except Exception as e:
            print(f"Contract file creation failed: {str(e)}")
            return None

# Advanced WhatsApp integration using pywhatkit (for scheduled sending)
class AdvancedWhatsAppSender:
    def __init__(self):
        """Initialize advanced WhatsApp sender with pywhatkit"""
        try:
            import pywhatkit as pwk
            self.pwk = pwk
            self.available = True
            print("✅ Advanced WhatsApp integration available")
        except ImportError:
            print("⚠️ pywhatkit not available - using basic WhatsApp Web integration")
            self.pwk = None
            self.available = False
    
    def schedule_contract_message(self, phone_number: str, contract_data: Dict, 
                                 send_time_minutes: int = 1) -> Dict:
        """Schedule a WhatsApp message to be sent with contract details"""
        
        if not self.available:
            return {"success": False, "error": "Advanced WhatsApp not available"}
        
        try:
            # Create message
            sender = WhatsAppContractSender()
            message = sender.create_contract_message(contract_data)
            
            # Calculate send time
            now = datetime.now()
            send_time = now + timedelta(minutes=send_time_minutes)
            
            # Schedule message
            self.pwk.sendwhatmsg(
                phone_no=phone_number,
                message=message,
                time_hour=send_time.hour,
                time_min=send_time.minute,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            
            return {
                "success": True,
                "scheduled_time": send_time.strftime('%Y-%m-%d %H:%M'),
                "message": "Contract message scheduled successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to schedule message: {str(e)}"
            }
