import json
import os
from src.models.Dhathu import Dhathu, DhathuForm, DhathuKridantaForm, DhathuRupa, Kridanta_Rupa

def populate_dhathu_object_dict(base_file_path):
    return {dhathu.base_index: dhathu for dhathu in (Dhathu(raw_data) for raw_data in json.load(open(base_file_path, "r"))["data"])}

def dump_dhathu_base_csv(dhathu_object_dict):
    # Print Base information of all dhatus in csv format
    with open("data/dhathu/dhathu_base.csv", "w") as f:
        f.write(Dhathu.base_csv_column_names() + "\n")
        for _, dhathu in dhathu_object_dict.items():
            f.write(dhathu.to_base_csv_string() + "\n")

def populate_dhathu_lakaar(dhathu_object_dict, form, file_path):
    lakaar_collection = json.load(open(file_path, "r"))
    for base_index, lakaar_dict in lakaar_collection.items():
        dhathu_object_dict[base_index].dhathu_forms[form] = DhathuForm(form, lakaar_dict)

def dump_dhathu_lakaar_csv(dhathu_object_dict, form):
    with open(f"data/dhathu/{form}.csv", "w") as f:
        f.write(f"{Dhathu.lakaar_csv_column_names()}\n")
        for _, dhathu in dhathu_object_dict.items():
                dhathu_form = dhathu.dhathu_forms.get(form)
                if dhathu_form:
                    for lakaar_code, dhathu_rupa in dhathu_form.lakaar_dict.items():
                        f.write(dhathu.to_lakaar_csv_string(lakaar_code, dhathu_rupa) + "\n")
def populate_dhathu_kridanta(dhathu_object_dict, kridanta, file_path):
    kridanta_collection = json.load(open(file_path, "r"))
    for base_index, kridanta_dict in kridanta_collection.items():
        dhathu_object_dict[base_index].kridanta_forms[kridanta] = DhathuKridantaForm(kridanta, kridanta_dict)

def dump_dhathu_kridanta_csv(dhathu_object_dict, kridanta):
    with open(f"data/dhathu/{kridanta}.csv", "w") as f:
        f.write(f"{Dhathu.kridanta_csv_column_names()}\n")
        for _, dhathu in dhathu_object_dict.items():
                kridanta_form = dhathu.kridanta_forms.get(kridanta)
                if kridanta_form:
                    for kridanta_rupa in kridanta_form.kridanta_dict.values():
                        f.write(dhathu.to_kridanta_csv_string(kridanta, kridanta_rupa) + "\n")

def create_lakaar_excel_workbook(dhathu_object_dict, ):
    #TODO : Create an excel workbook with each sheet representing a Dhathuform
    #       and containing the corresponding dhatus and all its lakaars
    # Currently creating a separate csv for each lakaar form, 
    # and copying them to excel manually. This can be automated in the future.
    pass


if __name__ == "__main__":

    base_file_path = os.path.expanduser("~/Documents/git_projects_personal/data/dhatu/data.txt")
    dhathu_object_dict = populate_dhathu_object_dict(base_file_path)
    dump_dhathu_base_csv(dhathu_object_dict)
    # for form in Dhathu.DHATHU_FORM_NAMES:
    #     file_path =  os.path.expanduser(f"~/Documents/git_projects_personal/data/dhatu/dhatuforms_vidyut_{form}.txt")
    #     populate_dhathu_lakaar(dhathu_object_dict, form, file_path)
    #     dump_dhathu_lakaar_csv(dhathu_object_dict, form)
    # create_lakaar_excel_workbook(dhathu_object_dict)

    for kridanta in Dhathu.DHATHU_KRIDANTA_FORM_NAMES:
        file_path =  os.path.expanduser(f"~/Documents/git_projects_personal/data/dhatu/dhatuforms_vidyut_{kridanta.replace('kridanta', 'krut')}.txt")
        populate_dhathu_kridanta(dhathu_object_dict, kridanta, file_path)
        dump_dhathu_kridanta_csv(dhathu_object_dict, kridanta)