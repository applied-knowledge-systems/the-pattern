
def loadAutomata():
    from urllib.request import urlopen
    import ahocorasick 
    import joblib

    try:
        Automata=joblib.load("/tmp/automata_fresh_semantic.pkl.lzma")
    except:
        automata_file=urlopen("https://s3.eu-west-2.amazonaws.com/assets.thepattern.digital/automata_fresh_semantic.pkl.lzma")
        
        with open('/tmp/automata_fresh_semantic.pkl.lzma', 'wb') as f:
            f.write(automata_file.read())
        Automata=joblib.load("/tmp/automata_fresh_semantic.pkl.lzma")    
    return Automata

def find_matches(sent_text, A):
    matched_ents = []
    for char_end, (eid, ent_text) in A.iter_long(sent_text):
        char_start = char_end - len(ent_text)
        matched_ents.append((eid, ent_text, char_start, char_end))
    # remove shorter subsumed matches
    longest_matched_ents = []
    for matched_ent in sorted(matched_ents, key=lambda x: len(x[1]), reverse=True):
        longest_match_exists = False
        char_start, char_end = matched_ent[2], matched_ent[3]
        for _, _, ref_start, ref_end in longest_matched_ents:
            if ref_start <= char_start and ref_end >= char_end:
                longest_match_exists = True
                break
        if not longest_match_exists:
            # print("adding match to longest")
            longest_matched_ents.append(matched_ent)
    return [t for t in longest_matched_ents if len(t[1])>3] 

Automata=loadAutomata()