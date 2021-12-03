from AES_Utils.tables import AES_SBOX,REV_AES_SBOX
def lookup(byte):
    x = byte >> 4
    y = byte & 15
    return int(AES_SBOX[x][y],16)


def reverse_lookup(byte):
    x = byte >> 4
    y = byte & 15
    return int(REV_AES_SBOX[x][y],16)


def multiply_2(value):
    res = value << 1
    res &= 0xff
    if (value & 128) != 0:
        res = res ^ 0x1b
    return res


def multiply_3(value):
    return multiply_2(value) ^ value


def mix_columns(grid):
    new_grid = [[], [], [], []]
    for i in range(4):
        col = [grid[j][i] for j in range(4)]
        col = mix_column(col)
        for i in range(4):
            new_grid[i].append(col[i])
    return new_grid


def mix_column(column):
    res = [
        multiply_2( column[0] ) ^ multiply_3( column[1] ) ^ column[2] ^ column[3],
        multiply_2( column[1] ) ^ multiply_3( column[2] ) ^ column[3] ^ column[0],
        multiply_2( column[2] ) ^ multiply_3( column[3] ) ^ column[0] ^ column[1],
        multiply_2( column[3] ) ^ multiply_3( column[0] ) ^ column[1] ^ column[2],
    ]
    return res

def rotate_row_left(row, n=1):
    return row[n:] + row[:n]


def add_sub_key(block_grid, key_grid):
    result = []

    for i in range(4):
        result.append([])
        for j in range(4):
            result[-1].append(block_grid[i][j] ^ key_grid[i][j])
    return result


def extract_key_for_round(expanded_key, round):
    return [ row [ round * 4 : round * 4 + 4 ] for row in expanded_key]


def create_4_by_4(s):
    all = []
    for i in range(len(s)//16):
        b = s[i*16: i*16 + 16]
        grid = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                grid[i].append(b[i + j*4])
        all.append(grid)
    return all


def expand_key(key, rounds):

    rcon = [[1, 0, 0, 0]]

    for _ in range(1, rounds):
        rcon.append([rcon[-1][0]*2, 0, 0, 0])
        if rcon[-1][0] > 0x80:
            rcon[-1][0] ^= 0x11b

    key_grid = create_4_by_4(key)[0]

    for round in range(rounds):
        last_column = [ row[-1] for row in key_grid ]

        last_column_rotate_step = rotate_row_left(last_column)

        last_column_sbox_step = [ lookup(b) for b in last_column_rotate_step ]

        last_column_rcon_step = [ last_column_sbox_step[i]
                                 ^ rcon[round][i] for i in range(len(last_column_rotate_step)) ]

        for r in range(4):
            key_grid[r] += bytes([last_column_rcon_step[r]
                                  ^ key_grid[r][round*4]])

        for i in range(len(key_grid)):
            for j in range(1, 4):
                key_grid[i] += bytes( [key_grid[i][ round*4 + j]
                                      ^ key_grid[i][ round*4 + j + 3] ])

    return key_grid
