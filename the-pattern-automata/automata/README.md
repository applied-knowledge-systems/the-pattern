# Aho-Corasick 

Scripts to import UMLS Metathesaurus into Aho-Corasick into Redis cluster

Highly experimental - relevance isn't up to scratch or usable

need to run 

```
sudo mysql  umls_meta --skip-column-names --raw  < cui_term.sql | redis-cli -p 30004 --pipe
```
on all nodes. 
For demo load to single node:

```
sudo mysql  umls_meta --skip-column-names --raw  < cui_term.sql | redis-cli -h 10.144.17.211 --pipe 
```

To Extract All search terms for building Aho-Corasick automata:

```
#dump all words to CUI into file for Aho Corasick Automata
sudo mysql --skip-column-names --raw umls_meta -e "select WD, CUI from MRXW_ENG" >words_cui.tsv
```
# So far best performing Aho-Corasick automata is made using query above and aho_corasick_create_canonical_semantic.py

To install UMLS Metathesaurus follow: 
https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/index.html


Select canonical names for concepts from UMLS

'''
select CUI, STR from MRCONSO where LAT='ENG' AND TS='P' AND STT='PF' AND ISPREF='Y' limit 5
'''

```
select a.CUI, a.STR from MRCONSO a, MRREL b where a.cui=b.cui2 AND a.LAT='ENG' AND a.TS='P' AND a.STT='PF' AND a.ISPREF='Y' limit 5

SELECT * FROM MRREL WHERE cui2 = 'C0032344' AND stype2 = 'AUI'

```

```
sudo mysql --raw umls_meta  -e "select a.CUI, a.STR,b.* from MRCONSO a, MRREL b where a.cui=b.cui1 AND b.STYPE1='AUI' AND a.LAT='ENG' AND a.TS='P' AND a.STT='PF' AND a.ISPREF='Y' limit 5"
```
Find atom matching a word (non normalised)
```
SELECT b.* FROM MRXW_ENG a, MRCONSO b WHERE a.wd = 'bleeding' AND a.cui = b.cui AND a.sui = b.sui AND b.LAT='ENG' AND b.TS='P' AND b.STT='PF' AND b.ISPREF='Y';
```
(count 7127 for just bleeding)
todo: Find atom matching a word with canonical concept 

1. Find atoms matching a normalized string.

SELECT b.* FROM MRXNS_ENG a, MRCONSO b
WHERE a.nstr = 'abnormal bleed'
     AND a.cui = b.cui
     AND a.lui = b.lui;
sudo mysql --raw umls_meta  -e "SELECT a.nstr,a.cui,b.* FROM MRXNS_ENG a, MRCONSO b WHERE a.nstr = 'abnormal bleed' AND a.cui = b.cui AND a.lui = b.lui;"

sudo mysql --raw umls_meta  -e "SELECT a.nstr,a.cui,b.STR FROM MRXNS_ENG a, MRCONSO b WHERE a.nstr = 'abnormal bleed' AND a.cui = b.cui AND a.lui = b.lui AND b.LAT='ENG' AND b.TS='P' AND b.STT='PF' AND b.ISPREF='Y' ORDER BY CHAR_LENGTH(b.STR);"

select non normalised term, cui and canonical name

sudo mysql --raw umls_meta  -e "SELECT a.wd,a.cui,b.STR FROM MRXW_ENG a, MRCONSO b WHERE a.wd = 'bleeding' AND a.cui = b.cui AND a.sui = b.sui AND b.LAT='ENG' AND b.TS='P' AND b.STT='PF' AND b.ISPREF='Y' ORDER BY CHAR_LENGTH(b.STR);"

sudo mysql --raw umls_meta  -e "SELECT distinct a.wd, b.cui FROM MRXW_ENG a, MRCONSO b WHERE a.wd = 'bleeding' AND a.cui = b.cui AND a.sui = b.sui AND b.LAT='ENG' AND b.TS='P' AND b.STT='PF' AND b.ISPREF='Y';"

sudo mysql --raw umls_meta  -e "SELECT distinct a.wd, b.cui FROM MRXW_ENG a, MRCONSO b, MRREL c WHERE a.wd = 'bleeding' AND a.cui = b.cui AND a.sui = b.sui AND b.LAT='ENG' AND b.TS='P' AND b.STT='PF' AND b.ISPREF='Y' AND a.cui=c.cui1 and c.STYPE1='SCUI';"

SELECT distinct a.wd, b.cui FROM MRXW_ENG a, MRCONSO b, MRREL c WHERE a.wd = 'bleeding' AND a.cui = b.cui AND a.sui = b.sui AND b.LAT='ENG' AND b.TS='P' AND b.STT='PF' AND b.SAB = 'MTH' and b.TTY = 'CV' AND b.ISPREF='Y' AND a.cui=c.cui1 and c.STYPE1='SCUI';

SELECT c.* FROM MRCONSO a, MRSAT b, MRCONSO c, MRXW_ENG d WHERE a.sab = 'MTH' AND a.tty = 'CV' AND a.str = 'MetaMap NLP View' AND a.cui = b.cui AND a.cui=d.cui and d.wd="bleeding" AND b.atn = 'CV_CODE' AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.ISPREF='Y' limit 5;

select distinct a.wd, a.cui,b.*  from MRXW_ENG a, MRSTY b where a.cui=b.cui limit 5;

SELECT distinct d.wd, d.cui FROM MRCONSO a, MRSAT b, MRXW_ENG d WHERE a.sab = 'MTH' AND a.tty = 'CV' AND a.cui = b.cui AND a.cui=d.cui AND b.atn = 'CV_CODE' limit 5

select a.wd, a.cui,b.* from MRXW_ENG a, MRSTY b, MRCONSO c where a.cui=b.cui AND a.cui=c.cui AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.ISPREF='Y' ORDER BY CHAR_LENGTH(c.STR) limit 5;

select distinct a.wd, a.cui,c.cui, c.str from MRXW_ENG a, MRCONSO c where a.cui=c.CUI AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.TTY="PN" AND c.ISPREF='Y'

Try:
- [ ] anst|T017|Anatomical Structure
- [ ] dsyn|T047|Disease or Syndrome
- [ ] bpoc|T023|Body Part, Organ, or Organ Component 
- [ ] diap|T060|Diagnostic Procedure
SET @list='T017,T047,T023,T060';

SELECT b.* FROM MRSTY b, MRCONSO c where b.cui=c.cui AND FIND_IN_SET(b.tui, @list) > 0 limit 5; 
SELECT a.wd,b.* FROM MRXW_ENG a, MRSTY b, MRCONSO c where a.cui=b.cui and b.cui=c.cui AND FIND_IN_SET(b.tui, @list) > 0 limit 5;


SELECT distinct a.wd,b.TUI, b.STN,b.STY FROM MRXW_ENG a, MRSTY b, MRCONSO c where a.cui=b.cui and a.lui=c.lui and b.cui=c.cui AND FIND_IN_SET(b.tui, @list) > 0 AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.ISPREF='Y' limit 5;

select distinct a.nstr, a.cui from MRXNS_ENG a, MRCONSO c where a.cui=c.CUI AND a.lui=c.lui AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.TTY="PN" AND c.ISPREF='Y'AND c.CODE='NOCODE' limit 5;


select distinct a.nstr, a.cui from MRXNS_ENG a, MRCONSO c where a.cui=c.CUI AND a.lui=c.lui AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.TTY="PN" AND c.ISPREF='Y'AND c.CODE='NOCODE' limit 5;


select distinct a.wd, a.cui,c.str from MRXW_ENG a, MRCONSO c where a.cui=c.CUI AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.TTY="PN" AND c.ISPREF='Y' limit 5;
select distinct a.wd, a.cui,c.str from MRXW_ENG a, MRSTY b, MRCONSO c where a.cui=b.cui AND a.cui=c.CUI AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.TTY="PN" AND c.ISPREF='Y' AND FIND_IN_SET(b.tui, @list) > 0 limit 5;


CREATE TABLE IF NOT EXISTS MRSTY_MRCONSO AS (select distinct a.wd, a.cui,c.str from MRXW_ENG a, MRSTY b, MRCONSO c where a.cui=b.cui AND a.cui=c.CUI AND c.LAT='ENG' AND c.TS='P' AND c.STT='PF' AND c.TTY="PN" AND c.ISPREF='Y' AND FIND_IN_SET(b.tui, @list) > 0 );

select distinct wd, cui from MRSTY_MRCONSO where CHAR_LENGTH(wd)>4 group by wd HAVING COUNT(wd) > 1 order by CHAR_LENGTH(wd) limit 100;


# Final solution
(to be validated)
```
sudo mysql --skip-column-names  --raw umls_meta  -e "select STR, CUI from MRCONSO where LAT='ENG' AND TS='P' AND STT='PF' AND ISPREF='Y'" >canonical_str_cui.tsv
sudo mysql --skip-column-names  --raw umls_meta  -e "select distinct wd, cui from MRSTY_MRCONSO where CHAR_LENGTH(wd)>4 group by wd HAVING COUNT(wd) > 1 order by CHAR_LENGTH(wd) DESC" >canonical_str_cui_semantic.tsv

select distinct wd, cui from MRSTY_MRCONSO where CHAR_LENGTH(wd)>4 group by wd HAVING COUNT(wd) > 1 order by CHAR_LENGTH(wd)
```

# TODO:

- [ ] test wd (non normalised term) and nd - normalised term for aho-corasick
- [ ] another approach is to select relevant dictionary based on role: Defined Role (Surgeon vs Radiologist vs Nurse), select relevant semantic layer from UMLS (based on Semantic Types: Sign or Symptom) and then select corresponding wd or nstr
- [ ] try to limit scope to person, decease and diagnosis
- [ ] make sure stopwords are filtered

Latest Automata available: 

https://s3.eu-west-2.amazonaws.com/assets.thepattern.digital/automata_syns.lzma
both produce good enough results:
- automata_syns.lzma - no filtering applied (filtering on matching)
- automata_fresh_words_cui.pkl - filtered less than 4 characters, not stop words


# References
- https://github.com/NCBI-Codeathons/Use-UMLS-and-Python-to-classify-website-visitor-queries-into-measurable-categories
Top search categories
     - Disease or Syndrome 
     - Intellectual Product
     - Theraputic or Preventive procedure
     - Body location or region
     - Body Part, Organ or Organ Compoment
     - Clinical attribute
     - Functional Concept
     - Manufactured Object 
     - Organism Attribute
     - Plant 

https://github.com/OHDSI/CommonEvidenceModel

https://metamap.nlm.nih.gov/Docs/SemanticTypes_2018AB.txt
https://github.com/OHDSI/KnowledgeBase
https://github.com/OHDSI/KnowledgeBase/blob/master/LAERTES/SemMED/UMLS-semantic-network-SRDEF.txt
https://gist.github.com/joelkuiper/4869d148333f279c2b2e
