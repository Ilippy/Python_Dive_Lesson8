import os
import json
import csv
import pickle


def traverse_directory(directory):
    result = []
    for dir_path, dir_name, file_name in os.walk(directory):
        # print(f'{dir_path = }\n{dir_name = }\n{file_name = }')
        result += get_file_or_folder_dict(directory, file_name, "File")
        result += get_file_or_folder_dict(directory, dir_name, "Directory")
        for folder in dir_name:
            result += traverse_directory(os.path.join(directory, folder))
    return result


def get_file_or_folder_dict(directory, lst, type_):
    res = []
    for file_or_folder in lst:
        path = os.path.join(directory, file_or_folder)
        if type_ == "Directory":
            size = get_folder_size(os.path.join(directory, file_or_folder))
        else:
            # TODO: Если убрать try/except то будет ошибка, не пойму почему
            try:
                size = os.path.getsize(path) if not os.path.islink(path) else 0
            except FileNotFoundError:
                size = 0
        res.append({'Path': path, "Type": type_, "Size": size})
    return res


def get_folder_size(directory):
    local_files_size = 0
    for dir_path, dir_names, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dir_path, f)
            if not os.path.islink(fp):
                local_files_size += os.path.getsize(fp)
        return local_files_size + sum(get_folder_size(os.path.join(directory, path)) for path in dir_names)
    return local_files_size


def save_results_to_json(results, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def save_results_to_csv(results, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Path', 'Type', 'Size'])
        for result in results:
            writer.writerow([result['Path'], result['Type'], result['Size']])


def save_results_to_pickle(results, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(results, f)


def main():
    path = os.path.dirname(os.getcwd())
    result = traverse_directory(path)
    save_results_to_json(result, "files.json")
    save_results_to_csv(result, "files.csv")
    save_results_to_pickle(result, "pickle.pkl")
    for line in result:
        if line["Type"] == "Directory":
            print(line["Path"].split(os.sep)[7:], line["Type"], line["Size"])


if __name__ == '__main__':
    main()
