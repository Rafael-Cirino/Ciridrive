from ciridrive_python import ciridrive

ciri = ciridrive()

# values = ciri.sheet_to_json("17p_SDlN6eW8jHmrGiHR3mwRzzZgGwGXFXBV7-HMtWBk")
# print(values)

# id_folder = ciri.create_folder(name_folder="testPPP")
# print(id_folder)

# ciri.drive_upload("/home/cirulei/Documentos/Ciridrive/ciridrive_python/sheet_json.json")

# print(ciri.copy_drive("17p_SDlN6eW8jHmrGiHR3mwRzzZgGwGXFXBV7-HMtWBk"))

ciri.move_drive(
    "1y4Yge66VDobx4eKthJ_XlW_-YMhsuwtpQguu9kG1tls", "1FOQ-e13gAO-OiwaPGIAHntQwlraSFAIR"
)

"""
ciri.search_files(
    "id",
    "0Byk3LcJwnlR7fkgwSWlfd0tsdk9HcWU5eXJ1SW5QMjJ0S3RXQ2U3TWhGeXpMaXl6LWpIclk",
    status=True,
)
"""
"""
ciri.drive_download("10XeP4YhtXQ1Q9N0oXq2J5eFbEXccb1AS")
ciri.drive_download("1nu7O_-0RQnlpgJja52DuErCO-rIMH-rIvJomiUyuitc")
ciri.drive_download("18W-4vKTRAI-t_5AF9CnAMMITCgt6LXKR")
ciri.drive_download("1DDw9MIDvi8CaWu_ZPItSHyiFOCHhW3Xq")
"""

# ciri.sheet_to_list("1TagLVILL_uBmsffZoC07pYLQ3ZDSRe5G8Led3oA6Ysc")
