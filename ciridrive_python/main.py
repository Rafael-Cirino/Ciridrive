from ciridrive_python import ciridrive

ciri = ciridrive()

# values = ciri.sheet_to_json("17p_SDlN6eW8jHmrGiHR3mwRzzZgGwGXFXBV7-HMtWBk")
# print(values)

id_folder = ciri.create_folder(name_folder="testPPP")
print(id_folder)

ciri.up_Drive("/home/cirulei/Documentos/Ciridrive/ciridrive_python/sheet_json.json")
