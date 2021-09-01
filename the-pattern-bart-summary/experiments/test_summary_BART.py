summarization = None

def loadSummarization():
    from transformers import pipeline
    global summarization
    summarization = pipeline("summarization")
    return summarization


def parse_sentence():
    global summarization
    if not summarization:
        summarization=loadSummarization()
    full_text = """At a very high level, one of the most critical steps in any ML pipeline is called AI serving, a task usually performed by an AI inference engine. The AI inference engine is responsible for the model deployment and performance monitoring steps in the figure above, and represents a whole new world that will eventually determine whether applications can use AI technologies to improve operational efficiencies and solve real business problems. """
    summary_text = summarization(full_text)[0]['summary_text']
    print(summary_text)


def main():
    parse_sentence()

if __name__ == "__main__":
    main()
