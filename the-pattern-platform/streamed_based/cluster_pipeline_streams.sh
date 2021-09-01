gears-cli run --host 127.0.0.1 --port 30001 lang_detect_gears_paragraphs.py --requirements requirements_gears_lang.txt
gears-cli run --host 127.0.0.1 --port 30001 spacy_sentences_streams.py --requirements requirements_gears_spacy.txt
echo "spacy_sentences_streams.py registered."
gears-cli run --host 127.0.0.1 --port 30001 symspell_sentences_streamed.py --requirements requirements_gears_symspell.txt
echo "symspell_sentences_streamed.py registered."
gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_streamed.py --requirements requirements_gears_aho.txt
echo "sentences_matcher_streamed.py registered."
sleep 10 
echo "10 seconds for cluster to recover"
gears-cli run --host 127.0.0.1 --port 30001 edges_to_graph_streamed.py --requirements requirements_gears_graph.txt
echo "edges_to_graph_streamed.py registered"
