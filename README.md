# CERT: Coordination Observability Framework

> **Mathematical framework for systematic observation of AI coordination behavior**

CERT provides a production-ready framework for measuring and analyzing coordination effects in multi-agent AI systems. Built for AI researchers who need to understand how different LLM providers interact and coordinate in real-world scenarios.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (NOT Python 2.7)
- API keys for Claude and/or Hugging Face
- Docker (optional, for containerized deployment)

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd cert-coordination-observability

# Install dependencies
pip3 install -r requirements.txt

# Install in development mode
pip3 install -e .
```

### 2. Configuration

Create and configure your API keys:

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Add your API keys to `.env`:
```env
# API Keys
CLAUDE_API_KEY=sk-ant-api03-your-key-here
HUGGINGFACE_API_KEY=hf_your-key-here

# Model Configuration
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1
```

### 3. Test Installation

```bash
# Run basic functionality tests
python3 tests/test_deployment.py

# Test LLM provider integration
python3 tests/test_llm_providers.py

# Test API endpoints
python3 tests/test_api.py
```

### 4. Start the Server

```bash
# Production-ready startup
python3 start_server.py

# Or simple startup for development
python3 -m cert.api.server
```

### 5. Verify API is Running

```bash
# Health check
curl http://localhost:8000/health

# Test behavioral consistency
curl -X POST http://localhost:8000/measure/consistency \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test_agent",
    "prompt": "What is AI?",
    "responses": [
      "AI is artificial intelligence",
      "Artificial intelligence is AI", 
      "AI refers to artificial intelligence"
    ]
  }'

# Test coordination effect
curl -X POST http://localhost:8000/measure/coordination \
  -H "Content-Type: application/json" \
  -d '{
    "agent_a_id": "claude",
    "agent_b_id": "deepseek",
    "agent_a_baseline": 0.85,
    "agent_b_baseline": 0.80,
    "coordinated_performance": 0.88,
    "interaction_pattern": "sequential"
  }'
```

## 🎯 Core Features

### Behavioral Consistency Analysis
Measure how consistently an agent behaves across multiple interactions:
```python
from cert.core.behavioral_analysis import BehavioralAnalyzer

analyzer = BehavioralAnalyzer()
result = analyzer.measure_consistency(
    agent_id="claude",
    prompt="Explain quantum computing",
    responses=[response1, response2, response3]
)
print(f"Consistency Score: {result['consistency_score']:.3f}")
```

### Coordination Effect Measurement
Quantify the impact of coordination between agents:
```python
from cert.core.coordination_effects import CoordinationAnalyzer

analyzer = CoordinationAnalyzer()
result = analyzer.calculate_coordination_effect(
    agent_a_baseline=0.85,
    agent_b_baseline=0.80,
    coordinated_performance=0.88,
    interaction_pattern="sequential"
)
print(f"Coordination Effect (γ): {result['coordination_effect']:.3f}")
```

## 🤖 LLM Provider Support

### Claude Integration
```python
from ll_providers.claude import ClaudeProvider

claude = ClaudeProvider()  # Uses CLAUDE_API_KEY from .env
response = await claude.generate("Explain machine learning")
```

### Deepseek Integration
```python
from ll_providers.huggingface import HuggingFaceProvider

deepseek = HuggingFaceProvider.create_deepseek_provider()
response = await deepseek.generate("Write a Python function")
```

### Llama Integration
```python
from ll_providers.huggingface import HuggingFaceProvider

llama = HuggingFaceProvider.create_llama_provider(model_size="7b")
response = await llama.generate("What is artificial intelligence?")
```

## 📊 Example Usage

### Multi-Provider Consistency Analysis
```python
# Run the comprehensive example
python3 examples/multi_provider_cert_test.py

# Or run individual quickstart examples
python3 examples/quickstart.py
python3 examples/autogen_integration.py
python3 examples/swarm_integration.py
```

### API Integration Example
```python
import requests

# Consistency measurement
response = requests.post('http://localhost:8000/measure/consistency', json={
    "agent_id": "multi_provider",
    "prompt": "Explain renewable energy",
    "responses": [claude_response, deepseek_response, llama_response]
})

consistency_data = response.json()
print(f"Multi-provider consistency: {consistency_data['consistency_score']:.3f}")
```

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the Docker image
docker build -t cert-coordination-observability .

# Run with environment file
docker run -p 8000:8000 --env-file .env cert-coordination-observability

# Or run with direct environment variables
docker run -p 8000:8000 \
  -e CLAUDE_API_KEY=your-key \
  -e HUGGINGFACE_API_KEY=your-key \
  cert-coordination-observability
```

### Docker Compose (Optional)
```yaml
version: '3.8'
services:
  cert-api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

## 🧪 Testing

### Run All Tests
```bash
# Basic functionality
python3 tests/test_deployment.py

# LLM provider tests
python3 tests/test_llm_providers.py

# API endpoint tests
python3 tests/test_api.py

# Performance tests
python3 tests/test_performance.py
```

### Test Individual Components
```bash
# Test only Claude
python3 -c "
from ll_providers.claude import ClaudeProvider
claude = ClaudeProvider()
print('Claude:', claude.get_provider_info())
"

# Test only Hugging Face
python3 -c "
from ll_providers.huggingface import HuggingFaceProvider
hf = HuggingFaceProvider()
print('HuggingFace:', hf.get_provider_info())
"
```

## 📋 API Reference

### Endpoints

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

#### `POST /measure/consistency`
Measure behavioral consistency
```json
{
  "agent_id": "string",
  "prompt": "string", 
  "responses": ["string", "string", "string"]
}
```

#### `POST /measure/coordination`
Measure coordination effect
```json
{
  "agent_a_id": "string",
  "agent_b_id": "string",
  "agent_a_baseline": 0.85,
  "agent_b_baseline": 0.80,
  "coordinated_performance": 0.88,
  "interaction_pattern": "sequential"
}
```

## 🔧 Configuration

### Environment Variables
```env
# Required API Keys
CLAUDE_API_KEY=sk-ant-api03-...
HUGGINGFACE_API_KEY=hf_...

# Optional Model Configuration
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Available Models
# Llama: meta-llama/Llama-2-7b-chat-hf, meta-llama/Llama-2-13b-chat-hf
# Deepseek: deepseek-ai/deepseek-llm-7b-chat, deepseek-ai/deepseek-coder-6.7b-instruct
```

### Model Selection
```python
# Change Hugging Face model
hf = HuggingFaceProvider(model_name="meta-llama/Llama-2-7b-chat-hf")

# Use different Claude model
claude = ClaudeProvider()
response = await claude.generate(prompt, model="claude-3-opus-20240229")
```

## 📈 Performance

### Expected Response Times
- **Claude API**: 1-3 seconds
- **Hugging Face API**: 2-5 seconds
- **CERT Consistency Analysis**: ~300ms
- **CERT Coordination Analysis**: ~5ms

### Memory Usage
- **Base framework**: ~200MB
- **With sentence transformers**: ~500MB
- **Docker container**: ~1GB

## 🛠️ Troubleshooting

### Common Issues

**Python Version Error**
```bash
# Check Python version
python3 --version
# Must be 3.8+, not 2.7
```

**Missing Dependencies**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade
```

**API Key Issues**
```bash
# Verify API keys are loaded
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('Claude key:', 'CLAUDE_API_KEY' in os.environ)
print('HF key:', 'HUGGINGFACE_API_KEY' in os.environ)
"
```

**Port Already in Use**
```bash
# Change port in .env
echo "PORT=8001" >> .env
```

### Debug Mode
```bash
# Run with debug logging
python3 start_server.py --debug

# Check logs
tail -f cert_server.log
```

## 🏗️ Architecture

### Core Components
- **`cert/core/`**: Mathematical framework implementation
- **`cert/api/`**: FastAPI REST endpoints
- **`ll_providers/`**: LLM provider integrations
- **`examples/`**: Usage examples and integrations
- **`tests/`**: Comprehensive test suite

### Mathematical Framework
- **Behavioral Consistency**:
- 
  $C(A_i, p) = \frac{1 - \sigma({d(r_j, r_k)})}{\mu({d(r_j, r_k)})}$
- **Coordination Effect**:

  $\gamma = \frac{\textrm{Coordinated Performance}}{\textrm{Individual Performance}}$
  
## 🤝 Contributing

### Development Setup
```bash
# Install in development mode
pip3 install -e .

# Run tests before committing
python3 -m pytest tests/

# Format code
black cert/ ll_providers/ examples/
```

### Adding New Providers
1. Create provider class in `ll_providers/`
2. Inherit from `LLMProvider` base class
3. Implement `generate()` and `get_provider_info()` methods
4. Add tests in `tests/test_providers.py`

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

Built for AI researchers studying coordination effects in multi-agent systems. Supports real-world deployment scenarios with production-ready infrastructure.

## 📞 Support

For issues and questions contact javier@jmarin.info, or 
- Check the troubleshooting section above
- Run the test suite: `python3 tests/test_deployment.py`
- Review server logs: `tail -f cert_server.log`
