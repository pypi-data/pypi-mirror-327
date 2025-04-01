#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
import os
import random
import string
from datetime import datetime, timedelta, timezone
import argparse

class SecureShareCLI:
    def __init__(self):
        # Using public instance credentials
        self.supabase_url = "https://xkiehleqrymixjhfoaja.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhraWVobGVxcnltaXhqaGZvYWphIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMDIwMzEsImV4cCI6MjA1NDU3ODAzMX0.wHx8-u90Huz6PWwg0mt6A4hxX0pAZWn174Q6YeKPDpY"
        self.frontend_url = "https://secureshare-site.vercel.app"
        self.rest_url = f"{self.supabase_url}/rest/v1"

    def detect_secrets(self, code):
        secrets = []
        patterns = {
            'API_KEY': r'(?:api[_-]?key|apikey)[\'"]?\s*(?::|=)\s*[\'"]?([a-zA-Z0-9_\-]{20,})[\'"]?',
            'PASSWORD': r'(?:password|passwd|pwd)[\'"]?\s*(?::|=)\s*[\'"]?([^\'"\s]+)[\'"]?',
            'TOKEN': r'(?:token|jwt|bearer)[\'"]?\s*(?::|=)\s*[\'"]?([a-zA-Z0-9_\-\.]+)[\'"]?',
            'SECRET_KEY': r'(?:secret[_-]?key|secretkey)[\'"]?\s*(?::|=)\s*[\'"]?([a-zA-Z0-9_\-]{20,})[\'"]?'
        }
        
        import re
        for line_num, line in enumerate(code.split('\n'), 1):
            for secret_type, pattern in patterns.items():
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    secrets.append({
                        'type': secret_type,
                        'line': line_num,
                        'value': match.group(1)
                    })
        return secrets

    def redact_secrets(self, code, secrets):
        for secret in secrets:
            code = code.replace(secret['value'], '[REDACTED]')
        return code

    def share_code(self, code, title="Untitled Snippet", language="text"):
        try:
            secrets = self.detect_secrets(code)
            redacted_code = self.redact_secrets(code, secrets)
            share_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)
            expires_at_iso = expires_at.isoformat().replace('+00:00', 'Z')
            
            data = {
                "share_id": share_id,
                "original_content": code,
                "redacted_content": redacted_code,
                "title": title,
                "language": language,
                "expires_at": expires_at_iso
            }

            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }

            req = urllib.request.Request(
                f"{self.rest_url}/code_snippets",
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 201:
                    share_url = f"{self.frontend_url}/share/{share_id}"
                    
                    if secrets:
                        print("\nWarning: Sensitive information detected!")
                        print("The following secrets were found and redacted:")
                        for secret in secrets:
                            print(f"- {secret['type']} on line {secret['line']}")
                    
                    print(f"\nCode shared successfully!")
                    print(f"Share URL: {share_url}")
                    return True
                else:
                    print(f"Error: Failed to share code")
                    return False
                    
        except Exception as e:
            print(f"Error: Failed to share code - {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='SecShare CLI - Share code snippets securely')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                      help='File containing code to share (reads from stdin if not specified)')
    parser.add_argument('-t', '--title', default="Untitled Snippet",
                      help='Title for the code snippet')
    parser.add_argument('-l', '--language', default="text",
                      help='Programming language of the code snippet')
    
    args = parser.parse_args()
    
    try:
        code = args.file.read()
        cli = SecureShareCLI()
        cli.share_code(code, args.title, args.language)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if args.file is not sys.stdin:
            args.file.close()

if __name__ == "__main__":
    main()