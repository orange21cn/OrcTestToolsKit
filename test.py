# coding=utf-8

# 处理列表
def sanitize(time):
    if '-' in time:
        splitter = '-'
    elif ':' in time:
        splitter = ':'
    else:
        return (time)
    min, sec = time.split(splitter)
    return min + '.' + sec


# 创建类

# class Athlete:
#     def __init__(self, p_name, p_birth, p_time=None):
#         self.name = p_name
#         self.birth = p_birth
#         self.time = p_time
class Athlete:
    def __init__(self, name, birth, time):
        self.name = name
        self.birth = birth
        self.time = time

    def top3(self):
        return (sorted(set([sanitize(each) for each in self.time]))[0:3])


# 读james.txt文件
def get_data(filename):
    try:
        with open(filename) as jaf:
            data = jaf.readline()
            print (data)
            data1 = data.strip().split(',')
            print(data1)
            print data1[0]
            print data1[1]
            print data1[2:]
            return Athlete(data1[0], data1[1], data1[2:])  # 出错的位置：提示typeError:this constructor takes no arguments
    except IOError as ioerr:
        print("file error:" + str(ioerr))
        return (None)


#
# # 类的调用
if __name__ == '__main__':
    james = get_data('abc.txt')
    print(james.name + "'s fastest time are:" + str(james.top3()))
# abc = Athlete(1, 2, 3)
#
# class Athlete:
#     def __init__(self, p_name, p_birth, p_time=None):
#         self.name = p_name
#         self.birth = p_birth
#         self.time = p_time
#
#
# abc = Athlete(2, 3, 4)
