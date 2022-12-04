def seat_id(seat_code):
    row_id = seat_code[:7].replace("B", "1").replace("F", "0")
    col_id = seat_code[7:].replace("R", "1").replace("L", "0")
    return 8 * int(row_id, base=2) + int(col_id, base=2)


# Download data
with open("aoc_2020_5.txt", "r") as file:
    seat_data = [line.strip() for line in file]

occupied_seat_ids = {seat_id(seat) for seat in seat_data}
all_seat_ids = {i * 8 + j for i in range(128) for j in range(8)}

empty_seats = all_seat_ids - occupied_seat_ids

my_seat = [i for i in empty_seats if ((i - 1) not in empty_seats and (i + 1) not in empty_seats)]

print(my_seat[0])
