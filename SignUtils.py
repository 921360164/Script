#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

'''
align && sign apk
java -jar apktool.jar d --only-main-classes 解决反编译失败（dex被加密问题）
'''
def align(apk, jks, alias, pwd):
    dir_name, full_file_name = os.path.split(apk)
    file_name, file_ext = os.path.splitext(full_file_name)

    # 校验是否align
    verify_align_path = 'zipalign -c 4 \'{}\''.format(apk)
    print('verify align:{}'.format(verify_align_path))
    verify_code = os.system(verify_align_path)
    if verify_code == 0:
        # aligned && sign
        sign(file_name, jks, alias, pwd, apk, dir_name)
    else:
        align_path = 'zipalign -f -v 4 \'{}\' \'{}_aligned.apk\''.format(apk, file_name)
        print('align:{}'.format(align_path))
        align_code = os.system(align_path)
        if align_code == 0:
            # aligned && sign
            sign(file_name, jks, alias, pwd, '{}_aligned.apk'.format(file_name), dir_name)
        else:
            print('align fail!')


'''
签名 apk
'''
def sign(file_name, jks, alias, pwd, align_file, out_path):
    sign_path = 'apksigner sign --ks \'{0}\' --ks-key-alias \'{1}\' --ks-pass pass:{2} --key-pass pass:{2} --out \'{' \
                '3}_signed.apk\' \'{4}\''.format(jks, alias, pwd, os.path.join(out_path, file_name), align_file)
    print('sign:{}'.format(sign_path))
    sign_code = os.system(sign_path)
    if sign_code == 0:
        print('sign success!')
    else:
        print('sign fail!')


'''
验证apk签名是否有效
'''
def verify(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file.endswith('.apk'):
            verify_sign_path = 'apksigner verify -v \'{}\''.format(os.path.join(path, file))
            verify_sign_res = os.system(verify_sign_path)
            if verify_sign_res == 0:
                print('sign success:{}'.format(file))
            else:
                print('sign fail:{}'.format(file))

        else:
            continue

'''
批量签名
'''
def multiSign(path, jks, alias, pwd):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if file.endswith('.apk'):
                align(os.path.join(path, file), jks, alias, pwd)
            else:
                continue
        else:
            multiSign(os.path.join(path, file), jks, alias, pwd)


if __name__ == '__main__':
    try:
        print('usage: SignUtils -f xxxx.apk -j xxx.jks -a xxx -s xxxx')  # 单包签名
        print('usage: SignUtils -v xxxx')  # 验证签名是否有效
        print('usage: SignUtils -p xxxx -j xxx.jks -a xxx -s xxxx')  # 批量签名
        # 签名
        if sys.argv[1] == '-f' and sys.argv[2] != '' and sys.argv[3] == '-j' and sys.argv[4] != '' and sys.argv[
            5] == '-a' and sys.argv[6] != '' and sys.argv[7] == '-s' and sys.argv[8] != '':
            align(sys.argv[2], sys.argv[4], sys.argv[6], sys.argv[8])
        # 验证签名
        elif sys.argv[1] == '-v' and sys.argv[2] != '':
            verify(sys.argv[2])
        # 批量签名
        elif sys.argv[1] == '-p' and sys.argv[2] != '' and sys.argv[3] == '-j' and sys.argv[4] != '' and sys.argv[
            5] == '-a' and sys.argv[6] != '' and sys.argv[7] == '-s' and sys.argv[8] != '':
            multiSign(sys.argv[2], sys.argv[4], sys.argv[6], sys.argv[8])
        else:
            print('argv analysis error')

    except Exception as e:
        print('error:{}'.format(e))
