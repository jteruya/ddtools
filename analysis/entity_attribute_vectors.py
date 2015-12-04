from csv import writer
from sys import argv

def csv_to_list(file_name):
  with open(file_name) as f:
    return [[item.strip() for item in line.split(',')] for line in f.readlines()[1:]]

def create_entity_attribute_vectors(entity_list,entity_attribute_list):

  entity_attribute_vectors = []
  for entity in entity_list:
    attribute_vector = []
    for entity_attribute in entity_attribute_list:
      entityid = entity_attribute[0]
      attribute = entity_attribute[1]
      flag = entity_attribute[2]
      if entity == entityid:
        attribute_vector.append(flag)
    record = [entity]
    record.extend(attribute_vector)
    entity_attribute_vectors.append(record)
  return entity_attribute_vectors

def create_csv(list_name,csv_name):
  with open(csv_name,'w') as f:
    w = writer(f)
    for item in list_name:
      w.writerow(item)

def main():

  # Source files
  entity1_attributes_csv = argv[1]
  entity2_attributes_csv = argv[2]

  # Entity phrases
  entity1_attributes = csv_to_list(entity1_attributes_csv)
  entity2_attributes = csv_to_list(entity2_attributes_csv)

  # Entities
  entities1 = sorted(set(list(zip(*entity1_attributes))[0]))
  entities2 = sorted(set(list(zip(*entity2_attributes))[0]))

  # Entity phrase vectors
  entity1_attribute_vectors = create_entity_attribute_vectors(entities1,entity1_attributes)
  entity2_attribute_vectors = create_entity_attribute_vectors(entities2,entity2_attributes)

  # Write to CSV
  create_csv(entity1_attribute_vectors,entity1_attributes.split('.')[0]+'_vectors.csv')
  create_csv(entity2_attribute_vectors,entity2_attributes.split('.')[0]+'_vectors.csv')

  return 'yay'

if __name__ == '__main__':
  main()
