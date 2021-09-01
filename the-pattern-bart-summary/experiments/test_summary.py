from transformers import T5ForConditionalGeneration, T5Tokenizer

def main():

    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    # T5 uses a max_length of 512 so we cut the article to 512 tokens.
    text = """At a very high level, one of the most critical steps in any ML pipeline is called AI serving, a task usually performed by an AI inference engine. The AI inference engine is responsible for the model deployment and performance monitoring steps in the figure above, and represents a whole new world that will eventually determine whether applications can use AI technologies to improve operational efficiencies and solve real business problems. """
    inputs = tokenizer.encode("summarize: " + text, max_length=512, truncation=True)
    outputs = model.generate(torch.tensor([inputs]), max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(output)
if __name__ == "__main__":
    main()