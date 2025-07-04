#!/usr/bin/env python3
"""
Production-ready startup script for CERT Coordination Observability Framework
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cert_server.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def load_environment():
    """Load environment variables"""
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logging.info("Environment variables loaded from .env")
    else:
        logging.warning("No .env file found. Using system environment variables.")

def verify_dependencies():
    """Verify all required dependencies are available"""
    required_packages = [
        'fastapi', 'uvicorn', 'numpy', 'scipy', 
        'sentence_transformers', 'pydantic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        logging.error(f"Missing packages: {', '.join(missing)}")
        logging.error("Please install with: pip install -r requirements.txt")
        return False
    
    logging.info("All dependencies verified")
    return True

def main():
    """Main startup function"""
    setup_logging()
    logging.info("Starting CERT Coordination Observability Framework")
    
    # Load environment
    load_environment()
    
    # Verify dependencies
    if not verify_dependencies():
        sys.exit(1)
    
    # Import and start server
    try:
        from cert.api.server import app
        import uvicorn
        
        # Configuration
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8000))
        workers = int(os.getenv('WORKERS', 1))
        
        logging.info(f"Starting server on {host}:{port} with {workers} workers")
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=workers,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()