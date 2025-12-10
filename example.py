"""
Example script showing how to use the ChatBot class programmatically
"""
from chatbot import ChatBot


def main():
    # Initialize chatbot
    chatbot = ChatBot()
    
    # Example conversation
    messages = [
        "Hello! What can you do?",
        "Can you explain what machine learning is?",
        "Thank you!"
    ]
    
    print("\n" + "=" * 60)
    print("Example Conversation")
    print("=" * 60 + "\n")
    
    for message in messages:
        print(f"User: {message}")
        response = chatbot.chat(message)
        print(f"Assistant: {response}\n")
    
    # Show history
    print("\n" + "=" * 60)
    print("Conversation History:")
    print("=" * 60)
    history = chatbot.get_history()
    for i, msg in enumerate(history, 1):
        print(f"\n[{i}] {msg['role'].capitalize()}: {msg['content']}")


if __name__ == "__main__":
    main()
