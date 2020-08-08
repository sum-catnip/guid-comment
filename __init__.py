from binaryninja.plugin import PluginCommand
from binaryninja import BinaryView

import struct


def parse_part(data: bytes, fmt: str, pad: int):
    return f'{struct.unpack(fmt, data)[0]:0{pad}x}'


def parse_guid(bv: BinaryView, addr: int):
    data1 = parse_part(bv.read(addr, 4), '<L', 8)
    data2 = parse_part(bv.read(addr + 4, 2), '<H', 4)
    data3 = parse_part(bv.read(addr + 6, 2), '<H', 4)
    data4 = bv.read(addr + 8, 8).hex()
    return f'{{{data1}-{data2}-{data3}-{data4[:4]}-{data4[4:]}}}'


def comment_guids(bv: BinaryView):
    for k, v in bv.data_vars.items():
        if v.type.get_string_before_name() == 'GUID':
            guid = parse_guid(bv, v.address)
            existing = bv.get_comment_at(v.address)
            if guid not in existing:
                comment = existing or '' + guid
                bv.set_comment_at(v.address, comment)


PluginCommand.register('GUID comment',
                       'comment GUID instances in the proper format',
                       comment_guids)
