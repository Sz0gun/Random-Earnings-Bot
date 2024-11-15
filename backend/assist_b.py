import openai
import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

try:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    openai.api_key = os.getenv("OPENAI_API_KEY")
except Exception as e:
    print(f"Error with environment variables: {e}")

# Initialize Telegram client
client = TelegramClient(session=None, api_id=API_ID, api_hash=API_HASH).start(bot_token=TELEGRAM_BOT_TOKEN)

# Dictionary to store user conversations
user_conversations = defaultdict(list)

# Function to generate response using OpenAI API (corrected)
async def generate_response(user_id, message):
    # Add user message to conversation history
    user_conversations[user_id].append({
        "role": "user",
        "content": message
    })
    
    # Build the conversation history (messages field)
    messages = [{"role": "user", "content": message}]
    for entry in user_conversations[user_id]:
        messages.append(entry)

    try:
        # Corrected OpenAI API call for chat models (use `chat/completions.create()`)
        # Run the OpenAI API call in a separate thread to avoid blocking
        response = await asyncio.to_thread(openai.ChatCompletion.create,
                                           model="gpt-4o",  # Use the appropriate chat model (e.g., gpt-4)
                                           messages=messages,  # Messages field to simulate conversation
                                           max_tokens=150,  # Adjust token limit
                                           temperature=0.7)  # Adjust temperature for response creativity

        reply = response['choices'][0]['message']['content'].strip()  # Extract the assistant's response
        
        # Add assistant's response to the conversation history
        user_conversations[user_id].append({
            "role": "assistant", "content": reply
        })

        return reply

    except Exception as e:
        print(f"Error in generating response: {e}")
        return f"An error occurred: {e}"

# Function to handle new messages
@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id  # Get the user ID
    user_message = event.message.text  # Get the message text

    print(f"Received message from {user_id}: {user_message}")

    # Generate a response via OpenAI (async)
    response_text = await generate_response(user_id, user_message)
    print(f"Generated response: {response_text}")

    # Send the generated response back to the user
    await event.respond(response_text)

# Start the Telegram client
async def main():
    await client.start()
    await client.run_until_disconnected()

# Run the client without using asyncio.run (use Telethon's loop)
if __name__ == "__main__":
    client.loop.run_until_complete(main())
