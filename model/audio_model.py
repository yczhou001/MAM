from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
torch.manual_seed(1234)

class AudioChatbot():
    def __init__(self, cache_path='/your/cache/path', device="cuda"):
        self.cache_path = cache_path
        self.device = device
    def chat(self, audio: str, text: str):
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-Audio-Chat",cache_dir=self.cache_path, trust_remote_code=True)


        model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio-Chat",cache_dir=self.cache_path, device_map=self.device, trust_remote_code=True).eval()


        query = tokenizer.from_list_format([
            {'audio': audio}, 
            {'text': text}
        ])
        response, history = model.chat(tokenizer, query=query, history=None)
        return response
