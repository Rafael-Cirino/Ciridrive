from ciridrive_python import ciridrive

ciri = ciridrive()
values = ciri.sheet_to_list("17p_SDlN6eW8jHmrGiHR3mwRzzZgGwGXFXBV7-HMtWBk", "tab")
print(values)