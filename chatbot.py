"""
Chatbot implementation using Xenova/gpt-4o model
"""
import torch
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings("ignore")

from config import (
    MODEL_NAME,
    LOCAL_MODEL_PATH,
    DEVICE,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
    DO_SAMPLE,
    SYSTEM_PROMPT,
    MAX_HISTORY_LENGTH,
    LOAD_IN_8BIT,
    LOAD_IN_4BIT,
    TRUST_REMOTE_CODE
)


class ChatBot:
    """Chatbot class using Xenova/gpt-4o model"""
    
    def __init__(self):
        """Initialize the chatbot with the model"""
        # Determine model path (local or Hugging Face)
        if LOCAL_MODEL_PATH and os.path.exists(LOCAL_MODEL_PATH):
            model_path = LOCAL_MODEL_PATH
            print(f"Loading model from local path: {model_path}")
        else:
            model_path = MODEL_NAME
            if LOCAL_MODEL_PATH:
                print(f"Warning: Local model path '{LOCAL_MODEL_PATH}' not found, using Hugging Face: {MODEL_NAME}")
            else:
                print(f"Loading model from Hugging Face: {MODEL_NAME}")
        
        print(f"Device: {DEVICE}")
        
        try:
            # Load tokenizer
            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=TRUST_REMOTE_CODE
            )
            
            # Set pad token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            if LOCAL_MODEL_PATH and os.path.exists(LOCAL_MODEL_PATH):
                print("Loading model from local storage...")
            else:
                print("Loading model (this may take a while on first run - downloading from Hugging Face)...")
            
            model_kwargs = {
                "trust_remote_code": TRUST_REMOTE_CODE,
            }
            
            # Set dtype based on device
            if DEVICE == "cuda" and torch.cuda.is_available():
                model_kwargs["torch_dtype"] = torch.float16
                model_kwargs["device_map"] = "auto"
            else:
                model_kwargs["torch_dtype"] = torch.float32
                model_kwargs["device_map"] = None
            
            # Handle quantization
            if LOAD_IN_8BIT:
                try:
                    from transformers import BitsAndBytesConfig
                    model_kwargs["load_in_8bit"] = True
                    model_kwargs["quantization_config"] = BitsAndBytesConfig(load_in_8bit=True)
                except ImportError:
                    print("Warning: bitsandbytes not available, loading in full precision")
            elif LOAD_IN_4BIT:
                try:
                    from transformers import BitsAndBytesConfig
                    model_kwargs["load_in_4bit"] = True
                    model_kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True)
                except ImportError:
                    print("Warning: bitsandbytes not available, loading in full precision")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                **model_kwargs
            )
            
            # Move to device if not using device_map
            if model_kwargs.get("device_map") is None:
                self.model = self.model.to(DEVICE)
            
            self.model.eval()
            
            # Initialize conversation history
            self.conversation_history: List[Dict[str, str]] = []
            
            print("Model loaded successfully!")
            print(f"Model is using device: {next(self.model.parameters()).device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("\nTroubleshooting tips:")
            print("1. Check your internet connection (model needs to be downloaded)")
            print("2. Verify the model name is correct on Hugging Face")
            print("3. Ensure you have enough disk space for the model")
            print("4. Check if you have sufficient RAM/VRAM")
            raise
    
    def format_prompt(self, user_message: str) -> str:
        """Format the prompt with system message and conversation history"""
        # Try to use the model's chat template if available
        if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template is not None:
            # Prepare messages for chat template
            messages = []
            
            # Add system message if history is empty
            if not self.conversation_history:
                messages.append({"role": "system", "content": SYSTEM_PROMPT})
            
            # Add recent conversation history
            recent_history = self.conversation_history[-MAX_HISTORY_LENGTH:]
            for msg in recent_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Apply chat template
            formatted = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            return formatted
        else:
            # Fallback to simple formatting
            if not self.conversation_history:
                formatted = f"{SYSTEM_PROMPT}\n\n"
            else:
                formatted = ""
            
            # Add recent conversation history
            recent_history = self.conversation_history[-MAX_HISTORY_LENGTH:]
            for msg in recent_history:
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    formatted += f"User: {content}\n"
                elif role == "assistant":
                    formatted += f"Assistant: {content}\n"
            
            # Add current user message
            formatted += f"User: {user_message}\nAssistant:"
            
            return formatted
    
    def generate_response(self, user_message: str) -> str:
        """Generate a response to the user message"""
        try:
            # Format prompt
            prompt = self.format_prompt(user_message)
            
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048
            ).to(DEVICE)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=MAX_NEW_TOKENS,
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                    do_sample=DO_SAMPLE,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode response
            generated_text = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            ).strip()
            
            # Clean up response (remove any trailing user/assistant labels and special tokens)
            generated_text = generated_text.split("User:")[0].strip()
            generated_text = generated_text.split("Assistant:")[0].strip()
            
            # Remove common chat template artifacts
            for token in ["<|im_end|>", "<|endoftext|>", "</s>", "<|end|>"]:
                if generated_text.endswith(token):
                    generated_text = generated_text[:-len(token)].strip()
            
            return generated_text
            
        except Exception as e:
            return f"Error generating response: {e}"
    
    def chat(self, user_message: str) -> str:
        """Main chat method that handles conversation history"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Generate response
        response = self.generate_response(user_message)
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation history cleared.")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history.copy()
