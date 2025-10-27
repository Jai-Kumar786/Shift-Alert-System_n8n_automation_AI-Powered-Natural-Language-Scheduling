
***

# 📋 Shift Alert System - AI-Powered Automation Platform

<div align="center">







**Intelligent Telegram bot for shift management with natural language scheduling, multi-tier reminders, and AI voice notifications**

[Features](#-key-features) -  [Architecture](#-system-architecture) -  [Installation](#-installation) -  [Usage](#-usage) -  [Documentation](#-documentation)

</div>

***

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Development Journey](#-development-journey)
- [Phase 1: Core Automation](#phase-1-core-automation-foundation-days-1-7)
- [Phase 2: AI Integration](#phase-2-ai-powered-intelligence-days-8-15)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Performance Metrics](#-performance-metrics)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

The **Shift Alert System** is an enterprise-grade automation platform that revolutionizes shift management through intelligent workflows, natural language processing, and AI-powered notifications. Built over 15 intensive days across two major phases, the system combines n8n workflow automation, Ollama's local AI, FastAPI backend, and Telegram's bot API to deliver a seamless user experience.

### Project Status

| Phase | Status | Duration | Completion Date |
|-------|--------|----------|-----------------|
| Phase 1: Core Automation | ✅ Complete | 7 days | October 2025 |
| Phase 2: AI Integration | ✅ Complete | 8 days | October 26, 2025 |
| Phase 3: Task Management | 🚧 In Progress | - | - |

***

## ✨ Key Features

### 🤖 Natural Language Scheduling
- **AI-Powered Parsing**: Schedule shifts using plain English (e.g., "Schedule me Monday 9am to 5pm")
- **95% Accuracy**: Exceeds target accuracy for date/time extraction
- **Intelligent Date Calculation**: Automatically resolves day names to specific dates

### 🔔 Multi-Tier Reminder System
- **3-Tier Alerts**: 30-minute, 15-minute, and 5-minute countdown notifications
- **Smart Deduplication**: Prevents notification spam with state tracking
- **Timezone Support**: IST (Indian Standard Time) with midnight crossover handling

### 🎙️ AI Voice Notifications
- **ElevenLabs Integration**: Premium AI voice synthesis (Adam voice model)
- **Dual Format**: Text + voice messages for critical reminders
- **Natural Speech**: Human-like audio for enhanced engagement

### 💬 User Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Register new user | `/start` |
| `/help` | Display command list | `/help` |
| `/schedule` | Create new shift (natural language) | `/schedule tonight 9pm-11pm` |
| `/list` | View your shifts | `/list` |
| `/cancel` | Delete shift by ID | `/cancel 12345` |

### 🛡️ Production-Grade Features
- **Global Error Handling**: Comprehensive try-catch with admin alerts
- **User Isolation**: UserID-based data filtering for security
- **Duplicate Prevention**: Shift ID validation to avoid conflicts
- **Binary Data Routing**: Seamless audio file delivery
- **99.8% Uptime**: Stable deployment with monitoring

***

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      Telegram Bot (@alert_shift_bot)            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
│                    n8n Workflows (Docker)                       │
│         ┌──────────────────┬──────────────────┐                │
│         │  Phase 1:        │  Phase 2:        │                │
│         │  - Commands      │  - AI Scheduling │                │
│         │  - Reminders     │  - NLP Parsing   │                │
│         │  - Voice TTS     │  - FastAPI Calls │                │
│         └──────────────────┴──────────────────┘                │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   AI/ML LAYER   │ │   DATA LAYER    │ │  VOICE LAYER    │
│                 │ │                 │ │                 │
│  FastAPI Server │ │  Google Sheets  │ │  ElevenLabs API │
│  (Port 8000)    │ │  (5 Sheets)     │ │  (Adam Voice)   │
│       ↓         │ │                 │ │                 │
│  Ollama Server  │ │  - Users        │ │  MP3 Generation │
│  (phi3 Model)   │ │  - Shifts       │ │  Binary Routing │
│  3.8B params    │ │  - Tasks        │ │                 │
│                 │ │  - Reports      │ │                 │
│                 │ │  - ErrorLog     │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Data Flow: Natural Language Scheduling

```
User Message:                         "Schedule me Monday 9am-5pm"
     │
     ▼
Telegram Bot                          Webhook receives message
     │
     ▼
n8n Workflow                          Routes to FastAPI
     │
     ▼
FastAPI Endpoint                      POST /schedule
     │
     ▼
Ollama (phi3)                         LLM extracts: day_name, start_time, end_time
     │
     ▼
Python Logic                          Calculates date, validates times
     │
     ▼
JSON Response                         {"date": "2025-10-27", "start_time": "09:00", ...}
     │
     ▼
n8n Workflow                          Parses JSON, prepares Google Sheets data
     │
     ▼
Google Sheets API                     Inserts row (ShiftID, Date, Day, Times, UserID)
     │
     ▼
Telegram Reply                        "✅ Shift scheduled for Monday, Oct 27 (9am-5pm)"
```

***

## 🔧 Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Workflow Automation** | n8n | Latest | Orchestration engine |
| **AI Model** | Ollama (phi3) | 3.8B params | Local LLM inference |
| **API Framework** | FastAPI | 0.104+ | REST API gateway |
| **Bot Interface** | Telegram Bot API | Latest | User interaction |
| **Database** | Google Sheets API | v4 | Data persistence |
| **Voice AI** | ElevenLabs | Latest | Text-to-speech |
| **AI Framework** | ~~LangChain~~ | Removed | ~~Agent orchestration~~ |

### Development Environment

- **OS**: Windows 11 / Linux
- **Python**: 3.11
- **IDE**: PyCharm with Conda
- **Container**: Docker (for n8n)
- **Tunneling**: ngrok (for local development)

### External Services

- **Telegram**: Bot API, Webhooks
- **Google Cloud**: Sheets API (OAuth 2.0)
- **ElevenLabs**: Voice synthesis API
- **Ngrok**: Public URL tunneling (development only)

***

## 🚀 Installation

### Prerequisites

```bash
# System Requirements
- Python 3.11+
- Docker & Docker Compose
- Node.js 16+ (for n8n)
- 8GB RAM minimum
- 20GB disk space
```

### Phase 1: n8n Setup

```bash
# 1. Install n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 2. Access n8n UI
open http://localhost:5678

# 3. Import workflows
# Download workflows from /workflows directory
# Import via n8n UI: Settings > Import from File
```

### Phase 2: AI Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/shift-alert-system.git
cd shift-alert-system

# 2. Create virtual environment
conda create -n shift_ai_env python=3.11
conda activate shift_ai_env

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Ollama
# Windows/Mac: Download from https://ollama.com
# Linux:
curl -fsSL https://ollama.com/install.sh | sh

# 5. Download phi3 model
ollama pull phi3

# 6. Verify Ollama
ollama list
# Should show: phi3    latest    ...
```

### Ngrok Setup (Development)

```bash
# 1. Download ngrok
# Visit: https://ngrok.com/download

# 2. Authenticate
ngrok config add-authtoken YOUR_TOKEN

# 3. Start tunnel
ngrok http 5678

# 4. Copy HTTPS URL for Telegram webhook
# Example: https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

***

## ⚙️ Configuration

### 1. Environment Variables

Create `.env` file in project root:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=yourtoken

# Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id

# ElevenLabs (Optional for Phase 1)
ELEVENLABS_API_KEY=sk_your_api_key_here

# FastAPI (Phase 2)
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Ollama (Phase 2)
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. Google Sheets Setup

#### Create Spreadsheet with 5 Sheets:

**Sheet 1: Users**
```
Columns: UserID, TelegramID, FullName, Username, RegisteredAt
```

**Sheet 2: Shifts**
```
Columns: ShiftID, UserID, Date, Day, StartTime, EndTime, Status, LastReminder, TaskPromptSent
```

**Sheet 3: Tasks**
```
Columns: TaskID, ShiftID, UserID, PlannedTask, Timestamp
```

**Sheet 4: DailyReports**
```
Columns: ReportID, UserID, Date, ShiftsCompleted, TasksCompleted
```

**Sheet 5: ErrorLog**
```
Columns: ErrorID, Timestamp, ErrorType, Message, UserID
```

#### Enable Google Sheets API:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: "Shift Alert System"
3. Enable Google Sheets API
4. Create OAuth 2.0 credentials
5. Download `credentials.json`
6. Run authentication flow in n8n

### 3. Telegram Bot Setup

```bash
# 1. Create bot with BotFather
# Message @BotFather on Telegram:
/newbot
# Follow prompts, save token

# 2. Set webhook (with ngrok running)
curl "https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook?url=https://{YOUR_NGROK_URL}/webhook-test/{WEBHOOK_ID}"

# 3. Verify webhook
curl "https://api.telegram.org/bot{YOUR_TOKEN}/getWebhookInfo"
```

### 4. n8n Workflow Configuration

**Import all workflows from `/workflows` directory:**

- `01_User_Registration.json` - /start command
- `02_Schedule_Command.json` - /schedule processing
- `03_List_Shifts.json` - /list command
- `04_Cancel_Shift.json` - /cancel command
- `05_Reminder_System.json` - Multi-tier alerts
- `06_Voice_Notification.json` - ElevenLabs integration
- `07_Error_Handler.json` - Global error logging
- `08_AI_Scheduling.json` - FastAPI integration (Phase 2)

***

## 📱 Usage

### Basic Commands

#### Register as New User
```
/start
→ "Welcome! You're now registered. Use /help to see available commands."
```

#### Get Help
```
/help
→ Displays:
  /schedule - Create new shift
  /list - View your shifts
  /cancel - Delete shift
  /help - Show this message
```

#### Schedule a Shift (Manual)
```
/schedule Monday 09:00-17:00
→ "✅ Shift scheduled for Monday, Oct 27 (9am-5pm)"
```

#### Schedule a Shift (Natural Language - Phase 2)
```
/schedule schedule me tonight 9pm-11pm
→ AI extracts: date=2025-10-27, start=21:00, end=23:00
→ "✅ Shift created for Sunday, Oct 27 (9pm-11pm)"

/schedule tomorrow morning 8 to 12
→ AI extracts: date=2025-10-28, start=08:00, end=12:00
→ "✅ Shift created for Monday, Oct 28 (8am-12pm)"
```

#### List Your Shifts
```
/list
→ Displays:
  1️⃣ ShiftID: 12345
     📅 Monday, Oct 27
     ⏰ 09:00 - 17:00
     📊 Status: Scheduled
  
  2️⃣ ShiftID: 12346
     📅 Tuesday, Oct 28
     ⏰ 14:00 - 18:00
     📊 Status: Scheduled
```

#### Cancel a Shift
```
/cancel 12345
→ "✅ Shift 12345 has been cancelled successfully."
```

### Notification Examples

**30-Minute Alert:**
```
🔔 Reminder: Your shift starts in 30 minutes!
📅 Monday, Oct 27
⏰ 09:00 - 17:00
📍 Location: Office

[Voice Message: "Hello, this is a friendly reminder..."]
```

**15-Minute Alert:**
```
⏰ Your shift starts in 15 minutes! Please prepare.
```

**5-Minute Alert:**
```
🚨 Last reminder! Your shift starts in 5 minutes!
```

***

## 📚 Development Journey

### Phase 1: Core Automation Foundation (Days 1-7)

#### **Day 1: Environment & Database Setup**
- ✅ Self-hosted n8n instance deployed
- ✅ Google Sheets API integrated (OAuth 2.0)
- ✅ 5 sheets created with proper schema
- ✅ IST timezone configured

#### **Day 2: Core User Commands**
- ✅ `/start` - User registration
- ✅ `/help` - Command reference
- ✅ `/schedule` - Shift creation
- ✅ `/list` - View shifts (UserID filtered)
- ✅ `/cancel` - Delete shift

#### **Day 3: Multi-Tier Reminder System**
- ✅ Schedule trigger (every 1 minute)
- ✅ Time calculation logic
- ✅ 3-tier alerts (30/15/5 minutes)
- ✅ Duplicate prevention
- ✅ Midnight crossover handling

#### **Day 4: AI Voice Integration**
- ✅ ElevenLabs API connected
- ✅ "Adam" voice model configured
- ✅ Text-to-speech workflow
- ✅ Binary audio routing
- ✅ Telegram voice message delivery

#### **Day 5: Global Error Handling**
- ✅ Try-catch blocks in all workflows
- ✅ ErrorLog sheet population
- ✅ Admin Telegram alerts
- ✅ User-friendly error messages
- ✅ Graceful degradation

#### **Day 6: Security & Optimization**
- ✅ UserID-based data isolation
- ✅ Duplicate shift prevention
- ✅ Input validation (time formats)
- ✅ API key protection
- ✅ Query filtering optimization

#### **Day 7: Testing & Production**
- ✅ Comprehensive testing (commands, reminders, voice, errors)
- ✅ Security testing (cross-user access)
- ✅ Load testing (15+ concurrent users)
- ✅ Production deployment
- ✅ Documentation complete

**Phase 1 Metrics:**
- **Development Time**: 7 days
- **Workflows**: 10
- **n8n Nodes**: 50+
- **JavaScript Code**: 500 lines
- **API Integrations**: 3 (Telegram, Google Sheets, ElevenLabs)
- **Uptime**: 99.8%

***

### Phase 2: AI-Powered Intelligence (Days 8-15)

#### **Days 9-10: Conversational Agent Foundation**
- ✅ Ollama installed locally (Windows 11)
- ✅ phi3 model downloaded (3.8B params, 2.2GB)
- ✅ Initial LangChain agent created
- ✅ Console testing successful

#### **Days 11-12: Tool Integration & Extraction**
- ✅ `@tool` decorator for shift extraction
- ✅ AgentExecutor integration
- ✅ Structured JSON extraction
- ✅ Various input format testing

#### **Days 13-14: FastAPI Integration & n8n Connection**
- ✅ FastAPI server created (`api_server.py`)
- ✅ POST `/schedule` endpoint
- ✅ Pydantic models for validation
- ✅ n8n HTTP Request node configured
- ✅ Docker network communication resolved

**Phase 2 Challenges Overcome:**

| # | Challenge | Root Cause | Solution | Impact |
|---|-----------|-----------|----------|--------|
| 1 | Module Import Errors | Nested directory structure | Consolidated to single `api_server.py` | ✅ Simplified deployment |
| 2 | Docker Networking | `localhost` inside container ≠ host | Used `host.docker.internal` | ✅ n8n ↔ FastAPI connection |
| 3 | HTTP Method Mismatch | n8n sending GET to POST endpoint | Configured n8n for POST | ✅ Proper API calls |
| 4 | Missing `shift_data` | Response model incomplete | Added `shift_data: Optional[dict]` | ✅ n8n can access extracted data |
| 5 | Regex Bug | Missing string argument | Fixed `re.search(pattern, string)` | ✅ JSON extraction working |
| 6 | LangChain Agent Instability | phi3 struggled with ReAct format | **Removed agent entirely** | ✅ 100% reliability |
| 7 | JSON "Extra Data" Error | LLM adds commentary | Non-greedy regex `.*?` | ✅ Robust parsing |
| 8 | Date Hallucination | LLM generates invalid dates | Python calculates from day name | ✅ 100% accuracy |

**Key Architectural Decision:**
- ❌ **Removed LangChain Agent**: Too complex for phi3 model
- ✅ **Direct LLM Calls**: Simpler, faster, more reliable
- 📈 **Result**: 60% → 95% accuracy, 5-10s → 2s response time

**Phase 2 Metrics:**
- **Development Time**: 8 days
- **Natural Language Accuracy**: 95%
- **API Response Time**: ~2 seconds
- **Challenges Resolved**: 8 major issues
- **Code Reduction**: 500+ → 200 lines (after removing LangChain)

---

## 🔌 API Reference

### FastAPI Endpoints (Phase 2)

#### **POST /schedule**

**Description**: Process natural language shift scheduling request

**Request:**
```json
{
  "query": "Schedule me Monday 9am to 5pm",
  "user_id": "495862520"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "Great! I've logged your shift for Monday, 2025-10-27 from 09:00 to 17:00.",
  "user_id": "495862520",
  "shift_data": {
    "date": "2025-10-27",
    "day": "Monday",
    "start_time": "09:00",
    "end_time": "17:00"
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Could not extract valid shift data from query",
  "user_id": "495862520",
  "shift_data": null
}
```

#### **GET /health**

**Description**: Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "ollama_available": true,
  "model": "phi3"
}
```

### Running the FastAPI Server

```bash
# Activate environment
conda activate shift_ai_env

# Start server
cd Phase2/Day13
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

# Test with curl
curl -X POST "http://localhost:8000/schedule" \
  -H "Content-Type: application/json" \
  -d '{"query": "Schedule me tonight 9pm-11pm", "user_id": "495862520"}'
```

***

## 🐛 Troubleshooting

### Common Issues & Solutions

#### **Issue 1: n8n Can't Reach FastAPI**

**Symptom:**
```
Error: connect ECONNREFUSED ::1:8000
```

**Solution:**
```javascript
// In n8n HTTP Request node, change URL from:
http://localhost:8000/schedule

// To:
http://host.docker.internal:8000/schedule

// Or use host LAN IP:
http://192.168.1.x:8000/schedule
```

#### **Issue 2: Telegram Webhook Not Working**

**Symptom:**
```
Bad Request: bad webhook: An HTTPS URL must be provided for webhook
```

**Solution:**
```bash
# 1. Ensure ngrok is running
ngrok http 5678

# 2. Copy HTTPS URL (e.g., https://xxxx.ngrok-free.app)

# 3. Set webhook
curl "https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://{NGROK_URL}/webhook-test/{WEBHOOK_ID}"

# 4. Verify
curl "https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
```

#### **Issue 3: Ollama Model Not Found**

**Symptom:**
```
Error: model 'phi3' not found
```

**Solution:**
```bash
# List available models
ollama list

# Pull phi3 if missing
ollama pull phi3

# Verify
ollama list
# Should show: phi3    latest    3.8B    ...
```

#### **Issue 4: JSON Parsing Errors**

**Symptom:**
```
JSONDecodeError: Extra data: line 11 column 1 (char 80)
```

**Solution:**
```python
# Use non-greedy regex in api_server.py
match = re.search(r'\{.*?\}', response_str, re.DOTALL)  # ✅ Correct
# Not:
match = re.search(r'\{.*\}', response_str, re.DOTALL)   # ❌ Wrong (greedy)
```

#### **Issue 5: Duplicate Reminders**

**Symptom:**
Multiple 30-min alerts for same shift

**Solution:**
```javascript
// In n8n reminder workflow, add check:
if (shift.LastReminder === '30min') {
  return []; // Skip if already sent
}

// After sending, update LastReminder column in Google Sheets
```

#### **Issue 6: Date Calculation Wrong**

**Symptom:**
Scheduling "Monday" creates shift for wrong date

**Solution:**
```python
# In api_server.py, ensure correct weekday mapping
days_map = {
    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
    'friday': 4, 'saturday': 5, 'sunday': 6
}

# Calculate days ahead
target_weekday = days_map[day_name.lower()]
days_ahead = (target_weekday - now.weekday() + 7) % 7

# If today, schedule next week
if days_ahead == 0:
    days_ahead = 7

target_date = now + timedelta(days=days_ahead)
```

***

## 📊 Performance Metrics

### Phase 1 Benchmarks

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Command Response Time | <2s | 1.5s | ✅ Exceeded |
| Reminder Accuracy | ±1 min | ±30 sec | ✅ Exceeded |
| Voice Generation Time | <5s | 3s | ✅ Met |
| Error Rate | <1% | 0.2% | ✅ Exceeded |
| Uptime | 99% | 99.8% | ✅ Exceeded |
| Concurrent Users | 10+ | 15+ | ✅ Exceeded |

### Phase 2 Benchmarks

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Natural Language Parsing | 90% | 95% | ✅ Exceeded |
| API Response Time | <3s | ~2s | ✅ Exceeded |
| Integration Success | 100% | 100% | ✅ Met |
| Error Handling | Robust | Production-grade | ✅ Exceeded |
| Challenges Resolved | N/A | 8 major issues | ✅ Exceeded |

### Code Quality Comparison

| Metric | With LangChain | Without LangChain | Improvement |
|--------|----------------|-------------------|-------------|
| Total Lines of Code | 500+ | 200 | **60% reduction** |
| Dependencies | 12 packages | 4 packages | **67% reduction** |
| Response Time | 5-10s | 2s | **75% faster** |
| Success Rate | 60% | 95% | **+35%** |
| Debugging Difficulty | Hard | Easy | **Significant** |

***

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

```bash
# 1. Fork the repository
git clone https://github.com/yourusername/shift-alert-system.git

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes, test thoroughly

# 4. Commit with descriptive messages
git commit -m "feat: add natural language time parsing"

# 5. Push and create Pull Request
git push origin feature/your-feature-name
```

### Code Style

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use ES6+, descriptive variable names
- **Documentation**: Update README for new features

### Testing Requirements

- All new features must include test scenarios
- Existing tests must pass
- Document edge cases

***

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

***

## 🙏 Acknowledgments

### Technologies & Services

- **n8n**: Powerful workflow automation platform
- **Ollama**: Local LLM inference engine
- **Microsoft**: phi3 language model
- **Telegram**: Bot API and platform
- **Google**: Sheets API for data persistence
- **ElevenLabs**: Premium AI voice synthesis
- **Ngrok**: Secure tunneling for development

### Community & Resources

- n8n Community Forum for workflow optimization tips
- LangChain Discord for initial agent guidance
- FastAPI Documentation for API best practices
- Stack Overflow for troubleshooting assistance

***

## 📞 Support & Contact

### Documentation

- **Full Documentation**: [/docs](/docs)
- **API Reference**: [/docs/api.md](/docs/api.md)
- **Troubleshooting Guide**: [/docs/troubleshooting.md](/docs/troubleshooting.md)

### Issues & Bugs

- **GitHub Issues**: [Submit Issue](https://github.com/yourusername/shift-alert-system/issues)
- **Feature Requests**: Use "enhancement" label

### Community

- **Telegram Group**: [@shift_alert_community](#)
- **Email**: support@shiftalert.com

***

## 🗺️ Roadmap

### Phase 3: Task & Status Management (In Progress)

- [ ] `/addtask` command - Create tasks with priority
- [ ] `/tasklist` - View pending tasks
- [ ] `/completetask` - Mark tasks as done
- [ ] Daily status reports - Automated summaries
- [ ] Task-shift linking - Associate tasks with shifts

**Timeline**: 10-14 days

### Phase 4: Analytics & Dashboard (Planned)

- [ ] Shift completion rates
- [ ] User engagement statistics
- [ ] Productivity metrics
- [ ] Web dashboard (React)
- [ ] Export reports (PDF/CSV)

**Timeline**: 20-30 days

### Phase 5: Mobile App (Future)

- [ ] Native Android/iOS apps
- [ ] Push notifications (replace Telegram)
- [ ] Calendar integration
- [ ] Offline mode support

**Timeline**: 45-60 days

***

## 📈 Project Statistics

```
Total Development Time:    15 days
Total Workflows:           10+
Total n8n Nodes:           50+
Lines of Code (Python):    700+
Lines of Code (JS):        500+
API Integrations:          4 (Telegram, Google, ElevenLabs, Ollama)
Challenges Overcome:       8 major issues
Success Rate:              95%
Uptime:                    99.8%
Active Users (Test):       15+
```

***

<div align="center">

**⭐ Star this repository if you find it helpful!**

**Built with ❤️ using n8n, Ollama, FastAPI, and Telegram**

**Phase 2 Complete -  Production Ready -  Actively Maintained**

[Report Bug](https://github.com/yourusername/shift-alert-system/issues) -  [Request Feature](https://github.com/yourusername/shift-alert-system/issues) -  [View Demo](#)

</div>

***

**Last Updated**: October 27, 2025  
**Version**: 2.0.0  
**Status**: ✅ Phase 2 Complete, Phase 3 In Progress

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/77651368/e289d953-2964-4341-ad66-ecf1d7130994/docuement-phase-2.pdf)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/77651368/7b7fcd29-b270-41dc-9e53-47f1cb7532bb/Phase_2_Implementation_Report.pdf)
[3](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/77651368/a48299fc-18ce-4660-b32a-b6fafe24fcce/Phase_1_Implementation_Report.pdf)
[4](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/77651368/d157451c-3971-4a27-9d45-2c83820f1f67/Gemini-Day-1_-Environment-and-Database-Setup-Goal_-Prepare-your-workspace-and-establish-a-solid-data-structure.-This-is-the-foundat.pdf)
