import pandas as pd
import json
file_path = r"/Users/srihitagollapudi/Documents/Sanskrit_project/data/dhatu/"

file_name_lst = ["dhatuforms_vidyut_shuddha_krut","dhatuforms_vidyut_nich_krut","dhatuforms_vidyut_san_krut","dhatuforms_vidyut_yang_krut","dhatuforms_vidyut_yangluk_krut"]

def krutha_to_excel(file_path,file_name):

    json_data = "/Users/srihitagollapudi/Documents/Sanskrit_project/data/dhatu/data.txt"
    with open(json_data, "r", encoding="utf-8") as f:
        dathu_name_data = json.load(f)
    dathu_name_lookup = {item["baseindex"]: item["dhatu"] for item in dathu_name_data["data"]}

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f) 
    rows = []
    for record_id, forms in data.items():
        row = {"id": record_id}
        dathu_name = {"dhatu": dathu_name_lookup.get(record_id, "Not Found")}
        row.update(dathu_name)
        parts_1=[]
        for suffix, value in forms.items():
            # parts = [v.strip() for v in value.split(",") if v.strip()]
            if ";" in value:
                value = value.split(";")
                # parts = [v for v in value.split(",")]
                for entry in value:
                    parts_1.append([x for x in entry.split(",")])
                # print(parts_1)
                # row[suffix] = list(zip(*parts_1))
                # row[suffix] = "[{}]".format("- ".join(f"('{a}'-'{b}')" for a, b in zip(*parts_1)))
                row[suffix] = "[{}]".format(
                                "- ".join(
                                    "(" + "-".join(x for x in item) + ")"
                                    for item in zip(*parts_1)
                                )
                            )
                # print(row[suffix])
                # break
            else:
                parts = [v for v in value.split(",")]
                parts[0] = f"({parts[0]})"
                row[suffix] = f"{'-'.join(parts)}"
        rows.append(row)
    df = pd.DataFrame(rows)
    return df
    # return df.to_csv(f"{file_name}.csv", index=True)

with pd.ExcelWriter("/Users/srihitagollapudi/Documents/Sanskrit_project/sanskrit/data/dhathu/excel_books/Kruth.xlsx", engine="openpyxl") as writer:
    for file_name in file_name_lst:

        path = file_path + file_name + ".txt"
        df = krutha_to_excel(path,file_name)
        df.to_excel(writer, sheet_name=file_name, index=False)

    