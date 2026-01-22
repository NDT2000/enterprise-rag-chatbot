# enterprise-rag-chatbot
Academic & Programming RAG Chatbot with AWS deployment

A production-ready Academic & Programming Assistant powered by Retrieval Augmented Generation (RAG).  
This full-stack application enables users to upload course materials, research papers, and programming documentation, then interact with an AI chatbot that provides contextual answers with proper citations.

---

## Tech Stack

**Backend:** FastAPI (Python 3.11) with LangChain for RAG orchestration  
**Database:** PostgreSQL 16 with pgvector extension for semantic search  
**Cache:** Redis 7 for performance optimization  
**AI:** OpenAI GPT-4 with custom retrieval pipeline  
**Infrastructure:** AWS ECS/Fargate, Application Load Balancer, RDS, S3, CloudFront  
**Frontend:** React with TypeScript and Tailwind CSS  
**IaC:** Terraform for automated AWS deployment  
**CI/CD:** GitHub Actions for continuous deployment

---

## Features

- 🔐 JWT-based authentication with role-based access control  
- 📄 Multi-format document processing (PDF, DOCX, Markdown, code files)  
- 🤖 Hybrid search combining semantic (vector) and keyword matching  
- 💬 Real-time streaming chat with conversation memory  
- 📊 Citation tracking with source attribution and page numbers  
- ⚡ Auto-scaling architecture with CloudWatch monitoring  
- 🔒 Rate limiting and security best practices  
- 📈 Cost optimization with intelligent model routing  

---

## Project Status

**Day 1 Complete:**  
Development environment setup, backend foundation, and local database configuration.

---

## Directory Structure

├── backend/              # FastAPI application  
│   ├── app/  
│   │   ├── api/         # REST endpoints  
│   │   ├── core/        # Configuration & security  
│   │   ├── services/    # Business logic (RAG, auth)  
│   │   ├── models/      # Database models  
│   │   └── db/          # Database connection  
│   ├── tests/           # Unit & integration tests  
│   └── requirements.txt  
├── frontend/            # React application (TBD)  
├── terraform/           # AWS infrastructure as code  
├── docs/                # Architecture diagrams & API docs  
├── docker-compose.yml   # Local development environment  
└── README.md  

# Getting Started Prerequisites:  
Python 3.11+ Docker Desktop Node.js 18+ Terraform 1.5+ AWS CLI configured  

## Local Development:  

# Start database and cache
docker-compose up -d

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Run backend server
uvicorn app.main:app --reload

# API available at: 
http://localhost:8000

# Interactive docs:
http://localhost:8000/docs

## Architecture
Microservices architecture deployed on AWS:

-API Gateway: Application Load Balancer with SSL termination

-Compute: ECS Fargate for containerized backend

-Storage: S3 for documents, RDS PostgreSQL for structured data

-Cache: ElastiCache Redis for session and query caching

-CDN: CloudFront for static asset delivery

-Monitoring: CloudWatch for logs, metrics, and alarms
