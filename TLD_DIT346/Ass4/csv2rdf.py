def devide_wiki_label(label):
    return label.split("/")[-1]
    
def devide_line(line, rdf_type, keys, key_types):
    line = line.strip('\n')
    split_line = line.split('\t')
    object_id = devide_wiki_label(split_line[0])
    rdf = f":{object_id} rdf:type :{rdf_type}"
    for it, word in enumerate(split_line[1:]):
        if key_types[it] == 'relation':
            rdf += f" ;\n:{keys[it]} :{devide_wiki_label(word)}"
        else:
            rdf += f" ;\n:{keys[it]} '{word}'"
    rdf += ".\n"
    return rdf

def write_output(output_file, output):
    with open(output_file, 'w') as f:
        for l in output:
            f.writelines(l)

def csv2rdf(text_file, rdf_type, keys, key_types):
    output = []
    with open(text_file, 'r') as f:
        for line in f:
            output.append(devide_line(line, rdf_type, keys, key_types))
    output_file = f"{text_file.split('.')[0]}.rdf"
    write_output(output_file, output)

if __name__ == "__main__":
    rdf_type = 'Person'
    text_file = f'{rdf_type}.tsv'
    keys = ['personName', 'alumnusOf', 'bornIn', 'employeeOf']
    key_types = ['str', 'relation', 'relation', 'relation']
    csv2rdf(text_file, rdf_type, keys, key_types)
