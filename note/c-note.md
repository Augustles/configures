##c语言笔记
char: 8位整数
short: 16位整数
int: 32位整数
long: 在32位系统是32整数, 在64位系统是64位整数
long long: 64位整数
bool: 8位整数,在stdbool.h定义了bool /true/false

float: 32位4字节浮点数, 精确度6
double: 64位8字节浮点数, 精确度15
long double: 80位10字节浮点数, 精确度19

变量一般用单引号,
int, char, float, double, void
变量声明 extern关键词, 全局变量
extern char name, pass;
变量定义
int age;
实际初始化
age = 23;

存储类定义 C 程序中变量/函数的范围（可见性）和生命周期
auto int month;
auto只能用在函数内部, 即auto只能修饰局部变量
register int miles; register 存储类, 定义存储在寄存器的局部变量
static int age; static 存储类可以修饰全局变量, 也可以局部静态变量
extern char ty; extern 存储类修饰一个全局的变量

二进制, 八进制, 十六进制写法转化
0b101, 073, 0x4b
字符常量
\n换行
\r回车
\t水平制表符
\f换页符
使用#define预处理器, const关键词定义常量
#define pi 3.14
const int age = 23;
sizeof() 返回变量的大小
&age 返回变量地址
int *p; 一个整型变量的指针
p = 23;
printf("%d", *p); 通过指针访问值

算术运算符
+, -, *, /, %
++, 自加, --自减
关系运算符
==, !=, >, <, >=, <=
逻辑运算符
&& 与, 相当于python的and
|| 或, 相当于的or
! 非, 相当于not
位运算符
~, >>, <<, ^, |, &

数组
int n[10]; 数组n, 有十个元素
n[1] = 3, 数组n第一个元素是3
字符串
char h[9] = {'h', 'e', 'l', 'l', 'o', '\0'};
char g[6] = "hello"
结构体
struct Books
{
    char title[50];
    char author[100];
    char subject[50];
    int book_id;
};
共用体
union Data
{
    int i;
    float f;
    char str[20];
};

c预处理器命令
C 预处理器只不过是一个文本替换工具而已,
在实际编译之前完成的预处理
#define xyz 223 定义宏
#include<stdio.h> 系统目录加载一个源代码文件,'stdio.h'当前目录
#undef 取消已定义的宏
#ifdef 如果宏已经定义,返回真
#ifndef 如果宏没有定义,则返回真
#if 如果条件为,编译下面代码
#else #if替代方案
#elif 如果#if不为真,当前条件为真,编译以下
#endif 结束条件编译块
#error 当遇到标准错误是,输出错误消息
#proagma
预定义宏
__DATE__ 当前日期,MMM DD YYYY格式
__TIME__ 当前时间,HH:MM:SS格式
__FILE__ 当前文件名
__LINE__ 当前行号
__STDC__ 当编译器以 ANSI 标准编译时，则定义为 1
