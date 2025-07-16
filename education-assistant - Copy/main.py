# main.py
from educator.rag_pipeline import legal_education_rag

if __name__ == "__main__":
    query = input("Enter a legal question: ")
    answer = legal_education_rag(query)
    print("\n🔍 Answer:\n", answer)
