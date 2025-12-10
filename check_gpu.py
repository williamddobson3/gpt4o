"""
Script to check GPU availability and CUDA setup
"""
import sys

try:
    import torch
    
    print("=" * 60)
    print("GPU/CUDA Check")
    print("=" * 60)
    
    print(f"\nPyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"cuDNN version: {torch.backends.cudnn.version()}")
        print(f"Number of GPUs: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"\nGPU {i}:")
            print(f"  Name: {torch.cuda.get_device_name(i)}")
            print(f"  Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
            print(f"  Compute Capability: {torch.cuda.get_device_properties(i).major}.{torch.cuda.get_device_properties(i).minor}")
        
        # Test GPU allocation
        print("\n" + "-" * 60)
        print("Testing GPU allocation...")
        try:
            test_tensor = torch.randn(1000, 1000).cuda()
            print("✓ GPU allocation successful!")
            del test_tensor
            torch.cuda.empty_cache()
        except Exception as e:
            print(f"✗ GPU allocation failed: {e}")
    else:
        print("\n⚠ No CUDA-capable GPU detected.")
        print("The chatbot will run on CPU (slower performance).")
        print("\nTo use GPU, ensure:")
        print("1. NVIDIA GPU is installed")
        print("2. NVIDIA drivers are installed (nvidia-smi should work)")
        print("3. CUDA toolkit is installed")
        print("4. PyTorch with CUDA support is installed")
    
    print("\n" + "=" * 60)
    
except ImportError:
    print("Error: PyTorch is not installed.")
    print("Install it with: pip install torch")
    sys.exit(1)
except Exception as e:
    print(f"Error checking GPU: {e}")
    sys.exit(1)
