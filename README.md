# ☕ Coffee Shop Barista Voice Agent - Complete Implementation

## 🎉 Day 2 Challenge - FULLY COMPLETED (Including Advanced Features!)

This project is a fully functional Coffee Shop Barista Voice Agent built for the Murf AI Voice Agents Challenge. It includes **both the primary goals AND the advanced HTML visualization system**.

---

## ✨ Features Implemented

### ✅ Primary Goals (Required)
- **Barista Persona**: Friendly, engaging coffee shop assistant
- **Order State Management**: Tracks drink type, size, milk, extras, and customer name
- **Intelligent Conversation**: Asks clarifying questions until order is complete
- **JSON Order Saving**: Saves orders to `backend/orders/` with timestamp

### 🎨 Advanced Features (Optional - COMPLETED!)
- **HTML Beverage Visualization**: Dynamic cup rendering based on order
- **Size-Based Display**: Small/medium/large cup sizes
- **Whipped Cream Topping**: Visual representation when ordered
- **Order Receipt**: Beautiful formatted summary
- **Real-Time Display**: Live data streaming to frontend
- **Smooth Animations**: Professional UI with Framer Motion

---

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

```powershell
# Install everything
.\install.ps1

# Start the application
.\start_app.ps1

# Open browser to http://localhost:3000
```

### Option 2: Manual Setup

See **QUICKSTART.md** or **SETUP_GUIDE.md** for detailed instructions.

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── src/
│   │   └── agent.py          # Main agent with barista + HTML generation
│   ├── orders/               # Saved orders (JSON)
│   ├── .env.local            # API keys (configured)
│   └── pyproject.toml        # Python dependencies
├── frontend/
│   ├── components/
│   │   └── app/
│   │       ├── order-visualization.tsx  # NEW: HTML display component
│   │       └── session-view.tsx         # Updated with visualization
│   ├── .env.local            # LiveKit config (configured)
│   └── package.json          # Node dependencies
├── install.ps1               # Automated installer
├── start_app.ps1             # Start all services
├── QUICKSTART.md             # Quick reference guide
├── SETUP_GUIDE.md            # Detailed setup instructions
├── ADVANCED_FEATURES.md      # HTML visualization documentation
└── DAY2_COMPLETE.md          # Task completion summary
```

---

## 🛠️ Technologies Used

### Backend
- **Python 3.9+** with **uv** package manager
- **LiveKit Agents** - Voice AI framework
- **Murf Falcon TTS** - Fastest text-to-speech API
- **Google Gemini 2.5 Flash** - Large language model
- **Deepgram Nova-3** - Speech-to-text
- **LiveKit Data Channels** - Real-time HTML streaming

### Frontend
- **React 18+** / **Next.js 14+**
- **TypeScript** - Type-safe development
- **Framer Motion** - Smooth animations
- **LiveKit Components React** - Real-time communication
- **Tailwind CSS** - Styling

---

## 🎯 How It Works

1. **User connects** via web browser
2. **Barista greets** and starts taking order
3. **Agent collects** drink type, size, milk, extras, name
4. **Order saved** to JSON file when complete
5. **HTML generated** with beverage visualization
6. **Frontend displays** beautiful animated order view
7. **User sees** their drink and receipt on screen!

---

## 📸 What You'll See

### Voice Interaction
- Natural conversation with the barista
- Clarifying questions for each order detail
- Friendly confirmations

### Visual Display
- **Animated modal overlay** when order completes
- **Cup visualization** matching your order size
- **Drink colors** based on coffee type
- **Whipped cream** topping (if ordered)
- **Complete receipt** with all order details
- **Order number** and timestamp
- **Professional design** with gradient background

---

## 📋 Example Order Flow

```
You: "Hi, I'd like a coffee"
Barista: "Welcome to Murf Coffee Shop! What drink would you like?"
You: "A large latte please"
Barista: "Great choice! A latte it is. What size... wait, you said large! Got it."
You: "With oat milk"
Barista: "Perfect! Oat milk noted."
You: "And whipped cream"
Barista: "Added whipped cream to your order!"
You: "Name is Alex"
Barista: "Thanks Alex! [Saves order] Check your screen!"

[Beautiful visualization appears showing large latte cup with whipped cream]
```

---

## 📦 API Keys (Pre-Configured)

The following API keys have been configured in `.env.local` files:

- ✅ **Murf AI API Key**: For Falcon TTS (ultra-fast voice synthesis)
- ✅ **Google API Key**: For Gemini LLM (intelligent conversations)
- ✅ **Deepgram API Key**: For Nova-3 STT (accurate speech recognition)

---

## 📚 Documentation

- **README.md** (this file) - Overview
- **QUICKSTART.md** - Fast setup guide
- **SETUP_GUIDE.md** - Detailed instructions & troubleshooting
- **ADVANCED_FEATURES.md** - HTML visualization technical docs
- **DAY2_COMPLETE.md** - Task completion summary
- **backend/orders/README.md** - Order files explanation

---

## 🆘 Troubleshooting

### Issue: Services won't start
**Solution**: Run `.\install.ps1` to check prerequisites and install dependencies

### Issue: No visualization appears
**Check**: 
1. Order must be complete (all fields filled)
2. Check browser console for errors
3. Verify backend is publishing data (check logs)

### Issue: TypeScript errors in frontend
**Solution**: These are expected before `pnpm install` - run the installer

For more help, see **SETUP_GUIDE.md**

---

## 🎓 Learning Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Murf Falcon TTS API](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Data Channels](https://docs.livekit.io/home/client/data/)
- [Framer Motion](https://www.framer.com/motion/)

---

## 📹 Next Steps

To complete the Day 2 Challenge:

1. **Test your agent** - Place orders and see visualizations
2. **Record a video** showing:
   - Voice interaction with barista
   - **HTML beverage visualization appearing**
   - Saved JSON order file
3. **Post on LinkedIn** with:
   - Your video
   - Description of what you built
   - Mention: "Built with Murf Falcon - fastest TTS API"
   - Tag: @Murf AI
   - Hashtags: #MurfAIVoiceAgentsChallenge #10DaysofAIVoiceAgents

---

## 🏆 Achievement Unlocked

**Day 2 Challenge**: ✅ COMPLETE  
**Advanced Challenge**: ✅ COMPLETE

You've built:
- ✅ Functional voice AI barista
- ✅ Complete order management
- ✅ JSON order persistence
- ✅ **HTML beverage visualization**
- ✅ **Real-time data streaming**
- ✅ **Beautiful animated UI**

Keep up the amazing work! 🚀☕✨

---

## 📄 License

This project is based on MIT-licensed templates from LiveKit and includes integration with Murf Falcon TTS.

---

**Built for the Murf AI Voice Agents Challenge**  
**Powered by Murf Falcon - The Consistently Fastest TTS API**

