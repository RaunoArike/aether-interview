from openai import OpenAI

client = OpenAI()

def main():
    file = client.files.create(
        file=open("training.jsonl", "rb"),
        purpose="fine-tune"
    )
    client.fine_tuning.jobs.create(
        training_file=file.id,
        model="gpt-4o-mini-2024-07-18"
    )

if __name__ == "__main__":
    main()
