from tkinter import *
from lxml import etree
import threading
import urllib3
import time
import os


class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("EdusrcSelect漏洞查询v2.0")           #窗口名                               
        self.init_window_name.geometry('750x475+10+10')        #750 475为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.resizable(0,0)                   #固定大小
        #标签
        self.init_data_label = Label(self.init_window_name, text="*Page：",fg='Crimson')
        self.init_data_label.place(x=10, y=10) 
        self.init_data_label = Label(self.init_window_name, text="-->")
        self.init_data_label.place(x=90, y=10)
        self.init_data_label = Label(self.init_window_name, text="作者：Anyyy   所有数据来源:https://src.sjtu.edu.cn/list  ")
        self.init_data_label.place(x=280, y=10)
        self.init_data_label = Label(self.init_window_name, text="获取sessionid(更准确)："  )
        self.init_data_label.place(x=280, y=40)
        self.init_data_label = Label(self.init_window_name, text="打开https://src.sjtu.edu.cn登录账号密码  ")
        self.init_data_label.place(x=280, y=70)
        self.init_data_label = Label(self.init_window_name, text="Google:F12--->Application--->Cookies--->https://src.sjtu.edu.cn--->sessionid  ")
        self.init_data_label.place(x=280, y=100)
        self.init_data_label = Label(self.init_window_name, text="Firefox:F12--->存储--->Cookie--->https://src.sjtu.edu.cn--->sessionid  ")
        self.init_data_label.place(x=280, y=130)  
        self.keyword_data_label = Label(self.init_window_name, text="*关键词：",fg='Crimson')
        self.keyword_data_label.place(x=10, y=50)
        self.cookie_data_label = Label(self.init_window_name, text="Sessionid：",fg='Gray')
        self.cookie_data_label.place(x=10, y=100)        
        self.log_label = Label(self.init_window_name, text="查询结果",fg='Crimson')
        self.log_label.place(x=10, y=200)
        self.log_label = Label(self.init_window_name, text="Copyright@2021  www.anyiblog.top",fg='DimGray')
        self.log_label.place(x=10, y=450) 
        #文本框
        self.init_data_Text1 = Text(self.init_window_name, width=3, height=1)  #page1
        self.init_data_Text1.place(x=60, y=15) 
        self.init_data_Text2 = Text(self.init_window_name, width=3, height=1)  #page2
        self.init_data_Text2.place(x=120, y=15) 
        self.keyword_data_Text = Text(self.init_window_name, width=20, height=1)  #关键词
        self.keyword_data_Text.place(x=70, y=55)
        self.cookie_data_Text = Text(self.init_window_name, width=20, height=1)  #Sessionid
        self.cookie_data_Text.place(x=90, y=105) 
        self.log_data_Text = Text(self.init_window_name, width=100, height=9)  # 结果框
        self.log_data_Text.place(x=10, y=220)
        self.Scroll=Scrollbar(self.init_window_name) #下拉框
        self.Scroll.pack(side=RIGHT,fill=Y)
        self.Scroll.place(x=700,y=220,height=120)
        self.Scroll.config(command= self.log_data_Text.yview)
        #按钮
        self.var=IntVar() #复选框
        self.check_button=Checkbutton(self.init_window_name,text="将结果保存至桌面",variable=self.var,command=self.selectedChecks)
        self.check_button.place(x=15,y=350)
        self.str_trans_to_select_button = Button(self.init_window_name, text="开始查询", bg="lightblue", width=10,command=self.str_trans_to_select)  # 调用内部方法  加()为直接调用
        self.str_trans_to_select_button.place(x=600, y=180)
        mainloop() 


    #功能函数
    def str_trans_to_select(self):
        self.log_data_Text.delete(1.0,END)
        page1 = self.init_data_Text1.get(1.0,END).strip().replace("\n","")
        page2 = self.init_data_Text2.get(1.0,END).strip().replace("\n","")
        select = self.keyword_data_Text.get(1.0,END).strip().replace("\n","")
        cookie = self.cookie_data_Text.get(1.0,END).strip().replace("\n","")
        if page1 == '' or page2 == '':
            self.write_log_to_Text("请输入完整的页码！")
        else:
            if page1.isdigit() == False or page2.isdigit() == False:
                 self.write_log_to_Text("页码仅可输入数字！")
            else:
                if page1 <= "0" or page2 <= "0" :
                    self.write_log_to_Text("页码不可小于或等于0！")
                else:
                    try:
                        self.config(page1,page2,select,cookie)
                    except Exception as e:
                        print(e)
                        pass
    
    def config(self,page1,page2,select,cookie):
        for i in range(int(page1),int(int(page2)+1)):
            for k in range(1,16):
                threads={threading.Thread(target=self.school,args=(i,k,select,cookie,))}
                for line in threads:
                    line.start()
                    time.sleep(0.25)

    def school(self,i,k,select,cookie):
        http = urllib3.PoolManager()
        r = http.request(
            'GET',
            "https://src.sjtu.edu.cn/list/?page="+str(i),
            headers= {
                'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
                'Host':"src.sjtu.edu.cn",
                'Cookie':"sessionid="+str(cookie)
                },
            timeout = 4.0
            )
        html=r.data.decode('utf-8','ignore')
        _element =etree.HTML(html)
        text=_element.xpath("normalize-space(.//tr[@class='row']["+str(k)+"]/td[2]/a/text())")
        time=_element.xpath("//tr[@class='row']["+str(k)+"]/td[normalize-space(@class)='am-text-center am-hide-sm-down'][1]/text()")
        writer=_element.xpath("normalize-space(.//tr[@class='row']["+str(k)+"]/td[@class='am-text-center']/a/text())")
        if select in text:
            self.write_log_to_Text("Page"+str(i)+":"+str(time)+":"+str(text)+"     ---By:"+str(writer))
        else:
            self.write_log_to_Text("Page"+str(i)+" 未找到目标")

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +": " + str(logmsg) + "\n"      #换行
        self.log_data_Text.insert(END, logmsg_in)
        self.selectedChecks(logmsg_in)
    
    #复选框判断
    def selectedChecks(self,logmsg_in):
        if logmsg_in:
            if self.var.get()==1:
                path=open(os.path.join(os.path.expanduser('~'),"Desktop").replace('\\','/')+"/result.txt",'a+')
                path.write(logmsg_in)
                path.close()
            else:
                pass
        else:
            pass

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()
