# Quick Start - Coffee Shop Barista Agent

## 🚀 Super Quick Start (Automated)

```powershell
# Run the automated installer (first time)
.\install.ps1

# Then start the app
.\start_app.ps1
```

Open browser to **http://localhost:3000** and start ordering! ☕

---

## Run the Application (3 Simple Steps)

### 1. Install Dependencies (First Time Only)

```powershell
# Backend
cd backend
uv sync
uv run python src/agent.py download-files

# Frontend
cd ../frontend
pnpm install
```

### 2. Start All Services

From the project root:

```powershell
.\start_app.ps1
```

This opens 3 PowerShell windows:
- LiveKit Server
- Backend Agent
- Frontend (http://localhost:3000)

### 3. Use the Agent

1. Open browser to **http://localhost:3000**
2. Click **Connect**
3. Talk to the barista and place your order!
4. **🎨 See your beautiful beverage visualization appear!**
5. Find your saved order in `backend/orders/`

## Manual Start (Alternative)

If the script doesn't work, run these in 3 separate terminals:

```powershell
# Terminal 1
livekit-server --dev

# Terminal 2
cd backend
uv run python src/agent.py dev

# Terminal 3
cd frontend
pnpm dev
```

## What the Barista Does

The agent will ask you for:
- ☕ Drink type (latte, cappuccino, espresso, etc.)
- 📏 Size (small, medium, large)
- 🥛 Milk (whole, skim, oat, almond, soy, none)
- ✨ Extras (extra shot, syrups, toppings)
- 📝 Your name

Once complete:
- ✅ Saves order to JSON file
- 🎨 **Shows beautiful HTML beverage visualization**
- 📋 **Displays order receipt**
- ☁️ **Shows whipped cream if ordered**

## Prerequisites

Install these first if you don't have them:

```powershell
# uv (Python package manager)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# pnpm (Node package manager)
npm install -g pnpm

# LiveKit Server
# Download from: https://github.com/livekit/livekit/releases
```

## Need Help?

See `SETUP_GUIDE.md` for detailed instructions and troubleshooting.
