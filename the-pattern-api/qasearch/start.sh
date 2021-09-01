python export_load_bert.py
gears-cli run --host 127.0.0.1 --port 30001 tokeniser_gears_redisai.py --requirements requirements.txt
gears-cli run --host 127.0.0.1 --port 30001 qa_redisai_gear_map_keymiss_np.py
gears-cli run --host 127.0.0.1 --port 30001 tokeniser_gears_redisai_register.py --requirements requirements.txt 
# validate by redis-cli -c -p 30001 -h 127.0.0.1 get "bertqa{5M5}_PMC140314.xml:{5M5}:44_When air samples collected?"