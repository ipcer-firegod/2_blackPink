# d1
## 18-模版字符串
```js
    // // 模板字符串 外面用`` 里面 ${变量名}
    // document.write(`我今年${age}岁了`)
    let uname = prompt('请输入您的姓名:')
    let age = prompt('请输入您的年龄:')
    // 输出
    document.write(`大家好，我叫${uname}， 我今年贵庚${age}岁了`)
```
## 22-显示转换
```javascript
    // 显示转换数字
    // <!--! prompt 得到是字符串类型 要转换为 数字型  -->
    let num = Number(prompt('输入年薪'))
    let num = +prompt('输入年薪')
  
    // 
```
  转为数字的方法有，分别意味着：
  Number: 转换为数字类型
  parseInt: 转换为整数
  parseFloat: 转换为浮点数

- 通过 `Number` 显示转换成数值类型，当转换失败时结果为 `NaN`（Not a Number）即不是一个数字。
- 未定义是比较特殊的类型，只有一个值 undefined，只声明变量，不赋值的情况下，变量的默认值为 undefined，一般很少【直接】为某个变量赋值为 undefined。

# d2
## 
20-综合案例

# d3
##
数组操作
13-数组筛选
16-综合案例
17-冒泡排序

# d4
##
15-立即执行函数
    // (function(){})()
    // (function(){}())

18-转化为布尔类型

# d5
##
04-遍历对象
05-遍历数组对象
06-渲染学生信息表
08-数学内置对象
14-数据类型存存储

```js
    // 取到 N ~ M 的随机整数
    function getRandom(N, M) {
      return Math.floor(Math.random() * (M - N + 1)) + N
    }
```