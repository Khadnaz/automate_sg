import json
import os
import configparser

def LoadCredentials(profile_name):
    """Load Alibaba Cloud credentials from multiple possible sources"""
    
    # Method 1: Try environment variables first (MOST SECURE)
    if os.environ.get('ALIBABA_ACCESS_KEY_ID') and os.environ.get('ALIBABA_ACCESS_KEY_SECRET'):
        return {
            'accessKeyId': os.environ.get('ALIBABA_ACCESS_KEY_ID'),
            'accessKeySecret': os.environ.get('ALIBABA_ACCESS_KEY_SECRET'),
            'region': os.environ.get('ALIBABA_REGION_ID', 'me-central-1')
        }
    
    # Method 2: Try JSON format credentials file
    json_config_file = os.path.expanduser('~/.aliyuncli/credentials')
    
    if os.path.exists(json_config_file):
        try:
            with open(json_config_file, 'r') as f:
                content = f.read()
                config = json.loads(content)
                
            if profile_name in config:
                profile = config[profile_name]
                return {
                    'accessKeyId': profile.get('aliyun_access_key_id'),
                    'accessKeySecret': profile.get('aliyun_access_key_secret'),
                    'region': profile.get('region_id', 'me-central-1')
                }
        except (json.JSONDecodeError, FileNotFoundError):
            pass  # Try next method
    
    # Method 3: Try INI/Config format
    ini_config_file = os.path.expanduser('~/.aliyuncli/credentials')
    
    if os.path.exists(ini_config_file):
        try:
            config = configparser.ConfigParser()
            config.read(ini_config_file)
            
            if profile_name in config:
                return {
                    'accessKeyId': config[profile_name].get('aliyun_access_key_id'),
                    'accessKeySecret': config[profile_name].get('aliyun_access_key_secret'),
                    'region': config[profile_name].get('region_id', 'me-central-1')
                }
        except:
            pass
    
    # Method 4: Try alternative config location
    alt_config_file = os.path.expanduser('~/.aliyuncli/config.json')
    
    if os.path.exists(alt_config_file):
        try:
            with open(alt_config_file, 'r') as f:
                config = json.load(f)
                
            if profile_name in config:
                profile = config[profile_name]
                return {
                    'accessKeyId': profile.get('aliyun_access_key_id'),
                    'accessKeySecret': profile.get('aliyun_access_key_secret'),
                    'region': profile.get('region_id', 'me-central-1')
                }
        except:
            pass
    
    # Method 5: Windows-specific location
    if os.name == 'nt':  # Windows
        win_config_file = os.path.join(os.environ.get('USERPROFILE', ''), '.aliyuncli', 'credentials')
        
        if os.path.exists(win_config_file):
            try:
                with open(win_config_file, 'r') as f:
                    content = f.read()
                    # Try JSON first
                    try:
                        config = json.loads(content)
                        if profile_name in config:
                            profile = config[profile_name]
                            return {
                                'accessKeyId': profile.get('aliyun_access_key_id'),
                                'accessKeySecret': profile.get('aliyun_access_key_secret'),
                                'region': profile.get('region_id', 'me-central-1')
                            }
                    except json.JSONDecodeError:
                        # Try INI format
                        config = configparser.ConfigParser()
                        config.read_string(content)
                        
                        if profile_name in config:
                            return {
                                'accessKeyId': config[profile_name].get('aliyun_access_key_id'),
                                'accessKeySecret': config[profile_name].get('aliyun_access_key_secret'),
                                'region': config[profile_name].get('region_id', 'me-central-1')
                            }
            except:
                pass
    
    # Method 6: Direct configuration (ONLY for testing - replace with your NEW credentials)
    # ⚠️ SECURITY WARNING: Never commit real credentials to version control!
    # ⚠️ Replace these placeholders with your actual NEW credentials
    if profile_name == 'sg_auth':
        print("WARNING: Using hardcoded credentials. This is not secure for production!")
        return {
            'accessKeyId': '',  # Replace with your NEW Access Key ID
            'accessKeySecret': '',  # Replace with your NEW Secret Key
            'region': 'me-central-1'  # Middle East (Riyadh)
        }
    
    # If nothing worked, return error
    print(f"Error: Could not load credentials for profile '{profile_name}'")
    print(f"Tried the following methods:")
    print(f"  1. Environment variables (ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET)")
    print(f"  2. ~/.aliyuncli/credentials (JSON format)")
    print(f"  3. ~/.aliyuncli/credentials (INI format)")
    print(f"  4. ~/.aliyuncli/config.json")
    if os.name == 'nt':
        print(f"  5. %USERPROFILE%\\.aliyuncli\\credentials")
    print(f"\nTo fix this, either:")
    print(f"  - Set environment variables")
    print(f"  - Create a credentials file")
    print(f"  - Update the hardcoded values in this file (not recommended)")
    
    return False

# Test function to verify credentials are loading
if __name__ == "__main__":
    creds = LoadCredentials('sg_auth')
    if creds:
        print("✓ Credentials loaded successfully")
        print(f"  Region: {creds['region']}")
        print(f"  Access Key ID: {creds['accessKeyId'][:10]}..." if creds['accessKeyId'] else "  Access Key ID: Not set")
    else:
        print("✗ Failed to load credentials")