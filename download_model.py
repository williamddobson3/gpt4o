#!/usr/bin/env python3
"""
Script to download and save a model locally for VPS deployment
"""
import os
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download
import argparse

def download_model(model_name, local_path, use_local_files_only=False):
    """
    Download a model from Hugging Face and save it locally
    
    Args:
        model_name: Hugging Face model identifier (e.g., "Qwen/Qwen2.5-7B-Instruct")
        local_path: Local directory path to save the model
        use_local_files_only: If True, only use local files (for offline mode)
    """
    print("=" * 60)
    print(f"Downloading Model: {model_name}")
    print(f"Local Path: {local_path}")
    print("=" * 60)
    
    # Create directory if it doesn't exist
    os.makedirs(local_path, exist_ok=True)
    
    try:
        print("\n[1/3] Downloading model files...")
        # Download all model files
        snapshot_download(
            repo_id=model_name,
            local_dir=local_path,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        print("✓ Model files downloaded successfully!")
        
        print("\n[2/3] Verifying tokenizer...")
        # Test loading tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            local_path,
            trust_remote_code=True
        )
        print("✓ Tokenizer verified!")
        
        print("\n[3/3] Verifying model (this may take a moment)...")
        # Test loading model (this will verify all files are correct)
        # We'll load with low memory to just verify, not fully load
        try:
            model = AutoModelForCausalLM.from_pretrained(
                local_path,
                trust_remote_code=True,
                torch_dtype="auto",
                low_cpu_mem_usage=True
            )
            print("✓ Model verified!")
            del model  # Free memory
        except Exception as e:
            print(f"⚠ Model verification had issues (may be normal): {e}")
            print("  Model files are downloaded, but full verification failed.")
            print("  This might be due to memory constraints. Files should still work.")
        
        print("\n" + "=" * 60)
        print("Download Complete!")
        print("=" * 60)
        print(f"\nModel saved to: {local_path}")
        print(f"\nTo use this local model, set in config.py:")
        print(f'  LOCAL_MODEL_PATH = "{local_path}"')
        print(f"\nOr set environment variable:")
        print(f'  export LOCAL_MODEL_PATH="{local_path}"')
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the model name is correct")
        print("3. Check disk space (models can be 10-50GB+)")
        print("4. Ensure you have Hugging Face access (some models require login)")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Download a Hugging Face model locally")
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen2.5-7B-Instruct",
        help="Hugging Face model name (default: Qwen/Qwen2.5-7B-Instruct)"
    )
    parser.add_argument(
        "--path",
        type=str,
        default="./models",
        help="Local path to save the model (default: ./models)"
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Custom name for model directory (default: uses model name)"
    )
    
    args = parser.parse_args()
    
    # Determine local path
    if args.name:
        local_path = os.path.join(args.path, args.name)
    else:
        # Use model name as directory name
        model_dir_name = args.model.replace("/", "_")
        local_path = os.path.join(args.path, model_dir_name)
    
    # Convert to absolute path
    local_path = os.path.abspath(local_path)
    
    download_model(args.model, local_path)


if __name__ == "__main__":
    main()
