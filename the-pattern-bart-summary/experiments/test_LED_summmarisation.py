from transformers import LEDTokenizer, LEDForConditionalGeneration, LEDConfig
model = LEDForConditionalGeneration.from_pretrained('allenai/led-base-16384')
tokenizer = LEDTokenizer.from_pretrained('allenai/led-base-16384')
full_text = """At a very high level, one of the most critical steps in any ML pipeline is called AI serving, a task usually performed by an AI inference engine. The AI inference engine is responsible for the model deployment and performance monitoring steps in the figure above, and represents a whole new world that will eventually determine whether applications can use AI technologies to improve operational efficiencies and solve real business problems. """
inputs = tokenizer([full_text], max_length=1024, return_tensors='pt')
# Generate Summary
summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=50, early_stopping=True)
print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids])