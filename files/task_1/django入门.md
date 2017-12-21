---
title: django入门
date: 2017-11-24 10:41:09
tags:
---
安装django：
> pip install django

# 建立项目
(以学习笔记项目为例)
进入项目的空文件夹后执行：
> (project)$ <b>django-admin.py startproject project_name .</b>

一定不能忽略结尾的“.”，否则部署应用程序时将遇到一些配置问题。
此时使用ls可以看到project文件夹中，生成了project_name文件夹，和manage.py这两个文件。再看project_name中，共有settings.py,_init_.py,wsgi.py,urls.py四个文件。

## 创建数据库
> (project)$ <b>python manage.py migrate</b>

首次执行migrate时，将让Django确保数据库与项目的当前状态匹配，此时文件夹中生成了db.sqlite3这个新文件。

## 查看项目
> (project)$ <b>python manage.py sunserver</b>

根据提示打开localhost：8000看到成功生成的网页即可。端口被占用时，在runserver后加上要使用的端口号，则用该端口号运行程序。

# 创建应用程序

首先执行：
> (project)$ <b>python manage.py startapp learning_logs</b>

执行完之后，project目录下会生成learning_logs文件夹，该文件夹中包含六个文件：admin.py,\_init\_.py,migrations文件夹,models.py,test.py,views.py。其中最重要的是models.py,admin.py和views.py。

## 定义模型Topic：
打开models.py,创建一个继承Django中Model的类。
```
from django.db import models


# Create your models here
class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.text
```

## 激活模型
打开project_name中的settings.py，找到INSTALLED_APP,将刚刚创建的自己的app添加进去
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #my apps
    'learning_logs',
]
```
## 修改数据库
> (project)$ <b>python manage.py makemigrations learning_logs</b>

会得到提示：
> Migrations for 'learning_logs':
> learning_logs\migrations\0001_initial.py
>   - Create model Topic

表明django创建了一个名为0001_initial.py的迁移文件，这个文件会在数据库中为模型(刚刚在models.py中创建的)创建一个表。
应用迁移，使django可以修改数据库：
> python manage.py migrate

执行结果为OK即可。
当需要修改应用管理的数据时，都采取如下三个步骤：在models.py修改模型，调用makemigration，让Django迁移项目。

## 管理网站

创建超级用户
> (project)$ <b>python manage.py createsuperuser</b>

接下来按照提示输入用户名、邮箱和密码,会提示创建成功。
向管理网站注册模型：
在admin.py中加入如下代码：
```
#导入models.py中创建的模型
from learning_logs.models import Topic

admin.site.register(Topic)
```
确保终端中运行着Django服务器，打开localhost:8000/admin/，并输入刚刚创建的superuser的账号密码，打开管理页面，可以添加用户和用户组，还可以管理刚刚添加的模型Topic相关的数据
添加主题:
单击Topic后点击Add添加主题。

## 定义模型Entry
还是在models.py中定义，加入如下代码；
```
class Entry(models.Model):
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    data_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
        
    def __str__(self):
        return self.text[:50]+'...'
```
topic是外键的实例，将每个条目与主题关联起来。
接下来与创建Topic模型时一样，进行迁移模型和向管理网站注册。

在管理网站中添加一些entry的数据，打开Django shell
> (project)$ python manage.py shell

用于查看数据，方便debug。

# 创建网页：网站主页
## 映射url
将基础url映射到网站主页。打开project_name文件夹中urls.py看到
```
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
```
前两行导入为项目和管理网站管理url的函数和模块，urlpatterns包含项目中所有应用程序的url。需要把我们自己创建的应用程序的url也添加到其中：
```
rom django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    <b>url(r'', include('learning_logs.urls',namespace='learning_logs')),</b>
]
```
在应用程序文件夹（learning_logs)中创建urls.py,加入如下代码：
```
from django.conf.urls import url
from . import views

urlpatterns = [
    # homepage
    url(r'^$', views.index, name='index'),
]
```
url()函数的三个参数分别是：第一个是正则表达式，表示要匹配的url的格式，如果未找到符合的格式，则返回一个错误页面；第二个参数是当url匹配时调用的函数；第三个参数是该url模式的名称，便于在其他地方引用它。

## 编写视图
在learning_logs文件夹下打开views.py，此时文件夹中只有一行
```
from django.shortcuts import render
```
表明当前只导入了render()，它根据视图提供的数据渲染响应。接下来为主页编写视图：
```
def index(request):
    return render(request, 'learning_logs/index.html')
```
在刚刚的urls.py中指出，打开主页时调用index()函数也就是此处定义的index函数，向render传递的两个参数分别是原始请求对象和用于创建网页的模板。

## 编写模板
在应用程序文件夹中创建一个名为templates的文件夹,再创建一个与应用名称相同的文件夹，之后的模板都放在该文件夹下。创建index.html
```
<p>this is Index page</p>
```
此时打开localhost:8000/，会匹配到名为index的url，调用index函数，使用index.html渲染网页。

# 创建其他网站
## 模板继承
首先创建一个名为base.html的父模板，与index.html放在同一目录下。这个文件包含所有页面都有的元素：其他的模板都继承base.html。当前，所有页面都包含的元素只有顶端的标题。我们将在每个页面中包含这个模板，因此将这个标题设置为到主页的链接：
```
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a>
</p>

{%block content%}{%endblock content%}
```
其中\{\%\%\}是模板标签，用于生成要在网页中显示的信息。\{\% block content\%\}是块标签，content是占位符，包含的信息由子模板定义。
子模板不一定必须定义所有父模板中的块，因此在父模板中可使用任意多个块来预留空间，子模版根据需要定义相应数量的块。

子模版：
重写index.html,让它继承base.html，具体如下：
```
{%extends "learning_logs/base.html"%}
{%block content%}
    <p>Learning Log helps you keep track of your learning,for any topic you're learning about.</p>
{%endblock content%}
```
子模版第一行必须包含标签\{\%extends\%\}指明继承的父模板。子模版独有的内容放在块标签\{\% block\%\}中。

## 显示左右Topic的页面
在应用程序下的url.py中添加url模式：
> url(r'^topics/$",view.topics,name='topics')

在view.py中添加匹配topics/时的函数topics：
```
def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
```

创建topics.html：
```
{%extends "learning_logs/base.html"%}
{%block content%}
    <p>Topics</p>
    <ul>
        {%for topic in topics%}
        <li>{{topic}}</li>
        {%empty%}
        <li>No topics have been added</li>
        {%endfor%}
    </ul>
{%endblock content%}
```
\{\% for item in list \%\}和\{\% endfor\%\}是用于显示列表中项的标签对，类似一个for循环。
\{\% empty\%\}标签告诉Django在列表为空时如何处理。

## 显示特定topic的页面
ulrpattern：
>  url(r'^topics/(?P<topic_id>\d+)/$', views.topic),

视图：
```
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
```
页面topic.html：
```
{%extends 'learning_logs/base.html'%}
{%block content%}
    <p>Topic:{{topic}}</p>
    <p>Entries:</p>
    <ul>
        {%for entry in entries%}
        <li>
        <p>{{entry.date_added|date:'M d, Y H:i'}}</p>
        <p>{{entry.text|linebreaks}}</p>    
        </li>
        {%empty%}
        <li>There are no entries</li>
        {%endfor%}
    </ul>
{%endblock content%}
```
将显示所有主题的页面中的每个页面都设置为链接：
修改topics.html，
```
{%for topic in topics%}
	<!--原来没有添加链接，现在加上标签<a>-->
        <li><a href="{%url 'learning_logs:topic' topic.id%}">{{topic}}</a></li>
        {%empty%}
        <li>No topics have been added</li>
      {%endfor%}
```

# 让用户能够输入数据
## 由用户添加主题
用于添加主题的表单：
让用户提交信息的网页都是表单。在Django中创建表单最简单的方式是使用ModelForm,它会根据模型（在models.py中定义的）中的信息自动创建表单。在models.py同一目录下创建forms.py。
forms.py
---
```
from  django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
```
Meta类告诉Django根据哪个模型创建怎样的表单。在上面的代码中，根据Topic创建表单，包含字段text，label变量告诉Django不要为字段text生成标签。

ulrpattern：
> url(r'^new_topic/$', views.new_topic, name='new_topic'),

添加视图函数new_topic:
views.py
---
```
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import TopicForm

def new_topic(request):
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm
    else:
        # POST提交数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
```
如果用户提交的是GET请求，表明是新打开该页面，此时创建新表单。如果是POST请求表明用户在提交表单，form实例化一个TopicForm表单，其中包含着用户提交的信息。当表单通过验证确认有效，将表单中的数据写入数据库，再调用HttpResponseRedirect重定向到/topics的页面，reverse函数用于获取topics的url。在/topics的页面中可以看到刚刚提交的新数据。

模板new_topic.html:
new_topic.html
---
```
{%extends 'learning_logs/base.html'%}

{%block content%}
    <p>Add a new topic:</p>

    <form action="{%url 'learning_logs:new_topic'%}" method="post">
        {%csrf_token%}
        {{form.as_p}}
        <button name="submit">add topic</button>
    </form>
{%endblock content%}
```
\{\%csrf_token\%\}是Django自带的用于防止跨站请求伪造攻击的模板标签，模板变量\{\{form.as_p\}\}让Django自动创建显示表单所需要的全部字段，as_p表示以段落格式渲染所有表单元素。但Django不会为表单创建提交按钮，因此需要自己定义。

将new_topic链接到topics页面：
在topics.html中添加一个锚元素。
```
<a href="\{%url 'learning_logs:new_topic'%\}">Add a new topic</a>
```
(噗本来正常情况下打开/topics和/new_topic应该就没问题了，结果有的地方少了半个引号，有的地方多了个空格，都是不太容易察觉到的错误，而且IDE也没有提示警告，又不是很熟悉debug，看Traceback再猜大概才找到问题，html里的\{\%url "namespace:name"\%\}的冒号两边是不能有空格的，否则会解析出错。)

## 用户添加条目
定义一个用于添加新条目的表单：
forms.py
---
```
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
```
通过设置widget，覆盖Django中html表单元素的默认属性。此处是让textarea的宽度由默认的40修改为80.

urlpattern:
> url(r'^new_entry/(?P<topic_id>\d+)$', views.new_entry, name='new_entry'),

视图new_entry:
views.py
---
```
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                arge=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
```
第9行调用form.save()时传递了commit=False的参数，让Django不要存储到数据库，而是把数据存储到变量new_entry中，new_entry中加上topic属性后再存入数据库。12行的reverse方法需要两个参数，第一个是url,第二个是参数列表，需要包含url需要的所有实参。

模板new_entry.html:
new_entry.html
---
```
{% extends "learning_logs/base.html" %}

{%block content%}
<p><a href="{%url 'learning_logs:topic' topic.id%}">{{topic}}</a> </p>
<p>add a new entry:</p>
    <form action="{%url 'learning_logs:new_entry' topic.id%}" method="post">
        {%csrf_token%}
        {{form.as_p}}
        <button name="submit">add entry</button>
    </form>
{%endblock content%}
```

添加转到new_entry页面的链接：
topic.html
---
```
...
<p>Entries:</p>
    <p><a href="{% url 'learning_logs:new_entry' topic.id %}">Add a new entry</a></p>
    <ul>
    ...
```

## 编辑既有条目
urlpattern:
> url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

视图函数edit_entry:
views.py
---
```
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic,'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
```

模板edit_entry.html:
edit_entry
---
```
{%extends 'learning_logs/base.html'%}
{%block content%}
    <p><a href="{%url 'learning_logs:topic' topic.id%}">{{topic}}</a> </p>
    <p>Edit entry:</p>
    <form action="{%url 'learning_logs:edit_entry' entry.id%}" method="post">
        {%csrf_token%}
        {{form.as_p}}
        <button name="submit">save change</button>
    </form>
{%endblock content%}
```
在topic.html中添加上到编辑条目的界面的链接。