"""
xsv sample 10 2019AB/META/MRXW_ENG.RRF 
ENG|00000000|C5058512|L15639228|S18854984|
ENG|hgb|C0366824|L8892799|S11033629|
ENG|non|C0551055|L13462529|S16447050|
ENG|alcoholism||L0369748|S11847136|
ENG|igm|C1114011|L8557735|S10626593|
ENG|right||L8372651|S10420300|
ENG|8|C0646154|L1123160|S1349583|
ENG|mg|C3535033|L15196909|S18475089|
ENG|netilmicin||L5128002|S5827499|
ENG|x0026f3541|C5187483|L15917136|S19226683|
ENG|candida|C3592103|L11149228|S13783596|

"""
from automata.utils import loadAutomata, find_matches

test_tokens=[('alcoholism','C0476560'),('right','C2478367'),('netilmicin','C1318089'),('candida','C3592103'),('phenyl','C0050987'),('aaq2659','C4186045'),('bampurensis','C3357913')]

Automata=loadAutomata()
for each_test_token in test_tokens:
    matched=find_matches(each_test_token[0], Automata)
    print(matched)
    print(each_test_token[1])
    # assert(each_test_token[1]==matched[0][0])
