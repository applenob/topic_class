#coding=utf-8
def show_dict(dic):
    '''打印dict'''
    assert type(dic) == dict
    for key in dic:
            print key, ' : ', dic[key]
    print '--------------------------分隔符--------------------------'

def from_stamp_t0_string(stamp):
    '''时间戳到日期'''
    from datetime import datetime
    return datetime.fromtimestamp(float(stamp) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

def get_stamp(year,month,day,hour=0,minute=0,second=0):
    '''生成时间戳'''
    from datetime import datetime
    import time
    dt = datetime(year,month,day,hour,minute,second)
    tp = dt.timetuple()
    return int(time.mktime(tp))

def from_ustr_to_str(ustr):
    '''解码unicode字符串'''
    assert type(ustr) == str
    str_n = ustr.decode('unicode-escape')
    return str_n.encode('utf-8')

def part_ustr_to_str(ustr):
    import re
    us = re.findall(r'\\[u][0-9a-z]{4}', ustr)
    if len(us) == 0:
        return ustr
    else:
        for u in us:
            ustr = ustr.replace(u,from_ustr_to_str(u))
        return ustr

if __name__ == '__main__':
    # print from_stamp_t0_string('1468821711706')
    # print get_stamp(2016,7,15)
    print part_ustr_to_str('中国与乌克兰\u201c动力沙皇\u201d深度合作 助力大飞机')