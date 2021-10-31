# -*- coding: utf-8 -*-
import json
import telnetlib

class Dubbo(telnetlib.Telnet):
    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, port=0):
        super().__init__(host, port)
        # 触发dubbo提示符
        self.write(b'\n')

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        print("data##:{0}".format(data))
        self.write(str_.encode() + b'\n')
        return data

    def invoke(self, service_name, method_name, arg):
        # 组装invoke StudentService.getAll()这种形式
        self.command(Dubbo.prompt, "invoke {0}.{1}({2})".format(service_name, method_name, arg))
        # 执行invoke调用并返回结果
        data = self.command(Dubbo.prompt, "")
        # 对结果数据进行提取result:[{a:1}]
        data = data.decode(Dubbo.coding, errors="ignore").split('\n')[1].strip()
        # print("datax##:{0}".format(data))
        self.close()
        return data

    def do(self, conn, arg):
        data = conn.invoke('com.mangxiao.dubbo.samples.common.service.StudentService', 'getAll',arg)
        return data

if __name__ == '__main__':
    conn = Dubbo('8.131.87.108', 20881)
    # invoke_str = 'invoke StudentService.getAll()'
    s = conn.do(conn, "")
    print(s)
    s = s[9:len(s)-1]
    print(s)
    data = json.loads(s)
    print(data['id'])
    print(data['stuNo'])
    print(data['chineseScore'])
    print(data['englishScore'])
    print(data['mathScore'])
    # print("result##:{0}".format(r))
    # print(json.dumps(eval(result), indent=4, ensure_ascii=False))

