#python 3.7.1
import os

class Product:
  ids_file = "ids_file.txt"
  data_file = "data_file.txt"
  def __init__(self, name, description, quantity, price, created_at):
    self.___id = self.generateID()
    self.name = name
    self.description = description
    self.quantity = quantity
    self.price = price 
    self.created_at = self.timeNow()
    self.updated_at = "Not yet updated"
  
  def __str__(self):
    return f"{self.id}, {self.name}, {self.description}, {self.quantity}, {self.price}, {self.created_at}"
  
  @staticmethod
  def generateID():
    last_id = Product.get_last_id()
    if last_id:
      number_part = int(last_id.split('-')[1])
      new_number_part = number_part + 1
    else:
      new_number_part = 1
      
    new_id = f"Prod-{str(new_number_part).zfill(3)}"
    Product.save_last_id(new_id)
    return new_id
  
  @staticmethod
  def get_last_id():
    if os.path.exists(Product.ids_file):
      with open(Product.ids_file, 'r') as file:
        lines = file.readlines()
        if lines:
          return lines[-1].strip()
    return None
  
  @staticmethod
  def save_last_id(new_id):
    with open(Product.ids_file, 'w') as file:
      file.write(new_id + '\n')
      
  @staticmethod
  def save_product(product):
    with open(Product.data_file, 'w') as file:
      file.write(str(product) + '\n')
  
  @staticmethod
  def load_product():
    products = []
    if(os.path.exists(Product.data_file)):
      with open(Product.data_file, 'r') as file:
        for line in file:
          product = Product.from_string(line.strip())
          products.append(product)
    return products
    
  @staticmethod
  def from_string(data):
    name, description, quantity, price, barcode, created_at = data.split(',')
    return Product(name, description, quantity, price, barcode, created_at)
