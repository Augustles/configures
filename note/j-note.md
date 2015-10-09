# javascript note

* JavaScript的月份范围用整数表示是0~11
* 总结一下，有这么几条规则需要遵守：
* 不要使用new Number()、new Boolean()、new String()创建包装对象；
* 用parseInt()或parseFloat()来转换任意类型到number；
* 用String()来转换任意类型到string，或者直接调用某个对象的toString()方法；
* 通常不必把任意类型转换为boolean再判断，因为可以直接写if (myVar) {...}；
* typeof操作符可以判断出number、boolean、string、function和undefined；
* 判断Array要使用Array.isArray(arr)；
* 判断null请使用myVar === null；
* 判断某个全局变量是否存在用typeof window.myVar === 'undefined'；
* 函数内部判断某个变量是否存在用typeof myVar === 'undefined'。
* 最后有细心的同学指出，任何对象都有toString()方法吗？null和undefined就没有！确实如此，这两个特殊值要除外，虽然null还伪装成了object类型。
* 更细心的同学指出，number对象调用toString()报SyntaxError：
* 123.toString(); * SyntaxError
* 遇到这种情况，要特殊处理一下：
* 123..toString(); * '123', 注意是两个点！
* (123).toString(); * '123'

* for...in/of 遍历检查属性hasOwnProperty

* 任何一个函数的声明,都会具有5个property(方法或者属性)
function add(x,y)
{
    return x+y
}
console.log(add.length); * 返回add对象的参数个数
console.log(typeof add.prototype); * 返回object对象属性和方法
console.log(typeof add.call); * 返回function /add.apply/add.constructor
* javascript数据类型, 数组,对象,变量,Map,Set
* 比较始终用===
* 创建数组一般用 l = [1,3.14,'hello',null]
* new Array(1, 'hello', true, null)
* 变量var,不用var则会被视为全局变量
* 用'use strict'避免RefernceError错误
* typeof [] 判断类型 python type()
* instanceof a instanceof Array; /补充typeof局限python isinstance()
* hasOwnProperty
* confirm() 输入确认
* prompt('please enter a word') 相当于python的input()
* console.log(true) 日志输出,相当于print()
* && python and
* || or
* ! not

var obj = new Object(); * constructor notation创建对象
var d = {
    name:'august',
    'age':23,
}
d.name + d['age']

var date = new Date();
date.getFullYear(); * return year
date.getMonth(); * return month +1
date.getDate(); * return day


* 浏览器对象, 获取尺寸window.innerHeight,window.outerWeight
* 浏览器信息, navigator.appName, appVersion, language, platform, userAgent
* 操作dom
* 返回ID为'test'的节点：
var test = document.getElementById('test');
* 先定位ID为'test-table'的节点，再返回其内部所有tr节点：
var trs = document.getElementById('test-table').getElementsByTagName('tr');
* 先定位ID为'test-div'的节点，再返回其内部所有class包含red的节点：
var reds = document.getElementById('test-div').getElementsByClassName('red');
* 定位class为'c-red'
document.getElementsByClassName("c-red")
* 获取节点test下的所有直属子节点:
var cs = test.children;
* 获取节点test下第一个、最后一个子节点：
var first = test.firstElementChild;
var last = test.lastElementChild;
