'''
Utilities used by living

insert_names: insert a string into a comma-separated charfield
'''

def insert_names(names,name,index=0,max_length=65536):
    if names == '':
        return name
    while len(names)+len(name)>max_length:
        names = names[:names.rfind(',')]
    if index == 0:
        return name+','+names
    elif index == -1:
        return names+','+name
    else:
        names = names.split(',')
        names.insert(index,name)
        return ','.join(names)
