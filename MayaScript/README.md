<h2 align="center"> Maya脚本更新日志 </h2>

<h3 align="center">  </h3>
<p align="center">


## [ModelTool `|检查模型对称 镜像工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/ModelTool.py)

#### 2023-10-16  Verision: `1.0x`
<details>
<summary>详情</summary>
<pre>
1.Fix:存储选择模型的时机
2.reBS:可以从Bs窗口选择目标了
3.Fix:ExBS:属性锁定问题
4.connectBS:添加Bs属性连工具
5.添加模型反算的命令工具
</pre>
</details>

#### 2023-03-26  Verision: `0.1`
<details>
<summary>详情</summary>
<pre>
检查模型对称 镜像工具
<p align="left">
  ▽  2023-04-05  Ver_0.11
1.Fix: 修复尝试对称的类型错误
<p align="left">
  ▽  2023-04-11  Ver_0.12
1.优化翻转和镜像 只处理有移动的点
2.添加局部和世界轴向选项
3.更换对称检查算法
</pre>
</details>


## [ngSk2Weight `|基于NG2的自动分权重 Relax|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/ngSk2Weight.py)

#### 2023-10-16  Verision: `0.8x`
<details>
<summary>详情</summary>
<pre>
1.默认不Smooth权重
2.复制粘贴点权重功能重构 细分选项
3.支持从Maya权重提取成ng权重
4.模型不支持热度贴图时换用体素权重
5.添加默认权重精度限制
</pre>
</details>

#### 2023-03-25  Verision: `0.7x`
<details>
<summary>详情</summary>
<pre>
1.功能Ui分布
2.取消层功能
3.提取功能函数
<p align="left">
  ▽  2023-04-05  Ver_0.71
1.优化Smooth使用模式，增加强度调整功能
<p align="left">
  ▽  2023-04-11  Ver_0.72
1.Fix:影响值获取UI错误
</pre>
</details>


#### 2022-08-31  Verision: `0.6x`
<details>
<summary>详情</summary>
<pre>
基于NG2的自动分权重 和 Smooth权重
</pre>
</details>


## [CtrlTool `|控制器工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/CtrlTool.py)

#### 2021-02-04  Verision: `1.0x`
<details>
<summary>详情</summary>
<pre>
控制器创建和修改
<p align="left">
  ▽  2021-11-06  Ver_1.01
1.增加控制器形状保存功能
<p align="left">
  ▽  2022-06-06  Ver_1.02
1.修改颜色选择器样式
2.添加名字前后缀和替换按钮
<p align="left">
  ▽  2022-07-10  Ver_1.03
1.确保UI唯一性
2.修改控制器按钮生成方式, 使用循环内lambda
3.添加镜像控制器功能
4.修改放大缩小功能样式
5.优化编辑旋转缩放时流程
<p align="left">
  ▽  2022-08-11  Ver_1.04
1.移除一半不必要的icon数据
2.Fix: 修复镜像形状的规则
<p align="left">
  ▽  2023-03-26  Ver_1.05
1.形状颜色改为序号颜色模式
2.优化UI逻辑
3.优化保存形状功能，规划新规则
4.添加更多控制选项
5.镜像添加多个模式
<p align="left">
  ▽  2023-10-16  Ver_1.06
1.优化控制器组层级
2.增加控制器替换功能 整合进流程
3.Fix:增加前后缀时不应该使用长名称
</pre>
</details>

## [cur2IK_FX `|动力学曲线工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/cur2IK_FX.py)

#### 2020-12-09  Verision: `2.5x`
<details>
<summary>详情</summary>
<pre>
1.添加新的流程, 从骨骼开始建立
2.所有流程增加蒙皮骨骼作为最终结果
3.隐藏不需要的物体和属性
4.改用驱动关键帧对动力学开关进行控制
  (若动力学开启, 在2019和更高版本中, 会因为cache playbacka功能会引起崩溃)
5.清理冗余代码, 提升效率
6.修改Ui部件名，确保Ui的唯一性
7.Fix: 选择控制器时对名字的错误拆分
8.Fix: 插件报错后，错误信息不消失
<p align="left">
  ▽  2020-12-25  Ver_2.51
1.修改ui部件名, 与脚本的新名字保持一致
2.用刷新替代延迟运行，避免出错
<p align="left">
  ▽  2022-06-26  Ver_2.52
1.增加maya2022以上版本兼容
<p align="left">
  ▽  2022-08-11  Ver_2.53
1.移除控制器修改相关内容
<p align="left">
  ▽  2022-08-14  Ver_2.54
1.优化动力学控制的切换方式, 每根独立控制
<p align="left">
  ▽  2023-04-05  Ver_2.55
1.精简生成选项，省略部分控制层级
</pre>
</details>

#### 2020-10-23  Verision: `2.4x`
<details>
<summary>详情</summary>
<pre>
1.优化了窗口生成的方式, 又学了一招
2.UI微调
3.增加由骨骼控制曲线的选项
4.整合了创建流程. 但流程过长貌似不是好事, 模块化会更好一些??
5.选择控制器功能优化
6.根据新的创建选项，重写了整理函数
7.Fix: 在关掉动力学时创建曲线, 不生成shape的问题
<p align="left">
  ▽  2020-11-02  Ver_2.41
1.精简多余代码
2.Fix: Maya2016的Ui支持问题
3.Fix: 生成后直接删除控制器, 不能再次运行的问题
<p align="left">
  ▽  2020-11-20  Ver_2.42
1.Fix: 提取曲线时, 尝试居中对齐会报错
</pre>
</details>


## [WeightTool `|包含点调整.Save/Load.最大影响值检查|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/WeightTool.py)

#### 2022-07-02  Verision: `1.00`
<details>
<summary>详情</summary>
<pre>
1.修改列表筛选菜单
2.优化权重导入的归一化参数和精度
3.优化报绿颜色及内容
4.Check: 修改窗口样式
5.Check: 优化所有功能
<p align="left">
  ▽  2022-08-11  Ver_1.01
1.确保UI唯一性
2.移除报绿内容, 独立模块
2.CheckFix: 选择功能修复, 改为选择问题组件
<p align="left">
  ▽  2022-08-14  Ver_1.02
1.Fix: 调用不到脚本任务中的函数
<p align="left">
  ▽  2022-08-17  Ver_1.03
1.优化数据存储方法 使用变量
2.提高权重获取精度
3.增加在列表中选择骨骼时, 骨骼高亮
4.Check: 增加保存上一次选择的选项
5.Check: 增加处理进度条
6.Fix: 当有骨骼改名时, 列表不会刷新导致报错的问题
7.Fix: Check: 清理影响值时，使用了错误的骨骼列表
<p align="left">
  ▽  2022-08-20  Ver_1.04
1.Fix: 单文件运行时报错
2.Fix: ui界面运行时大小问题(未完全解决)
<p align="left">
  ▽  2022-09-15  Ver_1.05
1.Fix: py2中整数除法结果可能为0
<p align="left">
  ▽  2023-03-26  Ver_1.06
1.存取权重修改文件格式
2.检查权重优化流程 效率
3.拷贝工具整合
4.软选择工具
<p align="left">
  ▽  2023-04-11  Ver_1.07
1.删除无用代码，整合功能
<p align="left">
  ▽  2023-10-16  Ver_1.08
1.Fix:存取权重改为点id模式
2.拷权重:选两个模型简易运行
3.拷权重:优化拷点的流程和精准度
</pre>
</details>

#### 2022-05-10  Verision: `0.9x`
<details>
<summary>详情</summary>
<pre>
1.增加了deformerWeights处理权重功能(虽然MEL命令 但很快奥)
  --deformerWeights 只能处理Mesh模型
2.代码结构调整, Save/Load单列一类
3.打印Save/Load操作时间
4.报错换成中文
5.添加Python3支持
<p align="left">
  ▽  2022-05-15  Ver_0.91
1.添加Python3支持
2.优化代码效率
3.Fix: 文件选择时间被记入处理时间
4.Fix: 在不使用dW方式时, 批量模式提供了xml后缀
5.Fix: MayaUI项shiboken (long型 变为 int型)
6.Fix: 报绿在没有窗口的情况下报错
<p align="left">
  ▽  2022-06-18  Ver_0.92
1.去掉S/L批量模式, 修改支持的文件后缀
2.增加功能 仅恢复选择点的权重
</pre>
</details>

#### 2020-12-24  Verision: `0.8x`
<details>
<summary>详情</summary>
<pre>
1.增加 Api2.0 处理权重, 同时默认使用Api2.0
  --Api2.0 只能处理Mesh模型
2.添加右键菜单中的功能
3.运行效率优化, 代码优化
4.Fix: 在空白处右键, 不会弹出菜单的问题
5.Fix: Api获取蒙皮节点时, 会误判, 改为mel调用获取
<p align="left">
  ▽  2020-12-25  Ver_0.81
1.使用Api Load权重时, 避免使用eval处理数据，改用字符串处理获取数据
2.继续优化代码
3.Fix: 脚本功能不运行时, 选择骨骼列表会报错
<p align="left">
  ▽  2020-12-25  Ver_0.82
1.修改Ui部件名, 确保Ui的唯一性
2.Fix: 权重锤运行时报错
<p align="left">
  ▽  2021-01-04  Ver_0.83
1.Fix: 触发脚本时不会立刻运行的问题
2.Fix: 列表刷新时, 骨骼锁没被刷新的问题
<p align="left">
  ▽  2021-01-07  Ver_0.84
1.Fix: 给模型添加影响后, 骨骼列表不会刷新的问题. 可能导致报错
2.Fix: copy权重后会触发刷新, 此时的选择列表可能有问题, 导致报错
3.Fix: 删除搜索栏字符后, 骨骼列表不刷新的问题在2016以上版本中不存在
<p align="left">
  ▽  2021-03-15  Ver_0.85
1.WeightCheckTool: 功能和代码优化
2.Fix: WeightCheckTool: 选择点时, 如果点列表中显示有物体名，会报错
</pre>
</details>

#### 2020-11-26  Verision: `0.7x`
<details>
<summary>详情</summary>
<pre>
1.增加了api处理权重功能, 但默认使用Mel
2.使用并集、差集优化循环处理方式
3.修改文件选择窗口的实现方式
4.减小Save功能的权重精度, 控制在小数点后4位
5.使用重蒙皮时, 更新初始的绑定Pose
6.Fix: 刷新时选择中有transform, 不能获取权重的报错
7.Fix: 在空白处右键菜单获取物体为空, 导致的报错
8.Fix: Save点权重时因为缺少物体而报错
9.Fix: Load权重时因为有权重锁, 可能导致设置权重失败
<p align="left">
  ▽  2020-11-26  Ver_0.81
1.Fix: 晶格、曲线、曲面的权重调整功能修复
2.Fix: 使用api Load点权重时，权重完成了点还在循环判断，会报错
</pre>
</details>

#### 2020-09  Verision: `0.6x`
<details>
<summary>详情</summary>
<pre>
1.骨骼列表刷新优化, 刷新权重注释, 不更改列表本身
<p align="left">
  ▽  2020-10-21  Ver_0.63
1.骨骼列表实现层级或平铺, 0权重显示过滤
2.WeightCheckTool: Load性能优化
3.WeightCheckTool: Select逻辑修改
</pre>
</details>


## [CopyWeightTool `|拷贝权重工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/WeightTool.py)

#### 2021-11-06  Verision: `1.4x`
<details>
<summary>详情</summary>
<pre>
1.增加向Surface面拷贝的功能
2.优化运行效率
3.Fix: 源选择为点线面时, 没有正确传权重的问题
<p align="left">
  ▽  2022-01-05  Ver_1.41
1.添加Python3支持, 版本之间字符串处理规则不同
<p align="left">
  ▽  2022-07-02  Ver_1.42
1.停止使用字符串处理规则
<p align="left">
  ▽  2022-08-11  Ver_1.43
1.Fix: 点线面组件转换的错误参数
</pre>
</details>

#### 2020-12-29  Verision: `1.3x`
<details>
<summary>详情</summary>
<pre>
1. 增加向未蒙皮物体拷贝权重的功能
2. 优化流程, 优化代码
3. Fix: 源组件为物体时, 没有可删除的内容会报黄
4. Fix: 源组件没有蒙皮时报错
<p align="left">
  ▽  2020-12-31  Ver_1.31
1.增加向多个未蒙皮物体拷贝权重的功能
<p align="left">
  ▽  2021-03-25  Ver_1.32
1.优化运行效率，避免模型面数过多时产生崩溃卡死
</pre>
</details>

#### 2020-11-30  Verision: `1.2`
<details>
<summary>详情</summary>
<pre>
1.更改数据读取方式, 不再使用Py的eval, 可能导致Maya发生循环错误
</pre>
</details>

#### 2020-11-02  Verision: `1.1`
<details>
<summary>详情</summary>
<pre>
1.在拷贝时保留权重锁
2.Fix: 一个不能运行的小问题
</pre>
</details>


## [DataSaveUi `|临时储存物体或位置|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/DataSaveUi.py)

#### 2023-10-16  Verision: `1.4x`
<details>
<summary>详情</summary>
<pre>
1.复制数据到剪切板实现跨Maya传输
2.可以存储BS和材质信息
3.可以存储信息到文件内属性
4.优化结构
</pre>
</details>

#### 2020-11-30  Verision: `1.2x`
<details>
<summary>详情</summary>
<pre>
1.更改数据读取方式, 不再使用Py的eval, 可能导致Maya发生循环错误
2.Fix: 获取位置时, 选择为空没有及时停止运行
<p align="left">
  ▽  2021-02-26  Ver_1.21
1.修改功能描述
2.Fix: Get位移和旋转时只获得了位置的问题
<p align="left">
  ▽  2022-06-25  Ver_1.22
1.添加所选物体蒙皮骨骼的存储
2.将脚本内的数据存储处理方式改为字典 (当时怎么就傻的用字符串存了再拿呢?)
<p align="left">
  ▽  2022-07-24  Ver_1.23
1.Fix:中心位置时簇点不支持Locator
<p align="left">
  ▽  2022-07-24  Ver_1.24
1.添加物体颜色储存功能
</pre>
</details>

#### 2020-11-11  Verision: `1.1x`
<details>
<summary>详情</summary>
<pre>
1.添加所选物体中心位置的储存
2.Fix: Get时的判断逻辑
3.Fix: 临时物体没删除
<p align="left">
  ▽  2020-11-11  Ver_1.12
1.Fix: Get位置时会出现很大的偏移, 全部使用约束定位, 命令对空间的转换有问题
</pre>
</details>

#### 2020-11-10  Verision: `1.0`


## [PSDshape `|辅助PSD修型工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/PSDshape.py)

#### 2021-02-04  Verision: `0.8x`
<details>
<summary>详情</summary>
<pre>
New Tool
<p align="left">
  ▽  2021-02-08  Ver_0.81
1.添加帮助文档
2.Add功能重构, 分解流程
3.当Pose存在时, 对新模型只进行BS添加, 用旧数值进行控制
<p align="left">
  ▽  2021-04-02  Ver_0.82
1.Fix:解决上版本致命错误
2.Fix:添加属性时的错误判断
3.Fix:删除Pose时的错误循环
<p align="left">
  ▽  2022-07-23  Ver_0.85
1.防止UI名重复
2.添加必备插件的检查
3.Fix:规定创建Bs时的变形器顺序
4.Fix:模型塞回时的错误方法
<p align="left">
  ▽  2022-08-11  Ver_0.86
1.修改编辑按钮逻辑
2.增加传输属性功能, 方便应用已有修型
3.完善对多模型修型的支持
4.增加无控制器时的修型支持
<p align="left">
  ▽  2023-10-16  Ver_0.87
1.不再锁定辅助节点
</pre>
</details>


## [MirrorDriverKey `|镜像驱动关键帧|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/MirrorDriverKey.py)

#### 2021-12-25  Verision: `1.0`
<details>
<summary>详情</summary>
<pre>
New Tool
<p align="left">
  ▽  2022-08-11  Ver_1.01
1.确保UI唯一性
</pre>
</details>