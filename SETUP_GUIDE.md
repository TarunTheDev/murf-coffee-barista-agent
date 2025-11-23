# Coffee Shop Barista Agent - Setup Guide

## Day 2 Task Completed! ☕

This guide will help you get your Coffee Shop Barista Voice Agent up and running.

## What's Been Done

✅ **API Keys Configured**: Murf AI, Google Gemini, and Deepgram API keys have been set up  
✅ **Barista Persona**: Agent transformed into a friendly coffee shop barista  
✅ **Order State Management**: Full order tracking system implemented  
✅ **Function Tools**: Tools created to collect drink type, size, milk preference, extras, and customer name  
✅ **JSON Order Saving**: Completed orders are automatically saved to `backend/orders/` directory  

## Prerequisites

Before running the application, ensure you have:

1. **Python 3.9+** with [uv](https://docs.astral.sh/uv/) package manager
2. **Node.js 18+** with pnpm (`npm install -g pnpm`)
3. **LiveKit CLI** and **LiveKit Server**

### Installing Prerequisites on Windows

#### Install uv (Python package manager):
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Install pnpm (Node package manager):
```powershell
npm install -g pnpm
```

#### Install LiveKit:
Download from: https://github.com/livekit/livekit/releases

Or if you have Scoop:
```powershell
scoop install livekit
```

## Setup Instructions

### Step 1: Install Backend Dependencies

Open PowerShell in the project root and run:

```powershell
cd backend
uv sync
```

### Step 2: Download Required Models

```powershell
uv run python src/agent.py download-files
```

This downloads the Silero VAD model and LiveKit turn detector needed for voice processing.

### Step 3: Install Frontend Dependencies

```powershell
cd ../frontend
pnpm install
```

## Running the Application

You have two options:

### Option A: Run All Services with PowerShell Script (Recommended)

From the project root directory:

```powershell
.\start_app.ps1
```

This will start:
- LiveKit Server (port 7880)
- Backend Agent (listening for connections)
- Frontend App (http://localhost:3000)

Each service will open in its own PowerShell window.

### Option B: Run Services Manually in Separate Terminals

**Terminal 1 - LiveKit Server:**
```powershell
livekit-server --dev
```

**Terminal 2 - Backend Agent:**
```powershell
cd backend
uv run python src/agent.py dev
```

**Terminal 3 - Frontend:**
```powershell
cd frontend
pnpm dev
```

## Using the Coffee Shop Barista

1. **Open your browser** to http://localhost:3000

2. **Click "Connect"** to start a voice session with the barista

3. **Place your order** by speaking naturally. The barista will ask you for:
   - What drink you'd like (latte, cappuccino, espresso, etc.)
   - Size (small, medium, or large)
   - Milk preference (whole, skim, oat, almond, soy, or no milk)
   - Any extras (extra shot, syrups, whipped cream, etc.)
   - Your name

4. **Complete the order** - Once all information is collected, the barista will save your order

5. **Check your order** - Find the saved JSON file in `backend/orders/` directory

## Order Format

Each saved order contains:

```json
{
  "drinkType": "latte",
  "size": "medium",
  "milk": "oat milk",
  "extras": ["extra shot", "vanilla syrup"],
  "name": "John"
}
```

## Troubleshooting

### Issue: "livekit-server command not found"
**Solution:** Install LiveKit CLI from https://github.com/livekit/livekit/releases

### Issue: "uv command not found"
**Solution:** Install uv with: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Issue: "pnpm command not found"
**Solution:** Install pnpm with: `npm install -g pnpm`

### Issue: Backend fails to start
**Solution:** 
1. Check that all API keys in `backend/.env.local` are correct
2. Ensure LiveKit server is running first
3. Check Python version: `python --version` (should be 3.9+)

### Issue: Frontend can't connect
**Solution:**
1. Verify `frontend/.env.local` has the correct LIVEKIT_URL (ws://127.0.0.1:7880)
2. Make sure backend agent is running and connected to LiveKit
3. Check browser console for connection errors

## Testing the Agent

Try these example conversations:

**Example 1:**
- You: "Hi, I'd like a coffee"
- Agent: "Hello! Welcome to Murf Coffee Shop! What kind of drink would you like today?"
- You: "I'll have a latte"
- Agent: "Great choice! A latte it is. What size would you like - small, medium, or large?"
- You: "Medium please"
- Agent: "Got it! Medium size. What type of milk would you like?"
- You: "Oat milk"
- Agent: "Perfect! Oat milk noted. Would you like any extras like an extra shot, vanilla syrup, or whipped cream?"
- You: "Add vanilla syrup"
- Agent: "Added vanilla syrup to your order! And what name should I put on this order?"
- You: "Sarah"
- Agent: "Thanks Sarah! Let me save your order..." [Order saved]

## Next Steps

Now that your Coffee Shop Barista is working:

1. **Test the agent** by placing different orders
2. **Record a video** of your interaction with the agent
3. **Show the saved JSON** order file
4. **Post on LinkedIn** about completing Day 2 of the #MurfAIVoiceAgentsChallenge

## Advanced Challenge (Optional)

Want to go further? Try implementing:
- HTML-based beverage visualization that changes based on order details
- Order receipt rendering
- Custom drink recommendations

See `challenges/Day 2 Task.md` for more details!

## Files Modified

- `backend/.env.local` - API keys configured
- `frontend/.env.local` - LiveKit connection configured
- `backend/src/agent.py` - Coffee barista agent implementation with order tools

Enjoy building with the fastest TTS API - Murf Falcon! ☕🚀
