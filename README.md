# Tiny Limit

## What is TinyLimit?
tinylimit is a python modules that limits and anti-limits the calling rate of a function
与其他的limit库所不同的是，tinylimit在实战中考虑到了这些因素：
- 提供anti-limit的方法

    为了让client无视被调用函数所做出的limit限制，我们提供将调用结果保存下来，如果达到被调函数已达调用频率上线，client不是直接报错，而是直接返回最近一次的调用缓存，在某些场景下（比如获取某一日的PV），读取缓存数据并不会令程序逻辑紊乱，却避免了client堵塞。这样client可以按自己的需要随意调用受限函数即可，避免client写冗长的容错逻辑

- 根据上下文施加limit

    大部分的limit库是以函数为单位做limit，实际上很多第三方的API接口的限制单位为token，不同的token不会共享同一个limit额度，所以以函数名为指纹太泛，我们这里取了类实例的上下文、函数名、函数的参数列表三类信息来形成被调对象的指纹，用以应对这类场景

## Programming Language
- python 2.7
- python 3.7

## Install
```
pip install tinylimit 
```

## Quick Start
use python decorators syntax to wrap the call target
```
from tinylimit import AntiLimit

@AntiLimit(2,1)
def Add(a, b):
    return a + b

class Foo():
    @AntiLimit(2,1)
    def Bar(self, a, b):
        return a - b
```

## Functions List
- AntiLimit()