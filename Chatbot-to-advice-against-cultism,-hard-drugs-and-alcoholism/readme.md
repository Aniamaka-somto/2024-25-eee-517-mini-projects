# Student Counseling Chatbot System

## Overview

A chatbot system designed to provide guidance and support to students facing issues related to cultism, alcohol abuse, and drug addiction. The system consists of two main parts:

1. **Rasa Backend** - Handles natural language understanding and conversation logic
2. **React Frontend** - Provides the user interface for chatting with the bot

## System Components

### Rasa Backend

The Rasa backend processes user messages, understands intents, and generates appropriate responses. It includes:

- **NLU (Natural Language Understanding)** - Understands what users are saying
- **Core** - Manages conversation flow and decides what to say next
- **Actions** - Custom Python code for complex responses and external API calls
- **Domain** - Defines intents, entities, slots, and responses

### React Frontend

The React frontend provides a chat interface where users can interact with the bot. It includes:

- **Chat Interface** - Real-time messaging display
- **Message Input** - Text area for typing messages
- **Bot Responses** - Displays text, buttons, and images from the bot
- **Connection Status** - Shows if the bot is online

## How It Works

```
User types message → React Frontend → Rasa Backend → Processes message → Sends response → React Frontend → Displays to user
```

1. User types a message in the React chat interface
2. React sends the message to Rasa via REST API
3. Rasa processes the message using trained NLU and Core models
4. Rasa generates a response (text, buttons, or images)
5. React receives the response and displays it to the user

## Rasa Backend Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Install Rasa
pip install rasa[full]
pip install rasa-sdk
```

### Project Structure

```
rasa-backend/
├── data/
│   ├── nlu.yml          # Training examples for understanding user messages
│   ├── stories.yml      # Example conversations
│   └── rules.yml        # Simple if-this-then-that rules
├── actions/
│   ├── __init__.py
│   └── actions.py       # Custom Python actions
├── domain.yml           # Bot's knowledge base (intents, responses, etc.)
├── config.yml           # ML pipeline configuration
├── endpoints.yml        # Server configuration
└── models/              # Trained models (created after training)
```

### Key Files Explained

**domain.yml** - Defines what your bot knows:

```yaml
intents:
  - greet
  - ask_help
  - emergency

responses:
  utter_greet:
    - text: "Hello! How can I help you today?"

  utter_help:
    - text: "I'm here to provide support and resources."
```

**data/nlu.yml** - Training examples:

```yaml
nlu:
  - intent: greet
    examples: |
      - hello
      - hi there
      - good morning

  - intent: ask_help
    examples: |
      - I need help
      - can you help me
      - I'm struggling
```

**data/stories.yml** - Conversation flows:

```yaml
stories:
  - story: Basic greeting and cultism inquiry
    steps:
      - intent: greet
      - action: utter_greet
      - intent: ask_about_cultism
      - action: utter_cultism_info
```

**actions/actions.py** - Custom Python code:

```python
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher

class ActionProvideEmergencyHelp(Action):
    def name(self):
        return "action_provide_emergency_help"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Emergency contacts: Campus Security: 555-0123")
        return []
```

### Training and Running Rasa

1. **Train the model:**

   ```bash
   rasa train
   ```

2. **Start the action server (if you have custom actions):**

   ```bash
   rasa run actions
   ```

3. **Start the Rasa server:**

   ```bash
   rasa run --enable-api --cors "*"
   ```

4. **Test in command line:**
   ```bash
   rasa shell
   ```

### How Rasa Processes Messages

1. **NLU Pipeline** - Takes user message and extracts:

   - **Intent** - What the user wants (e.g., "ask_help")
   - **Entities** - Important information (e.g., "alcohol" from "I have an alcohol problem")

2. **Core** - Uses the intent to decide what to do next:

   - Looks at conversation history
   - Follows trained stories and rules
   - Chooses appropriate response or action

3. **Response Generation** - Sends back:
   - Text messages
   - Buttons for quick replies
   - Images or other media (not available at the moment)

## React Frontend Setup

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
# or
yarn install
```

### Project Structure

```
react-frontend/
├── src/
│   ├── components/
│   │   ├── ChatArea.tsx      # Displays chat messages
│   │   ├── TextArea.tsx      # Message input field
│   │   ├── ChatBubble.tsx    # Individual message bubbles
│   │   └── ConnectionStatus.tsx # Shows connection status
│   ├── contexts/
│   │   └── ChatContext.tsx   # Manages chat state
│   ├── utils/
│   │   └── rasaUtils.ts      # API communication with Rasa
│   ├── App.tsx               # Main application component
│   ├── index.tsx             # Application entry point
│   ├── index.css             # Global styles and Tailwind imports
│   └── config.ts             # Configuration settings
├── public/
├── package.json
└── .env                      # Environment variables
```

### Key Components Explained

**App.tsx** - Main application:

```tsx
function App() {
  return (
    <ChatProvider>
      <div className="chat-container">
        <ConnectionStatus />
        <ChatArea />
        <TextArea />
      </div>
    </ChatProvider>
  );
}
```

**ChatContext.tsx** - Manages chat state:

```tsx
const ChatContext = createContext({
  messages: [],
  sendMessage: (text: string) => {},
  isConnected: false,
});
```

**rasaUtils.ts** - Communicates with Rasa:

```typescript
export const sendMessageToRasa = async (message: string) => {
  const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sender: "user",
      message: message,
    }),
  });
  return response.json();
};
```

### Environment Configuration

Create a `.env` file:

```env
REACT_APP_RASA_URL=http://localhost:5005
REACT_APP_BOT_NAME=Student Support Bot
```

### Running the React Frontend

```bash
# Development mode
npm run dev
# or
yarn dev

# Production build
npm run build
npm run preview
```

### How React Communicates with Rasa

1. **User Input** - User types message in TextArea component
2. **Send to Rasa** - rasaUtils.ts sends POST request to Rasa webhook
3. **Receive Response** - Rasa sends back response with text/buttons/images
4. **Display Response** - ChatArea component displays the bot's response
5. **Update State** - ChatContext updates the conversation history

## Running the Complete System

### Step 1: Start Rasa Backend

```bash
# Terminal 1 - Start action server (if you have custom actions)
cd rasa-backend
rasa run actions

# Terminal 2 - Start Rasa API server
cd rasa-backend
rasa run --enable-api --cors "*"
```

### Step 2: Start React Frontend

```bash
# Terminal 3 - Start React development server
cd react-frontend
npm run dev
```

### Step 3: Test the System

1. Open browser to `http://localhost:5173`
2. Type a message in the chat interface
3. See the bot respond based on your Rasa training

## Customization

### Adding New Bot Capabilities (Rasa)

1. **Add training examples** in `data/nlu.yml`:

   ```yaml
   - intent: ask_about_drugs
     examples: |
       - tell me about drug abuse
       - what are the dangers of drugs
       - drug addiction help
   ```

2. **Add responses** in `domain.yml`:

   ```yaml
   responses:
     utter_drug_info:
       - text: "Drug abuse can have serious health consequences..."
   ```

3. **Create conversation flow** in `data/stories.yml`:

   ```yaml
   - story: drug information
     steps:
       - intent: ask_about_drugs
       - action: utter_drug_info
   ```

4. **Retrain the model:**
   ```bash
   rasa train
   ```

### Customizing the React Interface

1. **Change colors/styling** - Modify Tailwind classes in components
2. **Add new message types** - Update ChatBubble component
3. **Modify layout** - Adjust App.tsx structure
4. **Add features** - Create new components and integrate them

## Testing

### Test Rasa

```bash
# Test in command line
rasa shell

# Test specific components
rasa test nlu
rasa test core
```

### Test React

```bash
# Run tests
npm test

# Manual testing
# Open browser and interact with the chat interface
```

## Troubleshooting

### Common Rasa Issues

- **"No model found"** - Run `rasa train` first
- **Action server not responding** - Make sure `rasa run actions` is running
- **Bot gives generic responses** - Check your training data and retrain

### Common React Issues

- **"Connection failed"** - Make sure Rasa server is running on correct port
- **CORS errors** - Make sure Rasa is started with `--cors "*"`
- **Messages not displaying** - Check browser console for JavaScript errors

### Connection Issues

- Rasa default port: `5005`
- React default port: `5173`
- Make sure both servers are running
- Check firewall settings

## Important Notes

- **This is a support tool, not a replacement for professional help**
- Always provide emergency contact information
- Test thoroughly before deploying to students
- Keep conversation logs private and secure
- Regularly update contact information and resources
