import requests
import json
import os

# Função para chamar a API de IA
def call_ai_api(user_message):
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"  # Usando variável de ambiente
    }
    data = {
        "inputs": user_message  # Mensagem do usuário
    }

    # Chamada para a API Hugging Face, utilizando o modelo GPT-2 como exemplo
    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt2",  # Escolha o modelo desejado
        headers=headers,
        json=data
    )
    
    # Verificação de erro na resposta
    if response.status_code != 200:
        return f"Erro na API: {response.status_code}"
    
    response_data = response.json()
    return response_data[0]['generated_text']  # Extraindo a resposta do modelo

# Função para comentar no GitHub Issue
def post_comment_on_github(issue_number, comment):
    url = f"https://api.github.com/repos/Alexrocha666/Finanbot/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {os.getenv('MY_GITHUB_TOKEN')}"  # Usando o token do GitHub
    }
    data = {"body": comment}
    
    # Enviando o comentário para o issue no GitHub
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        return f"Comentário postado com sucesso!"
    else:
        return f"Erro ao postar comentário: {response.status_code}"

# Principal
def main():
    # Obtendo a mensagem do issue (este valor seria extraído automaticamente no GitHub)
    user_message = "Olá, como você está?"  # Exemplo estático

    # Chamar a IA para obter a resposta
    ai_response = call_ai_api(user_message)

    # Número do Issue - para testar, você pode substituir manualmente o número do issue
    issue_number = 1  # Substitua pela lógica de extração do número do issue (vem do evento GitHub)

    # Postar o comentário com a resposta gerada pela IA
    result = post_comment_on_github(issue_number, ai_response)
    print(result)

if __name__ == "__main__":
    main()
