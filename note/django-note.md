##djangonote

tutorial1
1.django-admin.pystartnewsubject;创建新项目
2.pythonmanage.pyrunserver0.0.0.0:8080;绑定.0开发用服务器
3.pythonmanage.pysyncdb;创建数据库的表
4.pythonmanage.pystartappblog;创建blog应用
5.settings.py激活INSTALLED_APPS的blog应用

tutorial2
admin应用

tutorial3
1.view.py,HttpResponse,render,get_object_or_404()
2.url.py,url,patterns
3.form.py,Template(模版加载),Context(渲染内容)





tips:
1.pythonmanage.pyshell;进入django交互shell

django的调度逻辑图

目录
setting
url转发
view视图
django模版
form表单
model
一、settings
引用setting项
from django.conf import settings
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
二、urlconf
主页url文档
urlpatterns是所有url的链表，可以+=
from django.conf.urls import patterns,include,url
urlpatterns=patterns('',)
urlpatterns+=patterns('',
url(r'^tag/(?P\w+)/$','tag'),)
可以使用include来引用app内部urls.py文件
url(r'^elist/',include('elist.urls')),
url中引用参数
在需要捕捉的地方用括号括起来
(r'homeworklist/edit/([^/]+)/$',edit_homeworklist),
调用结果：edit_homeworklist(request,参数)

命名参数?P
(r'homeworklist/edit/(?P[^/]+)/$',edit_homeworklist),
调用结果：edit_homeworklist(request,id='参数')
patterns的前缀字符串,用于缩短视图函数
urlpatterns=patterns('',
url(r'^articles/(\d{4})/$','news.views.year_archive'),)

等价：
urlpatterns=patterns('new.views',
url(r'^articles/(\d{4})/$','year_archive'),)
url()函数
格式：
url(regex,view,kwargs=None,name=None,prefix='')
传递参数：
url(r'^blog/(?P\d{4})/$','year_archive',{'foo':'bar'}),
命名url
url(r'^archive/(\d{4})/$',archive,name="full-archive"),
url(r'^archive-summary/(\d{4})/$',archive,{'summary':True},name="arch-summary"),
在模板中使用
{%url'arch-summary'1945%}
{%url'full-archive'2007%}
url的反向解析
Intemplates:Usingtheurltemplatetag.
InPythoncode:Usingthedjango.core.urlresolvers.reverse()function.
InhigherlevelcoderelatedtohandlingofURLsofDjangomodelinstances:Theget_absolute_url()method.
详细文档
redirect()文档
虽然这个函数不属于urlconf配置的一部分，但是他在功能上起到转向分发的作用，所以我也把他放到这一节。常见的使用方法：
传入一个对象,返回访问这个对象的url（推荐使用reverse()）
传入一个url,进行跳转
return redirect('/some/url/')
return redirect('http://example.com/')
三、view
输入request,返回response.
HttpResponse(最简单)
文档
from django.http import HttpResponse
html="Itisnow%s."%now
return HttpResponse(html)
render_to_response
文档
from django.shortcuts import render_to_response
render_to_response(template_name[,dictionary][,context_instance][,content_type])
范例
return render_to_response('myapp/index.html',{"foo":"bar"},
mimetype="application/xhtml+xml")
默认的render_to_response是不包含request，如果要使用HttpRequest,需要手工定义context_instance=RequestContext(request)
return render_to_response('my_template.html',
my_data_dictionary,
context_instance=RequestContext(request))
render(应用模板，比较简洁)
文档,默认使用RequestContext的render_to_response
from django.shortcuts import render
render(request,template_name[,dictionary][,context_instance]
[,content_type][,status][,current_app])
request
模板名称
附加字典
上下文对象
内容类型
状态200404500
return render(request,'myapp/index.html',{"foo":"bar"},
content_type="application/xhtml+xml")
和django.template下的手工loader等效
t=loader.get_template('myapp/template.html')
c=RequestContext(request,{'foo':'bar'})
returnHttp Response(t.render(c),
content_type="application/xhtml+xml")
四、模板
{% extends "base_generic.html" %}
{%blocktitle%}{{section.title}}{%endblock%}
{%blockcontent%}
{{section.title}}
{%forstoryinstory_list%}
{{story.headline|upper}}
{{story.tease|truncatewords:"100"}}
{%endfor%}
{%endblock%}
变量
{{变量名}}
点的解释顺序
1.字典
2.属性
3.方法
4.列表索引
过滤器
可以用来修饰变量，{{变量名|过滤器}}
使用参数的例子{{value|add:"2"}}
内置的过滤器目录
default默认值{{value|default:"nothing"}}
标签
{%标签名称%}
内置的模板标签目录
for endfor
for...empty
if elif else endif
{#注释内容#}单行注释
{%comment%}...{%endcomment%}多行注释
{%verbatim%}...{%endverbatim%}禁止render,比如包围javascript模板
{%csrf_token%}保护
now现在日期、时间详细格式
Itis{%now"jSFYH:i"%}
{%cycle'row1''row2'%}交替详细文档
regroup可以根据字段、属性进行分组详细文档
根据国家进行分组
{%regroupcities|dictsort:"country"bycountryascountry_list%}
i fequal如果相等
if noequal如果不等
if changed如果改变
{%fordateindays%}
{%ifchangeddate.date%}{{date.date}}{%endifchanged%}
{%ifchangeddate.hourdate.date%}
{{date.hour}}
{%endifchanged%}
{%endfor%}
布尔操作详细文档（优先级由低到高）
or
and
not
in
==、!=、>、>=、<、<=
{%include其他模板%}
{%include"foo/bar.html"%}
传递参数
{% include"name_snippet.html" with person="Jane" greeting="Hello"%}
{%ssi本地文件%}详细文档
url
第一个参数是view函数的路径，格式是package.package.module.function之后的参数使用/连接
范例
{%url'path.to.view'argarg2asthe_url%}
I'mlinkingto{{the_url}}
可以使用过滤器,但大部分过滤器都返回字符串结果
{%ifathlete_list|length>1%}
Team:{%forathleteinathlete_list%}...{%endfor%}
{%else%}
Athlete:{{athlete_list.0.name}}
{%endif%}
继承
{%block名称%}...{%endblock%}
{%extends"base.html"%}必须第一行
{%blocktitle%}Myamazingblog{%endblock%}
{{block.super}}引用父模版的内容{%block名称%}...{%endblock名称%}方便阅读
五、form表单
第一部分：定义
可以使用两种方式
自己定义详细文档
fromdjangoimportforms
class ContactForm(forms.Form):
    subject=forms.CharField(max_length=100)
    message=forms.CharField()
    sender=forms.EmailField()
    cc_myself=forms.BooleanField(required=False)
继承model详细文档
from django.forms import ModelForm
#有定义模块
classArticle(models.Model):
headline=models.CharField(max_length=200)
#...
sites=models.ManyToManyField(Site)
classArticleForm(ModelForm):
classMeta:
model=Article
第二部分：显示
在把form表单和模板进行结合之前，先要知道如何处理提交的表单。
(预备知识)在view中的标准处理form的框架
fromdjango.shortcutsimportrender
fromdjango.httpimportHttpResponseRedirect

defcontact(request):
ifrequest.method=='POST':#表单被提交
form=ContactForm(request.POST)#表单绑定了post数据
ifform.is_valid():#所有的表单验证通过
#对数据进行一些处理
#...
return HttpResponseRedirect('/thanks/')#转向或者其他操作
else:
form=ContactForm()#没有提交的表单

returnrender(request,'contact.html',{
'form':form,
})
统一显示
form.as_p由
包围,分行显示
form.as_table生成表格
form.as_ul生成列表项
#实际的模板例子(contact.html)
{%csrf_token%}
{{form.as_p}}


单独自定义显示详细文档


{{form.subject.errors}}
Emailsubject:
{{form.subject}}


引用字段
{{form.字段名}}
引用字段验证错误
{{form.字段名.errors}}
第三部分：验证
详细文档分为多个层次,检测失败会返回ValidationError
to_python()　　　　[forms.Field]转换成python的类型使用范例
validate()　　　　[forms.Field]针对特别字段验证，又不想放到验证器当中，不返回值
run_validators()　运行所有字段级别验证，收集错误，不需要改写
字段级别clean() 调用上面3项验证，一旦有错，验证停止，否则返回cleandata字典
表单级别clean_()　验证特别的字段
表单级别clean()　负责整个表单的验证，手工返回self.cleaned_data
form组件自身的验证
默认django会自动对form组件的post内容根据定义的类型进行验证,如果需要自定义，需要在forms.Field中定义。
范例(上面的ContactForm为例)：
>>>data={'bookid':'aa','days':datetime.datetime.now(),'subject':'ehllo'}
>>>f=ContactForm(data)
>>>f.is_valid()
False
>>>f.errors
{'bookid':[u'Enterawholenumber.']}
定义Field子类进行验证
使用to_python()和validate()的例子：
假设需要定义一个多邮件的组合字段，用逗号分隔邮件地址
fromdjangoimportforms
fromdjango.core.validatorsimportvalidate_email

classMultiEmailField(forms.Field):
defto_python(self,value):
"Normalizedatatoalistofstrings."

#Returnanemptylistifnoinputwasgiven.
ifnotvalue:
return[]
returnvalue.split(',')

defvalidate(self,value):
"Checkifvalueconsistsonlyofvalidemails."

#Usetheparent'shandlingofrequiredfields,etc.
super(MultiEmailField,self).validate(value)

foremailinvalue:
validate_email(email)
form内针对字段的验证
举一个验证recipients字段必须包含fred@example.com项目
classContactForm(forms.Form):
#Everythingasbefore.
...

defclean_recipients(self):
data=self.cleaned_data['recipients']
if"fred@example.com"notindata:
raiseforms.ValidationError("YouhaveforgottenaboutFred!")

#Alwaysreturnthecleaneddata,whetheryouhavechangeditor
#not.
returndata
form表单的组合验证
如果我们有个需求需要验证比如密码和重复密码是否相同的话。这样验证单个字段的方法就没有用了,需要form的clean()方法
classContactForm(forms.Form):
#Everythingasbefore.
...

def clean(self):
    cleaned_data=super(ContactForm,self).clean()
    password=self.cleaned_data.get('password','').strip()
    password1=self.cleaned_data.get('password1','').strip()
if password and password1 and password!=password1:
    msg=u'两次密码输入不一致'
    self._errors["password1"]=ErrorList([msg])
    delself.cleaned_data["password1"]
    return self.cleaned_data
第四部分：访问clean的数据
表单的Post数据如果通过了验证，就叫做cleaned数据，被存放在Form.cleaned_data字典中。
>>>data={'bookid':'12','days':datetime.datetime.now(),'subject':'ehllo'}
>>>f=ContactForm(data)
>>>f.is_valid()
True
>>>f.cleaned_data
{'bookid':12,'days':datetime.date(2013,6,16),'subject':u'ehllo'}
>>>f.cleaned_data['days']
datetime.date(2013,6,16)
六、model
主页url文档一个model类表示一个数据表，一个类的实例代表表中的记录
第一部分：定义
字段的命名不能包括两个下划线
简单的例子
from django.db import models

class Person(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
字段类型
类型清单BooleanField、CharField(max_length=None)...
自定义新类型
通用参数
null　　　　默认False
blank　　　　默认False,True字段允许为空
default　　　默认值,也可是可调用的对象
help_text　　
primary_key　　True,会把当前字段当成主键
unique　　True,表示唯一
verbose_name　　字段名字
choices　　　选择,使用get_字段名称_desplay()显示内容
fromdjango.dbimportmodels

classPerson(models.Model):
SHIRT_SIZES=(
('S','Small'),
('M','Medium'),
('L','Large'),
)
name=models.CharField(max_length=60)
shirt_size=models.CharField(max_length=1,
choices=SHIRT_SIZES)


#使用choice的例子
>>>p=Person(name="FredFlintstone",shirt_size="L")
>>>p.save()
>>>p.shirt_size
u'L'
>>>p.get_shirt_size_display()
u'Large'

#使用enumerate生成choice的例子
#和上面的定义作用类似
SHIRT_SIZES=enumerate(("Small","Medium","Large"))
关系
ForeignKey　　　　详细文档
引用未定义　　　　''字符串
递归　　　　　　　　'self'
ManyToManyField　　详细文档使用范例
OneToOneField　　　　
元数据
ordering　　　　　　　　　　顺序
db_table　　　　　　　　　　数据库名称
verbose_name　　　　　　　对象名称
verbose_name_plural　　　复数对象名称
详细清单
classOx(models.Model):
horn_length=models.IntegerField()

classMeta:
ordering=["horn_length"]
verbose_name_plural="oxen"
模型方法
property　　　　　　　　　　属性
def_get_full_name(self):
    "Returns theperson's fullname."
    return'%s%s'%(self.first_name,self.last_name)
full_name=property(_get_full_name)
__unicode__()　　　　　　　文本格式显示对象
get_absolute_url()　　　　　　　返回对象的url地址详细文档
save()　　　　　　　保存
delete()　　　　　　　删除
第二部分：查询
文档范例的model定义
建立实体(记录)
用字典作为参数实例化一个model类，然后save()保存。
b=Blog(name='BeatlesBlog',tagline='AllthelatestBeatlesnews.')
b.save()
修改记录
普通model,首先用get()等方法检索一个实体对象，修改属性，然后save()保存。
更新外键ForeignKey
>>>e=Entry(headline='headline',body_text='aaa',
pub_date=datetime.datetime.now(),
mod_date=datetime.datetime.now(),
n_comments=12,n_pingbacks=3,
rating=5)
>>>e.blog=b
>>>e.save()
更新ManyToManyField
>>>joe=Author(name='bbb',email='aaa@test.com')
>>>joe.save()
>>>e.authors.add(joe)
#另外一种方法建立
>>>newjoe=Author.objects.create(name='John')
>>>newjoe.save()
>>>e.authors.add(newjoe)
#同时增加多个对象关系
>>>entry.authors.add(john,paul,george,ringo)
普通检索记录
QuerySet　　　　检索集合结果，也可以看成是数据对象的集合，
　　　　　　　　　可以有0-n个过滤器(filter)
Manager　　　　每个model都至少有一个Manager，默认名称是objects
#获取所有记录
>>>all_entries=Entry.objects.all()
使用过滤器
filter　　　　包含匹配
exclude　　　不包含匹配
#过滤年
>>>Entry.objects.filter(pub_date__year=2006)

#连续串联过滤
#所有headline满足What开头，出版时间在2005年1月30至今
>>>Entry.objects.filter(
headline__startswith='What'
).exclude(
pub_date__gte=datetime.date.today()
).filter(
pub_date__gte=datetime(2005,1,30)
)
使用get获得单个对象
没有结果会报DoesNotExist，多个结果报MultipleObjectsReturned
>>>one_entry=Entry.objects.get(pk=1)
#结果切片
>>>Entry.objects.all()[5:10]
查找类型　　　　Lookups完整列表
exact　　　　精确匹配
Entry.objects.get(id__exact=14)
iexact　　　　不区分大小写匹配
Blog.objects.get(name__iexact='beatlesblog')
contains　　　　区分大小写包含
icontains　　　　不区分大小写包含
startswith　　　　开始
endswith　　　　结束
in　　　　　　　　在列表内
Entry.objects.filter(id__in=[1,3,4])
#动态生成列表
inner_qs=Blog.objects.filter(name__contains='Cheddar')
entries=Entry.objects.filter(blog__in=inner_qs)
pk
可以使用pk作为主键进行检索get(id__exact=14)(id=14)(pk=14)效果相同。
#一些例子
>>>Blog.objects.filter(pk__in=[1,4,7])
>>>Blog.objects.filter(pk__gt=14)
跨越关系检索记录
双下划线能够扩展到相关的model字段范例模型
#检索Entry-->blog-->name是"BeatlesBlog"
>>>Entry.objects.filter(blog__name__exact='BeatlesBlog')
#pk的跨越关系检索
>>>Entry.objects.filter(blog__pk=3)
双下划线加上小写的model名，可以反方向引用
#反向检索Blog-->entry-->headline包含'Lennon'
>>>Blog.objects.filter(entry__headline__contains='Lennon')
使用F()表达式进行检索
可以对同一个model的不同字段进行比较、计算(加减乘除)
>>>fromdjango.db.modelsimportF

#检索Entry中n_comments数值比n_pingbacks的记录
>>>Entry.objects.filter(n_comments__gt=F('n_pingbacks'))

#(计算范例)n_comments数值比n_pingbacks多两倍的记录
>>>Entry.objects.filter(n_comments__gt=F('n_pingbacks')*2)

#(使用双下划线跨越关系和F()类的例子)
#所有authors的name与blog的name相同
>>>Entry.objects.filter(authors__name=F('blog__name'))
使用Q类进行复杂检索
filter进行筛选，组合条件都是AND关系，使用Q对象能进行OR关系组合条件。
Q实例是筛选条件的封装,|OR&与
fromdjango.db.modelsimportQ
Q(question__startswith='What')

Poll.objects.get(
Q(question__startswith='Who'),
Q(pub_date=date(2005,5,2))|Q(pub_date=date(2005,5,6))
)
第三部分：其他操作
比较记录对象
>>>some_obj==other_obj
删除记录对象
默认情况下以该对象为主键的对应记录被删除>>>Entry.objects.filter(pub_date__year=2005).delete()
拷贝记录对象
把pk设为None，然后保存
>>>blog=Blog(name='Myblog',tagline='Bloggingiseasy')
>>>blog.save()#blog.pk==1

>>>blog.pk=None
>>>blog.save()#blog.pk==2
一次更新多条记录
update()
>>>Entry.objects.filter(pub_date__year=2007).update(headline='Everythingisthesame')
引用关联对象
e(Entry)-->blog属性
>>>e.blog
_set　　　　反向引用b(Blog)-->Entry
>>>b.entry_set.all()
select_related()　　　　递归取得关联数据，进入cache
>>>e=Entry.objects.select_related().get(id=2)
>>>print(e.blog)#直接使用缓存
