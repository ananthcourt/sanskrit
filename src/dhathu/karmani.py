import pandas as pd
import json
file_path = r"/Users/srihitagollapudi/Documents/Sanskrit_project/data/dhatu/"
file_name_lst = ["dhatuforms_vidyut_nich_karmani","dhatuforms_vidyut_san_karmani","dhatuforms_vidyut_shuddha_karmani","dhatuforms_vidyut_yang_karmani","dhatuforms_vidyut_yangluk_karmani"]

json_data = "/Users/srihitagollapudi/Documents/Sanskrit_project/data/dhatu/data.txt"
with open(json_data, "r", encoding="utf-8") as f:
    dhatu_name_data = json.load(f)

dathu_name_lookup = {item["baseindex"]: item["dhatu"] for item in dhatu_name_data["data"]}

def karmani_to_excel(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        rows = []
        for record_id, forms in data.items():
            row = {
                "id": record_id,
                "dhatu": dathu_name_lookup.get(record_id, "Not Found")
            }
            row.update(forms)
            rows.append(row)
        return pd.DataFrame(rows)

output_file = "/Users/srihitagollapudi/Documents/Sanskrit_project/sanskrit/data/dhathu/excel_books/karmani.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for file_name in file_name_lst:
        path = file_path + file_name + ".txt"
        df = karmani_to_excel(path)
        sheet_name = file_name[:31]
        df.to_excel(writer,sheet_name=sheet_name,index=False)
