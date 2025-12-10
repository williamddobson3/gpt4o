"""
Main entry point for the chatbot CLI
"""
import sys
from chatbot import ChatBot


def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("  GPT-4o Chatbot (Xenova/gpt-4o)")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type your message and press Enter to chat")
    print("  - Type '/clear' to clear conversation history")
    print("  - Type '/history' to view conversation history")
    print("  - Type '/exit' or '/quit' to exit")
    print("  - Type '/help' to show this help message")
    print("\n" + "=" * 60 + "\n")


def print_history(chatbot: ChatBot):
    """Print conversation history"""
    history = chatbot.get_history()
    if not history:
        print("No conversation history.")
        return
    
    print("\n" + "-" * 60)
    print("Conversation History:")
    print("-" * 60)
    for i, msg in enumerate(history, 1):
        role = msg["role"].capitalize()
        content = msg["content"]
        print(f"\n[{i}] {role}:")
        print(f"    {content}")
    print("-" * 60 + "\n")


def main():
    """Main function"""
    print_welcome()
    
    try:
        # Initialize chatbot
        chatbot = ChatBot()
        print("\nChatbot is ready! Start chatting...\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ["/exit", "/quit"]:
                    print("\nGoodbye!")
                    break
                
                elif user_input.lower() == "/clear":
                    chatbot.clear_history()
                    continue
                
                elif user_input.lower() == "/history":
                    print_history(chatbot)
                    continue
                
                elif user_input.lower() == "/help":
                    print_welcome()
                    continue
                
                # Generate and print response
                print("\nAssistant: ", end="", flush=True)
                response = chatbot.chat(user_input)
                print(response)
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except EOFError:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
                continue
    
    except Exception as e:
        print(f"Failed to initialize chatbot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
