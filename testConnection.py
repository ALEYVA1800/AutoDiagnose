import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role":"user","content":"Responde solo 'ok' si me escuchas"}]
)

print(response['message']['content'])
