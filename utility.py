import requests

def check_ollama_status():
    MODEL_NAME = "llama3.1:8b"
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            if MODEL_NAME in model_names:
                print(f"Ollama is running. Model '{MODEL_NAME}' is available.")
                return True
            else:
                print(f"Ollama is running, but model '{MODEL_NAME}' is not found.")
                print(f"Available models: {', '.join(model_names)}")
                print(f"\nTo download the model, run:")
                print(f"  ollama pull {MODEL_NAME}")
                return False
        else:
            print("Ollama is not responding correctly.")
            return False
    except requests.exceptions.ConnectionError:
        print("Cannot connect to Ollama. Please ensure Ollama is running.")
        print("\nTo start Ollama:")
        print("  1. Download from: https://ollama.ai")
        print("  2. Run: ollama serve")
        print(f"  3. Pull model: ollama pull {MODEL_NAME}")
        return False
    except Exception as e:
        print(f"Error checking Ollama: {str(e)}")
        return False
