# CERT Framework Deployment Guide

## Overview
This guide will help you deploy the CERT (Coordination Observability Framework) for production use with real LLM integration.

## Prerequisites
- Python 3.8+ (NOT Python 2.7)
- Docker (optional, for containerized deployment)
- Git

## Quick Start

### 1. Install Dependencies
```bash
# Use Python 3 explicitly
python3 -m pip install -r requirements.txt

# Or install the package in development mode
python3 -m pip install -e .
```

### 2. Configure Environment
Copy and edit the `.env` file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Your `.env` should contain:
```
CLAUDE_API_KEY=your_claude_key_here
HUGGINGFACE_API_KEY=your_hf_key_here
HOST=0.0.0.0
PORT=8000
WORKERS=1
```

### 3. Test Installation
```bash
python3 test_deployment.py
```

### 4. Start Server
```bash
# Production-ready startup
python3 start_server.py

# Or simple startup for development
python3 -m cert.api.server
```

### 5. Test API
```bash
# In a separate terminal
python3 test_api.py
```

## Docker Deployment

### Build Image
```bash
docker build -t cert-coordination-observability .
```

### Run Container
```bash
docker run -p 8000:8000 --env-file .env cert-coordination-observability
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Behavioral Consistency
```bash
curl -X POST http://localhost:8000/measure/consistency \\
  -H "Content-Type: application/json" \\
  -d '{
    "agent_id": "test_agent",
    "prompt": "What is AI?",
    "responses": [
      "AI is artificial intelligence",
      "Artificial intelligence is AI", 
      "AI refers to artificial intelligence"
    ]
  }'
```

### Coordination Effect
```bash
curl -X POST http://localhost:8000/measure/coordination \\
  -H "Content-Type: application/json" \\
  -d '{
    "agent_a_id": "agent_a",
    "agent_b_id": "agent_b", 
    "agent_a_baseline": 0.8,
    "agent_b_baseline": 0.9,
    "coordinated_performance": 0.75,
    "interaction_pattern": "sequential"
  }'
```

## Integration with Real LLMs

### Claude Integration
```python
from ll_providers.claude import ClaudeProvider

claude = ClaudeProvider(api_key="your_claude_key")
responses = []
for i in range(3):
    response = claude.generate("Explain quantum computing")
    responses.append(response)

# Measure consistency
from cert.core.behavioral_analysis import BehavioralAnalyzer
analyzer = BehavioralAnalyzer()
result = analyzer.measure_consistency("claude", "quantum computing", responses)
```

### Hugging Face Integration
```python
from ll_providers.huggingface import HuggingFaceProvider

hf = HuggingFaceProvider(api_key="your_hf_key")
# Similar usage as Claude
```

## Troubleshooting

### Common Issues
1. **Python Version**: Ensure you're using Python 3.8+
2. **Dependencies**: Install all requirements with `pip install -r requirements.txt`
3. **API Keys**: Make sure your .env file contains valid API keys
4. **Port Conflicts**: Change PORT in .env if 8000 is occupied

### Logs
- Server logs: `cert_server.log`
- Check console output for real-time logs

## Production Considerations

### Performance
- Use multiple workers: set `WORKERS=4` in .env
- Consider using gunicorn for production
- Monitor memory usage with sentence transformers

### Security
- Use HTTPS in production
- Secure your API keys
- Consider rate limiting

### Monitoring
- Health check endpoint: `/health`
- Monitor response times and accuracy
- Log all coordination measurements

## Next Steps
1. Deploy to cloud platform (AWS, GCP, Azure)
2. Set up monitoring and alerting
3. Implement authentication if needed
4. Scale horizontally with load balancer