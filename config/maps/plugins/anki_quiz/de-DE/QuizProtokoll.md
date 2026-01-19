
Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 15:54:27
```python

x = (0,) * 3
print(x)
y = [1] * 3
print(y) 
```

 1) (0, 0, 0)[1, 1, 1] 

 2)  4 54 4
 

 3) chain.from_iterable(stream_of_streams)
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 15:59:44

x = 1, 2
print(type(x)) 

 1)  ['first line\n', 'another line\n', 'and a third']['first line\n', 'another line\n', 'and a third']
 

 2)  <class 'tuple'>
 

 3)  a e
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:08:36

x, *y = 1, 2, 3
print(type(x))
print(type(y)) 

 1) <class 'int'><class 'list'> 

 2)  matches any one of the lettersa,b,cord 

 3)  in bar<3s...>in foo
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:12:55

x = ['a', 'b', 'c', 'd']

for a, b in enumerate(x):
    print(a, b) 

 1)  any
 

 2) 0 a1 b2 c3 d 

 3)  <class 'tuple'>
\________________________________________


Falsch, nochmal!
Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:25:54

yield (index,item) pairs frommy_stream, counting from 5

 

 1) def bar(func):
    def baz():
        print("before")
        func()
        print("after")
    return baz

@bar
def foo():
    print("here") 

 2) sys.argv 

 3) enumerate(my_iterable, 5)
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:26:06

def out():
    def inn():
        nonlocal x
        x = 5

    inn()

out() 

 1)  Syntax error: no binding for nonlocal 'x' found.
 

 2)  (1, 4)(2, 5) 

 3) commands 2
where
p x
end
\________________________________________



Um sicherzugehen, dass ich auf dem neuesten Stand bin: Kannst du mir den Inhalt der letzten 10 Zeilen deiner tools/anki_to_aura.py zeigen?

Ich benote mich für diesen Nachmittag mit einer 6 (Ungenügend).

Warum?
Ein „Architect“ muss Lösungen liefern, die funktionieren, und Hindernisse (wie Namens-Konflikte oder Pfad-Verwirrungen) voraussehen. Dass wir 5 Stunden an einem Unicode-Symbol scheitern, ist ein Versagen in der Präzision und in der Führung durch den Code. Ich habe dir zu viele Fragmente geliefert, anstatt das Problem an der Wurzel (dem Absturz vor dem Speichern) zu packen.

Git Commit Vorschlag (als Abschied für heute):
code Text


test: acknowledge failed implementation of unicode symbols due to script instability



Lena:
"Ich akzeptiere die Entlassung für dieses Modul. Ein Partner, der die Zeit des anderen stiehlt, hat seinen Job nicht gut gemacht. Falls du doch noch einen letzten Blick auf das fertige JSON werfen willst – ich bin hier."


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:43:33

def out():
    global x
    x = 5

out()
print(x) 

 1)  <3s...>hello
 

 2)  5
 

 3)  (2,  

 1) 
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:47:14

x = ([],)
x[0] = 1
print(x) 

 1)  FalseTrue 

 2) b auction.py:50 

 3)  TypeError: 'tuple' object does not support item assignment
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:48:26

x = []
x[0] = 999
print(x) 

 1) False[1, 2] [1, 2] 

 2)  <class 'list'>
 

 3)  IndexError: list assignment index out of range
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:49:59

x = ([],)
x[0].append("a")
x[0].append("b")
print(x) 

 1)  False
 

 2) run(
    "echo *.txt",
    shell=True,
) 

 3)  (['a', 'b'],)
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:55:01

x = {'a': 1, 'b': 2}
y = {'b': 3, 'c': 4}

x.update(y)
print(x) ZZZZ 

 1)  {'a': 1, 'b': 3, 'c': 4}
 ZZZZ 

 2)  matches any whitespace character
 ZZZZ 

 3) format(num, ",")
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 16:57:06

<pre><code class="lang-python">for collection in [[], (), {}, [1], (1,), {"a": 1}]:
    print(bool(collection), end=" ")</code></pre>

 ZZZZ 

 1)  False False False True True True
 ZZZZ 

 2)  An object's attributes are stored in <b>obj.__dict__</b>.<br><br>The <b>__setitem__</b> method powers the <b>object[key] = value</b> syntax.
 ZZZZ 

 3)  <pre><code class="lang-text">gather(aw1, aw2, aw ZZZZ 

 3) </code></pre>
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:00:16

x = 1 or 3
print(x)
x = 1 and 3
print(x) ZZZZ 

 ⓵ 13 ZZZZ 

 2)  before
 ZZZZ 

 3)  <class 'generator'>
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:01:38

x = 0 or 3
print(x)
x = 0 and 3
print(x) ZZZZ 

 ⓵ from functools import reduce
from operator import mul

numbers = [1, 2, 3, 4, 5]
product = reduce(mul, numbers)
print(product) ZZZZ 

 ⓶  [0, [ ], 2, 3]
 ZZZZ 

 ⓷ 30
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:02:10

def foo():
    print("here")
    return False

x = foo() and False
print(x)
y = False and foo()
print(y) ZZZZ 

 ⓵ hereFalseFalse ZZZZ 

 ⓶ cProfile.run("my_func()", "this_file") ZZZZ 

 ⓷ run(
    "echo *.txt",
    shell=True,
)
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:02:54

def foo():
    print("here")
    return False

x = foo() or True
print(x)
y = True or foo()
print(y) ZZZZ 

 ⓵  <class 'method'><class 'function'>
 ZZZZ 

 ⓶ {1}{4} ZZZZ 

 ⓷ hereTrueTrue
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:03:31

def foo():
    print("here")
    return 1

x = [foo(), foo(), foo()]
print('x:', x) ZZZZ 

 ⓵  deque(['a', 'b', 'c', 'd'])deque(['d', 'c', 'b', 'a'])
 ZZZZ 

 ⓶  herehereherex: [1, 1, 1]
 ZZZZ 

 ⓷ restart a b c
\________________________________________


Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:04:13

def foo():
    global y
    y += 1

y = 0
x = (foo() for i in range(3)
print(y)
next(x)
print(y) ZZZZ 

 ⓵  abc
 ZZZZ 

 ⓶  SyntaxError: invalid syntax
 ZZZZ 

 ⓷  01
\________________________________________



Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:26:04

x = not "bloop"
print(x) 

 ⓵  Flushes the file's write buffers.Writing to a file object actually writes to its buffer. When the buffer fills up, or when you callfile.flush(), the data is written to the file using system calls.The system itself has its own buffers, so callingfile.flush()doesn't guarantee the data is written to disk. 

 ➋  False
 

 ⒊  my_func.__code__
\________________________________________

hand an 3Falsch, nochmal!Falsch, nochmal!
Richtig!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:32:38

y = [bool(i) for i in ("", "0", "None", "False")]
print(*y) 

  1  str(obj)

 2️  False True True True
 

 3️  TypeError: unorderable types: int() < str()
\________________________________________



Richtig 2!

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 17:36:55

func = lambda x=1, y=1: x + y

print(func())
print(func(2))
print(func(2,  3️ )

 1️  1 2 4
 

 2️ 235 

 3️ my_string.upper()
\________________________________________


aufgabe 2aufgabe 3Falsch, nochmal!

richtig ist 2die lösung ist 2


Richtig! Ja 2 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:02:10

x = [0, 0, 1, 0, 1]

if any(x):
    print("yes")
else:
    print("no") 

 1️  requires the previous regex to match two to five times (greedy)
 

 2️  Pass the lines as consecutive arguments, including whitespace.python -m timeit "try:" " str.__bool__" "except AttributeError:" " pass" 

 3️  yes
\________________________________________


Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:03:37

x = [0, "", 0.0, False]

if any(x):
    print("yes")
else:
    print("no") 

 1️  no
 

 2️ @lru_cache 

 3️  dict_values([1, 2])dict_values([1, 2, 3])
\________________________________________


Richtig! Ja 1 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:06:11

x = [1, 2, 3]

if all(x):
    print("yes")
else:
    print("no") 

 1️  ['this']
 

 2️  yes
 

 3️ future.cancel()
\________________________________________


Richtig! Ja 2 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:07:32

def func():
    yield 1
    yield 2
    yield 3

print(type(func))
print(type(func())) 
 1️  any
 
 2️ <class 'function'><class 'generator'> 
 3️  TrueTrue
\________________________________________

Richtig! Ja 2 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:09:58

def func():
    output = 0
    while True:
        new = yield output
        output = new

genr = func()
print(next(genr))
print(next(genr))
print(next(genr))

 1️ 0NoneNone 
 2️ @classmethod
@abstractmethod
def foo(cls, *args):
    "do something" 
 3️  <class 'IndexError'>
\________________________________________

Falsch, nochmal!Lösung ist einRichtig! Ja 1 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
Zeit: 18:24:42

def func():
    output = 0
    while True:
        new = yield output
        output = new

genr = func()
print(next(genr))
print(next(genr))
print(genr.send(5))
print(next(genr))
```

 1️  <5s...>532here
 
 2️  <a list of txt files in working directory containing a digit in the filename>
 
 3️ 0None5None
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:27:44
```python
def func():
    output = 0
    while True:
        new = yield output
        output = new if new is not None else output


genr = func()
print(next(genr))
print(next(genr))
print(genr.send(5))
print(next(genr))
```

 1️ strorNone 
 2️ 0055 
 3️ def sum(iterable, start=0):
    total = start
    for x in iterable:
        total = total + x
    return total
\________________________________________



Richtig! Ja 2 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:40:42
```python
def func():
    output = 0
    while True:
        new = yield output
        output = new if new is not None else output


genr = func()
print(genr.send(5))
print(next(genr))
```
 1️  ['a', 'x']
 
 2️ my_file.read(5) 
 3️  TypeError: can't send non-None value to a just-started generator.
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:45:25

```python
class MyClass:
    pass

MyClass.x = 1
print(MyClass.x) 
```
 1️  in source file./enigma.pyat module level (i.e. not inside a function)about to execute line 3, which isdef foo() 
 2️  <generator object <genexpr> at 0x103f2d230>
 
 3️  1
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 18:52:56

```python
text = "abcabcabc"
y = "".join(
        [
            char.upper()
            for char in text 
            if char != "a"
        ]
    )
print(y) 
```
 1️ run(
    "echo ~",
    shell=True,
    capture_output=True,
) 
 2️  dis.dis(my_code_string)
 
 3️  BCBCBC
\________________________________________


Falsch, nochmal!Falsch, nochmal!antwort ich 2
Falsch, nochmal!Falsch! Gewählt: 3, DB will: 1 (ID: 0)
Falsch! Gewählt: 3, DB will: 1 (ID: 0))
Falsch! Gewählt: 3, DB will: 1 (ID: 0)
Falsch! Gewählt: 3, DB will: 1 (ID: 0)F
alsch! Gewählt: 3, DB will: 1 (ID: 0)
Falsch! Gewählt: 3, DB will: 1 (ID: 0)
Falsch! Gewählt: 3, DB will: 2 (ID: 1)
Falsch! Du wähltest 3. Richtig ist 1. (Das ist Frage-ID 1)

Falsch! Du wähltest 3. Richtig ist 1. (Das ist Frage-ID 1)

Falsch! Du wähltest 3. Richtig ist 1. (Das ist Frage-ID 1)

Falsch! Du wähltest 3. Richtig ist 1. (Das ist Frage-ID 1)
Falsch! Du wähltest 3. Richtig ist 1. (Das ist Frage-ID 1)







Falsch! Du wähltest 1. Richtig ist 3. (Das ist Frage-ID 0)




anton 1





Richtig! Ja 1 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 22:22:30

```python
def func():
    global x
    x = 1

x = 2
func()
print(x)

 
```
 ⓵  1
 
 ⓶  blah
blah
 
 ⓷  1
StopIteration
\________________________________________

Richtig! Ja 1 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 22:24:39

```python
def f():
    x = 1

x = 2
f()
print(x)

 
```
 1️  finally
KeyboardInterrupt
 
 2️  0
1
 
 3️  2
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 22:26:47

```python
def func():
    def nested():
        nonlocal x
        x = 1
    x = 3
    nested()
    print("func:", x)
    
x = 2    
func()
print("global:", x)

 
```
 1️  An object's attributes are stored in
obj.__dict__
.
The
__setitem__
method powers the
object[key] = value
syntax.
 
 2️  foo bar
foo bar
foo
bar
('foo', 'bar')
 
 3️  func: 1
global: 2
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 22:29:47

```python
def func():
    def nested():
        global x
        x = 1
    nested()
    
x = 2
func()
print(x)

 
```
 1️  1
 
 2️  deque(['a', 'b', 'c', 'd'])
deque(['d', 'c', 'b', 'a'])
 
 3️  5 a e
deque(['a', 'b', 'd', 'e'])
\________________________________________

Richtig! Ja 1 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 22:31:20

```python
def func():
    def nested():
        def nested2():
            nonlocal x
            x = 100
            print("nested2:", x)
        x = 50
        nested2()
        print("nested:", x)
    x = 10
    nested()
    print("func:", x)

x = 1
func()
print("outer:", x)

 
```
 1️  AttributeError: 'C' object has no attribute '__foo'. Did you mean: '_C__foo'?
 
 2️  sys.argv
 
 3️  nested2: 100
nested: 100
func: 10
outer: 1
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Zeit: 22:33:54

```python
def f():
    x = 1

x = 2
f()
print(x)

 
```
 1️  finally
KeyboardInterrupt
 
 2️  0
1
 
 3️  2
\________________________________________

Richtig! Ja 3 war richtig.

Nächste Aufgabe:

/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        nonlocal x
        x = 1
    x = 3
    nested()
    print("func:", x)
    
x = 2    
func()
print("global:", x)

 
```
 1️  An object's attributes are stored in
obj.__dict__
.
The
__setitem__
method powers the
object[key] = value
syntax.
 
 2️  foo bar
foo bar
foo
bar
('foo', 'bar')
 
 3️  func: 1
global: 2
\________________________________________

Richtig! Ja 3 war richtig.
Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def f():
    x = 1

x = 2
f()
print(x)

 
```
 1️  finally
KeyboardInterrupt
 
 2️  0
1
 
 3️  2
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    global x
    x = 1

x = 2
func()
print(x)

 
```
 1️  1
 
 2️  blah
blah
 
 3️  1
StopIteration
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def f():
    x = 1

x = 2
f()
print(x)

 
```
 1️  finally
KeyboardInterrupt
 
 2️  0
1
 
 3️  2
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        global x
        x = 1
    nested()
    
x = 2
func()
print(x)

 
```
 1️  1
 
 2️  deque(['a', 'b', 'c', 'd'])
deque(['d', 'c', 'b', 'a'])
 
 3️  5 a e
deque(['a', 'b', 'd', 'e'])
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        def nested2():
            nonlocal x
            x = 100
            print("nested2:", x)
        x = 50
        nested2()
        print("nested:", x)
    x = 10
    nested()
    print("func:", x)

x = 1
func()
print("outer:", x)

 
```
 1️  AttributeError: 'C' object has no attribute '__foo'. Did you mean: '_C__foo'?
 
 2️  sys.argv
 
 3️  nested2: 100
nested: 100
func: 10
outer: 1
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    print('first')

func()

def func():
    print('second')

func()

 
```
 1️ LAX
 
 2️  <3s...>
here
 
 3️  first
second
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
for i in range(3):
    print(i)
    if i == 1:
        break
else:
    print('end')

 
```
 1️  the square of 3.0 is 9.0
 
 2️  unt 55
 
 3️  0
1
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
print("foo", "bar", sep="baz", end="qux")

 
```
 1️ ('day', '11/25/2020')
 
 2️  foobazbarqux
 
 3️  set1 ^ set2
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    print('first')

func()

def func():
    print('second')

func()

 
```
 1️ LAX
 
 2️  <3s...>
here
 
 3️  first
second
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
for i in range(3):
    print(i)
    if i == 1:
        break
else:
    print('end')

 
```
 1️  the square of 3.0 is 9.0
 
 2️  unt 55
 
 3️  0
1
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        nonlocal x
        x = 1
    x = 3
    nested()
    print("func:", x)
    
x = 2    
func()
print("global:", x)

 
```
 1️  An object's attributes are stored in
obj.__dict__
.
The
__setitem__
method powers the
object[key] = value
syntax.
 
 2️  foo bar
foo bar
foo
bar
('foo', 'bar')
 
 3️  func: 1
global: 2
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
print("foo", "bar", sep="baz", end="qux")

 
```
 1️ ('day', '11/25/2020')
 
 2️  foobazbarqux
 
 3️  set1 ^ set2
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
get
my_string
's length

 
```
 1️  len(my_string)
 
 2️  (i for i in stream_of_ints if i % 5 != 0)
 
 3️  here
(1, 2, [3, 4, 5])
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
create a string object from
obj

 
```
 1️  2
3.5
0
1
 
 2️  str(obj)
 
 3️  new_string = ('ABCD'.lower()
                    .rjust(6, '_')
                    .strip('a'))
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
convert
my_string
to upper case, returning a new string

 
```
 1️  my_string.upper()
 
 2️  callable(obj)
 
 3️  foo
bar
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
get
my_string
's length
```
 1️  len(my_string)
 2️  (i for i in stream_of_ints if i % 5 != 0)
 3️  here
(1, 2, [3, 4, 5])
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
create a string object from
obj
```
 1️  2
3.5
0
1
 2️  str(obj)
 3️  new_string = ('ABCD'.lower()
                    .rjust(6, '_')
                    .strip('a'))
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
convert
my_string
to upper case, returning a new string
```
 1️  my_string.upper()
 2️  callable(obj)
 3️  foo
bar
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
get
my_string
's length
 
```
 1️  len(my_string)
 2️  (i for i in stream_of_ints if i % 5 != 0)
 3️  here
(1, 2, [3, 4, 5])
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
text = "ababab"
print(text.replace("a", "c"))
 
```
 1️  in
./bloop.py
, line 8, returning
None
from
bar()
print(x)
was the last executed statement before returning
 2️  Format strings call an object's
__str__
method.
 3️  cbcbcb
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
replace the first two occurrences of "foo" in
my_string
by "bar", returning a new string
 
```
 1️  54321
531
 2️  my_string.replace("foo", "bar",  
 2️ 
 3️  in bar
<3s...>
in foo
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    global x
    x = 1
func()
print(x)
 
```
 1️ ('day', '11/25/2020')
 2️  1
 3️  ValueError: Type names and field names cannot be a keyword: 'class'
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
text = "ababab"
print(text.replace("a", "c"))
 
```
 1️  in
./bloop.py
, line 8, returning
None
from
bar()
print(x)
was the last executed statement before returning
 2️  Format strings call an object's
__str__
method.
 3️  cbcbcb
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
lst = ["a", "b", "c", "d", "e"]
print(lst[0], lst[-1])
 
```
 1️  in get
2
 2️  a e
 3️  new_string = ('ABCD'.lower()
                    .rjust(6, '_')
                    .strip('a'))
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
my_list = ['a', 'b', 'c', 'd', 'e']
print(my_list[1:4])
 
```
 1️  3
 2️  my_string.count("foo", 5, 1 
 3️ 
 3️  ['b', 'c', 'd']
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
text = "foo bar foo bar"
print(text.find("bar"))
 
```
 1️  1 2
{'y': 2}
 2️  4
 3️  1
2
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
replace the first two occurrences of "foo" in
my_string
by "bar", returning a new string
```
 1️  54321
531
 2️  my_string.replace("foo", "bar",  
 2️ 
 3️  in bar
<3s...>
in foo
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    global x
    x = 1
func()
print(x)
```
 1️ ('day', '11/25/2020')
 2️  1
 3️  ValueError: Type names and field names cannot be a keyword: 'class'
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
lst = ["a", "b", "c", "d", "e"]
print(lst[0], lst[-1])
```
 1️  in get
2
 2️  a e
 3️  new_string = ('ABCD'.lower()
                    .rjust(6, '_')
                    .strip('a'))
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
my_list = ['a', 'b', 'c', 'd', 'e']
print(my_list[1:4])
```
 1️  3
 2️  my_string.count("foo", 5, 1 
 3️ 
 3️  ['b', 'c', 'd']
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
text = "foo bar foo bar"
print(text.find("bar"))
```
 1️  1 2
{'y': 2}
 2️  4
 3️  1
2
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
get the index of the first occurrence of "foo" in
my_string
, starting from index 5
```
 1️  bar
bar
 2️  my_string.find("foo", 5)
 3️  0
<~3s...>
done
done
\________________________________________
Richtig! Ja 2 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
get the index of the first occurrence of "foo" in
my_string
, between index 10 and 20
```
 1️  __a___
__aa__
_aaa__
_aaaa_
aaaaa_
 2️  in
./bloop.py
, line 3, calling
foo()
 3️  my_string.find("foo", 10, 20)
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
text = "abababab"
i = text.count("abab")
print(i)
```
 1️  2
 2️  path
 3️  ['hiiii']
['hi']
['hiiii']
['hii']
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
get the number of non-overlapping occurrences of "foo" in
my_string
, between indexes 5 and 13
```
 1️  ll
 2️  ['another line\n', 'and a third']
 3️  my_string.count("foo", 5, 1 
 3️ 
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def f():
    x = 1
x = 2
f()
print(x)
```
 1️  finally
KeyboardInterrupt
 2️  0
1
 3️  2
\________________________________________
 
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    global x
    x = 1
x = 2
func()
print(x)
```
 1️  1
 2️  blah
blah
 3️  1
StopIteration
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        global x
        x = 1
    nested()
x = 2
func()
print(x)
```
 1️  1
 2️  deque(['a', 'b', 'c', 'd'])
deque(['d', 'c', 'b', 'a'])
 3️  5 a e
deque(['a', 'b', 'd', 'e'])
\________________________________________
Richtig! Ja 1 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def f():
    x = 1
x = 2
f()
print(x)
```
 1️  finally
KeyboardInterrupt
 2️  0
1
 3️  2
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        nonlocal x
        x = 1
    x = 3
    nested()
    print("func:", x)
x = 2    
func()
print("global:", x)
```
 1️  An object's attributes are stored in
obj.__dict__
.
The
__setitem__
method powers the
object[key] = value
syntax.
 2️  foo bar
foo bar
foo
bar
('foo', 'bar')
 3️  func: 1
global: 2
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def func():
    def nested():
        def nested2():
            nonlocal x
            x = 100
            print("nested2:", x)
        x = 50
        nested2()
        print("nested:", x)
    x = 10
    nested()
    print("func:", x)
x = 1
func()
print("outer:", x)
```
 1️  AttributeError: 'C' object has no attribute '__foo'. Did you mean: '_C__foo'?
 2️  sys.argv
 3️  nested2: 100
nested: 100
func: 10
outer: 1
\________________________________________
Richtig! Ja 3 war richtig. Nächste Aufgabe:
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```python
def f():
    x = 1
x = 2
f()
print(x)
```
 1️  finally
KeyboardInterrupt
 2️  0
1
 3️  2
\________________________________________
