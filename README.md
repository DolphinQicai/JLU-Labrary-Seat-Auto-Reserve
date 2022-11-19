# JLU Labrary Seat Auto Reserve
# JLU图书馆座位自动预约

## 主要实现方法
- selenium模拟浏览器登录，获得cookies、accno、token
- requests发包，预约座位
- 多线程实现短时间内多次发包

## 更新
- final.py实现本地发单个包
- final3.py部署云服务器并实现批量发包
- final4.py增加发包数量，并提前发包，成功预约后自动发邮件提醒
