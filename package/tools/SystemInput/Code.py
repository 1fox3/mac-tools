#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 键盘输入对应的编码
# 参考链接：https://docs.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes
VK_CODE = [
    'a',
    's',
    'd',
    'f',
    'h',
    'g',
    'z',
    'x',
    'c',
    'v',
    'b',
    'q',
    'w',
    'e',
    'r',
    'y',
    't',
    '1',
    '2',
    '3',
    '4',
    '6',
    '5',
    '=',
    '9',
    '7',
    '-',
    '8',
    '0',
    ']',
    'o',
    'u',
    '[',
    'i',
    'p',
    'l',
    'j',
    '\'',
    'k',
    ';',
    '\\',
    ',',
    '/',
    'n',
    'm',
    '.',
    '`',
    ' ',
    '\r',
    '\t',
    '\n',
    'return',
    'tab',
    'space',
    'delete',
    'escape',
    'command',
    'shift',
    'capslock',
    'option',
    'alternate',
    'control',
    'rightshift',
    'rightoption',
    'rightcontrol',
    'function',
]

# 组合按键的对应关系
MULTI_KEY_MAP = {
    'A': ['shift', 'a'],
    'B': ['shift', 'b'],
    'C': ['shift', 'c'],
    'D': ['shift', 'd'],
    'E': ['shift', 'e'],
    'F': ['shift', 'f'],
    'G': ['shift', 'g'],
    'H': ['shift', 'h'],
    'I': ['shift', 'i'],
    'J': ['shift', 'j'],
    'K': ['shift', 'k'],
    'L': ['shift', 'l'],
    'M': ['shift', 'm'],
    'N': ['shift', 'n'],
    'O': ['shift', 'o'],
    'P': ['shift', 'p'],
    'Q': ['shift', 'q'],
    'R': ['shift', 'r'],
    'S': ['shift', 's'],
    'T': ['shift', 't'],
    'U': ['shift', 'u'],
    'V': ['shift', 'v'],
    'W': ['shift', 'w'],
    'X': ['shift', 'x'],
    'Y': ['shift', 'y'],
    'Z': ['shift', 'z'],
    ':': ['shift', ';'],
    '"': ['shift', "'"],
    '<': ['shift', ','],
    '>': ['shift', '.'],
    '?': ['shift', '/'],
    '~': ['shift', '`'],
    '!': ['shift', '1'],
    '@': ['shift', '2'],
    '#': ['shift', '3'],
    '$': ['shift', '4'],
    '%': ['shift', '5'],
    '^': ['shift', '6'],
    '&': ['shift', '7'],
    '*': ['shift', '8'],
    '(': ['shift', '9'],
    ')': ['shift', '0'],
    '_': ['shift', '-'],
    '|': ['shift', '\\'],
    '+': ['shift', '='],
    'window_max': ['command', 'shift', '='],
    'window_close': [['command', 'q'], ['command', 'q']],
}
