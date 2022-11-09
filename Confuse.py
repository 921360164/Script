#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

if __name__ == "__main__":
    length = 12
    result = set()
    keywords = ['p', 'P', '0']

    for each in range(1, 100000):
        for length in range(6, 13):
            temp = keywords[random.randint(0, 1)]
            for i in range(1, length + 1):
                temp += random.choice(keywords)
            result.add(temp)

    print("成功生成字典，数量：", len(result))

    with open("/Users/weijiazheng/Desktop/dictionary_rules.txt", mode='w+', encoding='utf-8') as f:
        f.writelines("\n".join(result))
        f.flush()
