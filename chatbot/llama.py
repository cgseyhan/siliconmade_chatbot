# Gerekli kütüphane
from llama_cpp import Llama  # LLaMA modelini çalıştırmak için

# LlamaChatbot adında bir sınıf tanımlıyoruz
class LlamaChatbot:
    
    def __init__(self, model_path: str):
        # Llama sınıfını kullanarak modeli başlatıyoruz
        self.model = Llama(
            model_path=model_path,  # Kullanılacak GGUF modelinin yolu
            n_ctx=2048,             # Token sayısı
            n_threads=4,            # Kullanılacak CPU sayısı
            verbose=False           # Ayrıntılı loglama
        )

    # Sistem ve kullanıcı girdilerinden tam bir prompt oluşturan yardımcı fonksiyon
    def build_prompt(self, system_prompt: str, user_input: str) -> str:

        # LLaMA'nın özel biçimlendirmesine uygun olarak tam prompt metni oluşturulur
        full_prompt = (
            "<|begin_of_text|>"                            
            "<|start_header_id|>system<|end_header_id|>\n" 
            f"{system_prompt}\n"                           
            "<|eot_id|>"                                   
            "<|start_header_id|>user<|end_header_id|>\n"   
            f"{user_input}\n"                              
            "<|eot_id|>"                                   
            "<|start_header_id|>assistant<|end_header_id|>\n"  
        )

        return full_prompt  # Oluşturulan prompt döndürülür

    # Prompt'u oluşturur, modeli çalıştırır ve yanıtı döndürür
    def chat(self, system_prompt: str, user_input: str) -> str:
        prompt = self.build_prompt(system_prompt, user_input)      # Tam prompt oluşturulur
        output = self.model(prompt, stop=["<|eot_id|>"])           # Model çalıştırılır, <|eot_id|> görünce durması sağlanır
        return output["choices"][0]["text"].strip()                # Modelin çıktısından yanıt alınıp temizlenerek döndürülür