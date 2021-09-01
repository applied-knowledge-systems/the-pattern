

def process_item(x):
    log(f"Shard ID {x}")
    log('shard id %s' % hashtag())
    execute('set','debug{%s}'% hashtag(),1)

bg = GearsBuilder('ShardsIDReader')
bg.foreach(process_item)
bg.count()
bg.run()
