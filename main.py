from rag import tanya

print("📘 Academic RAG Chatbot (type 'exit' to quit)\n")

while True:
    q = input("You: ")
    if q.lower() == "exit":
        break
    print("\nBot:", tanya(q), "\n")
