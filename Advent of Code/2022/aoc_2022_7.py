from dataclasses import dataclass, field
from pprint import pprint

with open("aoc_2022_7.txt") as file:
    commands_from_file = file.readlines()


@dataclass
class File:
    name: str
    size: int
    parent: str | None = None

    def __str__(self):
        return f'{self.name} (file, size={self.size})'


@dataclass
class Directory:
    name: str
    parent: str = None
    children: dict[str: object] = field(default_factory=lambda: dict())

    @property
    def size(self):
        size = 0
        for child in self.children.values():
            size += child.size
        return size

    def show_tree(self, indent=""):
        print(indent + "- " + str(self))
        indent += "  "
        for child in self.children.values():
            if isinstance(child, File):
                print(indent + "- " + str(child))
            else:
                child.show_tree(indent)

    def __str__(self):
        return f'{self.name} (dir, size={self.size})'


def parse_command(command_line: str) -> tuple[str, str | None]:
    parts = command_line[2:].strip().split()
    cmd, *other = parts
    if len(parts) > 1:
        operand = parts[1]
    else:
        operand = None
    return cmd, operand


def parse_content(content_line: str) -> File | Directory:
    parts = content_line.strip().split()
    if parts[0] == "dir":
        content = Directory(name=parts[1])
    elif parts[0].isdigit():
        content = File(name=parts[1], size=int(parts[0]))
    else:
        raise TypeError(f"File or directory not recognised in {content_line}")
    return content


def read_file_structure(command_data: list[str]) -> Directory:
    root = Directory(name="/")
    current_directory = root
    current_children = {name for name in root.children}

    for line in command_data[1:]:
        if line[0] == "$":
            operation, dir_name = parse_command(line)
            if operation == "ls":
                current_children = current_directory.children
                current_directory.children = dict()
            elif operation == "cd":
                if dir_name == "..":
                    current_directory = current_directory.parent
                else:
                    current_directory = current_directory.children[dir_name]

        else:
            dir_content = parse_content(line)
            dir_content.parent = current_directory
            if dir_content.name in current_children:
                dir_content = current_children[dir_content.name]
            current_directory.children[dir_content.name] = dir_content
    return root


def find_dir_sizes(root_dir: Directory, dir_sizes=None):
    if dir_sizes is None:
        dir_sizes = []

    if isinstance(root_dir, Directory):
        dir_sizes.append(root_dir.size)

    for child in root_dir.children.values():
        if isinstance(child, Directory):
            dir_sizes = find_dir_sizes(child, dir_sizes)

    return dir_sizes


my_root = read_file_structure(commands_from_file)
# print(my_root.size)
# my_root.show_tree()
directory_sizes = find_dir_sizes(my_root)

print(f"Solution to problem 1 is {sum(ds for ds in directory_sizes if ds <= 100_000)}")

unused_space = 70_000_000 - my_root.size
rqd_space = 30_000_000 - unused_space

print(f'Solution to problem 2 is {min(ds for ds in directory_sizes if ds >= rqd_space)}')
