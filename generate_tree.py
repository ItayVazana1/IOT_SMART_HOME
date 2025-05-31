import os


def generate_file_tree(start_path, prefix=""):
    tree_lines = []
    for item in sorted(os.listdir(start_path)):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            tree_lines.append(f"{prefix}📁 {item}/")
            tree_lines.extend(generate_file_tree(item_path, prefix + "    "))
        else:
            tree_lines.append(f"{prefix}📄 {item}")
    return tree_lines


def save_tree_to_file(root_path, output_filename="project_tree.txt"):
    project_name = os.path.basename(os.path.abspath(root_path))
    tree = [f"{project_name}/"]
    tree.extend(generate_file_tree(root_path))

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(tree))
    print(f"✅ File tree saved to: {output_filename}")


# Replace with your project path
if __name__ == "__main__":
    project_root = "."  # Current directory
    save_tree_to_file(project_root)
