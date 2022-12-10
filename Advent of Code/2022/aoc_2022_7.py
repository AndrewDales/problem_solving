from dataclasses import dataclass, field
from pprint import pprint


@dataclass
class SystemContent:
    name: str
    parent: str | None
    size: int | None
    type: str
    children: set[str] = field(default_factory=set)

    def __post_init__(self):
        if self.type == "dir" and self.parent:
            self.name += "_" + self.parent


explored_content = dict()


def parse_line(line_content: str, cd_name: str):
    cd = explored_content[cd_name]
    content_parts = line_content.strip().split()
    system_content = None
    # if cd is None:
    #     parent_name = None
    # else:
    parent_name = cd.name

    if content_parts[0] == "$":
        command = content_parts[1]
        if command == "cd":
            dir_name = content_parts[2]
            if dir_name[:2] == '..':
                system_content = explored_content[cd.parent]
            else:
                system_content = SystemContent(name=dir_name,
                                               parent=parent_name,
                                               size=None,
                                               type="dir",
                                               )
    else:
        content_name = content_parts[1]
        command = "write"
        if content_parts[0] == "dir":
            system_content = SystemContent(name=content_name,
                                           parent=parent_name,
                                           size=None,
                                           type="dir")
        else:
            size = int(content_parts[0])
            system_content = SystemContent(name=content_name,
                                           parent=parent_name,
                                           size=size,
                                           type="file"
                                           )
    return system_content, command


def find_size(content_name, file_structure):
    system_content = file_structure[content_name]
    size = 0

    if system_content.type == "file":
        size = system_content.size
    elif system_content.type == "dir":
        for child in system_content.children:
            size += find_size(child, file_structure)
    return size


def print_tree(dir_item: SystemContent, indent=""):
    print(indent + dir_item.name)
    for child in dir_item.children:
        if child in explored_content:
            print_tree(explored_content[child], indent+"\t")


with open("aoc_2022_7.txt") as file:
    command_data = file.readlines()

root = SystemContent(name="/", parent=None, type="dir", size=None)
explored_content[root.name] = root
cd_name = root.name

for line in command_data[1:]:
    current_item, action = parse_line(line, cd_name)
    if action == "ls":
        pass
    elif action == "cd":
        cd_name = current_item.name
        #if current_item.name not in explored_content:
        explored_content[cd_name] = current_item
        # print(cd_name)
    elif action == "write":
        explored_content[cd_name].children.add(current_item.name)
        if current_item.type == "file":
            explored_content[current_item.name] = current_item

# pprint(explored_content)

sizes = {}

for name, file_item in explored_content.items():
    if file_item.type == "dir":
        sizes[name] = find_size(name, explored_content)

small_dir_sizes = sum(val for val in sizes.values() if val <= 100_000)

print(small_dir_sizes)
