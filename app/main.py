import requests


def ask_llm(question):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "codellama",
        "prompt": question,
        "stream": False
    }

    response = requests.post(url, json=data)

    result = response.json()

    return result["response"]


question = input("Ask CampusAI a question: ")

answer = ask_llm(question)

print("\nCampusAI:")
print(answer)