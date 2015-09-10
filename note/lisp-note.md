string, "hello"
symbol, 'hello
boolean, t, nil

t True
(), nill表示空列表 False,'',[],(),{}

list, cons构造列表,须有首个元素,至少两个常数
(cons 'a 'b) 产生的列表
(cons 'hello nil)
(list)
car取列表第一个元素 l[0]
cdr取列表除第一个以外元素 l[0:]
可以用first, second, third取list值 l[2],切片会少1


(let ((x 3) (y 9)) (+ x y))定义局部变量

(defparameter *x* 3)定义全局变量,一般用*x*表示
(defconstant limit (+ *glob* 1))定义常量
(setf x 99) x = 99
(psetq x 9 y 5 z 97) x,y,z = 9,5,97
(routef x y) , x,y = y,x
t对自身求值,是表示逻辑真
nil表示逻辑假,又为空表
如果实参是空表,则函数null返回T
format格式化输出,接收两个及以上参数
read输入
prin1,princ输出,前者程序,后为人

运算符
+, -, *, /, mod
min, max,
power, 乘方, sqrt, 求幂
