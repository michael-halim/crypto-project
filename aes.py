from AES_Utils.help_function import *

def encrypt(key, data):

    pad = bytes(16 - len(data) % 16)

    if len(pad) != 16:
        data += pad

    grids = create_4_by_4(data)

    expanded_key = expand_key(key, 11)

    temp_grids = []

    round_key = extract_key_for_round(expanded_key, 0)

    for grid in grids:
        temp_grids.append(add_sub_key(grid, round_key))

    grids = temp_grids

    for round in range(1, 10):
        temp_grids = []

        for grid in grids:
            sub_bytes_step = [[lookup(val) for val in row] for row in grid]
            shift_rows_step = [rotate_row_left(
                sub_bytes_step[i], i) for i in range(4)]
            mix_column_step = mix_columns(shift_rows_step)

            round_key = extract_key_for_round(expanded_key, round)

            add_sub_key_step = add_sub_key(mix_column_step, round_key)
            temp_grids.append(add_sub_key_step)

        grids = temp_grids

    temp_grids = []
    round_key = extract_key_for_round(expanded_key, 10)

    for grid in grids:
        sub_bytes_step = [[lookup(val) for val in row] for row in grid]
        shift_rows_step = [rotate_row_left(
            sub_bytes_step[i], i) for i in range(4)]


        add_sub_key_step = add_sub_key(shift_rows_step, round_key)
        temp_grids.append(add_sub_key_step)

    grids = temp_grids

    int_stream = []
    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_stream.append(grid[row][column])

    return bytes(int_stream)


def decrypt(key, data):

    grids = create_4_by_4(data)
    expanded_key = expand_key(key, 11)
    temp_grids = []
    round_key = extract_key_for_round(expanded_key, 10)

    temp_grids = []

    for grid in grids:

        add_sub_key_step = add_sub_key(grid, round_key)
        shift_rows_step = [rotate_row_left(
            add_sub_key_step[i], -1 * i) for i in range(4)]
        sub_bytes_step = [[reverse_lookup(val) for val in row]
                          for row in shift_rows_step]
        temp_grids.append(sub_bytes_step)

    grids = temp_grids

    for round in range(9, 0, -1):
        temp_grids = []

        for grid in grids:
            round_key = extract_key_for_round(expanded_key, round)
            add_sub_key_step = add_sub_key(grid, round_key)

            mix_column_step = mix_columns(add_sub_key_step)
            mix_column_step = mix_columns(mix_column_step)
            mix_column_step = mix_columns(mix_column_step)
            shift_rows_step = [rotate_row_left(
                mix_column_step[i], -1 * i) for i in range(4)]
            sub_bytes_step = [
                [reverse_lookup(val) for val in row] for row in shift_rows_step]
            temp_grids.append(sub_bytes_step)

        grids = temp_grids
        temp_grids = []

    round_key = extract_key_for_round(expanded_key, 0)

    for grid in grids:
        temp_grids.append(add_sub_key(grid, round_key))

    grids = temp_grids

    int_stream = []
    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_stream.append(grid[row][column])

    return bytes(int_stream)

"""
import os
path = 'D:\\Kuliah Infor\\Kripto\\Proyek\\crypto-project\\7.txt'
if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()
    import base64
    data = base64.b64decode(data.replace('\n',''))

    key = b'YELLOW SUBMARINE'
    d = dec(key, data)
"""

"""
import base64
cipher = encrypt(b'yunusyunusyunusy', b'ini adalah kalimat rahasia saya')
cipher = base64.b64encode(cipher)
cipher = cipher.decode("utf-8")
print(cipher)

cobadecrypt = base64.b64decode(cipher)
plaintext = decrypt(b'yunusyunusyunusy', cobadecrypt)
plaintext = plaintext.decode("utf-8")
print(plaintext)
"""