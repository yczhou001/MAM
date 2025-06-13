import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class MedicalAssistant:
    def __init__(self, model_name="sethuiyer/Medichat-Llama3-8B", device="cuda"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        self.sys_message = ''' 
        You are an AI Medical Assistant trained on a vast dataset of health information. Please be thorough and
        provide an informative answer. If you don't know the answer to a specific medical inquiry, advise seeking professional help.
        '''

    def format_prompt(self, question, sys_message=None):
        if not sys_message:
            messages = [
                {"role": "system", "content": self.sys_message},
                {"role": "user", "content": question}
            ]
        else:
            messages = [
                {"role": "system", "content": sys_message},
                {"role": "user", "content": question}
            ]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return prompt

    def generate_response(self, question, sys_message=None, max_new_tokens=512):
        prompt = self.format_prompt(question, sys_message)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
        answer = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0].strip()
        answer = answer.split("<|im_start|>assistant\n")[-1].strip()
        return answer

if __name__ == "__main__":
    assistant = MedicalAssistant()
    question = '''
    Symptoms:
    Dizziness, headache, and nausea.

    What is the differential diagnosis?
    '''
    response = assistant.generate_response(question)
    print(response)
