---
title: C++学习笔记
tags: [C++, 编程, 命名空间]
created: 2026-06-04
type: note
status: active
summary: C++ 系统学习笔记，涵盖命名空间、输入输出、缺省参数、函数重载等核心概念。
---

 ### c++入门
#### 命名空间
在C/C++中，变量、函数和类都是大量存在的，这些变量、函数和类的名称将都存在于全局作用域中，可能会导致很多冲突。**使用命名空间的目的是对标识符的名称进行本地化，以避免命名冲突或名字污染，**`**namespace**`**关键字的出现就是为了解决这种问题。**

```cpp
#include <stdio.h>
#include <stdlib.h>

int rand = 10;

int main()
{
    printf("%d\n", rand);
    
    return 0;
}
```

以上代码编译后会报错："error c2365："rand"：重定义：以前的定义是"函数""。C语言没办法解决类似这样的命名冲突问题，所以C++提出了`namespace`来解决。

##### 命名空间的定义
定义命名空间，需要使用到`namespace`关键字，后面跟命名空间的名字，然后接一对花括号`{}`即可，`{}`中即为命名空间的成员。

```cpp
// bit是命名空间的名字，一般开发中是用项目名。
// 1.正常的命名空间定义
namespace bit
{
    // 命名空间中可以定义变量、函数、类型
    int rand = 10;

    int Add(int left, int right)
    {
        return left + right;
    }

    struct Node
    {
        struct Node* next;
        int val;
    };
}

// 2.命名空可以嵌套
// test.cpp
namespace N1
{
    int a;
    int b;
    int Add(int left, int right)
    {
        return left + right;
    }

    namespace N2
    {
        int c;
        int d;
        int Sub(int left, int right)
        {
            return left - right;
        }
    }
}

// 3.通过一个工程中允许存在多个相同名称的命名空间，编译器最后会合成同一个命名空间中。
// ps：一个工程中的test.h和上面test.cpp中两个N1会被合并成一个
// test.h
namespace N1
{
    int Mul(int left, int right)
    {
        return left * right;
    }
}
```

:::color2
**注意：一个命名空间就定义了一个新的作用域，命名空间中所有的内容都局限于该命名空间中。**

:::

##### 命名空间的使用
命名空间中的成员该如何使用呢？例如：

```cpp
#include <iostream>

namespace bit
{
    // 命名空间中可以定义变量、函数、类型
    int a = 0;
    int b = 1;

    int Add(int left, int right)
    {
        return left + right;
    }

    struct Node
    {
        struct Node* next;
        int val;
    };
}

int main()
{
    // 编译报错：error c2065："a"：未声明的标识符
    printf("%d\n", a);

    return 0;
}
```

命名空间的使用有三种方式：

+ **使用命名空间名称及作用域限定符**

```cpp
int main()
{
    printf("%d\n", bit::a);

    return 0;
}
```

+ **使用**`**using**`**将命名空间中某个成员引入**

```cpp
#include <iostream>

namespace bit
{
    // 命名空间中可以定义变量、函数、类型
    int a = 0;
    int b = 1;

    int Add(int left, int right)
    {
        return left + right;
    }

    struct Node
    {
        struct Node* next;
        int val;
    };
}

int main()
{
    // 编译报错：error c2065："a"：未声明的标识符
    printf("%d\n", a);

    return 0;
}
```

+ **使用**`**using namespace**`**命名空间名称引入**

```cpp
#include <iostream>

namespace bit
{
    // 命名空间中可以定义变量、函数、类型
    int a = 0;
    int b = 1;

    int Add(int left, int right)
    {
        return left + right;
    }

    struct Node
    {
        struct Node* next;
        int val;
    };
}

int main()
{
    // 编译报错：error c2065："a"：未声明的标识符
    printf("%d\n", a);

    return 0;
}
```

#### C++输入与输出
```cpp
#include <iostream>

// std是C++标准库的命名空间名，C++将标准库的定义实现都放在这个命名空间中
// 使用C++的东西，就必须要加std
using namespace std; 

int main()
{
    cout << "Hello world!" << endl;

    return 0;
}
```

`using namespace std`是将`std`命名空间引入，`std`是C++标准库的命名空间，C++将标准库的定义实现都放在这个命名空间中，所以，要使用C++标准库的函数或对象，就必须要添加`std`。对以上代码要素说明：

1. 使用`cout`**标准输出对象(控制台)**和`cin`**标准输入对象(键盘)**时，必须包含`iostream`头文件以及按命名空间使用方法使用`std`。
2. `cout`和`cin`是**全局的流对象**，`endl`是特殊的C++符号，表示**换行输出**，他们都包含在`iostream`头文件中。
3. `**<<**`**是流插入运算符，**`**>>**`**是流提取运算符。**
4. 使用C++输入输出更方便，无需像C语言中`scanf/printf`输入输出时那样，需要手动控制格式，C++的输入输出可以自动识别变量类型。
5. `<<`和`>>`涉及**运算符重载**等知识(即可做输入输出运算符，也可做移位运算符)。

标准库中定义了4个IO对象：

+ `**cin**`**：**`**istream**`**类型的对象，被称为标准输入。  **
+ `**cout**`**：**`**ostream**`**类型的对象，被称为标准输出。**
+ `cerr`：`ostream`类型的对象，标准错误，输出警告和错误消息。
+ `clog`：`ostream`类型的对象，标准错误，输出程序运行时一般性信息。

C++如何对浮点数控制输出、精度、小数点后的位数呢？可以使用`setiosflags`与`setprecision`来控制：

```cpp
#include <iostream>
#include <iomanip>

using namespace std;

int main()
{
    double d = 10.5234500;

    cout << d << endl;                                            // 10.5235
    cout << "setprecision(1): " << setprecision(1) << d << endl;  // 1e+01
    cout << "setprecision(2): " << setprecision(2) << d << endl;  // 11
    cout << "setprecision(3): " << setprecision(3) << d << endl;  // 10.5
    cout << "setprecision(4): " << setprecision(4) << d << endl;  // 10.52
    cout << "setprecision(5): " << setprecision(5) << d << endl;  // 10.523
    cout << "setprecision(6): " << setprecision(6) << d << endl;  // 10.5235
    cout << "setprecision(7): " << setprecision(7) << d << endl;  // 10.52345
    cout << "setprecision(8): " << setprecision(8) << d << endl;  // 10.52345
    cout << "setprecision(9): " << setprecision(9) << d << endl;  // 10.52345
    // 可见，单独用setprecision时，小数部分末尾为0时，无法输出0的部分

    cout << d << endl;                                            // 10.52345
    // setiosflags(ios::fixed)与setprecision(n)一起使用，可以控制小数点右边的数字个数
    cout << setiosflags(ios::fixed);  // 使用固定小数点格式
    cout << "setprecision(1): " << setprecision(1) << d << endl;  // 10.5
    cout << "setprecision(2): " << setprecision(2) << d << endl;  // 10.52
    cout << "setprecision(3): " << setprecision(3) << d << endl;  // 10.523
    cout << "setprecision(4): " << setprecision(4) << d << endl;  // 10.5235
    cout << "setprecision(5): " << setprecision(5) << d << endl;  // 10.52345
    cout << "setprecision(6): " << setprecision(6) << d << endl;  // 10.523450
    cout << "setprecision(7): " << setprecision(7) << d << endl;  // 10.5234500
    cout << "setprecision(8): " << setprecision(8) << d << endl;  // 10.52345000
    cout << "setprecision(9): " << setprecision(9) << d << endl;  // 10.523450000

    return 0;
}
```

其中，`setprecision(n)`用来设置输出`n`个数，会四舍五入，小数部分末尾为0时，无法输出0。`setiosflags(ios::fixed)`用来设置固定小数点格式，如果变量末尾有0也会输出。可以使用`setiosflags(ios::fixed || ios::showpoint)`来设置，当`precesion(n)`的n为0时，即精度为0，如果有`showpoint`，输出结果会显示小数点：

```cpp
#include <iostream>
#include <iomanip>

using namespace std;

int main()
{
    double s = 10.5234500;

    cout << s << endl;
    cout << setiosflags(ios::fixed);

    cout << "setiosflags(0)" << setprecision(0) << s << endl;  // 11
    cout << "setiosflags(1)" << setprecision(1) << s << endl;  // 10.5
    cout << "setiosflags(2)" << setprecision(2) << s << endl;  // 10.52

    // ios::showpoint精度为0时，会显示小数点
    cout << setiosflags(ios::fixed | ios::showpoint);  
    cout << "setiosflags(0)" << setprecision(0) << s << endl;  // 11.
    cout << "setiosflags(1)" << setprecision(1) << s << endl;  // 10.5
    cout << "setiosflags(2)" << setprecision(2) << s << endl;  // 10.52

    return 0;
}
```

注意：早期标准库将所有功能在全局域中实现，声明在`.h`后缀的头文件中，使用时只需包含对应头文件即可，后来将其实现在`std`命名空间下，为了和C的头文件区分，也为了正确使用命名空间，规定C++头文件不带`.h`，旧编译器(`VC6`)中还支持`iostream.h`格式，后续编译器已不支持，因此推荐使用`iostream + std`的方式。

```cpp
#include <iostream>

using namespace std;

int main()
{
    int a = 1;
    double b = 1.0;
    char c = 'w';

    // 可自动识别变量类型
    cout << a << endl;
    cout << b << " " << c << endl;

    return 0;
}
```

:::color2
`std`命名空间的使用惯例：

1. 在日常学习中，建议直接`using namespace std`即可。
2. `using namespace std`展开，标准库全部暴露出来，如果我们定义跟库重名的类型、对象、函数，就存在冲突问题。**所以建议在项目开发中使用**`**std::cout**`**，也可以使用指定命名空间 **`**using std::cout**`**的方式展开常用的库对象、类型等方式。**

:::

```cpp
#include <iostream>

using namespace std;

int cout = 0;  // cout变量

int main()
{
    cout << cout << endl;  // C2872	“cout”: 不明确的符号	

    return 0;
}
```

以上代码编译不通过，提示`cout`变量不明确，意思是命名空间`std`中有`cout`是用来标准输出的，与此处定义的变量名冲突了，所以，这就是`using namespace std`展开的问题。可以不使用此变量名，如果非要使用此变量名，有以下解决方案：

```cpp
#include <iostream>

int cout = 0;

int main()
{
    std::cout << cout << std::endl;

    return 0;
}
```

但是解决方案1中，每次要展开写`std::cout`相对麻烦，有更方便的解决方案如下：

```cpp
#include <iostream>

using std::cout;
using std::endl;

int cout1 = 0;  // 除了cout endl不行，其他可以定义变量名

int main()
{
    cout << cout1 << endl;

    return 0;
}
```

#### 缺省参数 
##### 缺省参数的概念
**缺省参数是声明或定义函数时，为函数的参数指定一个缺省值。**在调用该函数时，如果没有指定实参则采用该形参的缺省值，否则使用指定的实参。

```cpp
#include <iostream>

using namespace std; 

void Func(int a = 0)
{
    cout << a << endl;
}

int main()
{
    Func();    // 没有传参时，使用参数默认值
    Func(10);  // 传参时，使用指定参数

    return 0;
}
```

##### 缺省参数的分类
+ **全部缺省参数**

```cpp
void Func(int a = 0, int b = 20, int c = 30)
{
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;
}
```

+ **半缺省参数**

```cpp
void Func(int a, int b = 20, int c = 30)
{
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;
}
```

注意：

:::color2
1. **半缺省参数必须从右往左连续缺省，不能间隔缺省。传参必须从左往右依次传参。**
2. **缺省参数不能在函数声明和定义中同时出现。**
3. **缺省值必须是常量或全局变量。**
4. **C语言不支持(编译器不支持)。**

:::

```cpp
// test.h
void Func(int a = 10);

// test.cpp
void Func(int a = 20) {}
// 如果声明与定义位置同时出现，恰巧两个位置提供的值不同，那编译器就无法确定到底该用哪个缺省值。
```

#### 函数重载
自然语言中一个词可以有多重含义，人们可以通过上下文来判断该词真实的含义，即该词被重载了。比如：有个笑话，国有两个体育项目大家根本不用看，也不用担心。一个是乒乓球，一个是男足。前者是"谁也赢不了！"，后者是"谁也赢不了！"。

##### 函数重载的概念
函数重载：函数的一种特殊情况，**C++允许在同一作用域中声明几个功能类似的同名函数，这些同名函数的形参列表(参数个数或类型或类型顺序)不同，常用来处理实现功能类似数据类型不同的问题。函数重载是一种静态多态。所谓多态，即同一个东西表示不同的形态，多态分为静态多态(编译时的多态)与动态多态(运行时的多态)。**

```cpp
#include <iostream>

using namespace std; 

// 1.参数类型不同
int Add(int left, int right)
{
    cout << "int Add(int left, int right)" << endl;

    return left + right;
}

double Add(double left, double right)
{
    cout << "double Add(double left, double right)" << endl;

    return left + right;
}

// 2.参数个数不同
void f()
{
    cout << "f()" << endl;
}

void f(int a)
{
    cout << "f(int a)" << endl;
}

// 3.参数类型顺序不同
void f(int a, char b)
{
    cout << "f(int a, char b)" << endl;
}

void f(char b, int a)
{
    cout << "f(char b, int a)" << endl;
}

int main()
{
    Add(10, 20);
    Add(1.5, 2.5);

    f();
    f(10);

    f(10, 'w');
    f('w', 10);;

    return 0;
}
```

##### 函数重载的作用
**重载函数通常用来在同一个作用域内，用同一个函数名命名一组功能相似的函数，这样减少了函数名的数量，避免了名字空间的污染，对于程序的可读性有很大的好处。**

##### C++支持函数重载的原理--名字修饰(name Mangling)
```cpp
#include <iostream>

using namespace std;

int Add(int a, int b)
{
    cout << "test to overLoad (int Add)" << endl;
    return a + b;
}

double Add(double a, double b)
{
    cout << "test to overLoad (double Add)" << endl;
    return a + b;
}

int main()
{
    cout << "test start!" << endl;
    int ir = Add(1, 2);
    double dr = Add(1.1, 2.2);

    return 0;
}
```

**为什么C++支持函数重载，而C语言不支持呢？**

在C/C++中，一个程序要运行起来，需要经历以下几个阶段：**预处理、编译、汇编、链接**。 

1. 实际项目通常是由多个头文件和多个源文件构成，当在`a.cpp`中调用了`b.cpp`中定义的`Add`函数时，编译后链接前，编译器只检测到了`b.cpp`中是否含有`Add`函数的声明，但`a.o`的目标文件中没有`Add`的函数地址，因为`Add`是在`b.cpp`中定义的，所以`Add`的地址在`b.o`中，那么该怎么调用呢？
2. 所以链接阶段时，面对`Add`函数，**链接器看到**`**a.o**`**调用**`**Add**`**，但是没有**`**Add**`**的地址，就会到**`**b.o**`**的符号表中找**`**Add**`**的地址，然后链接到一起。**
3. 那么链接时，面对`Add`函数，链接器会使用哪个名字去找呢？这里每个编译器都有自己的函数名修饰规则。
4. C语言不存在函数重载，主要需要在函数修饰中体现出函数的调用约定：
    1. `**__stdcall**`**：函数名前加上一个下划线前缀**`**_**`**，函数名后加上一个**`**@**`**符号和其参数的字节数，例如：**`**_funcName@number**`**。**
    2. `**__cdecl**`**：仅在输出函数名前加上一个下划线前缀，例如：**`**_funcName**`**。**
    3. `**__fastcall**`**：在输出函数名前加上一个**`**@**`**符号，后面也是一个**`**@**`**符号和其参数的字节数，例如：**`**@funcName@number**`**。**
5. C++编译器的函数名修饰规则为：
    1. **在Linux下，采用**`**g++**`**编译完成后，函数名的修饰发生了改变，编译器将函数参数类型信息添加到修改后的名字中。Linux下**`**g++**`**编译器的修饰格式为：**`**_Z+函数名长度+函数名+参数1类型首字母+参数2类型首字母+...**`**，如果参数是指针，则被修饰为**`**Pi**`**，如上述代码中**`**int Add(int a, int b)**`**函数修饰后为：**`**_Z3Addii**`**，而**`**double Add(double a, double b)**`**函数修饰后为：**`**_Z3Adddd**`**，若有带指针参数的函数**`**void func(int a, double b, int* p)**`**，则修饰后为：**`**_Z4funcidPi**`**。**
    2. **在Windows下，函数名修饰包含调用约定、返回值类型、参数个数及类型。总体格式为：**`**?+[构造/析构]+ 函数名+@@+调用约定+返回值类型+各个参数类型+结束标志**`**(**`**?funcName@YG*****@Z**`**或**`**?funcName@@YG*XZ**`**)，例如以**`**_stdcall**`**调用约定为例，**`**int Test1(char* var1, unsigned long)**`**函数修饰后为：**`**?Test1@@YGHPADK@Z**`**。**
        1. 构造/析构：可选项，只有构造函数和析构函数有，其中构造器：0，析构器：1。
        2. 函数名：包括类名和命名空间名，格式为：`函数名@类名@@命名空间`。
        3. 调用约定：
            1. `__stdcall`：`@@YG`
            2. `__cdecl`：`@@YA`
            3. `__fastcall`：`@@YI`，如果函数是类的成员函数，调用约定为`__thiscall`，根据保护方式不同，又分为：
                1. `public__thiscall`：`@@QAE`
                2. `protect_thiscall`：`@@IAE`
                3. `private__thiscall`：`@@AAE`
                4. `public__thiscall const`：`@@QBE`
                5. `protect__thiscall const`：`@@IBE`
                6. `private__thiscall const`：`@@ABE`
        4. 返回值、参数的类型标识：
            1. `B`：`const`
            2. `D`：`char`
            3. `E`：`unsigned char`
            4. `F`：`short`
            5. `G`：`unsigned short`
            6. `H`：`int`
            7. `I`：`unsigned int`
            8. `J`：`long`
            9. `K`：`unsigned long`
            10. `M`：`float`
            11. `N`：`double`
            12. `_N`：`bool`
            13. `PA`：指针(`*`，后面的代号表示指针类型，同类型指针连续出现，以0代替，一个0表示一次重复)
            14. `PB`：`const`指针
            15. `AA`：引用(`&`)
            16. `AB`：`const`引用
            17. `U`：类或结构体，通常后跟结构体的类型名，用`@@`表示结构体类型名的结束。
            18. `V`：类，通常后跟结构体的类型名，用`@@`表示结构类型名的结束。
            19. `W4`：`enum`
            20. `X`：`void`
            21. `Z`：结束标记
            22. `@`：空，构造或析构使用
        5. 结束标志：参数表后以`@Z`标识整个名字的结束，如果该函数无参数，则以`Z`标识结束。

##### extern "C"
有时候在C++工程中可能需要将某些函数按照C的风格来编译，可以在函数前加`extern "C"`，意思是告诉编译器将该函数按照C语言的规则来编译。例如，`tcmalloc`是Google用C++实现的一个项目，提供`tcmalloc`和`tcfree`两个接口来使用，但如果是C项目就没办法使用，那么Google就是用`extern "C"`来解决。这个功能主要用在以下情况：

+ C++代码中调用C语言代码。
+ 在C++的头文件中使用。
+ 多人协同开发时，有的擅长C，有的擅长C++，这种情况可以使用。

有以下例子：`moduleA`、`moduleB`两个模块，B调用A中的代码，其中A是用C语言实现的，而B是用C++实现的，下面给出一种实现方法：

```cpp
// moduleA头文件
#ifndef _MODULE_A_H_  // 对于模块A来说，这个宏是为了防止头文件的重复引用
#define _MODULE_A_H_
int fun(int, int);
#endif

// moduleA实现文件moduleA.c  // 模块A的实现部分并没有改变
#include "moduleA"

int fun(int a, int b)
{
    return a + b;
}

// moduleB头文件
#ifndef _MODULE_B_H_  // 很明显这一部分也是为了防止重复引用
#define _MODULE_B_H_
#ifdef __cplusplus  // 告诉编译器，如果定义了__cplusplus则采用C语言方式进行编译
extern "C"
{
#include"moduleA.h"
#endif
    // 其他代码
#ifdef __cplusplus
}
#endif
#endif

// moduleB实现文件 moduleB.cpp // B模块的实现也没有改变，只是头文件的设计变化了
#include "moduleB.h"

int main()
{
    cout << fun(2, 3) << endl;
}
```

#### 引用
##### 引用概念
**引用并非对象，不是新定义一个变量，而是给已存在变量取了一个别名，编译器不会为引用变量开辟内存空间，它和它引用的变量公用一块内存空间。**`**类型& 引用变量名(对象名) = 引用实体;**`

C++11中新增了一种引用，即右值引用，会在后续进行介绍。通常我们所说的引用指的是左值引用：

```cpp
#include <iostream>

using namespace std;

int main()
{
    int a = 20;
    int& ra = a;  // 定义引用类型，ra是a的引用，ra指向a(是a的另一个名字)

    cout << "a的地址：" << &a << endl;
    cout << "ra的地址：" << &ra << endl;  // 地址相同

    return 0;
}
```

```cpp
#include <iostream>

using namespace std;

int main()
{
    int a = 1;

    int& ra = a;  // 三个别名
    int& rb = a;
    int& rc = rb;

    rc = 2;  // 更改其中一个别名的值，所有别名都会改变

    cout << a << endl;  

    return 0;
}
```

**定义了引用后，对其进行的所有操作都是在与之绑定的对象上进行的**。上述代码中，变量`a`取了几个别名，更改其中一个别名，都会改变`a`本身的值。

**注意：引用类型必须和引用实体是同种类型。**

```cpp
#include <iostream>

int main()
{
    int i, & ri = i;
    i = 5; ri = 10;

    std::cout << i << " " << ri << std::endl;

    return 0;
}
```

##### 引用特性
1. **引用在定义时必须初始化。**
2. **一个变量可以有多个引用。**
3. **引用一旦引用一个实体，再不能引用其他实体。**

```cpp
#include <iostream>

using namespace std;

int main()
{
    int a = 20;
    // int& ra;  // 引用定义时不初始化会报错
    int& ra = a;
    int& rra = a;

    printf("%p %p %p\n", &a, &ra, &rra);

    return 0;
}
```

一般在初始化变量时，初始值会被拷贝到新建的对象中。然而**定义引用时，程序把引用和它的初始值绑定在一起，而不是将初始值拷贝给引用。一旦初始化完成，引用将和它的初始值对象一直绑定在一起。因为无法令引用重新绑定到另一个对象，因此引用必须初始化。**

##### 常引用
```cpp
#include <iostream>

using namespace std;

int main()
{
    const int a = 10;
    // int& ra = a;  // 该语句编译会报错，a为常量，如果可以，那么ra类型是int，可读可写，相矛盾
    const int& ra = a;
    //int& b = 10;   // 该语句编译会报错，b为常量，道理同上
    const int& b = 10;

    int c = 1;
    const int& e = c;  // 可以，c可读可写，e是别名，只读。

    double db = 3.14;
    const int& ri = db;  // 可以，本质如下
    // 此处 ri 引用了一个 int 型的数，对 ri 的操作应该是整数运算，但 db 却是一个双精度浮点数
    // 因此为了确保让 ri 绑定一个整数，编译器把上述代码变成了以下形式
    // const int tmp = db;   // 由双精度浮点数生成一个临时的整型常量
    // const int& ri = tmp;  // 让 ri 绑定这个临时变量
    

    int i = 0;
    double db = i;  // 隐式类型转换
    // double& rb = i;  // 编译报错
    const double& rb = i;  // 隐式转换，会产生double类型的临时变量，引用的是临时变量，具有常性，所以要加const

    // 对于指针，权限缩小也适用
    int num = 0;
    const int* cp1 = &num;
    // int* p1 = cp1;  // 编译报错，属于权限放大

    int* p2 = &num;
    const int* cp2 = p2;  // 可以，属于权限缩小

    return 0;
}
```

:::color2
**总结：引用取别名时，变量访问的权限可以缩小，不能放大。**

:::

##### 使用场景
1. **做参数**

```cpp
#include <iostream>

using namespace std;

void Swap(int& x, int& y)  // x为a别名 y为b别名
{
    int tmp = x;
    x = y;
    y = tmp;
}

int main()
{
    int a = 1;
    int b = 2;

    Swap(a, b);

    cout << "a:" << a << endl;
    cout << "b:" << b << endl;

    return 0;
}
```

2. **做返回值**

```cpp
#include <iostream>

using namespace std;

// 传值返回
int Count1()
{
    static int n = 0;
    n++;

    return n;  // 返回临时变量为n的拷贝，会多产生一个空间，相当于int tmp = n;
}

// 传引用返回
int& Count2()
{
    static int n = 0;
    n++;

    return n;  // 返回临时变量，不会产生空间，相当于int& tmp = n;
}

int main()
{
    int& r1 = Count1();  // 编译失败，因为要将临时变量tmp赋值给r1, int& r1 = tmp; 临时变量具有常性, 添加const即可
    int& r2 = Count2();  // 相当于int& tmp = n; 然后int& r2 = tmp; r2就是n的别名

    return 0;
}
```

下面代码输出什么结果？为什么？

```cpp
#include <iostream>

using namespace std;

// 普通的加法函数，返回值为 int
int Add1(int a, int b)
{
    int c = a + b; 
    return c; 
}

int main()
{
    // 调用 Add1，并将返回值绑定到一个 const int& 类型的引用 ret1
    const int& ret1 = Add1(1, 2);  // Add1返回一个局部变量c的拷贝临时变量
    Add1(3, 4); 

    cout << "Add2(1, 2) is : " << ret1 << endl;

    return 0; 
}
```

```cpp
#include <iostream>

using namespace std;

// 返回引用的加法函数，返回值为 int&
int& Add2(int a, int b)
{
    int c = a + b; 
    return c; 
}

int main()
{
    // 调用 Add2，并将返回值绑定到一个 int& 类型的引用 ret2
    int& ret2 = Add2(1, 2);  // Add2返回一个int& 局部变量c的引用
    Add2(3, 4); 

    cout << "Add2(1, 2) is : " << ret2 << endl;

    return 0; 
}
```

:::color2
对于上述代码，函数`Add1`和`Add2`的区别：`Add1`返回一个`int`值，这个值是局部变量`c`的拷贝，`Add2`返回一个`int&`值，即局部变量`c`的引用。对于`Add1`，`const int& ret1 = Add1(1, 2)`是安全的，因为`Add1`返回的是一个临时值，并且用`const int&`绑定临时值是合法的。即使后面再次调用`Add1(3, 4)`，对`ret1`的值不会产生影响，因为`ret1`绑定的临时值的生命周期被延长到`ret1`的生命周期结束；对于`Add2`， 局部变量`c`在函数返回时已经被销毁，这是一个悬空引用，因为`c`在函数返回后就超出了其作用域，所以返回对局部变量的引用会导致未定义行为。也就是说，`ret2`引用一个已经被销毁的变量的内存地址。  对于`Add2`，进行深入分析，当我们第一次调用它时，会在`Add2`栈帧中申请三个空间分别是`a`、`b`、`c`，对应的值分别是1、2、3，返回的是变量`c`的别名，`int& ret2 = Add2(1, 2)`，所以`ret2`成为了`c`的别名。返回时`Add2`栈帧被销毁，不具有访问权限，这时再次调用`Add2(3, 4)`这时会建立同样大小的栈帧，对应值分别是3、4、7，调用结束后栈帧销毁再返回回来，最后再使用`cout`对`ret2`进行访问，由于`ret2`是第二次调用栈帧空间的别名，所以输出结果为7。

:::

```cpp
#include <iostream>

using namespace std;

int& Add(int a, int b)
{
    int c = a + b; 
    return c; 
}

int main()
{

    int& ret = Add(1, 2);  
    printf("hello\n");

    cout << "Add(1, 2) is : " << ret << endl;  // 输出啥结果？

    return 0; 
}
```

:::color2
以上代码，当调用完`Add(1, 2)`返回后，其局部变量`c`所占用的占空间未被立即清除，但该内存区域标记为可供再次分配，空间内容未发生改变。当继续调用`printf`函数时，它会在栈上分配新的内存用于其执行，可能会覆盖`Add`函数先前使用的栈空间。因此，引用`ret`将引用已经被覆盖的内存，输出将是不确定的，可能是随机值。  

:::

如何解决这样问题？添加`static`即可：

```cpp
#include <iostream>

using namespace std;

int& Add(int a, int b)
{
    static int c = a + b; 
    return c; 
}

int main()
{

    int& ret = Add(1, 2);  
    printf("hello\n");
    Add(4, 5);

    cout << "Add(1, 2) is : " << ret << endl;  // 结果为3

    return 0; 
}
```

**为什么添加**`**static**`**就解决了此问题？因为此时变量**`**c**`**的空间在静态区，所以即便是**`**Add**`**函数调用完成销毁栈帧空间后，变量**`**c**`**并未被销毁，并在程序生命周期内保持存在，所以以上代码的结果为3。**

:::color2
**总结：函数返回时，出了函数作用域，如果返回对象还在(还没还给系统)，则可以使用引用返回，如果已经还给系统了，则不安全，必须使用传值返回。当前可以使用全局变量与静态变量作为引用返回。**

:::

##### 传值、传引用效率比较
以值作为参数或返回值类型，在传参和返回期间，函数不会直接传递实参或将变量本身直接返回，而是传递实参或返回变量的一份临时的拷贝，因此用值作为参数或者返回值类型，效率是非常低下的，尤其是当参数或返回值类型非常大时，效率就更低。

###### 值和引用作为函数参数的性能比较
```cpp
#include <iostream>

using namespace std; 

struct A{ int a[10000]; };

void TestFunc1(A a) {}

void TestFunc2(A& a) {}

void TestRefAndValue()
{
    A a;
    // 以值作为函数参数
    size_t begin1 = clock();
    for (size_t i = 0; i < 10000; ++i)
    {
        TestFunc1(a);
    }
    size_t end1 = clock();

    // 以引用作为函数参数
    size_t begin2 = clock();
    for (size_t i = 0; i < 10000; ++i)
    {
        TestFunc2(a);
    }
    size_t end2 = clock();

    // 分别计算两个函数运行结束后的时间
    cout << "TestFunc1(A)-time: " << end1 - begin1 << endl;
    cout << "TestFunc2(A&)-time: " << end2 - begin2 << endl;
}

int main()
{
    TestRefAndValue();

    return 0;
}
```

###### 值和引用的作为返回值类型的性能比较
```cpp
#include <iostream>

using namespace std;

struct A { int a[10000]; };

A a;
// 值返回
A TestFunc1() { return a; }

// 引用返回
A& TestFunc2() { return a; }

void TestReturnByRefOrValue()
{
    // 以值作为函数的返回值类型
    size_t begin1 = clock();
    for (size_t i = 0; i < 10000; ++i)
    {
        TestFunc1();
    }
    size_t end1 = clock();

    // 以引用作为和数额返回值类型
    size_t begin2 = clock();
    for (size_t i = 0; i < 10000; ++i)
    {
        TestFunc2();
    }
    size_t end2 = clock();

    // 计算两个函数运算完成之后的时间
    cout << "TestFunc1 time: " << end1 - begin1 << endl;
    cout << "TestFunc2 time: " << end2 - begin2 << endl;
}

int main()
{
    TestReturnByRefOrValue();

    return 0;
}
```

通过上述代码的比较，发现**传值和指针在作为传参以及返回值类型上效率相差很大。**

##### 引用和指针的区别
在语法概念上引用就是一个别名，没有独立空间，和其引用实体共用同一块空间。

```cpp
#include <iostream>

using namespace std;

int main()
{
    int a = 10;
    int& ra = a;

    cout << "&a = " << &a << endl;
    cout << "&ra = " << &ra << endl;

    return 0;
}
```

**在底层实现上实际是有空间的，因为引用是按照指针方式来实现的。**

```cpp
// 引用
int main()
{
    int a = 10;
    int& ra = a;
    ra = 20;

    return 0;
}

// 指针
int main()
{
    int a = 10;
    int* pa = &a;
    *pa = 20;

    return 0;
}
```

```cpp
// 引用
int a = 10;
00C1251F  mov         dword ptr [a],0Ah  
    int& ra = a;
00C12526  lea         eax,[a]  
00C12529  mov         dword ptr [ra],eax  
    ra = 20;
00C1252C  mov         eax,dword ptr [ra]  
00C1252F  mov         dword ptr [eax],14h  

// 指针
    int a = 10;
00F9251F  mov         dword ptr [a],0Ah  
    int* pa = &a;
00F92526  lea         eax,[a]  
00F92529  mov         dword ptr [pa],eax  
    *pa = 20;
00F9252C  mov         eax,dword ptr [pa]  
00F9252F  mov         dword ptr [eax],14h 
```

引用和指针的不同点：

:::color2
1. **引用概念上定义一个变量的别名，指针存储一个变量地址。**
2. **指针本身就是一个对象，允许对指针赋值和拷贝，在指针生命周期内可以先后指向不同的对象。**
3. **引用在定义时必须初始化**，指针没有要求。
4. 引用在初始化时引用一个实体后，就**不能再引用其他实体**，而指针可以在任何时候指向任何一个同类型实体。
5. **没有**`**NULL**`**引用，但有**`**NULL**`**指针。**
6. **在**`**sizeof**`**中含义不同：引用结果为引用类型的大小，但指针始终是地址空间所占字节个数。**
7. 引用自加即引用的实体增加1，指针自加即指针向后偏移一个类型的大小。
8. **有多级指针，但没有多级引用。**
9. 访问实体方式不同，**指针需要显式解引用，引用编译器自己处理。**
10. **引用比指针使用起来相对更安全。**

:::

#### 内联函数
##### 概念
以`inline`修饰的函数叫做内联函数，通过声明建议编译器展开内联函数，而不是使用正常的函数调用机制。编译时，C++编译器会**在调用内联函数的地方展开，没有函数调用建立栈帧的开销**，内联函数提升程序运行的效率。

```cpp
int Add(int left, int right)
{
    return left + right;
}

int main()
{
    int ret = 0;
    ret = Add(1, 2);

    return 0;
}
```

```cpp
    13:     int ret = 0;
00F627A5  mov         dword ptr [ret],0  
    14:     ret = Add(1, 2);
00F627AC  push        2  
00F627AE  push        1  
00F627B0  call        Add (0F614F6h)  
00F627B5  add         esp,8  
00F627B8  mov         dword ptr [ret],eax  
```

可以发现汇编代码中第6行有调用`Add`函数的指令。如果在上述函数前增加`inline`关键字将其改成内联函数，在编译期间编译器会用函数体替换函数的调用。

查看方式：

1. `Release`模式下，查看编译器生成的汇编代码中是否存在`call Add`。
2. `Debug`模式下，需要对编译器进行设置，否则不会展开。在"项目属性"中，选择"C/C++"中"常规"，将"调试信息格式"选项改为"程序数据库(/Zi)"；在"优化"中将"内联函数扩展"选项修改为"只适用于 __inline(Ob1)"。

```cpp
inline int Add(int left, int right)
{
    return left + right;
}

int main()
{
    int ret = 0;
    ret = Add(1, 2);

    return 0;
}
```

```cpp
    13:     int ret = 0;
00981525  mov         dword ptr [ret],0  
    14:     ret = Add(1, 2);
0098152C  mov         eax,1  
00981531  add         eax,2  
00981534  mov         dword ptr [ret],eax  
```

可以看见汇编代码中的第5、6行并没有进行函数调用。

##### 特性
1. `inline`是一种以**空间换时间**的做法，如果编译器将函数当成内联函数处理，**在编译阶段会用函数体替换函数调用**，缺陷是可能会使目标文件变大，优势是少了调用开销，提高程序运行效率。
2. `**inline**`**对于编译器而言只是一个建议请求，编译器可以选择忽略这个请求，不同编译器关于**`**inline**`**实现机制可能不同。**一般来说，内联机制用于优化规模较小、流程直接、频繁调用的函数。很多编译器不支持内联递归函数。**一般建议：鼓励对存取函数(accessors)、变异函数(mutators)和其他规模较小(10 行以下)、不是递归、且频繁调用的函数采用**`**inline**`**修饰，否则编译器会忽略**`**inline**`**特性。谨慎对待析构函数，析构函数往往比表面上更长，因为会暗中调用成员和基类的析构函数！**
3. `inline`不建议声明和定义分离，分离会导致链接错误。因为`inline`被展开，就没有函数地址了，链接就会找不到。

```cpp
// F.h
#include <iostream>

using namespace std;

inline void f(int i);

//F.cpp
#include "F.h"

void f(int i)
{
    cout << i << endl;
}

// main.cpp
#include "F.h"

int main()
{
    f(10);

    return 0;
}
// 链接错误：main.obj : error LNK2019: 无法解析的外部符号 "void __cdecl 
// f(int)" (?f@@YAXH@Z)，该符号在函数 _main 中被引用
```

#### auto关键字(C++11)
##### 类型别名思考
随着程序越来越复杂，程序中用到的类型也越来越复杂，具体体现在：

1. **类型难于拼写。**
2. **含义不明确导致容易出错。**

```cpp
#include <string>
#include <map>

int main()
{
    std::map<std::string, std::string> m{ {"apple", "苹果"}, {"orange", "橙子"}, {"pear", "梨"} };
    std::map<std::string, std::string>::iterator it = m.begin();

    while (it != m.end())
    {
        // ...
    }

    return 0;
}
```

`std::map<std::string, std::string>::iterator`是一个类型，但是类型太长了，特别容易写错。可以通过`typedef`给类型取别名，比如：

```cpp
#include <string>
#include <map>

typedef std::map<std::string, std::string> Map;

int main()
{
    Map m{ {"apple", "苹果"}, {"orange", "橙子"}, {"pear", "梨"} };
    Map::iterator it = m.begin();

    while (it != m.end())
    {
        // ...
    }

    return 0;
}
```

使用`typedef`给类型取别名确实可以简化代码，但是`typedef`又会遇到新的难题：

```cpp
#include <string>
#include <map>

typedef char* pstring;

int main()
{
    const pstring p1;  // 谁能编译通过？
    const pstring* p2; 

    return 0;
}
```

在编程时，常常需要把表达式的值赋值给变量，这就要求在变量声明的时候清楚的知道表达式的类型，然而有时候要做到这点并非那么容易，因此C++11给`auto`赋予了新的含义。

##### auto简介
在早期的C/C++中`auto`的含义是：使用`auto`修饰的变量，是具有自动存储器的局部变量，但遗憾的是一直没人去使用它，可以思考下为什么？

C++11中，标准委员会赋予了`auto`全新的含义，即：`**auto**`**不再是一个存储类型指示符，而是作为一个新的类型指示符来指示编译器，**`**auto**`**声明的变量必须由编译器在编译时期推导而得。**

```cpp
#include <iostream>

using namespace std;

int TestAuto()
{
    return 10;
}

int main()
{
    int a = 10;
    auto b = a;
    auto c = 'a';
    auto d = TestAuto();
    // auto e; 编译不通过，使用auto定义的变量必须进行初始化
    auto& f = a;
    auto* g = &a;  // 等同于auto g = &a; 无需手动添加*

    cout << typeid(b).name() << endl;
    cout << typeid(c).name() << endl;
    cout << typeid(d).name() << endl;
    cout << typeid(f).name() << endl;
    cout << typeid(g).name() << endl;

    return 0;
}
```

:::color2
**注意：使用**`**auto**`**定义变量时必须对其进行初始化，在编译阶段编译器需要根据初始化表达式来推导**`**auto**`**的实际类型。因此**`**auto**`**并非是一种"类型"的声明，而是一个类型声明时的"占位符"，编译器在编译期间会将**`**auto**`**替换为变量实际的类型。**

:::

##### auto的使用细节
1. `**auto**`**与指针和引用结合使用。用**`**auto**`**声明指针类型时，用**`**auto**`**和**`**auto***`**，没有任何区别，但用**`**auto**`**声明引用类型时则必须加**`**&**`**。**

```cpp
#include <iostream>

using namespace std;

int main()
{
    int x = 10;
    auto a = &x;
    auto* b = &x;
    auto& c = x;

    cout << typeid(a).name() << endl;
    cout << typeid(b).name() << endl;
    cout << typeid(c).name() << endl;

    *a = 20;
    *b = 30;
    c = 40;

    return 0;
}
```

2. **在同一行定义多个变量。当在同一行声明多个变量时，这些变量必须是相同的类型，否则编译器将会报错，因为编译器实际只对第一个类型进行推导，然后用推导出来的类型定义其他变量。**

```cpp
void TestAuto()
{
    auto a = 1, b = 2;
    auto c = 3, d = 4.0;  // 编译报错，c d的初始化表达式类型不同
}
```

##### auto不能推导的场景
1. `**auto**`**不能作为函数的参数。**

```cpp
// 此处代码编译失败，auto不能作为形参类型，因为编译器无法对a的实际类型进行推导
void TestAuto(auto a) {}
```

2. `**auto**`**不能直接用来声明数组。**

```cpp
void TestAuto()
{
    int a[] = { 1, 2, 3 };
    auto b[] = { 4, 5, 6 };
}
```

3. 为了避免与C++98中的`auto`发生混淆，C++11只保留了`auto`作为类型指示符的用法。
4. `auto`最常见的优势用法就是跟C++11提供的新式`for`循环与`lambda`表达式等进行配合使用。

#### 基于范围的for循环(C++11)
##### 范围for的语法
在C++98中，如果要遍历一个数组，可以按照以下方式进行：

```cpp
#include <iostream>

using namespace std;

void TestFor()
{
    int arr[] = { 1,2,3,4,5 };
    for (int i = 0; i < sizeof(arr) / sizeof(arr[0]); i++)
    {
        arr[i] *= 2;
    }

    for (int* p = arr; p < arr + sizeof(arr) / sizeof(arr[0]); p++)
    {
        cout << *p << endl;
    }
}

int main()
{
    TestFor();

    return 0;
}
```

对于一个有范围的集合而言，由程序员来说明循环的范围是多余的，有时候还会容易犯错误，因此C++11引入了基于范围的`for`循环。`**for**`**循环后的括号由冒号(**`**:**`**)分为两部分：第一部分是范围内用于迭代的变量，第二部分则表示被迭代的范围。**

```cpp
#include <iostream>

using namespace std;

void TestFor()
{
    int arr[] = { 1, 2, 3, 4,5 };
    for (auto& e : arr)
    {
        e *= 2;
    }

    for (auto e : arr)
    {
        cout << e << endl;
    }
}

int main()
{
    TestFor();

    return 0;
}
```

**注意：与普通循环类似，可以用**`**continue**`**来结束本次循环，也可以用**`**break**`**来跳出整个循环。**

##### 范围for的使用条件
1. `**for**`**循环迭代的范围必须是确定的。**对于数组而言，就是数组中第一个元素和最后一个元素的范围；

对于类而言，应该提供`begin`和`end`的方法，`begin`和`end`就是`for`循环迭代的范围。

```cpp
// 此段代码有问题，因为for的范围不确定
void TestFor(int arr[])
{
    for (auto& e : arr)  // 此处arr已经不再是数组，而是退化为指针
        cout << e << endl;
}
```

2. **迭代的对象要实现**`**++**`**和**`**==**`**的操作。**

#### 指针空值--nullptr(C++11)
##### C++98中的指针空值
在良好的C/C++编程习惯中，声明一个变量时最好给该变量一个合适的初始值，否则可能会出现不可预料的错误，比如未初始化的指针，如果一个指针没有合法的指向，可以按照如下方式对其进行初始化：

```cpp
void TestPtr()
{
    int* p1 = NULL;  // 需要#include <cstdlib>
    int* p2 = 0;
    // ...
}
```

`NULL`实际是一个宏，在传统的C头文件(`stddef.h`)中，可以看到如下代码：

```cpp
#ifndef NULL
#ifdef  __cplusplus
#define NULL    0
#else
#define NULL    ((void *)0)
#endif
#endif
```

可以看到，`NULL`可能被定义为字面常量0，或者被定义为无类型指针(`void*`)的常量。不论采取何种定义，在使用空值的指针时，都不可避免会遇到一些麻烦，例如：

```cpp
#include <iostream>

using namespace std;

void f(int n)
{
    cout << "f(int)" << endl;
}

void f(int* p)
{
    cout << "f(int*)" << endl;

}

int main()
{
    f(0);
    f(NULL);
    f((int*)NULL);  // f((void*)0);

    return 0;
}
```

以上代码中，程序本意是想通过`f(NULL)`调用指针版本的`f(int*)`函数，但是在C++中，由于`NULL`被定义成0，因此与程序的初衷相悖。在C++98中，字面常量0既可以是一个整型数字，也可以是无类型的指针(`void*`)常量，但编译器默认情况下将其看成是一个整型常量，如果要将其按照指针方式来使用，必须对其进行强转(`(void*)0`)。

注意：

:::color2
1. **在使用**`**nullptr**`**表示指针空值时，无需包含头文件，因为**`**nullptr**`**是C++11作为新关键字引入。**
2. **在C++11中，**`**sizeof(nullptr)**`**与**`**sizeof((void*)0)**`**所占字节数相同。**
3. **为了提高代码的健壮性，在后续表示指针空值时建议最好使用**`**nullptr**`**。**

:::

### 类与对象(上)
#### 面向过程与面向对象认识
C语言是面向过程的，关注的是过程，分析出求解问题的步骤，通过函数调用逐步解决问题。例如洗衣服：分解出过程如下：拿盆子 -> 放水 -> 放衣服 -> 放洗衣液 -> 手搓 -> 换水 -> 放洗衣液 -> 手搓 -> 拧干 -> 晾晒。

C++是基于面向对象的，关注的是对象， 将一件事情拆分成不同的对象，靠对象之间的交互完成。同样洗衣服，可以分为四个对象：人、衣服、洗衣液、洗衣机，洗衣服的过程：人将衣服放进洗衣机、倒入洗衣液、启动洗衣机、洗衣机自动完成。整个事件的过程主要是人、衣服、洗衣液、洗衣机四个对象之间交互完成的，人不需要关心洗衣机具体是如何洗衣服的。

#### struct与class的区别
**C++需要兼容C语言，所以C++中**`**struct**`**可以当成结构体使用。另外C++中**`**struct**`**还可以用来定义类，和**`**class**`**定义类是一样的，区别是**`**struct**`**定义类的默认访问控制和默认继承访问控制是**`**public**`**，**`**class**`**定义的类默认访问控制和默认继承访问控制是**`**private**`**。**

**C语言结构体只能定义变量，在C++中，结构体内不仅可以定义变量，也可以定义函数。**

```cpp
struct ListNodeC
{
    int value;
    struct ListNodeC* next;
    struct ListNodeC* prev;
};
```

```cpp
struct ListNodeCPP
{
    int value;
    struct ListNodeCPP* next;  // 兼容C的用法
    ListNodeCPP* prev;         // CPP的用法

    // 还可以定义函数(成员函数)
    ListNodeCPP* CreateNode(int value);
};
```

#### 类的定义
```cpp
class className
{
    // 类体：由成员函数和成员变量组成
};  // 一定要注意后面的分号
```

`class`为定义类的关键字，`className`为类的名字，`{}`中为类的主体，注意类定义结束时后面的分号不能省略。类体中内容称为**类的成员**：类中的变量称为**类的属性**或**成员变量**；类中的函数称为**类的方法**或**成员函数**。

类的两种定义方式：

1. **声明和定义全部放在类体中，需要注意：成员函数如果在类中定义，编译器可能会将其当成内联函数处理。**

```cpp
// 人
class Person
{
public:
    // 显示基本信息
    void ShowInfo()
    {
        cout << _name_ << "-" << _sex_ << "-" << _age_ << endl;
    }

public:
    char* _name_;
    char* _sex_;
    int   _age_;
};
```

2. **类声明放在**`**.h**`**文件中，成员函数定义放在**`**.cpp**`**文件中，注意：成员函数名前需要加**`**类名::**`**。**

```cpp
// person.h  // 声明放在类的头文件中
// 人
class Person
{
public:
    // 显示基本信息
    void ShowInfo();

public:
    char* _name_; 
    char* _sex_;
    int   _age_;
};
```

```cpp
// 定义放在类的实现文件person.cpp中
#include "person.h"

// 显示基本信息，实现输出：名字、性别、年龄
void Person::ShowInfo()
{
    cout << _name_ << "-" << _sex_ << "-" << _age_ << endl;
}
```

一般情况下，更期望采用第二种方式。

关于成员变量命名，看以下代码：

```cpp
class Date
{
public:
    void Init(int year)
    {
        // 这里的year到底是成员变量，还是函数形参
        year = year;
    }

private:
    int year;
};
```

以上代码中，成员变量命名会让人产生误解，对于成员变量命名规则建议如下：

```cpp
class Date
{
public:
    void Init(int year)
    {
        _year_ = year;
    }

private:
    int _year_;
};
```

或是如下：

```cpp
class Date
{
public:
    void Init(int year)
    {
        mYear = year;
    }

private:
    int mYear;
};
```

其他方式也可以，一般是添加前缀或后缀表示区分。

#### 类的访问限定符及封装
##### 访问限定符
C++实现封装的方式：用类将对象的属性与方法结合在一块，让对象更加完善，通过访问权限选择性的将其接口提供给外部的用户使用。

访问限定符有：`public`公有、`protected`保护、`private`私有。

访问限定符说明：

1. `**public**`**修饰的成员在类外可以直接被访问。**
2. `**protected**`**和**`**private**`**修饰的成员在类外不能直接被访问(此处**`**protected**`**和**`**private**`**类似)。**
3. **访问权限作用域从该访问限定符出现的位置开始到下一个访问限定符出现时为止。**
4. **如果后面没有访问限定符，作用域就到**`**}**`**即类结束。**
5. `**class**`**默认访问权限为**`**private**`**，**`**struct**`**为**`**public**`**(**`**struct**`**兼容C)。**

**注意：访问限定符只在编译时有用，当数据映射到内存后，没有任何访问限定符上的区别。**

```cpp
#include <iostream>

using namespace std;

class Student
{
public:  // 访问限定符 类外可直接访问
    // 成员函数
    void ShowInfo()
    {
        cout << _name_ << endl;  // 在类里面可以访问私有
        cout << _age_ << endl;
        cout << _stuid_ << endl;
    }

    int GetAge()
    {
        return _age_;
    }

private:  // 一般情况下，成员变量都是比较隐私的，会定义成private或protected
    // 成员变量
    char _name_[20];
    int  _age_;
    int  _stuid_;
};

int main()
{
    Student s1;
    Student s2;
    s1._age_;  // 类外无法直接访问私有
}
```

##### 封装
面向对象的三大特性：封装、继承、多态。

**封装：将数据和操作数据的方法进行有机结合，隐藏对象的属性和实现细节，仅对外公开接口来和对象进行交互。**

**在C++语言中实现封装，可以通过类将数据以及操作数据的方法进行有机结合，通过访问权限来隐藏对象内部实现细节，控制哪些方法可以在类外部直接被使用。**

#### 类的作用域
**类定义了一个新的作用域，类的所有成员都在类的作用域中。**在类体外定义成员时，需要使用`::`作用域操作符指明成员属于哪个类域。

```cpp
class Person
{
public:
    void PrintPersonInfo();

private:
    char _name_[20];
    char _gender_[3];
    int _age_;
};

// 这里需要指定PrintPersonInfo是属于Person这个类域
void Person::PrintPersonInfo()
{
    cout << _name_ << " " << _gender_ << " " << _age_ << endl;
}
```

#### 类的实例化
用类类型创建对象的过程，称为类的实例化。

1. **类是对对象进行描述的，类似于一个模型，限定了类有哪些成员，定义出一个类并没有分配实际的内存空间来存储它。**
2. **一个类可以实例化出多个对象，实例化出的对象占用实际的物理空间，存储类成员变量。**

```cpp
int main()
{
    Person._age = 100;  // 编译失败：error c2059：语法错误："."
    
    return 0;
}
```

`Person`类是没有空间的，只有`Person`类实例化出的对象才具体的年龄。

3. 类实例化出对象就像现实中使用建筑设计图建造出房子，类就像是设计图，只设计出需要什么东西，

但是并没有实体的建筑存在，同样类也是只是一个设计，实例化出的对象才能实际存储数据，占有物理空间。

#### 类对象模型
##### 如何计算类对象的大小
```cpp
class A
{
public:
    void PrintA()
    {
        cout << _a_ << endl;
    }

private:
    char _a_;
};
```

问题：类中既可以有成员变量，又可以有成员函数，那么一个类的对象中包含了什么？如何计算一个类的大小？

##### 类对象的存储方式猜测
+ **对象中包含类的各个成员。**

![画板](https://cdn.nlark.com/yuque/0/2024/jpeg/36162499/1722498426175-f897f5f6-3f78-434b-bc5c-a63126978650.jpeg)

**缺点：每个对象中成员变量是不同的，但是调用同一份函数，如果按照此方式存储，当一个类创建多个对象时，每个对象中都会保存一份代码，相同代码保存多次，浪费空间。**那么该如何解决呢？

+ **代码只保存一份，在对象中保存存放代码的地址。**

![画板](https://cdn.nlark.com/yuque/0/2024/jpeg/36162499/1722498332993-81e69b0e-14c4-4281-aaad-bb22f8d0d272.jpeg)

+ **只保存成员变量，成员函数存在公共的代码段。**

![画板](https://cdn.nlark.com/yuque/0/2024/jpeg/36162499/1722498426155-e5f01c3d-186c-4ace-b609-c1ad36897069.jpeg)

问题：对于上述三种存储方式，计算机到底是按照哪种方式存储的？

我们通过对下面的不同对象分别获取大小来分析：

```cpp
#include <iostream>

using namespace std;

// 类中既有成员变量，又有成员函数
class A1
{
public:
    void f1() {}

private:
    int _a_;
};

// 类中仅有成员函数
class A2
{
public:
    void f2() {}
};

// 空类
class A3
{

};

int main()
{
    cout << "sizeof(A1)" << sizeof(A1) << endl;  // 4
    cout << "sizeof(A2)" << sizeof(A2) << endl;  // 1
    cout << "sizeof(A3)" << sizeof(A3) << endl;  // 1

    return 0;
}
```

**结论：一个类的大小，实际就是该类中"成员变量"之和，当然要注意内存对齐。注意空类的大小，空类比较特殊，编译器给了空类一个字节来唯一标识这个类的对象。**

##### 结构体内存对齐规则
:::color2
+ **第一个成员在与结构体变量偏移量为0的地址处。**
+ **第2个成员变量开始对齐到对齐数的整数倍的地址处。**
+ **对齐数为编译器默认的一个对齐数与该成员大小的较小值**(VS中默认值为8，Linux中无对齐数)。
+ **结构体总大小为最大对齐数(每个成员变量都有一个对齐数)的整数倍。**
+ **如果嵌套了结构体，嵌套的结构体对齐到自己的最大对齐数的整数倍处，结构体的整体大小就是所有最大对齐数(含嵌套结构体的对齐数)的整数倍。**

:::

面试题：

1. 结构体怎么对齐？为什么要进行内存对齐？
2. 如何让结构体按照指定的对齐参数进行对齐？能否按照3、4、5即任意字节对齐？
3. 什么是大小端？如何测试某台机器是大端还是小端？有没有遇到过要考虑大小端的场景。

#### this指针
##### this指针的引出
我们先定义一个日期类`Date`：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    void Init(int year, int mouth, int day)
    {
        _year_ = year;
        _mouth_ = mouth;
        _day_ = day;
    }

    void Print()
    {
        cout << _year_ << "-" << _mouth_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _mouth_;
    int _day_;
};

int main()
{
    Date d1, d2;

    d1.Init(2022, 1, 11);
    d2.Init(2024, 5, 20);
    d1.Print();
    d2.Print();

    return 0;
}
```

对于上述类，有这样一个问题：`Date`类中有`Init`与`Print`两个成员函数，函数体中没有关于不同对象的区分，那么当`d1`调用`Init`函数时，该函数是如何知道应该设置`d1`对象，而不是设置`d2`对象呢？

在C++中，当成员函数被调用时，它会隐式地接收一个指向调用对象的指针，称为`this`指针。`this`指针指向的是调用该成员函数的对象。每当通过一个对象调用成员函数时，比如 `d1.Init(2022, 1, 11)`，编译器实际上会把这个调用转换成 `Date::Init(&d1, 2022, 1, 11)`。这样，成员函数内部可以通过 `this` 指针来访问调用该函数的具体对象。所以， 当`d1.Init(2022, 1, 11)`被调用时，`this`指针会指向`d1`对象，而当`d2.Init(2024, 5, 20)`被调用时，`this`指针会指向`d2`对象。 上述代码，如果手动添加`this`指针，即以下代码：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    void Init(int year, int month, int day)
    {
        // 通过 this 指针来访问对象的成员变量
        this->_year_ = year;
        this->_month_ = month;
        this->_day_ = day;
    }

    void Print()
    {
        // 通过 this 指针来访问对象的成员变量
        cout << this->_year_ << "-" << this->_month_ << "-" << this->_day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1, d2;

    d1.Init(2022, 1, 11);
    d2.Init(2024, 5, 20);
    d1.Print();
    d2.Print();

    return 0;
}
```

##### this指针的特性
1. `**this**`**指针的类型取决于它所在的类以及成员函数是否为**`**const**`**。  **
    1.  对于非`const`成员函数，`this`指针的类型是指向类类型的非`const`指针。
    2.  对于`const`成员函数，`this`指针的类型是指向类类型的`const`指针。  

```cpp
#include <iostream>

class MyClass
{
public:
    void NonConstFunction() 
    {
        // 在非 const 成员函数中，this 指针的类型是 MyClass*
        MyClass* ptr = this;
        std::cout << "Non-const member function called" << std::endl;
    }

    void ConstFunction() const
    {
        // 在 const 成员函数中，this 指针的类型是 const MyClass*
        const MyClass* ptr = this;
        std::cout << "Const member function called" << std::endl;
    }
};

int main()
{
    MyClass obj;

    // 调用非 const 成员函数
    obj.NonConstFunction();

    // 调用 const 成员函数
    obj.ConstFunction();

    return 0;
}
```

2. 只能在"成员函数"的内部使用。
3. `**this**`**指针本质上是"成员函数"的形参**，当对象调用成员函数时，将对象地址作为实参传递给`this`形参。所以**对象中不存储**`**this**`**指针。**
4. `**this**`**指针是"成员函数"第一个隐含的指针形参，一般情况由编译器通过**`**ecx**`**寄存器自动传递，不需要用户传递。**

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    void Init(int year, int mouth, int day)  // void Init(Date* this, int year, int mouth, int day)
    {
        this->_year_ = year;
        this->_mouth_ = mouth;
        this->_day_ = day;
    }

    void Print()  // void Print(Date* this)
    {
        cout << this->_year_ << "-" << this->_mouth_ << "-" << this->_day_ << endl;
    }

private:
    int _year_;
    int _mouth_;
    int _day_;
};

int main()
{
    Date d1, d2;

    d1.Init(2022, 1, 11);  // d1.Init(&d1, 2022, 1, 11)
    d2.Init(2024, 5, 20);
    d1.Print();  // d1.Print(&d1)
    d2.Print();

    return 0;
}
```

面试题：

1. `this`指针存在于进程地址空间的哪个区域？`this`指针本质也是形参，所以在栈上！
2. `this`指针可以为空吗？
3. 以下程序编译运行结果是？编译报错、运行崩溃、正常运行。

```cpp
#include <iostream>

using namespace std;

class A
{
public:
    void Print()
    {
        cout << "Print()" << endl;  // 此处this为空指针不影响，没有参与访问
    }

    void PrintA()
    {
        cout << _a_ << endl;  // 此处this为空则崩溃cout << this->_a << endl;
    }

private:
    int _a_;
};

int main()
{
    A* p = nullptr;
    p->Print();   // 正常，成员函数存在公共的代码段，p->Print()不会去找p指向的对象上找，访问成员函数才会去找
    p->PrintA();  // 崩溃

    return 0;
}
```

##### C语言和C++实现stack的对比
+ C语言实现

```cpp
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>

typedef int DataType; // 定义栈中数据的类型

typedef struct Stack
{
    DataType* array; // 动态数组，存储栈中的元素
    int capacity;    // 栈的容量
    int size;        // 栈中当前元素的个数
} Stack;

// 初始化栈
void stackInit(Stack* ps)
{
    assert(ps); // 检查 ps 是否为 NULL
    ps->array = (DataType*)malloc(sizeof(DataType) * 3); // 分配初始容量为 3 的动态数组
    if (NULL == ps->array) // 检查内存分配是否成功
    { 
        assert(0); // 如果分配失败，触发断言
        return;
    }
    ps->capacity = 3; // 设置栈的初始容量为 3
    ps->size = 0; // 初始化栈的大小为 0
}

// 销毁栈
void stackDestroy(Stack* ps) 
{
    assert(ps); // 检查 ps 是否为 NULL
    if (ps->array) // 如果栈的数组不为空
    { 
        free(ps->array); // 释放分配的内存
        ps->array = NULL; // 将指针置为空
        ps->capacity = 0; // 重置栈的容量
        ps->size = 0; // 重置栈的大小
    }
}

// 检查并扩展栈的容量
void checkCapacity(Stack* ps) 
{
    if (ps->size == ps->capacity) // 如果栈已满
    { 
        int newCapacity = ps->capacity * 2; // 新容量为当前容量的两倍
        DataType* tmp = (DataType*)realloc(ps->array, newCapacity * sizeof(DataType)); // 重新分配内存
        if (tmp == NULL) // 检查内存重新分配是否成功
        { 
            perror("Realloc申请空间失败！"); // 输出错误信息
            return;
        }
        ps->array = tmp; // 更新栈的数组指针
        ps->capacity = newCapacity; // 更新栈的容量
    }
}

// 入栈操作
void stackPush(Stack* ps, DataType data)
{
    assert(ps); // 检查 ps 是否为 NULL
    checkCapacity(ps); // 检查并扩展栈的容量
    ps->array[ps->size] = data; // 将数据放入栈顶
    ps->size++; // 增加栈的大小
}

// 检查栈是否为空
int stackEmpty(Stack* ps) 
{
    assert(ps); // 检查 ps 是否为 NULL
    return 0 == ps->size; // 返回栈是否为空
}

// 出栈操作
void stackPop(Stack* ps) 
{
    if (stackEmpty(ps)) // 如果栈为空
        return; // 什么也不做
    ps->size--; // 减少栈的大小
}

// 获取栈顶元素
DataType stackTop(Stack* ps) 
{
    assert(!stackEmpty(ps)); // 确保栈不为空
    return ps->array[ps->size - 1]; // 返回栈顶元素
}

// 获取栈的大小
int stackSize(Stack* ps)
{
    assert(ps); // 检查 ps 是否为 NULL
    return ps->size; // 返回栈的大小
}

// 主函数，测试栈的基本操作
int main() 
{
    Stack s; // 定义一个栈
    stackInit(&s); // 初始化栈

    // 压入元素 1, 2, 3, 4
    stackPush(&s, 1);
    stackPush(&s, 2);
    stackPush(&s, 3);
    stackPush(&s, 4);

    // 打印栈顶元素和栈的大小
    printf("%d\n", stackTop(&s)); // 输出栈顶元素 4
    printf("%d\n", stackSize(&s)); // 输出栈的大小 4

    // 弹出两个元素
    stackPop(&s);
    stackPop(&s);

    // 打印栈顶元素和栈的大小
    printf("%d\n", stackTop(&s)); // 输出栈顶元素 2
    printf("%d\n", stackSize(&s)); // 输出栈的大小 2

    stackDestroy(&s); // 销毁栈

    return 0; // 程序结束
}
```

可以看到，在用C语言实现时，`Stack`相关操作函数有以下共性：

+ 每个函数的第一个参数都是`Stack*`。
+ 函数中必须要对第一个参数检测，因为该参数可能会为`NULL`。
+ 函数中都是通过`Stack*`参数操作栈的。
+ 调用时必须传递`Stack`结构体变量的地址。

结构体中只能定义存放数据的结构，操作数据的方法不能放在结构体中，即**数据和操作数据的方式是分离开的**，而且实现上相当复杂一点，涉及到大量指针操作，稍不注意可能会错。

+ C++实现

```cpp
#include <iostream>
#include <cstdlib> // 包含 malloc 和 realloc 的库

using namespace std;

typedef int DataType;

class Stack 
{
public:
    // 初始化栈
    void Init() 
    {
        _array = (DataType*)malloc(sizeof(DataType) * 3); // 分配初始容量为 3 的动态数组
        if (NULL == _array) 
        {
            perror("malloc申请空间失败"); // 检查内存分配是否成功
            return;
        }

        _capacity = 3; // 设置栈的初始容量为 3
        _size = 0; // 初始化栈的大小为 0
    }

    // 入栈操作
    void Push(DataType data) 
    {
        checkCapacity(); // 检查并扩展栈的容量
        _array[_size] = data; // 将数据放入栈顶
        _size++; // 增加栈的大小
    }

    // 出栈操作
    void Pop() 
    {
        if (Empty())
            return;
        _size--; // 减少栈的大小
    }

    // 获取栈顶元素
    DataType Top() 
    {
        return _array[_size - 1]; // 返回栈顶元素
    }

    // 检查栈是否为空
    int Empty() 
    {
        return _size == 0; // 如果栈的大小为 0，则栈为空
    }

    // 获取栈的大小
    int Size() 
    {
        return _size; // 返回栈的大小
    }

    // 销毁栈
    void Destroy() 
    {
        if (_array) 
        {
            free(_array); // 释放分配的内存
            _array = NULL; // 将指针置为空
            _capacity = 0; // 重置栈的容量
            _size = 0; // 重置栈的大小
        }
    }

private:
    // 检查并扩展栈的容量
    void checkCapacity() 
    {
        if (_size == _capacity) // 如果栈已满
        { 
            int newCapacity = _capacity * 2; // 新容量为当前容量的两倍
            DataType* tmp = (DataType*)realloc(_array, newCapacity * sizeof(DataType)); // 重新分配内存
            if (tmp == NULL) // 检查内存重新分配是否成功
            { 
                perror("realloc申请空间失败！");
                return;
            }
            _array = tmp; // 更新栈的数组指针
            _capacity = newCapacity; // 更新栈的容量
        }
    }

private:
    DataType* _array; // 动态数组，存储栈中的元素
    int _capacity;    // 栈的容量
    int _size;        // 栈中当前元素的个数
};

int main() 
{
    Stack s; // 定义一个栈
    s.Init(); // 初始化栈

    // 压入元素 1, 2, 3, 4
    s.Push(1);
    s.Push(2);
    s.Push(3);
    s.Push(4);

    // 打印栈顶元素和栈的大小
    printf("%d\n", s.Top()); // 输出栈顶元素 4
    printf("%d\n", s.Size()); // 输出栈的大小 4

    // 弹出两个元素
    s.Pop();
    s.Pop();

    // 再次打印栈顶元素和栈的大小
    printf("%d\n", s.Top()); // 输出栈顶元素 2
    printf("%d\n", s.Size()); // 输出栈的大小 2

    s.Destroy(); // 销毁栈

    return 0; // 程序结束
}
```

**C++中通过类可以将数据及操作数据的方法进行完美结合，通过访问权限可以控制那些方法在类外可以被调用，即封装。**每个方法不需要传递`Stack*`参数，编译器编译之后该参数会自动还原，即**C++中**`**Stack***`**参数是编译器维护的，C语言中需要程序员自己维护。**

### 类和对象(中)
#### 类的6个默认成员函数
如果一个类中什么成员都没有，则被称为空类。空类中真的什么都没有吗？并不是，对于任何类，编译器会自动生成以下6个默认成员函数：

+ **初始化和清理：**
    - **构造函数：主要完成初始化工作。**
    - **析构函数：主要完成清理工作。**
+ **拷贝赋值：**
    - **拷贝构造：使用同类对象初始化创建对象。**
    - **赋值重载：主要是把一个对象赋值给另一个对象。**
+ **取地址重载(很少自己实现)：**
    - **普通对象取地址。**
    - `**const**`**对象取地址。**

#### 构造函数
##### 概念
对于以下`Date`类：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    void Init(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }
    
private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1;
    d1.Init(2024, 7, 7);
    d1.Print();

    Date d2;
    d2.Init(2024, 7, 8);
    d2.Print();

    return 0;
}
```

对于`Date`类，可以通过`Init`共有方法给对象设置日期，但如果每次创建对象时都调用该方法设置信息，未免有些麻烦，且如果在初始化之前调用`Print`成员函数打印日期，则会出现随机值。那能否在对象创建时就将信息设置好呢？**构造函数是一个特殊的成员函数，名字与类名相同，创建类类型对象时由编译器自动调用，以保证每个数据成员都有一个合适的初始值，并且在对象整个生命周期内只调用一次。**

##### 特征
构造函数是特殊的成员函数，需要注意的是，构造函数虽然名叫构造，但是**构造函数的主要任务并不是开辟空间创建对象，而是初始化对象，进行资源分配**。其特征如下：

+ **函数名与类名相同。**
+ **无返回类型。**
+ **对象实例化时编译器自动调用对应的构造函数。**
+ **初始化列表。**
+ **构造函数可以重载。**

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 1.带参构造函数
    Date(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // 2.无参构造函数
    Date()
    {
        _year_ = 0;
        _month_ = 1;
        _day_ = 1;
    }

    void Init(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(2022, 1, 1);  // 调用带参构造函数
    d1.Print();

    // 注意：如果通过无参构造函数创建对象时，对象后面不用跟括号，否则就成了函数声明
    // 以下代码的函数：声明了d2函数，该函数无参，返回一个日期类型的对象
    // warning C4930: “Date d2(void)”: 未调用原型函数(是否是有意用变量定义的?)
    Date d2;  // 调用无参构造函数
    d2.Print();

    return 0;
}
```

+ **如果类中没有显式定义构造函数，则C++编译器会自动生成一个无参的默认构造函数，一旦用户显式定义，编译器将不在生成。**

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 如果用户显式定义了构造函数，编译器将不再生成
    /*Date(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }*/

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;

};

int main()
{
    // 将Date类中构造函数屏蔽后，代码可以通过编译，因为编译器生成了一个无参的默认构造函数
    // 将Date类中构造函数放开，代码编译失败，因为一旦显式定义任何构造函数，编译器将不再生成
    // 无参构造函数，放开后报错：error C2512: “Date”: 没有合适的默认构造函数可用
    Date d1;
    d1.Print();  // -858993460--858993460--858993460

    return 0;
}
```

关于编译器生成的默认成员函数，有以下疑问：不显式实现构造函数的情况下，编译器会生成默认的构造函数。`d1`对象调用了编译器生成的默认构造函数，但是`d1`对象的成员变量`_year_`、`_month_`、`_day_`的值依然是随机值，所以编译器生成的默认构造函数并没有作用？

C++把类型分成内置类型和自定义类型。内置类型就是语言提供的数据类型，自定义类型例如`clas`

`s`、`struct`等。分析以下代码，会发现**编译器生成默认的构造函数会对自定义类型成员**`**_t_**`**调用它的默认成员函数**：

```cpp
#include <iostream>

using namespace std;

class Time
{
public:
    Time()
    {
        cout << "Time()" << endl;
        _hour_ = 0;
        _minute_ = 0;
        _second_ = 0;
    }

private:
    int _hour_;
    int _minute_;
    int _second_;
};

class Date
{
public:
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;

    Time _t_;
};

int main()
{
    Date d;     // 调用默认成员函数Time()
    d.Print();  // -858993460--858993460--858993460

    return 0;
}
```

上述代码执行结果为输出`Time()`和一串随机值的年月日，`Date`类中的基本数据类型是随机值，但自定义类型`_t_`被初始化为0，调用了`Time`类的构造函数。在C++11中，针对内置类型成员不初始化的缺陷打了补丁，即**内置类型成员变量在类中声明时可以给默认值：**

```cpp
#include <iostream>

using namespace std;

class Time
{
public:
    Time()
    {
        cout << "Time()" << endl;
        _hour_ = 0;
        _minute_ = 0;
        _second_ = 0;
    }

private:
    int _hour_;
    int _minute_;
    int _second_;
};

class Date
{
public:
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    // 基本类型
    // C++11支持，声明时给缺省值
    int _year_ = 2024;
    int _month_ = 1;
    int _day_ = 1;

    // 自定义类型
    Time _t_;
};

int main()
{
    Date d;     // Time()
    d.Print();  // 2024-1-1

    return 0;
}
```

+ **默认构造函数有3个：编译器默认生成的构造函数、无参构造函数、全缺省构造函数，并且默认构造函**

**数只能有一个。**

```cpp
#include <iostream>

using namespace std;

// Date 类定义
class Date
{
public:
    // 默认构造函数
    Date()
    {
        _year_ = 2024;
        _month_ = 1;
        _day_ = 1;
    }

    // 带默认参数的构造函数
    Date(int year = 2024, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // 带三个参数的构造函数(注意这里的函数重载与上一个函数冲突)
    /*
    Date(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }
    */

    // 打印日期函数
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;   // 年份
    int _month_;  // 月份
    int _day_;    // 日期
};

int main()
{
    Date d1;  //error, 不确定调用谁，可能是Date::Date(int, int, int)或是Date::Date(void)

    // 使用带参数的构造函数创建对象 d2
    Date d2(2022, 1, 1);
    d2.Print(); // 输出: 2022-1-1

    return 0;
}
```

上述代码中如果想实现用无参与带参的构造函数，会很不方便，可以使用全缺省构造函数解决：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 全缺省构造函数
    Date(int year = 2024, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1;
    d1.Print();  // 2024-1-1

    Date d2(2021, 1, 2);
    d2.Print();  // 2021-1-2

    return 0;
}
```

#### 析构函数
##### 概念
通过前面构造函数的学习，我们知道一个对象是怎么来的，那一个对象又是怎么消失的呢？  
       析构函数：与构造函数功能相反，析构函数并不是完成对对象本身的销毁，局部对象销毁工作是由编译器完成的。而**对象在销毁时会自动调用析构函数，完成对象中资源的释放。**

##### 特征
析构函数是特殊的成员函数，其特征如下：

+ **名称与类名相同但前面加**`**~**`。
+ **无返回值类型。**
+ **无参数**
+ **一个类只能有一个析构函数。若未显式定义，系统会自动生成默认的析构函数。析构函数不能重载。**
+ **对象生命周期结束时，C++编译器自动调用析构函数。**

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    ~Date()
    {
        cout << "~Date()" << endl;
    }

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d;  // ~Date()

    return 0;
}
```

+ **编译器生成的默认析构函数，对自定义类型成员调用它的析构函数。**

```cpp
#include <iostream>

using namespace std;

class Time
{
public:
    ~Time()
    {
        cout << "~Time()" << endl;
    }

private:
    int _hour_;
    int _minute_;
    int _second_;
};

class Date
{
private:
    // 基本数据类型
    int _year_ = 2025;
    int _month_ = 1;
    int _day_ = 1;

    // 自定义类型
    Time _t_;
};

int main()
{
    Date d;  // ~Date()

    return 0;
}
```

以上代码运行结束后输出：`~Time()`。在`main`方法中并未直接创建`Time`类的对象，为什么最后会调用`Time`类的析构函数？在`main`方法中创建了`Date`类的对象`d`，而`d`中包含4个成员变量，其中前3个成员变量是内置类型成员，销毁时不需要资源清理，最后系统直接将其内存回收即可；而`_t_`是`Time`类对象，所以在`d`销毁时，要将其内部包含的`Time`类的`_t_`对象销毁，所以要调用`Time`类的析构函数。但是在`main`方法中不能直接调用`Time`类的析构函数，实际要释放的是`Date`类对象，所以编译器会调用`Date`类的析构函数，而`Date`没有显式提供，则编译器会给`Date`类生成一个默认的析构函数，目的是在其内部调用`Time`。类的析构函数，即当`Date`对象销毁时，要保证其内部每个自定义对象都可以正确销毁。`main`函数中并没有直接调用`Time`类析构函数，而是显式调用编译器为`Date`类生成的默认析构函数。注意：创建哪个类的对象则调用该类的析构函数，销毁哪个类的对象则调用该类的析构函数。

:::color2
**在函数作用域内，对象的构造顺序是从上到下，而析构顺序是从下到上， 符合对象的生命周期管理规则：先构造的后析构，后构造的先析构。  **

:::

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date()
    {
        cout << "构造:" << endl;
        cout << "Date(): " << this << endl;
        _year_ = 2024;
        _month_ = 1;
        _day_ = 1;
    }

    ~Date()
    {
        cout << "析构:" << endl;
        cout << "~Date(): " << this << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    /*
    构造:
    Date(): 0053FC2C
    构造:
    Date(): 0053FC18
    析构:
    ~Date(): 0053FC18
    析构:
    ~Date(): 0053FC2C
    */
    Date d1;
    Date d2;

    return 0;
}
```

+ **如果类中没有申请资源时，析构函数可以不写，直接使用编译器生成的析构函数，比如**`**Date**`**类；有**

**资源申请时，一定要写，否则会造成资源泄漏，比如**`**Stack**`**类。**

```cpp
#include <iostream>  

using namespace std; 

typedef int DataType; // 定义一个类型别名，DataType 表示 int

class Stack
{
public:
    // 构造函数，初始化栈的容量，默认容量为 3
    Stack(size_t capacity = 3)
    {
        // 动态分配内存以存储栈的元素
        _array_ = (DataType*)malloc(sizeof(DataType) * capacity);
        if (NULL == _array_) // 检查内存分配是否成功
        {
            perror("malloc failed to apply for space!"); // 打印错误信息
            return;
        }

        _capacity_ = capacity; // 设置栈的容量
        _size_ = 0; // 初始化栈的大小为 0
    }

    // 向栈中压入一个元素
    void Push(DataType data)
    {
        // CheckCapacity(); // 检查栈是否需要扩容(此行代码被注释掉了)
        _array_[_size_] = data; // 将数据存入栈中
        _size_++; // 增加栈的大小
    }

    // 其他方法的声明(未实现)...

    // 析构函数，释放动态分配的内存
    ~Stack()
    {
        cout << "Automatic calling" << endl; // 打印析构函数被自动调用的信息
        if (_array_) // 检查数组是否为空
        {
            free(_array_); // 释放内存
            _array_ = nullptr; // 将指针置为 nullptr
            _capacity_ = 0; // 重置容量
            _size_ = 0; // 重置大小
        }
    }

private:
    DataType* _array_; // 指向栈元素数组的指针
    size_t _capacity_; // 栈的容量
    size_t _size_; // 栈的当前大小
};

int main()
{
    Stack s; // 创建一个栈对象，默认容量为 3
    s.Push(1); // 向栈中压入元素 1
    s.Push(2); // 向栈中压入元素 2

    return 0; // 结束程序，栈对象 s 被销毁，调用析构函数
}
```

#### 拷贝构造函数
##### 概念
创建对象时，可否创建一个与已存在对象一模一样的新对象呢？例如：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 0, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(2022, 1, 1);
    Date d2(2022, 1, 1);

    return 0;
}
```

其中对象`d1`与`d2`相同，但如果将`d1`的成员变量修改后，`d2`也要跟着变化才为相同对象，这样过于麻烦。

**拷贝构造函数：只有单个形参，该形参是对本类型对象的引用(一般常用**`**const**`**修饰)，在用已存在的类类型对象创建新对象时由编译器自动调用。**

##### 特征
拷贝构造函数也是特殊的成员函数，其特征如下：

+ **拷贝构造函数是构造函数的一个重载形式。**
+ **拷贝构造函数的参数只有一个且必须是类类型对象的引用。**

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 2024, int month = 1, int day = 2)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // Date(const Date& d) // 正确写法
    Date(const Date d)  // 错误写法，编译报错，无穷递归
    {
        _year_ = d._year_;
        _month_ = d._month_;
        _day_ = d._day_;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1;
    Date d2(d1);

    return 0;
}
```

上述代码写法`Date(const Date d)`中， 拷贝构造函数的参数是传值类型，这意味着在调用拷贝构造函数时，会尝试拷贝`d`参数，而这个拷贝动作本身会再次调用拷贝构造函数，导致无穷递归。对于此处无穷递归的现象，有以下代码：

```cpp
#include <iostream>  // 包含标准输入输出库

using namespace std;  // 使用标准命名空间

// 定义Date类
class Date
{
public:
    // 带有默认参数的构造函数，初始化年、月、日
    Date(int year = 0, int month = 1, int day = 1)
    {
        _year_ = year;  // 初始化年
        _month_ = month;  // 初始化月
        _day_ = day;  // 初始化日
    }

    // 打印日期的成员函数
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;  // 按"年-月-日"格式输出日期
    }

private:
    int _year_;  // 存储年的私有成员变量
    int _month_;  // 存储月的私有成员变量
    int _day_;  // 存储日的私有成员变量
};

// 一个接受Date对象的函数，传递的是副本
void f(Date d)
{
    d.Print();  // 调用传入对象的Print函数
}

int main()
{
    Date d1(2022, 1, 1);  // 使用构造函数创建Date对象d1，并初始化为2022年1月1日
    f(d1);  // 调用函数f，传递d1的副本

    return 0;  // 返回0，表示程序正常结束
}
```

上述代码中，当调用`f(d1)`时，会调用`Date`类的拷贝构造函数。虽然没有显式地定义拷贝构造函数，但编译器会生成一个默认的拷贝构造函数。这个默认的拷贝构造函数会逐成员地拷贝对象。因此，在进入 `f`函数之前，会调用拷贝构造函数来创建一个`Date`类型的临时对象`d`，并将`d1`的值拷贝给它。为了确认这一点，可以在类中添加一个拷贝构造函数，并在其中添加一些输出语句，以便观察拷贝构造函数的调用：  

```cpp
#include <iostream>  // 包含标准输入输出库

using namespace std;  // 使用标准命名空间

// 定义Date类
class Date
{
public:
    // 带有默认参数的构造函数，初始化年、月、日
    Date(int year = 0, int month = 1, int day = 1)
    {
        _year_ = year;  // 初始化年
        _month_ = month;  // 初始化月
        _day_ = day;  // 初始化日
        cout << "Constructor called" << endl;  // 输出构造函数被调用的信息
    }

    // 拷贝构造函数，接受一个Date对象的引用作为参数
    Date(const Date& d)
    {
        _year_ = d._year_;  // 使用传入对象的年初始化
        _month_ = d._month_;  // 使用传入对象的月初始化
        _day_ = d._day_;  // 使用传入对象的日初始化
        cout << "Copy constructor called" << endl;  // 输出拷贝构造函数被调用的信息
    }

    // 打印日期的成员函数
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;  // 按"年-月-日"格式输出日期
    }

private:
    int _year_;  // 存储年的私有成员变量
    int _month_;  // 存储月的私有成员变量
    int _day_;  // 存储日的私有成员变量
};

// 一个接受Date对象的函数，传递的是副本
void f(Date d)
{
    d.Print();  // 调用传入对象的Print函数
}

int main()
{
    Date d1(2022, 1, 1);  // 使用构造函数创建Date对象d1，并初始化为2022年1月1日
    f(d1);  // 调用函数f，传递d1的副本

    return 0;  // 返回0，表示程序正常结束
}
```

以上代码的输出结果为：

> Constructor called
>
> Copy constructor called
>
> 2022-1-1
>

所以正确的方式是传引用：

```cpp
#include <iostream>  // 包含标准输入输出库

using namespace std;  // 使用标准命名空间

// 定义Date类
class Date
{
public:
    // 带有默认参数的构造函数，初始化年、月、日
    Date(int year = 2024, int month = 1, int day = 2)
    {
        _year_ = year;  // 初始化年的私有成员变量
        _month_ = month;  // 初始化月的私有成员变量
        _day_ = day;  // 初始化日的私有成员变量
    }

    // 拷贝构造函数，接受一个Date对象的引用作为参数
    Date(const Date& d)
    {
        _year_ = d._year_;  // 使用传入对象的年初始化当前对象的年
        _month_ = d._month_;  // 使用传入对象的月初始化当前对象的月
        _day_ = d._day_;  // 使用传入对象的日初始化当前对象的日
    }

    // 打印日期的成员函数
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;  // 按"年-月-日"格式输出日期
    }

private:
    int _year_;  // 存储年的私有成员变量
    int _month_;  // 存储月的私有成员变量
    int _day_;  // 存储日的私有成员变量
};

int main()
{
    Date d1;  // 使用带默认参数的构造函数创建Date对象d1
    Date d2(d1);  // 使用拷贝构造函数创建Date对象d2，初始化为d1的副本

    // 也可以使用以下语句创建d3，效果与d2相同
    // Date d3 = d1;  // 也是拷贝构造操作，切勿当成后续的运算符重载！

    d1.Print();  // 调用d1的Print函数，输出d1的日期
    d2.Print();  // 调用d2的Print函数，输出d2的日期

    return 0;  // 返回0，表示程序正常结束
}
```

+ **若未显式定义，编译器会生成默认的拷贝构造函数。**默认的拷贝构造函数对象按内存存储字节序完成

拷贝，这种拷贝叫做浅拷贝或值拷贝。

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 构造函数
    Date(int year = 2024, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(1, 1, 1);
    Date d2(2, 2, 2);

    d1 = d2;
    d1.Print();  // 2-2-2
    d2.Print();  // 2-2-2

    Date d3(d1);  // 拷贝构造
    Date d4 = d1; // 拷贝构造
    d3.Print();  // 2-2-2
    d4.Print();  // 2-2-2

    return 0;
}
```

```cpp
#include <iostream>

using namespace std;

class Time
{
public:
    Time()
    {
        _hour_ = 1;
        _minute_ = 1;
        _second_ = 1;
    }

    Time(const Time& t)
    {
        _hour_ = t._hour_;
        _minute_ = t._minute_;
        _second_ = t._second_;

        cout << "Time::Time(const Time&)" << endl;
    }

private:
    int _hour_;
    int _minute_;
    int _second_;
};

class Date
{
    // 基本类型
    int _year_ = 2024;
    int _month_ = 1;
    int _day_ = 1;

    // 自定义类型
    Time _t_;
};

int main()
{
    Date d1;

    // 用已经存在的d1拷贝构造d2，此处会调用Date类的拷贝构造函数
    // 但Date类并未显式定义拷贝构造函数，则编译器会给Date类生成一个默认的拷贝构造函数
    Date d2(d1);

    return 0;
}
```

:::color2
**注意：在编译器生成的默认拷贝构造函数中，内置类型是按照字节方式直接拷贝的，而自定义类型是调用其拷贝构造函数完成拷贝的。**

:::

编译器生成的默认拷贝构造函数已经可以完成字节序的值拷贝了，还需要自己显式实现吗？请看以下代码：

```cpp
#include <iostream>  // 包含标准输入输出库
#include <cstdlib>  // 包含malloc和free函数的库

using namespace std;  // 使用标准命名空间

typedef int DataType;  // 定义DataType为int类型

// 定义Stack类
class Stack
{
public:
    // 构造函数，初始化栈的容量
    Stack(size_t capacity = 10)
    {
        _array_ = (DataType*)malloc(capacity * sizeof(DataType));  // 分配存储空间
        if (nullptr == _array_)
        {
            perror("Malloc failed to apply for space!");  // 输出分配失败信息
            return;
        }

        _size_ = 0;  // 初始化栈的大小为0
        _capacity_ = capacity;  // 初始化栈的容量
    }

    // 拷贝构造函数，实现深拷贝
    Stack(const Stack& s)
    {
        _array_ = (DataType*)malloc(s._capacity_ * sizeof(DataType));  // 为新栈分配空间
        if (nullptr == _array_)
        {
            perror("Malloc failed to apply for space!");  // 输出分配失败信息
            return;
        }

        // 复制元素
        for (size_t i = 0; i < s._size_; ++i)
        {
            _array_[i] = s._array_[i];
        }

        _size_ = s._size_;  // 复制大小
        _capacity_ = s._capacity_;  // 复制容量
    }

    // 入栈操作
    void Push(const DataType& data)
    {
        // 检查是否需要扩容(此处未实现CheckCapacity函数，可以根据需要添加)
        // CheckCapacity();
        _array_[_size_] = data;  // 将数据放入栈中
        _size_++;  // 栈大小增加
    }

    // 析构函数，释放分配的空间
    ~Stack()
    {
        if (_array_)
        {
            free(_array_);  // 释放内存
            _array_ = nullptr;  // 将指针置为空
            _capacity_ = 0;  // 重置容量
            _size_ = 0;  // 重置大小
        }
    }

private:
    DataType* _array_;  // 存储栈元素的指针
    size_t _size_;  // 当前栈的大小
    size_t _capacity_;  // 栈的容量
};

int main()
{
    Stack s1;  // 创建栈对象s1
    s1.Push(1);  // 入栈1
    s1.Push(2);  // 入栈2
    s1.Push(3);  // 入栈3
    s1.Push(4);  // 入栈4

    Stack s2(s1);  // 使用拷贝构造函数创建栈对象s2

    return 0;  // 返回0，表示程序正常结束
}
```

![](https://cdn.nlark.com/yuque/0/2024/png/36162499/1720493597562-409b9432-b4a2-43a8-95bd-e069bd5430af.png)

:::color2
**注意：类中如果没有涉及资源申请时，拷贝构造函数是否写都可以；一旦涉及到资源申请时，拷贝构造函数必须要写，否则就是浅拷贝，会造成同一块空间释放两次，导致崩溃。**

:::

```cpp
#include <iostream>  // 包含标准输入输出库

using namespace std;  // 使用标准命名空间

// 定义栈中存储的数据类型
typedef int DataType;

class Stack
{
public:
    // 构造函数，初始化栈的容量并分配内存
    Stack(size_t capacity = 10)
    {
        _array_ = (DataType*)malloc(capacity * sizeof(DataType));  // 分配容量为capacity的内存
        if (nullptr == _array_)
        {
            perror("Malloc failed to apply for space!");  // 输出分配失败信息
            return;
        }

        _size_ = 0;  // 初始化栈的大小为0
        _capacity_ = capacity;  // 初始化栈的容量
    }

    // 深拷贝构造函数
    Stack(const Stack& other)
    {
        _array_ = (DataType*)malloc(other._capacity_ * sizeof(DataType));  // 分配与other相同容量的内存
        if (nullptr == _array_)
        {
            perror("Malloc failed to apply for space!");  // 输出分配失败信息
            return;
        }

        _size_ = other._size_;  // 复制栈的大小
        _capacity_ = other._capacity_;  // 复制栈的容量
        for (size_t i = 0; i < _size_; ++i)
        {
            _array_[i] = other._array_[i];  // 逐个复制元素
        }
    }

    // 赋值运算符重载，用于深拷贝
    Stack& operator=(const Stack& other)
    {
        if (this != &other)  // 防止自赋值
        {
            DataType* newArray = (DataType*)malloc(other._capacity_ * sizeof(DataType));  // 分配新内存
            if (nullptr == newArray)
            {
                perror("Malloc failed to apply for space!");  // 输出分配失败信息
                return *this;
            }

            free(_array_);  // 释放旧内存
            _array_ = newArray;  // 指向新内存
            _size_ = other._size_;  // 复制栈的大小
            _capacity_ = other._capacity_;  // 复制栈的容量
            for (size_t i = 0; i < _size_; ++i)
            {
                _array_[i] = other._array_[i];  // 逐个复制元素
            }
        }
        return *this;  // 返回当前对象
    }

    // 向栈中压入数据
    void Push(const DataType& data)
    {
        // 这里可以加上扩容逻辑，例如 CheckCapacity();
        _array_[_size_] = data;  // 将数据压入栈
        _size_++;  // 栈的大小增加
    }

    // 析构函数，释放内存
    ~Stack()
    {
        if (_array_)
        {
            free(_array_);  // 释放内存
            _array_ = nullptr;  // 将指针置为空
            _capacity_ = 0;  // 重置容量
            _size_ = 0;  // 重置大小
        }
    }

private:
    DataType* _array_;   // 栈数组指针
    size_t _size_;       // 栈中元素个数
    size_t _capacity_;   // 栈的容量
};

int main()
{
    Stack s1;  // 创建栈对象s1
    s1.Push(1);  // 压入数据1
    s1.Push(2);  // 压入数据2
    s1.Push(3);  // 压入数据3
    s1.Push(4);  // 压入数据4

    // 使用深拷贝构造函数
    Stack s2(s1);

    return 0;  // 返回0，表示程序正常结束
}
```

+ 拷贝构造函数典型调用场景
    - 使用已存在对象创建新对象
    - 函数参数类型为类类型对象
    - 函数返回类型为类类型对象

```cpp
#include <iostream>  // 包含标准输入输出库

using namespace std;  // 使用标准命名空间

// 定义Date类
class Date
{
public:
    // 构造函数，初始化年、月、日，并输出构造函数被调用的信息
    Date(int year, int month, int day)
    {
        _year_ = year;  // 初始化年的私有成员变量
        _month_ = month;  // 初始化月的私有成员变量
        _day_ = day;  // 初始化日的私有成员变量
        cout << "Date(int, int, int):" << this << endl;  // 输出构造函数被调用的信息
    }

    // 拷贝构造函数，输出拷贝构造函数被调用的信息
    Date(const Date& d)
    {
        _year_ = d._year_;  // 复制传入对象的年
        _month_ = d._month_;  // 复制传入对象的月
        _day_ = d._day_;  // 复制传入对象的日
        cout << "Date(const Date& d):" << this << endl;  // 输出拷贝构造函数被调用的信息
    }

    // 析构函数，输出析构函数被调用的信息
    ~Date()
    {
        cout << "~Date():" << this << endl;  // 输出析构函数被调用的信息
    }

private:
    int _year_;  // 存储年的私有成员变量
    int _month_;  // 存储月的私有成员变量
    int _day_;  // 存储日的私有成员变量
};

// Test函数，接受一个Date对象，并返回一个Date对象
Date Test(Date d)
{
    Date temp(d);  // 使用拷贝构造函数创建临时对象temp
    return temp;  // 返回临时对象
}

int main()
{
    Date d1(2024, 1, 2);  // 使用构造函数创建Date对象d1
    Test(d1);  // 调用Test函数，传递d1的副本

    /*
    输出结果： 
    Date(int, int, int):0x7ffee3773bf0   // 创建d1对象
    Date(const Date& d):0x7ffee3773bd0   // 拷贝构造Test函数的形参d
    Date(const Date& d):0x7ffee3773bc0   // Test函数中创建临时对象temp
    Date(const Date& d):0x7ffee3773bb0   // 返回temp，创建临时对象用于返回值
    ~Date():0x7ffee3773bc0   // 销毁Test函数中的temp对象
    ~Date():0x7ffee3773bd0   // 销毁Test函数的形参d
    ~Date():0x7ffee3773bb0   // 销毁返回的临时对象
    ~Date():0x7ffee3773bf0   // 销毁main函数中的d1对象
    */

    return 0;  // 返回0，表示程序正常结束
}
```

1. **创建d1对象**：
    - `Date d1(2024, 1, 2);`调用构造函数`Date(int, int, int)`创建`d1`对象。
    - 输出: `Date(int, int, int):<地址d1>`。
2. **调用Test函数**：
    - `Test(d1);` 将`d1`传递给`Test`函数，这会调用`Test`函数的形参`d`的拷贝构造函数`Date(const Date& d)`。
    - 输出: `Date(const Date& d):<地址d的拷贝>`。
3. **在Test函数中创建temp对象**：
    - `Date temp(d);` 在 `Test` 函数中创建 `temp` 对象，调用 `Date(const Date& d)` 使用传入的 `d` 进行拷贝构造。
    - 输出: `Date(const Date& d):<地址temp>`。
4. **返回temp对象**：
    - `return temp;` 返回`temp`对象，这会调用`temp`的拷贝构造函数，创建一个临时对象用于返回值。
    - 输出: `Date(const Date& d):<返回的临时对象地址>`。
5. **析构在Test函数中的对象**：
    - 在 `Test` 函数结束时，析构`temp`和`d`对象。
    - 输出: `~Date():<地址temp>`。
    - 输出: `~Date():<地址d>`。
6. **销毁返回的临时对象**：
    - 返回的临时对象在使用后被销毁。
    - 输出: `~Date():<返回的临时对象地址>`。
7. **销毁d1对象**：
    - 在 `main` 函数结束时，销毁 `d1` 对象。
    - 输出: `~Date():<地址d1>`。

![](https://cdn.nlark.com/yuque/0/2024/png/36162499/1720494076303-e1264e78-ac4f-4a1e-82e8-5481e35c83d9.png)

##### 传引用与传值的区别
###### 传引用(const A& a)
在拷贝构造函数中使用引用传参(通常是`const`引用)，表示函数接收到的参数是对象的引用，而不是对象的副本。这意味着我们不会创建新的对象副本，仅仅使用原对象的内存地址，避免了不必要的拷贝，节省了时间与内存空间。

传引用的优势有以下：

+ **避免了不必要的拷贝：拷贝大的对象时，按值传递需要额外的内存和处理时间，而按引用传递则不需要拷贝整个对象。**
+ **避免无穷递归：如果使用按值传递，调用拷贝构造函数时，会再度创建对象副本，导致递归调用。**

以下为传引用的拷贝构造函数：

```cpp
#include <iostream>

class A
{
public:
    A() 
    {
        std::cout << "构造函数" << std::endl;
    }

    // 拷贝构造函数 - 使用引用传递
    A(const A& a) 
    {
        std::cout << "拷贝构造函数 - 引用传递" << std::endl;
    }
};

int main()
{
    A obj1;            // 调用构造函数
    A obj2(obj1);      // 调用拷贝构造函数，使用引用传递
    
    return 0;
}
```

输出结果为：

```cpp
构造函数
拷贝构造函数 - 引用传递
```

###### 传值(const A a)
在拷贝构造函数中使用值传递(`const A a`)，表示函数接收到的参数是传入对象的副本，而不是引用。传值会导致C++必须创建一个新的临时对象作为参数的拷贝，但这个新对象会再次调用拷贝构造函数，从而引发无穷递归。

传值的劣势有以下：

+ **导致无穷递归：传值时需要创建副本，而这个副本需要再调用拷贝构造函数创建另一个副本，导致递归调用。**
+ **性能开销：创建副本需要额外的内存分配和时间，特别是处理大型对象时，效率很低。**

以下为传值的拷贝构造函数：

```cpp
#include <iostream>

class A
{
public:
    A()
    {
        std::cout << "构造函数" << std::endl;
    }

    // 拷贝构造函数 - 使用值传递
    A(const A a)
    {
        std::cout << "拷贝构造函数 - 值传递" << std::endl;
    }
};

int main() 
{
    A obj1;           // 调用构造函数
    A obj2(obj1);     // 递归调用，导致栈溢出
    
    return 0;
}
```

以上代码会导致栈溢出，因为在拷贝构造时，按值传递需要拷贝对象`a`，而拷贝对象`a`又会调用拷贝构造函数，陷入无限递归，直到内存耗尽。

#### 赋值运算符重载
##### 运算符重载
有时候想要比较同一个类的不同对象，此时是不能直接比较的。用户自定义的类型，没有设定比较规则，不能直接将对象进行比较。例如`Date`类的两个对象`d1`与`d2`是不能直接`d1 == d2`或`d1 > d2`等比较操作的。

C++为了增强代码的可读性引入了运算符重载，运算符重载是具有特殊函数名的函数，也具有其返回值类型，函数名以及参数列表，其返回值类型与参数列表与普通的函数类似。

函数名为关键字`operator`后接需重载的运算符符号。**函数原型：返回值类型 operator操作符(参数列表)：**

```cpp
#include <iostream>

using namespace std;

// 全局 operator==
class Date
{
public:
    Date(int year = 2024, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // private:
    int _year_;
    int _month_;
    int _day_;
};

// 这里会发现运算符重载成全局的就需要成员变量为公有的，那么问题来了？封装性如何保证？
// 这里其实可以用以后的友元解决，或重载成成员函数。
bool operator==(const Date& d1, const Date& d2)
{
    return d1._year_ == d2._year_
        && d1._month_ == d2._month_
        && d1._day_ == d2._day_;
}

int main()
{
    Date d1(2022, 1, 2);
    Date d2(2021, 3, 1);
    //d1 == d2编译成operator==(d1, d2)，本质上就是函数调用
    cout << (d1 == d2) << endl;  // output: 0

    return 0;
}
```

这里我们的运算符重载为全局，无法访问类中的私有成员变量，所以临时将私有成员变量设置为公有，但不符合实际应用，如果直接将此函数放进类中，成为成员函数呢？这样就可以访问私有变量：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 2022, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // ==运算符重载尝试
    bool operator==(const Date& d1, const Date& d2)
    {
        return d1._year_ == d2._year_
            && d1._month_ == d2._month_
            && d1._day_ == d2._day_;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};



int main()
{
    Date d1(2022, 1, 2);
    Date d2(2022, 1, 1);

    cout << (d1 == d2) << endl;

    return 0;
}
```

编译后会提示："error C2804: 二进制“operator ==”的参数太多"，我们想要比较这两个对象？为什么会提示参数太多呢？，这里包含隐藏参数`this`，所以最终为：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 2022, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // d1 == d2 编译成d1.operator==(&d1, d2)
    bool operator==(const Date& d) const // bool operator==(Date* this, const Date& d)
    {
        return _year_ == d._year_  // this->_year == ...
            && _month_ == d._month_
            && _day_ == d._day_;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(2022, 1, 1);
    Date d2(2022, 1, 5);

    cout << (d1 == d2) << endl;  // 实际上为d1.operator==(d2), this指针不允许显式传入

    return 0;
}
```

以上代码是将`==`运算符重载，目的在于比较两个`Date`对象是否相等，同理可以对`>`运算符进行重载，比较两个日期类对象谁大谁小：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 构造函数，带有默认参数
    Date(int year = 2022, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // 运算符重载，比较两个 Date 对象的大小
    // d1 > d2 会被编译成 d1.operator>(d2)
    bool operator>(const Date& d) const // 增加 const 修饰符
    {
        // 首先比较年份
        // 如果 d1 的年份大于 d2 的年份，返回 true
        // 否则，如果年份相等，继续比较月份
        // 如果 d1 的月份大于 d2 的月份，返回 true
        // 否则，如果月份相等，继续比较日期
        // 如果 d1 的日期大于 d2 的日期，返回 true
        // 如果以上条件都不满足，返回 false
        return (_year_ > d._year_) ||
            (_year_ == d._year_ && _month_ > d._month_) ||
            (_year_ == d._year_ && _month_ == d._month_ && _day_ > d._day_);
    }

private:
    int _year_;  // 年份
    int _month_; // 月份
    int _day_;   // 日期
};

int main()
{
    Date d1(2022, 1, 2); // 创建 Date 对象 d1，日期为 2022 年 1 月 2 日
    Date d2(2023, 1, 2); // 创建 Date 对象 d2，日期为 2023 年 1 月 2 日

    // 输出 d1 是否大于 d2，结果为 0(false)，因为 2022 年小于 2023 年
    cout << (d1 > d2) << endl;
    
    return 0;
}
```

:::color2
**赋值运算符如果不显式实现，编译器会生成一个默认的。此时用户再在类外自己实现一个全局的赋值运算符重载，就和编译器在类中生成的默认赋值运算符重载冲突了，故赋值运算符重载只能是类成员函数。**

:::

赋值运算符使用的注意事项：

+ **不能通过连接其他符号来创建新的操作符，例如**`**operator@**`**。**
+ **重载运算符必须有一个类类型参数。**
+ **用于内置类型的运算符，其含义不能改变，例如内置的整型，不能改变其含义。**
+ **作为类成员函数重载时，其形参看起来比操作数数目少1，因为成员函数的第一个参数为隐藏**`**this**`**。**
+ `**.* :: sizeof ? .**`**5个运算符不能重载。**

##### 赋值运算符重载
+ 赋值运算符重载格式
    - 参数类型：`const T&`，传递引用可以提高传参效率。
    - 返回值类型：`T&`，返回引用可以提高返回效率，有返回值目的是为了支持连续赋值。
    - 检测是否自己给自己赋值。
    - 返回`*this`：要符合连续赋值的含义。

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 构造函数，带有默认参数
    Date(int year = 2022, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // 拷贝构造函数，用于创建对象的副本
    Date(const Date& d)
    {
        _year_ = d._year_;
        _month_ = d._month_;
        _day_ = d._day_;
    }

    // 赋值运算符重载，用于将一个对象的值赋给另一个对象
    Date& operator=(const Date& d)
    {
        if (this != &d)  // 防止自己赋值给自己
        {
            _year_ = d._year_;
            _month_ = d._month_;
            _day_ = d._day_;
        }

        return *this;
    }

private:
    int _year_;  // 年份
    int _month_; // 月份
    int _day_;   // 日期
};

int main()
{
    Date d1;        // 使用默认构造函数创建对象 d1，日期为 2022 年 1 月 1 日
    Date d2(1, 1, 1); // 使用带参数的构造函数创建对象 d2，日期为 1 年 1 月 1 日

    d1 = d2;  // 将对象 d2 的值赋给对象 d1

    return 0;
}
```

+ 用户没有显式实现时，编译器会生成一个默认赋值运算符，以值的方式逐字节拷贝。

```cpp
#include <iostream>

using namespace std;

class Time
{
public:
    Time()
    {
        _hour_ = 1;
        _minute_ = 1;
        _second_ = 1;
    }

    Time& operator=(const Time& t)
    {
        if (this != &t)
        {
            _hour_ = t._hour_;
            _minute_ = t._minute_;
            _second_ = t._second_;
        }

        return *this;
    }

private:
    int _hour_;
    int _minute_;
    int _second_;
};

class Date
{
private:
    // 基本类型
    int _year_ = 2022;
    int _month_ = 1;
    int _day_ = 1;

    // 自定义类型
    Time _t_;
};

int main()
{
    Date d1;
    Date d2;
    d1 = d2;

    return 0;
}
```

既然编译器生成的默认赋值运算符重载函数已经可以完成字节序的值拷贝了，为什么还需要自己实现呢？请看以下例子：

```cpp
#include <iostream>
#include <cstdlib> // 包含 malloc 和 free 函数

using namespace std;

// 定义数据类型
typedef int DataType;

// 定义栈类
class Stack
{
public:
    // 构造函数，初始化栈的容量和大小
    Stack(size_t capacity = 10)
    {
        _array_ = (DataType*)malloc(capacity * sizeof(DataType)); // 分配内存
        if (nullptr == _array_) // 检查内存分配是否成功
        {
            perror("Malloc failed to apply for space!");
            return;
        }

        _size_ = 0; // 初始化栈的大小
        _capacity_ = capacity; // 初始化栈的容量
    }

    // 入栈操作
    void Push(const DataType& data)
    {
        // 未实现的容量检查
        // ChckCapacity();
        _array_[_size_] = data; // 将数据放入栈中
        _size_++; // 增加栈的大小
    }

    // 析构函数，释放内存
    ~Stack()
    {
        if (_array_)
        {
            free(_array_); // 释放分配的内存
            _array_ = nullptr; // 将指针置为空
            _capacity_ = 0; // 重置容量
            _size_ = 0; // 重置大小
        }
    }

private:
    DataType* _array_; // 存放栈元素的数组指针
    size_t _size_; // 栈的当前大小
    size_t _capacity_; // 栈的容量
};

int main()
{
    Stack s1;
    s1.Push(1);
    s1.Push(2);
    s1.Push(3);
    s1.Push(4);

    Stack s2;
    s2 = s1; // 赋值操作

    return 0;
}
```

![](https://cdn.nlark.com/yuque/0/2024/png/36162499/1720498232357-d03bc468-c686-44e2-8e2c-66eae74749cb.png)

##### 前置++和后置++重载
```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 2022, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // 前置++：返回+1后的结果
    // 注意：this指向的对象函数结束后不会销毁，故以引用方式返回提高效率
    Date& operator++()
    {
        _day_ += 1;
        return *this;
    }

    // 后置++
    // 前置++和后置++都是一元运算符，为了让前置++与后置++形成能正确重载
    // C++规定：后置++重载时多增加一个int类型的参数，但调用函数时该参数不用换地，编译器自动传递
    // 注意：后置++为先使用后+1，因此需要返回+1之前的旧值，故需在实现时需要先将this保存一份，然后给this+1
    // 而temp是临时对象，因此只能以值的方式返回，不能返回引用
    Date operator++(int)
    {
        Date temp(*this);  // 拷贝构造
        _day_ += 1;
        return temp;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1;
    Date d2(2022, 1, 13);
    d1 = d2++;  // d1: 2022, 1, 13  d2: 2022, 1, 14
    d1 = ++d2;  // d1: 2022, 1, 15  d2: 2022, 1, 15

    return 0;
}
```

前置`++`返回+1后的结果，后置`++`先使用后+1。前置`++`和后置`++`都是一元运算符，为了让前置`++`与后置`++`形成能正确重载，C++规定：**后置**`**++**`**重载时多增加一个**`**int**`**类型的参数，但调用函数时该参数不用传递，编译器自动传递**。后置`++`为先使用后+1，因此需要返回+1之前的旧值，故需在实现时需要先将`this`保存一份，然后给`this+1`。

#### 日期类实现
```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    int GetMonthDay(int year, int month)
    {
        // 一年中每月的天数
        static int monthDays[13] = { 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };

        // 2月闰年情况处理
        if (month == 2 && (year % 400 == 0 || (year % 4 == 0 && year % 100 != 0)))
            return 29;

        return monthDays[month];
    }

    // 构造函数
    Date(int year = 0, int month = 1, int day = 1)
    {
        if (year >= 0
            && month >= 1
            && month <= 12
            && day >= 1
            && day <= GetMonthDay(year, month))
        {
            _year_ = year;
            _month_ = month;
            _day_ = day;
        }

        else
        {
            cout << "非法日期" << endl;
        }

    }

    // 拷贝函数
    Date(const Date& d)
    {
        _year_ = d._year_;
        _month_ = d._month_;
        _day_ = d._day_;
    }

    // 运算符重载：小于，用于比较两个日期对象的大小
    // d1 < d2 Compile to d1.operator(&d1, d2)
    inline bool operator<(const Date& d) // bool d1.operator(Date* this, const Date& d)
    {
        if (_year_ < d._year_)
            return true;
        else if (_year_ == d._year_ && _month_ < d._month_)
            return true;
        else if (_year_ == d._year_ && _month_ == d._month_ && _day_ < d._day_)
            return true;

        return false;
    }

    // 运算符重载：等于，用于比较两个日期对象是否相等
    // d1 == d2 Compile to d1.operator(&d1, d2)
    inline bool operator==(const Date& d) // bool operator(Date* this, const Date& d)
    {
        return _year_ == d._year_
            && _month_ == d._month_
            && _day_ == d._day_;
    }

    // 运算符重载：小于等于，用于比较两个日期对象是否小于等于
    // d1 <= d2 Compile to d1.operator<=(&d1, d2)
    bool operator<=(const Date& d)  // bool operator<=(Date* this, const Date& d)
    {
        return *this < d || *this == d;  // 复用上面的d1 < d2 与 d1 == d2
    }

    // 运算符重载：大于，用于比较两个日期对象是否大于
    // d1 > d2 Compile to d1.operator>(&d1, d2)
    bool operator>(const Date& d)  // bool operator>(Date* this, const Date& d)
    {
        return !(*this <= d);
    }

    // 运算符重载：大于等于，用于比较两个日期对象是否大于等于
    // d1 >= d2 Compile to d1.operator(&d1, d2)
    bool operator>=(const Date& d)  // bool operator>=(Date* this, const Date& d)
    {
        return !(*this < d);
    }

    // 运算符重载：不等于，用于比较两个日期对象是否不等于
    // d1 != d2 Compile to d1.operator(&d1, d2)
    bool operator!=(const Date& d)
    {
        return !(*this == d);
    }

    // 运算符重载：日期 + 天数，用于将一个日期对象加上指定天数
    Date operator+(int day)
    {
        Date ret(*this); // 用当前对象构造一个新的日期对象
        ret._day_ += day;

        while (ret._day_ > GetMonthDay(ret._year_, ret._month_))
        {
            // 如果日期的天不合法，则进位月
            ret._day_ -= GetMonthDay(ret._year_, ret._month_);
            ret._month_++;

            // 进位月后，如果月不合法，则进位年
            if (ret._month_ == 13)
            {
                ret._year_++;
                ret._month_ = 1;
            }
        }

        return ret;
    }

    // 运算符重载：日期自加天数，用于将当前日期对象加上指定天数
    Date& operator+=(int day)
    {
        _day_ += day;

        // 调整日期使其合法
        while (_day_ > GetMonthDay(_year_, _month_))
        {
            _day_ -= GetMonthDay(_year_, _month_);
            ++_month_;

            // 月份进位
            if (_month_ == 13)
            {
                ++_year_;
                _month_ = 1;
            }
        }

        return *this;
    }

    // 运算符重载：日期自减天数，用于将当前日期对象减去指定天数
    Date& operator-=(int day)
    {
        _day_ -= day;

        // 调整日期使其合法
        while (_day_ <= 0)
        {
            --_month_;
            if (_month_ == 0)
            {
                --_year_;
                _month_ = 12;
            }

            _day_ += GetMonthDay(_year_, _month_);
        }

        return *this;
    }

    // 运算符重载：日期减天数，用于将一个日期对象减去指定天数
    Date operator-(int day)
    {
        Date ret(*this);  // 用当前对象构造一个新的日期对象
        ret -= day;  // 调用自减天数的运算符重载
        return ret;
    }

    // 运算符重载：前置递增，用于将当前日期对象加1天
    Date& operator++()
    {
        *this += 1;
        return *this;
    }

    // 运算符重载：前置递减，用于将当前日期对象减1天
    Date& operator--()
    {
        *this -= 1;
        return *this;
    }

    // 运算符重载：日期相减，用于计算两个日期对象的天数差
    //int operator-(const Date& d)
    //{
    //    // 简化版，只计算两个同年日期的天数差
    //    // 声明一个变量days用于存储天数差
    //    int days = 0;

    //    // 创建一个临时的Date对象temp，初始值为参数d的值
    //    Date temp(d);

    //    // 循环，增加temp的日期直到temp与当前日期对象相等
    //    while (temp < *this)
    //    {
    //        ++temp; // 前置递增temp的日期(即增加一天)
    //        ++days; // 对应增加天数
    //    }

    //    // 循环，减少temp的日期直到temp与当前日期对象相等
    //    while (*this < temp)
    //    {
    //        --temp; // 前置递减temp的日期(即减少一天)
    //        --days; // 对应减少天数
    //    }

    //    // 返回计算出的天数差
    //    return days;
    //}

    int operator-(const Date& d)
    {
        int flag = 1;  // 日期大小不同标志，一边输出正负天数
        Date maxDate = *this;  // 拷贝构造
        Date minDate = d;
        if (*this < d)
        {
            maxDate = d;  // 赋值运算符重载
            minDate = *this;
            flag = -1;
        }

        size_t ndays = 0;
        while (minDate != maxDate)
        {
            ++minDate;
            ++ndays;
        }

        return ndays * flag;
    }

    // 打印日期
    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1;
    d1.Print(); // 输出默认全缺省日期

    Date d2(2022, 14, 4);  // 非法日期
    d2.Print();

    // 日期比较
    cout << (d1 < d2) << endl;
    cout << (d1 > d2) << endl;
    cout << (d1 == d2) << endl;
    cout << (d1 != d2) << endl;
    cout << (d1 <= d2) << endl;
    cout << (d1 >= d2) << endl;

    // 日期加天数
    Date d3(1, 1, 1);
    Date d4 = d3 + 1000;
    d4.Print();  // 输出增加1000天后的日期 3-9-28

    // 日期自减天数
    Date d5(2022, 1, 30);
    d5 -= 35;
    d5.Print();  // 输出减去35天后的日期

    // 前置递增
    Date d6(2024, 1, 1);
    ++d6;
    d6.Print();  // 输出递增一天后的日期

    // 前置递减
    Date d7(2025, 1, 1);
    --d7;
    d7.Print();  // 输出递减一天后的日期

    // 两日期相减
    Date d8(2025, 7, 8);
    Date d9(2025, 12, 31);
    cout << "d9 - d8: " << (d9 - d8) << "days" << endl;  // 输出两个日期之间的天数差

    return 0;
}
```

在实际的项目中，完整类的实现一般是声明和定义分离的，例如这里可分离为`Date.h`、`Date.cpp`、`main.cpp`：

```cpp
#ifndef DATE_H
#define DATE_H

#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 0, int month = 1, int day = 1);  // 构造函数
    Date(const Date& d);  // 拷贝函数

    // 运算符重载：比较日期对象
    bool operator<(const Date& d) const;
    bool operator==(const Date& d) const;
    bool operator<=(const Date& d) const;
    bool operator>(const Date& d) const;
    bool operator>=(const Date& d) const;
    bool operator!=(const Date& d) const;

    // 运算符重载：日期 + 天数
    Date operator+(int day) const;
    Date& operator+=(int day);
    Date& operator-=(int day);
    Date operator-(int day) const;

    // 运算符重载：前置递增/递减
    Date& operator++();
    Date& operator--();

    // 运算符重载：日期相减
    int operator-(const Date& d) const;

    // 打印日期
    void Print() const;

private:
    int GetMonthDay(int year, int month) const;

    int _year_;
    int _month_;
    int _day_;
};

#endif
```

```cpp
#include "Date.h"

int Date::GetMonthDay(int year, int month) const
{
    // 一年中每月的天数
    static int monthDays[13] = { 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };

    // 2月闰年情况处理
    if (month == 2 && (year % 400 == 0 || (year % 4 == 0 && year % 100 != 0)))
        return 29;

    return monthDays[month];
}

// 构造函数
Date::Date(int year, int month, int day)
{
    if (year >= 0
        && month >= 1
        && month <= 12
        && day >= 1
        && day <= GetMonthDay(year, month))
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }
    else
    {
        cout << "非法日期" << endl;
    }
}

// 拷贝函数
Date::Date(const Date& d)
{
    _year_ = d._year_;
    _month_ = d._month_;
    _day_ = d._day_;
}

// 运算符重载：小于，用于比较两个日期对象的大小
bool Date::operator<(const Date& d) const
{
    if (_year_ < d._year_)
        return true;
    else if (_year_ == d._year_ && _month_ < d._month_)
        return true;
    else if (_year_ == d._year_ && _month_ == d._month_ && _day_ < d._day_)
        return true;

    return false;
}

// 运算符重载：等于，用于比较两个日期对象是否相等
bool Date::operator==(const Date& d) const
{
    return _year_ == d._year_
        && _month_ == d._month_
        && _day_ == d._day_;
}

// 运算符重载：小于等于，用于比较两个日期对象是否小于等于
bool Date::operator<=(const Date& d) const
{
    return *this < d || *this == d;  // 复用上面的d1 < d2 与 d1 == d2
}

// 运算符重载：大于，用于比较两个日期对象是否大于
bool Date::operator>(const Date& d) const
{
    return !(*this <= d);
}

// 运算符重载：大于等于，用于比较两个日期对象是否大于等于
bool Date::operator>=(const Date& d) const
{
    return !(*this < d);
}

// 运算符重载：不等于，用于比较两个日期对象是否不等于
bool Date::operator!=(const Date& d) const
{
    return !(*this == d);
}

// 运算符重载：日期 + 天数，用于将一个日期对象加上指定天数
Date Date::operator+(int day) const
{
    Date ret(*this); // 用当前对象构造一个新的日期对象
    ret._day_ += day;

    while (ret._day_ > GetMonthDay(ret._year_, ret._month_))
    {
        // 如果日期的天不合法，则进位月
        ret._day_ -= GetMonthDay(ret._year_, ret._month_);
        ret._month_++;

        // 进位月后，如果月不合法，则进位年
        if (ret._month_ == 13)
        {
            ret._year_++;
            ret._month_ = 1;
        }
    }

    return ret;
}

// 运算符重载：日期自加天数，用于将当前日期对象加上指定天数
Date& Date::operator+=(int day)
{
    _day_ += day;

    // 调整日期使其合法
    while (_day_ > GetMonthDay(_year_, _month_))
    {
        _day_ -= GetMonthDay(_year_, _month_);
        ++_month_;

        // 月份进位
        if (_month_ == 13)
        {
            ++_year_;
            _month_ = 1;
        }
    }

    return *this;
}

// 运算符重载：日期自减天数，用于将当前日期对象减去指定天数
Date& Date::operator-=(int day)
{
    _day_ -= day;

    // 调整日期使其合法
    while (_day_ <= 0)
    {
        --_month_;
        if (_month_ == 0)
        {
            --_year_;
            _month_ = 12;
        }

        _day_ += GetMonthDay(_year_, _month_);
    }

    return *this;
}

// 运算符重载：日期减天数，用于将一个日期对象减去指定天数
Date Date::operator-(int day) const
{
    Date ret(*this);  // 用当前对象构造一个新的日期对象
    ret -= day;  // 调用自减天数的运算符重载
    return ret;
}

// 运算符重载：前置递增，用于将当前日期对象加1天
Date& Date::operator++()
{
    *this += 1;
    return *this;
}

// 运算符重载：前置递减，用于将当前日期对象减1天
Date& Date::operator--()
{
    *this -= 1;
    return *this;
}

// 运算符重载：日期相减，用于计算两个日期对象的天数差
int Date::operator-(const Date& d) const
{
    int flag = 1;  // 日期大小不同标志，一边输出正负天数
    Date maxDate = *this;  // 拷贝构造
    Date minDate = d;
    if (*this < d)
    {
        maxDate = d;  // 赋值运算符重载
        minDate = *this;
        flag = -1;
    }

    size_t ndays = 0;
    while (minDate != maxDate)
    {
        ++minDate;
        ++ndays;
    }

    return ndays * flag;
}

// 打印日期
void Date::Print() const
{
    cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
}
```

```cpp
#include "Date.h"

int main()
{
    Date d1;
    d1.Print(); // 输出默认全缺省日期

    Date d2(2022, 14, 4);  // 非法日期
    d2.Print();

    // 日期比较
    cout << (d1 < d2) << endl;
    cout << (d1 > d2) << endl;
    cout << (d1 == d2) << endl;
    cout << (d1 != d2) << endl;
    cout << (d1 <= d2) << endl;
    cout << (d1 >= d2) << endl;

    // 日期加天数
    Date d3(1, 1, 1);
    Date d4 = d3 + 1000;
    d4.Print();  // 输出增加1000天后的日期 3-9-28

    // 日期自减天数
    Date d5(2022, 1, 30);
    d5 -= 35;
    d5.Print();  // 输出减去35天后的日期

    // 前置递增
    Date d6(2024, 1, 1);
    ++d6;
    d6.Print();  // 输出递增一天后的日期

    // 前置递减
    Date d7(2025, 1, 1);
    --d7;
    d7.Print();  // 输出递减一天后的日期

    // 两日期相减
    Date d8(2025, 7, 8);
    Date d9(2025, 12, 31);
    cout << "d9 - d8: " << (d9 - d8) << "days" << endl;  // 输出两个日期之间的天数差

    return 0;
}
```

可以发现在`Date.h`头文件中的成员函数声明大多数都用了`const`修饰，少部分未使用`const`修饰：

+ **函数后面的**`**const**`**关键字**：这表示该成员函数是一个**常量成员函数**，即它不能修改类的任何成员变量。这种修饰符一般用于那些不会改变对象状态的函数，比如访问器函数和用于比较的函数。例如：
    - 比较运算符，如`operator<`、`operator==`等和打印函数`Print`都被声明为`const`，因为这些函数只读取对象的成员变量，不会修改它们。
    - 日期运算符，如`operator+`、`operator-`等也被声明为`const`，因为它们返回的是一个新的日期对象，不会修改当前对象。
+ **没有**`**const**`**修饰的函数**：这些函数可以修改对象的状态。例如：
    - 前置递增/递减运算符`operator++`和`operator--`会修改对象的日期值，所以不能是`const`。
    - 自加/自减运算符`operator+=`和`operator-=`也会修改对象的日期值，因此不能是`const`。
    - 日期相减运算符`operator-`需要访问和修改对象的状态来计算日期差异，所以不能是`const`。

:::color2
**结论：只要成员函数中不需要修改成员变量，都应该被声明为**`**const**`**。**

:::

#### const成员 
我们知道拷贝构造函数要传引用，如果里面内容不改变，尽量用`const`修饰：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 0, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    Date(const Date& d)
    {
        _year_ = d._year_;
        _month_ = d._month_;
        _day_ = d._day_;
    }

    void Print()
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

void f(const Date& d) // C2662	“void Date::Print(void)”: 不能将“this”指针从“const Date”转换为“Date &”
{
    d.Print();
}

int main()
{
    Date d1(2022, 1, 1);
    f(d1);

    return 0;
}
```

上述代码编译失败，原因是对象`d`不能调用成员函数`Print`，为什么呢？原因是`Print`函数不是`const`成员函数，因此它不能被`const`对象调用。具体来说，当在`f`函数中使用`const Date& d`时，`d`被视为一个常量引用，而常量引用只能调用`const`成员函数。需要将`Print`函数声明为`const`成员函数。这样可以保证`Print`函数在被调用时不会修改对象的状态。换种理解方式为：`f`函数原型为：`void f(cont Date& d)`，调用`d.Print()`实际上会被编译成`d.Print(&d)`，因为形参为`const`修饰，所以编译成`d.Print(const Date*)`，然而实际的成员函数为`void Print()`，因为隐藏了`this`指针，实际会被编译成`void Print(Date* this)`，所以这里形参为`Date* this`，调用成员函数传入的实参为`const Date*`，权限放大，导致编译失败，所以需要在成员函数的形参中添加`const`修饰，例如`const Date* this`，但是`this`指针是隐含的，无法显式添加`const`修饰。可以通过在函数声明和定义的末尾加上`const`关键字来实现这一点：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 构造函数，带有默认参数，默认日期为 0 年 1 月 1 日
    Date(int year = 0, int month = 1, int day = 1)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    // 拷贝构造函数，用于创建对象的副本
    Date(const Date& d)
    {
        _year_ = d._year_;
        _month_ = d._month_;
        _day_ = d._day_;
    }

    // 成员函数 Print，带有 const 关键字，表示该函数不会修改对象的成员变量
    void Print() const
    {
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;  // 年份
    int _month_; // 月份
    int _day_;   // 日期
};

// 函数 f，接受一个 const Date& 类型的参数，表示不能修改该对象
void f(const Date& d)
{
    d.Print();  // 调用 Date 类的 Print 成员函数，由于 Print 是 const 成员函数，可以在 const 对象上调用
}

int main()
{
    Date d1(2022, 1, 1);  // 创建 Date 对象 d1，日期为 2022 年 1 月 1 日
    f(d1);  // 调用函数 f，将 d1 作为参数传递

    return 0;
}
```

:::color2
**将**`**const**`**修饰的成员函数称之为**`**const**`**成员函数，实际修饰该成员函数隐含的**`**this**`**指针，即**`***this**`**。它表示该成员函数是一个常量成员函数，意思是该函数不会修改类的任何成员变量，也就是说， 在这个函数内部不能修改类的成员变量(成员变量是成员对象的一部分，对象是常量，成员变量亦不能更改)， 且只能调用其他的**`**const**`**成员函数：**

:::

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 0, int month = 1, int day = 1)
        : _year_(year), _month_(month), _day_(day) {}

    void Print() const  // const 成员函数
    {
        // 不能修改成员变量
        // _year_ = 2024; // 错误: 不能在 const 成员函数中修改成员变量
        cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

    void SetDate(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

    int GetYear() const  // const 成员函数
    {
        return _year_;  // 能访问成员变量
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

void PrintDate(const Date& d)
{
    d.Print();  // 可以调用 const 成员函数
    // d.SetDate(2024, 7, 13); // 错误: 不能调用非 const 成员函数
}

int main()
{
    const Date d1(2022, 1, 1); // d1 是一个常量对象
    d1.Print(); // 可以调用 Print，因为它是一个 const 成员函数

    // d1.SetDate(2023, 1, 1); // 错误: 不能调用非 const 成员函数

    Date d2(2023, 7, 13); // d2 是一个非常量对象
    d2.Print(); // 可以调用 Print，因为 d2 不是 const
    d2.SetDate(2024, 7, 13); // 可以调用 SetDate，因为 d2 不是 const

    PrintDate(d1); // 调用一个接收 const Date& 参数的函数
    PrintDate(d2); // 调用一个接收 const Date& 参数的函数

    return 0;
}
```

:::color2
**请思考以下问题：**

+ `**const**`**对象可以调用非**`**const**`**成员函数吗？不能。**`**const**`**对象只能调用**`**const**`**成员函数。因为**`**const**`**对象被保证不会修改其状态，而非**`**const**`**成员函数可能会修改对象的状态，所以编译器不允许**`**const**`**对象调用非**`**const**`**成员函数。  **
+ **非**`**const**`**对象可以调用**`**const**`**成员函数吗？ 可以。**`**const**`**成员函数不会修改对象的状态，所以非**`**const**`**对象可以安全地调用**`**const**`**成员函数。  **
+ `**const**`**成员函数内可以调用其他的非**`**const**`**成员函数吗？ 不能。**`**const**`**成员函数被保证不会修改对象的状态，而非**`**const**`**成员函数可能会修改对象的状态，所以在**`**const**`**成员函数中调用非**`**const**`**成员函数会违反这个保证，编译器会禁止这种操作。  **
+ **非**`**const**`**成员函数内可以调用其他的**`**const**`**成员函数吗？ 可以。非**`**const**`**成员函数可以调用**`**const**`**成员函数，因为**`**const**`**成员函数不会修改对象的状态，所以调用它是安全的。  **

**总结：权限不能放大，可以相同或缩小！**

:::

:::color2
**在C++中，**`**const**`**关键字可以用在很多地方，不同地方的含义有所不同，例如**`**const Date(const Date& d) const**`**，三个位置的作用分别是：**

+ **形参的**`**const**`**修饰符：用于修饰函数参数，表示该参数在函数内部不能被修改。这在传递对象或引用时尤为重要，防止意外修改参数内容。**
+ **成员函数后的**`**const**`**修饰符：用于修饰成员函数，表示该成员函数不会修改对象的状态(即成员变量)。**
+ **返回类型的**`**const**`**修饰符：用于修饰返回类型，表示返回的值是常量，不能被修改。**

:::

例如有以下例子：

```cpp
#include <iostream>

class Point
{
public:
    Point(int x = 0, int y = 0) : _x_(x), _y_(y) {}  // 构造函数
    Point(const Point& p);  // 拷贝构造函数

    // 访问器函数
    int getX() const;  // 成员函数后的 const
    int getY() const;

    // 修改器函数
    void setX(int x);
    void setY(int y);

    // 运算符重载
    bool operator==(const Point& p) const;  // 参数的 const 和成员函数后的 const

    // 打印点坐标
    void print() const;

private:
    int _x_, _y_;
};

// 拷贝构造函数
Point::Point(const Point& p) : _x_(p._x_), _y_(p._y_) {}

// 访问器函数实现
int Point::getX() const { return _x_; }
int Point::getY() const { return _y_; }

// 修改器函数实现
void Point::setX(int x) { _x_ = x; }
void Point::setY(int y) { _y_ = y; }

// 运算符重载实现
bool Point::operator==(const Point& p) const
{
    return _x_ == p._x_ && _y_ == p._y_;
}

// 打印点坐标
void Point::print() const
{
    std::cout << "(" << _x_ << ", " << _y_ << ")" << std::endl;
}

int main()
{
    Point p1(1, 2);
    Point p2(p1);  // 拷贝构造函数
    p2.setX(3);    // 修改 p2 的 x 坐标

    p1.print();    // 输出: (1, 2)
    p2.print();    // 输出: (3, 2)

    if (p1 == p2)
    {
        std::cout << "p1 is equal to p2" << std::endl;
    }
    else
    {
        std::cout << "p1 is not equal to p2" << std::endl;  // 这一行会被输出
    }

    return 0;
}
```

#### 取地址及const取地址操作符重载
这两个默认成员函数一般不用重新定义，编译器会默认生成：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year = 0, int month = 1, int day = 1)
        : _year_(year), _month_(month), _day_(day) {}

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d;

    cout << &d << endl;  // output d1 address

    return 0;
}
```

`&`操作符重载编译器会默认生成，如需显式重载，则如以下：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    // 构造函数，使用初始化列表来初始化成员变量
    Date(int year = 0, int month = 1, int day = 1)
        : _year_(year), _month_(month), _day_(day) {}

    // 重载取地址运算符，返回指向当前对象的指针
    Date* operator&()
    {
        return this;
    }

    // 重载取地址运算符，返回指向当前对象的 const 指针
    // 如果不返回 const 类型，则返回 Date* 指针，而 const 成员函数中的 this 指针实际上是 const Date*
    const Date* operator&() const  // 函数重载
    {
        return this;
    }

private:
    int _year_;  // 年份
    int _month_; // 月份
    int _day_;   // 日期
};

int main()
{
    Date d;

    cout << &d << endl;  // 输出 d 的地址

    return 0;
}
```

只有特殊情况才需要重载，比如不想让别人获取地址：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
public:
    Date(int year = 0, int month = 1, int day = 1)
        :_year_(year), _month_(month), _day_(day) {}

    Date* operator&()
    {
        return nullptr;
    }

    const Date* operator&() const  // 函数重载
    {
        return nullptr;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1;

    cout << &d1 << endl;  // output 00000000

    return 0;
}
```

### 类和对象(下)
#### 再谈构造函数
##### 构造函数体赋值
在创建对象时，编译器通过调用构造函数，给对象中各个成员变量一个合适的初始值：

```cpp
class Date
{
public:
    Date(int year, int month, int day)
    {
        _year_ = year;
        _month_ = month;
        _day_ = day;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};
```

虽然上述构造函数调用之后，对象中已经有了一个初始值，但是不能将其称为对对象成员变量的初始化，**构造函数体中的语句只能将其称为赋初值**，而不能称作初始化。因为**初始化只能初始化一次，而构造函数体内可以多次赋值。**

##### 初始化列表
**初始化列表即以一个冒号开始，接着是一个以逗号分隔的数据成员列表，每个成员变量后面跟一个放在括号中的初始值或表达式：**

```cpp
class Date
{
public:
    Date(int year, int month, int day)
        : _year_(year), _month_(month), _day_(day)
    {}

private:
    int _year_;
    int _month_;
    int _day_;
};
```

初始化列表需要注意以下几点：

+ **每个成员变量在初始化列表中只能出现一次(初始化只能初始化一次)。**
+ 类中包含以下成员，必须放在初始化列表位置进行初始化：
    - **引用成员变量。**
    - `**const**`**成员变量。**
    - **自定义类型成员且该类没有默认构造函数。**

```cpp
#include <iostream>

using namespace std;

// 定义类 A
class A
{
public:
    // 构造函数，使用初始化列表初始化 _a_
    A(int a)
        : _a_(a) {}

private:
    int _a_;  // 私有成员变量
};

// 定义类 B
class B
{
public:
    // 构造函数，使用初始化列表初始化成员变量
    B(int a, int ref)
        : _aobj_(a),  // 初始化 _aobj_，需要传递参数给 A 的构造函数
        _ref_(ref),   // 初始化引用成员变量 _ref_
        _n_(10)       // 初始化 const 成员变量 _n_
    {}

private:
    // 成员变量的声明
    A _aobj_;       // 类 A 的对象，没有默认构造函数
    int& _ref_;     // 引用成员变量
    const int _n_;  // const 成员变量
    int _x_;        // 普通成员变量，无需初始化列表初始化
};

int main()
{
    int value = 2;
    B b(1, value);  // 创建 B 类对象，传递参数给构造函数

    return 0;
}
```

+ 尽量使用初始化列表初始化，因为不管你是否使用初始化列表，对于自定义类型成员变量，一定会先使用初始化列表初始化。

```cpp
#include <iostream>

using namespace std;

class Time
{
public:
    Time(int hour = 0)
        : _hour_(hour)
    {
        cout << "Time" << endl;
    }

private:
    int _hour_;
};

class Date
{
public:
    Date(int day) {}

private:
    int _day_;
    Time _t_;
};

int main()
{
    Date d(1);  // output: Time

    return 0;
}
```

+  **成员变量的初始化顺序与它们在类中声明的顺序一致，而不是在初始化列表中的顺序。  **

```cpp
#include <iostream>

using namespace std;

class A
{
public:
    A(int a)
        : _a1_(a), _a2_(_a1_)
    {
        cout << _a1_ << " " << _a2_ << endl;
    }

private:
    int _a2_;
    int _a1_;
};

int main()
{
    A aa(1);  // 程序能否正常编译？若通过编译，程序运行结果是什么？

    return 0;
}
```

解释： 在C++中，成员变量的初始化顺序与它们在类中声明的顺序一致，而不是在初始化列表中的顺序。 类`A`中，成员变量的声明顺序是`_a2_`在前，`_a1_`在后。因此，它们的初始化顺序也是先初始化`_a2_`，然后再初始化`_a1_`。这意味着在初始化列表中使用`_a1_`初始化`_a2_`时，`_a1_`的值还未被初始化，导致未定义行为。

##### explicit关键字
先看以下代码：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year)
        : _year_(year)
    {
        cout << "Date(int year): " << _year_ << endl;
    }

    Date(const Date& d)
    {
        cout << "Date(const Date& d)" << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(1);    // 构造函数
    Date d2 = 2;   // 隐式类型转换，先构造出临时tmp(2)，再用tmp拷贝构造d2(tmp)，最后优化构造
    // const Date& d2 = 2; 不优化，引用就是中间产生的临时对象
    Date d3 = d1;  // 拷贝构造

    return 0;
}
```

上述代码中`Date d2 = 2`会产生隐式类型转换，这条语句中，`2`是一个 `int` 类型的值，但是目标类型是`Date`类。为了实现这个初始化，C++会进行隐式类型转换。这种类型转换会调用`Date` 类中可以接受一个`int` 参数的构造函数。转换过程如下：

+ 临时对象创建
    - `Date d2 = 2`首先会使用`Date(int year)`构造函数来创建一个临时的`Date`对象。这个临时对象的`_year_`成员变量被初始化为`2`。
    - 在这个过程中，构造函数`Date(int year)`会被调用，并输出`"Date(int year): 2"`。
+ 临时对象赋值给`d2`
    - 然后，编译器会使用这个临时对象来初始化`d2`。这通常会涉及拷贝构造函数`Date(const Date& d)`，即使在某些情况下，这个步骤可能会被优化掉(如在现代C++中的"返回值优化"或"拷贝省略")。
    - 在这种情况下，编译器会调用`Date(const Date& d)`拷贝构造函数来创建`d2`。拷贝构造函数会被调用，并输出`"Date(const Date& d)"`。

如果不希望类的构造函数进行隐式类型转换，可以将构造函数声明为`explicit`， 在C++中，使用`explicit`关键字可以防止隐式类型转换和隐式复制初始化：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    explicit Date(int year)
        : _year_(year)
    {
        cout << "Date(int year): " << _year_ << endl;
    }

    Date(const Date& d)
    {
        cout << "Date(const Date& d)" << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(1);    // 构造函数
    // Date d2 = 2;   // 错误：explicit构造函数阻止隐式转换
    Date d2(2);    // 正确：必须显式调用构造函数
    Date d3 = d1;  // 拷贝构造

    return 0;
}
```

以上做法为C++98针对单参数的做法，但是如果有多个参数呢：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    explicit Date(int year)
        : _year_(year)
    {
        cout << "Date(int year): " << _year_ << endl;
    }

    Date(const Date& d)
    {
        cout << "Date(const Date& d)" << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(1, 2, 3);
    Date d2 = (1, 2, 3);

    return 0;
}
```

以上如果有多个参数`Date d2 = (1, 2, 3)`则无法编译， 在C++11及更高版本中，可以使用**列表初始化来初始化对象**。列表初始化也可以触发隐式类型转换。如果不希望发生这种隐式类型转换，可以将构造函数声明为`explicit`。 

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    explicit Date(int year, int month, int day)
        : _year_(year), _month_(month), _day_(day)
    {
        cout << "Date(int year, int month, int day): " << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

    Date(const Date& d)
        : _year_(d._year_), _month_(d._month_), _day_(d._day_)
    {
        cout << "Date(const Date& d)" << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};

int main()
{
    Date d1(1, 2, 3);     // 直接调用构造函数，合法
    // Date d3 = {1, 2, 3};  // 错误：explicit构造函数阻止隐式转换
    Date d3{ 1, 2, 3 };     // 正确：显式调用构造函数
    Date d4 = d1;         // 拷贝构造

    return 0;
}
```

 对于列表初始化`{1, 2, 3}`，编译器会尝试找到一个匹配的构造函数，并使用该构造函数初始化对象。这与直接调用构造函数相似，也会触发隐式类型转换。  

#### static成员
##### 概念
**声明为**`**static**`**的类成员称为类的静态成员，用**`**static**`**修饰的成员变量，称之为静态成员变量；用**`**static**`**修饰的成员函数，称之为静态成员函数。静态成员变量一定要在类外进行初始化。**

**面试题：实现一个类，计算程序中创建出了多少个类对象。**

```cpp
#include <iostream>

using namespace std;

class A
{
public:
    A() { ++_scount_; };  // 构造函数，每创建一个对象，静态变量_scount_加1
    A(const A& a) { ++_scount_; };  //拷贝构造函数，每拷贝一个对象，静态变量_scount_加1
    ~A() { --_scount_; };  // 析构函数，每销毁一个对象，静态变量_scount_减1
    static int GetACount() { return _scount_; };  // 静态成员函数，返回当前静态变量_scount_的值

private:
    static int _scount_;  // 声明静态成员变量
};

int A::_scount_ = 0;  // 初始化静态成员变量

int main()
{
    cout << A::GetACount() << endl;  // 输出最开始对象计数，初始值为0
    A a1, a2;  // 创建两个对象，计数变为2
    A a3(a1);  // 拷贝构造一个对象，计数为3
    cout << A::GetACount() << endl;  // 输出当前对象计数，应为3

    return 0;
}
```

##### 特性
+ **静态成员为所有类对象所共享，不属于某个具体的对象，存放在静态区。**
+ **静态成员变量必须在类外定义，定义时不添加**`**static**`**关键字，类中只是声明。**
+ **类静态成员即可用**`**类名::静态成员**`**或者**`**对象.静态成员**`**来访问。**
+ **静态成员函数没有隐藏的**`**this**`**指针，不能访问任何非静态成员。**
+ 静态成员也是类的成员，受`public`、`protected`、`private`访问限定符限制。

问题：

1. 静态成员函数可以调用非静态成员函数吗？
2. 非静态成员函数可以调用类的静态成员函数吗？

解答：

1.  **静态成员函数不能直接调用非静态成员函数。**这是因为静态成员函数不与任何特定的对象实例关联，而非静态成员函数需要通过对象实例来调用。非静态成员函数通常依赖于对象的状态(即成员变量)，而静态成员函数没有这种关联。如果确实需要在静态成员函数中调用非静态成员函数，可以通过传递对象实例来实现：

```cpp
#include <iostream>

using namespace std;

class A
{
public:
    // 默认构造函数，每创建一个实例，计数器加1
    A() { ++_scount_; };

    // 拷贝构造函数，每创建一个实例，计数器加1
    A(const A& a) { ++_scount_; };

    // 析构函数，每销毁一个实例，计数器减1
    ~A() { --_scount_; };

    // 非静态成员函数
    void NonStaticFunction() const
    {
        cout << "Non-static member function called." << endl;
    }

    // 静态成员函数，可以通过对象实例调用非静态成员函数
    static void StaticFunction(A& a)
    {
        a.NonStaticFunction(); // 通过对象实例调用非静态成员函数
    }

    // 获取当前类实例的数量
    static int GetACount() { return _scount_; }

private:
    // 静态成员变量，用于统计类的实例数量
    static int _scount_;
};

// 初始化静态成员变量
int A::_scount_ = 0;

int main()
{
    A a1; // 创建一个实例，调用默认构造函数
    A::StaticFunction(a1);  // 通过静态成员函数调用非静态成员函数
    cout << A::GetACount() << endl; // 输出当前类实例的数量

    return 0;
}
```

2. ** 非静态成员函数可以调用类的静态成员函数。**由于静态成员函数与类相关联，而不是与特定对象实例相关联，因此可以在任何对象实例中直接调用静态成员函数。  

```cpp
#include <iostream>

using namespace std;

class A
{
public:
    // 默认构造函数，每创建一个实例，计数器加1
    A() { ++_scount_; }

    // 拷贝构造函数，每创建一个实例，计数器加1
    A(const A& a) { ++_scount_; }

    // 析构函数，每销毁一个实例，计数器减1
    ~A() { --_scount_; }

    // 非静态成员函数
    void NonStaticFunction() const
    {
        cout << "Non-static member function called." << endl;
        PrintACount();  // 调用静态成员函数
    }

    // 静态成员函数，用于打印当前实例数量
    static void PrintACount()
    {
        cout << "Current count: " << _scount_ << endl;
    }

    // 静态成员函数，用于获取当前实例数量
    static int GetACount() { return _scount_; }

private:
    // 静态成员变量，用于统计类的实例数量
    static int _scount_;
};

// 初始化静态成员变量
int A::_scount_ = 0;

int main()
{
    A a1;  // 创建一个实例，调用默认构造函数
    a1.NonStaticFunction();  // 调用非静态成员函数，它会进一步调用静态成员函数
    cout << A::GetACount() << endl;  // 输出当前类实例的数量

    return 0;
}
```

题目：求1+2+...+n，要求不能使用乘除法、循环、条件、递归。

```cpp
#include <iostream>
#include <vector>

using namespace std;

// 定义一个类 Sum，用于计算从1到给定数字的连续整数之和
class Sum
{
public:
    // 构造函数：每创建一个 Sum 对象，_i_ 的值加到 _sum_，并将 _i_ 增加1
    Sum()
    {
        _sum_ += _i_;
        ++_i_;
    }

    // 静态成员函数：返回当前的总和 _sum_
    static int GetSum()
    {
        return _sum_;
    }

private:
    // 静态成员变量：用于跟踪当前整数
    static int _i_;
    // 静态成员变量：用于存储累加和
    static int _sum_;
};

// 初始化静态成员变量
int Sum::_i_ = 1;
int Sum::_sum_ = 0;

// 定义一个解决方案类，用于封装计算逻辑
class Solution
{
public:
    // 成员函数：创建 n 个 Sum 对象，并返回累加和
    int SumSolution(int n)
    {
        // Sum a[n];  // 变长数组，看编译器支持
        vector<Sum> a(n); // 使用 vector 动态创建 n 个 Sum 对象
        return Sum::GetSum(); // 返回累加和
    }
};

int main()
{
    Solution sol; // 创建 Solution 类的对象
    int n;

    cout << "Enter a number: ";
    cin >> n; // 读取用户输入的数字

    // 输出从 1 到 n 的整数之和
    cout << "The sum of first " << n << " numbers is: " << sol.SumSolution(n) << endl;

    return 0;
}
```

#### 友元
 在C++中，友元函数是一种特殊的函数，可以访问类的私有和受保护成员。友元函数不是类的成员函数，但因为它被类声明为友元，所以它能够直接访问该类的私有和受保护成员。  

友元分为：**友元函数和友元类。**

##### 友元函数
友元函数在类中声明，在类外定义。请看以下示例：

```cpp
#include <iostream>

using namespace std;

// 定义一个类 Box
class Box
{
public:
    // 构造函数：初始化 Box 对象，并将 width 的值赋给私有成员 _width_
    Box(double width)
        : _width_(width)
    {}

    // 声明友元函数 PrintWidth，可以访问 Box 类的私有成员
    friend void PrintWidth(Box& b);

private:
    // 私有成员变量：存储盒子的宽度
    double _width_;
};

// 友元函数定义：PrintWidth 可以访问 Box 的私有成员 _width_
void PrintWidth(Box& b)
{
    // 访问并输出 Box 对象的私有成员 _width_
    cout << "Width of box: " << b._width_ << endl;
}

int main()
{
    // 创建一个 Box 对象，宽度初始化为 10.11
    Box box(10.11);

    // 调用友元函数 PrintWidth，传递 box 对象
    PrintWidth(box);

    return 0;
}
```

现在尝试重载`operator<<`，可以发现没办法将`operator<<`重载为成员函数。因为`cout`的输出流对象和隐含的`this`指针在抢占第一个参数的位置。`this`指针默认是第一个参数也就是左操作数了。但是实际使用中`cout`需要是第一个形参对象，才能使用。所以要将`operator<<`重载成全局函数。但又会导致类外没办法访问成员，此时就需要友元解决：

```cpp
#include <iostream>

using namespace std;

class Date
{
public:
    Date(int year, int month, int day)
        : _year_(year), _month_(month), _day_(day)
    {}

    // d1 << cout -> d1.operator<<(&d1, cout) 不符合常规调用
    // 因为成员函数第一个参数一定是隐藏的this，所以d1必须放在<<左侧
    ostream operator<<(ostream& _cout)
    {
        _cout << _year_ << "-" << _month_ << "-" << _day_ << endl;
    }

private:
    int _year_;
    int _month_;
    int _day_;
};
```

友元函数可以直接访问类的私有成员，它是定义在类外部的普通函数，不属于任何类，但需要在类的内部声明，声明时需要加`friend`关键字：

```cpp
#include <iostream>  

using namespace std;

class Date
{
    // 声明友元函数，使其能够访问私有成员变量
    friend ostream& operator<<(ostream& _cout, const Date& d);
    friend istream& operator>>(istream& _cin, Date& d);

public:
    // 构造函数，默认日期为1900年1月1日
    Date(int year = 1900, int month = 1, int day = 1)
        : _year_(year)
        , _month_(month)
        , _day_(day)
    {}

private:
    int _year_;   // 年
    int _month_;  // 月
    int _day_;    // 日
};

// 重载输出运算符，使其能够输出Date对象
ostream& operator<<(ostream& _cout, const Date& d)
{
    _cout << d._year_ << "-" << d._month_ << "-" << d._day_;  // 按"年-月-日"格式输出日期

    return _cout;
}

// 重载输入运算符，使其能够输入Date对象
istream& operator>>(istream& _cin, Date& d)
{
    _cin >> d._year_;   // 输入年
    _cin >> d._month_;  // 输入月
    _cin >> d._day_;    // 输入日

    return _cin;
}

int main()
{
    Date d;         // 创建Date对象，默认初始化为1900-1-1
    cin >> d;       // 输入日期
    cout << d << endl;  // 输出日期

    return 0;
}
```

对于友元函数，需要注意的是：

+ **友元函数可访问类的私有和保护成员，但不是类的成员函数。**
+ **友元函数不能用**`**const**`**修饰。**
+ **友元函数可以在类定义的任何地方声明，不受访问限定符限制。**
+ **一个函数可以是多个类的友元函数。**
+ **友元函数的调用与普通函数的调用原理相同。**

##### 友元类
友元类的所有成员函数都可以是另一个类的友元函数，都可以访问另一个类中的非公有成员。友元类具有以下特点：

+ 友元关系是单向的，不具有交换性。
+ 友元关系不能传递。
+ 友元关系不能继承。

```cpp
#include <iostream> 

using namespace std;

class Time
{
    friend class Date;  // 声明Date类为Time类的友元类，使Date类可以直接访问Time类的私有成员变量
public:
    // 构造函数，默认时间为0时0分0秒
    Time(int hour = 0, int minute = 0, int second = 0)
        : _hour(hour), _minute(minute), _second(second)
    {}

private:
    int _hour;    // 时
    int _minute;  // 分
    int _second;  // 秒
};

class Date
{
public:
    // 构造函数，默认日期为1900年1月1日
    Date(int year = 1900, int month = 1, int day = 1)
        : _year_(year), _month_(month), _day_(day)
    {}

    // 设置Time对象的时间
    void SetTimeofDate(int hour, int minute, int second)
    {
        // 直接访问Time类私有成员变量，因为Date类是Time类的友元类
        _t._hour = hour;
        _t._minute = minute;
        _t._second = second;
    }

private:
    int _year_;    // 年
    int _month_;   // 月
    int _day_;     // 日

    Time _t;      // Time对象，表示日期对应的时间
};
```

#### 内部类
**如果一个类定义在另一个类的内部，这个内部类就叫内部类。**内部类是一个独立的类，它不属于外部类，更不能通过外部类对象去访问内部类的成员。外部类对内部类没有任何优越的访问权限。

**内部类就是外部类的友元类，内部类可以通过外部类的对象参数来访问外部类中的所有成员，反之则不行。**

**特性：**

+ 内部类可以定义在外部类的`public`、`protected`、`private`区域。
+ 注意内部类可以直接访问外部类中的`static`成员，不需要外部类的对象/类名。
+ `sizeof(外部类)=外部类`，和内部类没有任何关系。

```cpp
#include <iostream>  

using namespace std;
class A
{
private:
    static int s_k;  // 静态成员变量s_k，所有A的对象共享
    int h;         // 非静态成员变量h，每个A的对象都有独立的副本

public:
    class B // B是A的嵌套类，天生就是A的友元类
    {
    public:
        // 友元类成员函数，可以访问A类的私有成员变量
        void foo(const A& a)
        {
            cout << s_k << endl;    // 访问A的静态成员变量s_k
            cout << a.h << endl;  // 访问A对象的非静态成员变量h
        }
    };
};

int A::s_k = 1;  // 初始化A的静态成员变量s_k

int main()
{
    A::B b;  // 创建A类的嵌套类B的对象b
    b.foo(A());  // 创建一个匿名A对象并调用B类的foo函数

    return 0;
}
```

#### 匿名对象
 匿名对象是指没有命名的临时对象，通常用于在需要一个临时对象的地方直接创建对象而不保存其引用或指针。这些对象在它们的上下文结束时(例如，在语句末或表达式末)会被销毁：

```cpp
#include <iostream> 

using namespace std;

class A
{
public:
    // 构造函数，带一个默认参数a
    A(int a = 0)
        : _a_(a)
    {
        cout << "A(int a)" << endl;  // 输出构造函数调用信息
    }

    // 析构函数
    ~A()
    {
        cout << "~A()" << endl;  // 输出析构函数调用信息
    }

private:
    int _a_;
};

class Solution
{
public:
    // 求和函数，返回参数n
    int SumSolution(int n)
    {
        // ..
        return n;
    }
};

int main()
{
    A aa1;  // 创建一个A类对象aa1，调用默认构造函数
    // 输出: A(int a)

    // 不能这样定义对象，编译器无法识别下面是对象定义还是函数声明
    // A aa1();

    // 定义一个匿名对象，生命周期只有这一行
    // 调用默认构造函数创建对象，并在这一行结束后调用析构函数销毁对象
    A();
    // 输出: A(int a)
    // 输出: ~A()

    A aa2(2);  // 创建一个A类对象aa2，调用带参数的构造函数
    // 输出: A(int a)

    Solution().SumSolution(10);  // 创建一个匿名的Solution对象并调用SumSolution方法
    // Solution类没有定义构造函数和析构函数，因此没有输出

    return 0;
    // 退出main函数时，aa1和aa2对象会被销毁，调用析构函数
    // 输出: ~A()
    // 输出: ~A()
}
```

匿名对象的一个常见用法是作为函数参数或返回值。匿名对象的创建方式通常有以下几种：

+ 直接创建临时对象

```cpp
class MyClass
{
public:
    MyClass(int x) : _x_(x) {}
    void print() const { cout << "Value: " << _x_ << endl; }

private:
    int _x_;
};

int main()
{
    MyClass(10).print();  // 创建一个匿名对象并调用其成员函数

    return 0;
}
```

+ 作为函数参数

```cpp
#include <iostream>  

using namespace std;  

class MyClass
{
public:
    MyClass(int x) : _x_(x) {}
    void print() const { cout << "Value: " << _x_ << endl; }

private:
    int _x_;
};

void display(const MyClass& obj)
{
    obj.print();
}

int main()
{
    display(MyClass(20));  // 创建一个匿名对象并传递给函数

    return 0;
}
```

+ 作为函数返回值

```cpp
#include <iostream>  

using namespace std;  

class MyClass
{
public:
    MyClass(int x) : _x_(x) {}
    void print() const { cout << "Value: " << _x_ << endl; }

private:
    int _x_;
};

MyClass createObject()
{
    return MyClass(30);  // 返回一个匿名对象
}

int main()
{
    MyClass obj = createObject();  // 接收返回的匿名对象
    obj.print();

    return 0;
}
```

#### 拷贝对象时编译器的优化
在传参和传返回值的过程中，编译器会做一些优化，减少对象的拷贝：

```cpp
#include <iostream>  

using namespace std;

class A
{
public:
    // 构造函数，带一个默认参数a
    A(int a = 0)
        : _a_(a)
    {
        cout << "A(int a)" << endl;  // 输出构造函数调用信息
    }

    // 拷贝构造函数
    A(const A& aa)
        : _a_(aa._a_)
    {
        cout << "A(const A& aa)" << endl;  // 输出拷贝构造函数调用信息
    }

    // 赋值重载运算符
    A& operator=(const A& aa)
    {
        cout << "A& operator=(const A& aa)" << endl;  // 输出赋值重载运算符调用信息

        if (this != &aa)  // 避免自赋值
        {
            _a_ = aa._a_;  // 赋值成员变量
        }

        return *this;
    }

    // 析构函数
    ~A()
    {
        cout << "~A()" << endl;  // 输出析构函数调用信息
    }

private:
    int _a_;  // 成员变量a
};

// 按值传递参数
void f1(A aa) {}

// 按值返回对象
A f2()
{
    A aa;
    return aa;
}

int main()
{
    // 传值传参
    A aa1;  // 调用默认构造函数
    f1(aa1);  // 调用拷贝构造函数
    // 输出: A(int a)
    // 输出: A(const A& aa)
    // 输出: ~A()

    cout << endl;

    // 传值返回
    f2();  // 调用默认构造函数和拷贝构造函数
    // 输出: A(int a)
    // 输出: A(const A& aa)
    // 输出: ~A()
    // 输出: ~A()

    cout << endl;

    // 隐式类型转换，连续构造+拷贝构造 -> 优化为一个构造
    f1(A(2));  // 调用带参数的构造函数
    // 输出: A(int a)
    // 输出: A(const A& aa)
    // 输出: ~A()
    // 输出: ~A()

    cout << endl;

    // 一个表达式中，连续拷贝构造+拷贝构造 -> 优化为一个拷贝构造
    A aa2 = f2();  // 调用默认构造函数和拷贝构造函数
    // 输出: A(int a)
    // 输出: A(const A& aa)
    // 输出: ~A()

    cout << endl;

    // 一个表达式中，连续拷贝构造+赋值重载 -> 无法优化
    aa1 = f2();  // 调用默认构造函数、拷贝构造函数和赋值运算符重载
    // 输出: A(int a)
    // 输出: A(const A& aa)
    // 输出: ~A()
    // 输出: A& operator=(const A& aa)

    cout << endl;

    return 0;  // 退出main函数时，销毁对象aa1和aa2
    // 输出: ~A()
    // 输出: ~A()
}
```

### C/C++内存管理
#### C/C++内存分布
在 C/C++ 程序中，内存通常分为以下几个区域：

1. **代码段(text segment)：**
    - 存储程序的机器代码和只读常量。
    - 这个区域通常是只读的，以防止程序意外修改其指令。
2. **数据段(data segment)：**
    - **初始化数据段(initialized data segment)：**
        * 存储已初始化的全局变量和静态变量。
        * 比如：`int g_var1 = 1;`或`static int gs_var2 = 1;`
    - **未初始化数据段(BSS segment)：**
        * 存储未初始化的全局变量和静态变量，程序开始时这些变量被初始化为0。
        * 比如：`int g_var2;`或`static int gs_var3;`
3. **堆(heap)：**
    - 动态内存分配区，由函数如`malloc`、`calloc`、`realloc`和`free`进行分配和释放。
    - 比如：`int* p = (int*)malloc(sizeof(int) * 4);`
4. **栈(stack)：**
    - 存储局部变量和函数调用信息(包括返回地址、参数、局部变量等)。
    - 栈内存由编译器自动管理，函数调用时分配，函数结束时释放。
    - 比如：`int local_var = 1;`或`int num[10];`

```cpp
#include <stdio.h>
#include <stdlib.h>

int g_var1 = 1;  // 数据段(初始化数据段)
static int gs_var2 = 1;  // 数据段(初始化数据段)
int g_var3;  // 数据段(未初始化数据段)

void Test()
{
    static int s_var3 = 1;  // 数据段(初始化数据段)
    int var4 = 1;  // 栈

    int num[10] = { 1, 2, 3, 4 };  // 栈
    char char1[] = "abcd";  // 栈，字符串常量"abcd"存储在代码段
    const char* p_char2 = "abcd";  // 栈，字符串常量"abcd"存储在代码段
    
    int* p_ptr1 = (int*)malloc(sizeof(int) * 4);  // 栈，*p_ptr1 存储在堆
    int* p_ptr2 = (int*)calloc(4, sizeof(int));  // 栈，*p_ptr2 存储在堆
    int* p_ptr3 = (int*)realloc(p_ptr2, sizeof(int) * 4);  // 栈，*p_ptr3 存储在堆

    free(p_ptr1);
    free(p_ptr3);
}

int main()
{
    Test();
    
    return 0;
}
```

#### C语言动态内存管理
C语言中，动态内存管理主要涉及`malloc`、`calloc`、`realloc`、`free`，它们的区别为：

+ `malloc`
    - **原型**：`void* malloc(size_t size);`
    - **功能**：分配指定大小(以字节为单位)的内存块，并返回指向该内存块的指针。**分配的内存未初始化，内容是未定义的。**
    - **返回值**：成功时返回指向分配内存的指针，失败时返回`NULL`。
    - **示例**：`int* p = (int*)malloc(sizeof(int) * 10);`
+ `calloc`
    - **原型**：`void* calloc(size_t num, size_t size);`
    - **功能**：分配指定数量的内存块，每个内存块的大小为指定的字节数，并将**所有内存块初始化为0。**
    - **返回值**：成功时返回指向分配内存的指针，失败时返回`NULL`。
    - **示例**：`int* p = (int*)calloc(10, sizeof(int));`
+ `realloc`
    - **原型**：`void* realloc(void* ptr, size_t size);`
    - **功能**：**调整先前分配的内存块大小。**`ptr`指向之前分配的内存块，可以通过`malloc`、`calloc`或`realloc`获取。如果`ptr`为`NULL`，则`realloc`的行为类似于`malloc`。如果`size` 为0并且`ptr`不为`NULL`，则相当于`free(ptr)`。
    - **返回值**：成功时返回指向新分配内存的指针，失败时返回`NULL`，原指针指向的内存不变。
    - **示例**：`int* p = (int*)realloc(p, sizeof(int) * 20);`
+ `free`
    - **原型**：`void free(void* ptr);`
    - **功能**：释放之前由`malloc`、`calloc`或`realloc` 分配的内存块。释放后，指针`ptr`仍然存在，但指向的内存不可用。
    - **示例**：`free(p);`

```cpp
#include <stdio.h>
#include <stdlib.h>

int main() 
{
    // 使用 malloc 分配内存
    int* arr1 = (int*)malloc(10 * sizeof(int));
    if (arr1 == NULL) 
    {
        printf("Memory allocation failed\n");
        return 1;
    }

    // 使用 calloc 分配内存
    int* arr2 = (int*)calloc(10, sizeof(int));
    if (arr2 == NULL)
    {
        printf("Memory allocation failed\n");
        free(arr1); // 在此处释放 arr1，因为它已经分配成功
        return 1;
    }

    // 使用 realloc 调整内存大小
    int* arr3 = (int*)realloc(arr1, 20 * sizeof(int));
    if (arr3 == NULL) 
    {
        printf("Memory reallocation failed\n");
        // free(arr1); // realloc失败时，arr1依然指向有效内存，无需释放
        free(arr2);
        return 1;
    }

    // 如果 realloc 成功，arr1 不再指向原始内存，因此不需要 free(arr1)
    // arr3 现在是有效的，所以释放 arr3 即可
    free(arr2);
    free(arr3);

    return 0;
}
```

#### C++中动态内存管理
C语言中的内存管理方式在C++中可以继续使用，但有些地方无能为力，而且使用起来比较麻烦，因此，C++又提出了自己的内存管理方式：**通过**`**new**`**和**`**delete**`**操作符进行动态内存管理。**

##### new/delete操作内置类型
```cpp
#include <iostream>

using namespace std;

int main()
{
    int* p_prt1 = new int;
    int* p_prt2 = new int(10);
    int* p_prt3 = new int[10];

    delete p_prt1;
    delete p_prt2;
    delete[] p_prt3;

    return 0;
}
```

```cpp
#include <iostream>

using namespace std;

int main()
{
    // 管理对象
    int* p_prt1 = new int;
    int* p_prt2 = new int(10);

    delete p_prt1;
    delete p_prt2;

    // 管理对象数组
    int* p_prt3 = new int[10];

    delete[] p_prt3;

    return 0;
}
```

+ **内存分配**
    - `int* p_ptr1 = new int;`：分配一个整数的内存。
    - `int* p_ptr2 = new int(3);`：分配一个整数的内存并初始化为3。
    - `int* p_ptr3 = new int[3];`：分配一个包含3个整数的数组的内存。
+ **内存释放**
    - `delete p_ptr1;`：释放`p_ptr1`指向的单个整数的内存。
    - `delete p_ptr2;`：释放`p_ptr2`指向的单个整数的内存。
    - `delete[] p_ptr3;`：释放`p_ptr3`指向的整数数组的内存。

:::color2
**使用**`**new**`**与**`**delete**`**时，重要注意事项： **

+ **使用**`**new[]**`**分配内存时，必须使用**`**delete[]**`**来释放内存，以避免未定义行为。  **
+ **确保每个**`**new**`**对应一个**`**delete**`**，每个**`**new[]**`**对应一个**`**delete[]**`**，以防止内存泄漏。  **

:::

##### new和delete操作自定义类型
```cpp
#include <iostream>

using namespace std;

class A
{
public:
    A(int a = 0)
        : _a_(a)
    {
        cout << "A():" << this << endl;
    }

    ~A()
    {
        cout << "~A():" << this << endl;
    }

private:
    int _a_;
};

int main()
{
    // new/delete和malloc/free最大的区别是，new/delete对于自定义类型除了开空间还会调用构造函数和析构函数
    A* p_p1 = (A*)malloc(sizeof(A));
    A* p_p2 = new A(1);  // A():002E7230

    free(p_p1);
    delete p_p2;  // ~A():002E7230

    // 内置类型几乎一样
    int* p_p3 = (int*)malloc(sizeof(int));  // C
    int* p_p4 = new int;

    free(p_p3);
    delete p_p4;

    A* p_p5 = (A*)malloc(3 * sizeof(int));
    A* p_p6 = new A[3]; 
    /*
    A():002E7234
    A():002E7238
    A():002E723C
    */

    free(p_p5);
    delete[] p_p6;
    /*
    ~A():002E723C
    ~A():002E7238
    ~A():002E7234
    */

    return 0;
}
```

:::color2
**注：在申请自定义类型的空间时，**`**new**`**会调用构造函数，**`**delete**`**会调用析构函数，而**`**malloc**`**与**`**free**`**则不会。**

:::

#### operator new与operator delete函数
##### operator new与operator delete函数
`new`和`delete`操作符在C++中用于动态内存的分配和释放，它们在底层依赖于全局函数`operator new`和`operator delete`来完成实际的内存管理任务，它们的差别是：

+ `**operator new**`**和**`**operator delete**`是全局函数，负责内存分配和释放。它们可以被用户自定义。
+ `**new**`**和**`**delete**`**操作符**是在高层次上操作的，它们不仅管理内存，还会调用构造函数和析构函数。
+ **自定义内存管理**可通过重载`operator new`和`operator delete` 实现，以控制内存的分配策略。

`**new**`**工作原理：**

1. **调用**`**operator new**`:
+ `new`操作符首先调用全局的`operator new`函数来申请足够的内存，以容纳请求的对象。  
+  例如`new A()`会调用`operator new(sizeof(A))`，请求分配`sizeof(A)`字节的内存。  

```cpp
void* memory = operator new(sizeof(A));
```

2. **调用构造函数**：
+ 内存分配成功后，`new`操作符会在刚分配的内存上调用相应的构造函数，初始化对象。

```cpp
A* obj = new(memory) A(1); // 在分配的内存上调用构造函数
```

3. **返回指针**：
+ 最后，`new`操作符返回一个指向初始化后对象的指针。

`**delete**`**工作原理：**

1. **调用析构函数**：
+ `delete`操作符首先会调用对象的析构函数，执行清理任务。

```cpp
obj->~A();  // 调用析构函数
```

2. **调用**`**operator delete**`：
+ 然后，`delete`操作符调用全局的`operator delete`函数来释放内存。

```cpp
operator delete(obj); // 释放内存
```

自定义`operator new`和`operator delete`：

```cpp
#include <iostream>
#include <cstdlib> // 包含 std::malloc 和 std::free 函数的头文件

using namespace std;

// 重载全局的 new 操作符
void* operator new(size_t size)
{
    // 打印分配内存的信息
    cout << "Custom operator new: Allocating: " << size << " bytes" << endl;

    // 使用 malloc 函数分配指定大小的内存
    void* p_ptr = malloc(size);

    // 如果内存分配失败，抛出 bad_alloc 异常
    if (!p_ptr)
    {
        throw bad_alloc();
    }

    // 返回分配的内存地址
    return p_ptr;
}

// 重载全局的 delete 操作符
void operator delete(void* p_ptr) noexcept
{
    // 打印释放内存的信息
    cout << "Custom operator delete: Freeing memory" << endl;

    // 使用 free 函数释放内存
    free(p_ptr);
}

// 定义一个类 A
class A
{
public:
    // 类 A 的构造函数
    A() { cout << "A Constructor" << endl; };

    // 类 A 的析构函数
    ~A() { cout << "A destructor" << endl; };
};

int main()
{
    // 使用自定义的 new 操作符创建类 A 的对象
    A* a = new A();

    // 使用自定义的 delete 操作符删除类 A 的对象
    delete a;

    return 0;
}
```

#### new和delete实现原理
##### 内置类型
如果申请的是内置类型的空间，`new`和`malloc`、`delete`和`free`基本类似，不同的地方是：`new`和`delete`申请和释放的是单个元素的空间，`new[]`和`delete[]`申请和释放的是连续空间，而且`new`在申请空间失败时会抛出异常，`malloc`则返回`NULL`。

##### 自定义类型
+ `**new**`**原理**
    - **调用**`**operator new**`**函数申请空间。**
    - **在申请的空间上执行构造函数，完成对象的构造。**
+ `**delete**`**原理**
    - **在空间上执行析构函数，完成对象中资源的清理工作。**
    - **调用**`**operator delete**`**函数释放对象的空间。**
+ `**new T[N]**`**原理**
    - **调用**`**operator new[]**`**函数，在**`**operator new[]**`**中实际调用**`**operator new**`**函数完成N个对象空间的申请。**
    - **在申请的空间上执行N次构造函数。**
+ `**delete[]**`**原理**
    - **在释放的对象空间上执行N次析构函数，完成N个对象中资源的清理。**
    - **调用**`**operator delete[]**`**释放空间，实际在**`**operator delete[]**`**中调用**`**operator delete**`**来释放空间。**

```cpp
#include <iostream>
#include <cstdlib>

using namespace std;

class A
{
public:
    A(int a = 0) : _a_(a)
    {
        cout << "A() Constructor: " << this << endl;
    }

    ~A()
    {
        cout << "~A() Destructor: " << this << endl;
    }

    // Overload operator new
    void* operator new(size_t size)
    {
        cout << "operator new: allocating " << size << " bytes" << endl;
        return ::operator new(size); // Call global operator new
    }

    // Overload operator delete
    void operator delete(void* ptr)
    {
        cout << "operator delete: deallocating " << ptr << endl;
        ::operator delete(ptr); // Call global operator delete
    }

    // Overload operator new[]
    void* operator new[](size_t size)
    {
        cout << "operator new[]: allocating " << size << " bytes" << endl;
        return ::operator new[](size); // Call global operator new[]
    }
    
    // Overload operator delete[]
    void operator delete[](void* ptr)
    {
        cout << "operator delete[]: deallocating " << ptr << endl;
        ::operator delete[](ptr); // Call global operator delete[]
    }

private:
    int _a_;
};

int main()
{
    // 单个对象的分配与释放
    A* p1 = new A(1);  // 调用 operator new 和 构造函数
    delete p1;         // 调用析构函数和 operator delete

    cout << "--------------------" << endl;

    // 数组对象的分配与释放
    A* p2 = new A[3];  // 调用 operator new[] 和 N 次构造函数
    delete[] p2;       // 调用 N 次析构函数和 operator delete[]

    return 0;
}
```

#### 定位new表达式(placement-new)
定位`new`表达式是在已分配的原始内存空间中调用构造函数初始化一个对象。使用格式：

+ `new (place_address) type`或者`new (place_address) type(initializer-list)`，其中`place_address`必须是一个指针，`initializer-list`是类型的初始化列表。

使用场景：

定位`new`表达式在实际中一般是配合内存池使用。因为内存池分配出的内存没有初始化，所以如果是自定义类型的对象，需要使用`new`的表达式进行显式调用构造函数进行初始化。

```cpp
#include <iostream>
#include <new>  // 包含 operator new 和 operator delete

using namespace std;

class A
{
public:
    A(int a = 0)
        : _a_(a)
    {
        cout << "A() Constructor: " << this << ", _a_: " << _a_ << endl;
    }

    ~A()
    {
        cout << "~A() Destructor: " << this << endl;
    }

private:
    int _a_;
};

int main()
{
    // 使用 malloc 分配内存，并使用定位 new 调用构造函数
    A* p_p1 = (A*)malloc(sizeof(A));
    if (p_p1 == nullptr) 
    {
        cout << "Memory allocation failed for p_p1" << endl;
        return 1;
    }

    new(p_p1) A;  // 定位 new, 默认构造函数
    p_p1->~A();   // 手动调用析构函数
    free(p_p1);   // 释放内存

    // 使用 operator new 分配内存，并使用定位 new 调用构造函数
    A* p_p2 = (A*)operator new(sizeof(A));
    if (p_p2 == nullptr) 
    {
        cout << "Memory allocation failed for p_p2" << endl;
        return 1;
    }

    new(p_p2) A(10);  // 定位 new, 带参数的构造函数
    p_p2->~A();       // 手动调用析构函数
    operator delete(p_p2);  // 释放内存

    return 0;
}
```

#### 常见面试知识点
##### malloc/free和new/delete的区别
`malloc`/`free`和`new`/`delete`的共同点是：都是从堆上申请空间，并且需要用户手动释放。不同点有以下：

+ `malloc`和`free`是函数，`new`和`delete`是操作符。
+ `malloc`申请的空间不会初始化，`new`可以初始化。
+ `malloc`申请空间时，需要手动计算空间大小并传递，`new`只需在其后跟上控件类型即可，如果是多个对象，在`[]`中指定对象数量即可。
+ `malloc`的返回值为`void*`，在使用时必须强转，`new`不需要，因为`new`后跟的是空间的类型。
+ `malloc`申请空间失败时返回`NULL`，使用时必须判空，`new`不需要，`new`需要捕获异常。
+ 申请自定义类型对象时，`malloc`/`free`只会开辟空间，不会调用构造函数与析构函数，而`new`在申请空间后会调用构造函数完成对象的初始化，`delete`在释放空间前会调用析构函数完成空间中资源的清理。

##### 内存泄漏
###### 什么是内存泄漏，有何危害
 内存泄漏是指程序在动态分配内存后，由于某种原因未能正确释放这些内存，从而导致这些内存无法被回收利用的现象。内存泄漏通常发生在使用堆内存时，即通过 `new`、`malloc` 等函数分配的内存没有通过 `delete`、`free` 等函数进行释放。长期运行的程序出现内存泄漏，影响很大，如操作系统、后台服务等等，出现内存泄漏会导致响应越来越慢，最终卡死。

```cpp
void MemoryLeaks()
{
    // 1. 内存申请了忘记释放
    int* p_p1 = (int*)malloc(sizeof(int));
    int* p_p2 = new int;
    
    // 2. 异常安全问题
    int* p_p3 = new int[10];

    Func(); // 这里的Func函数抛异常导致delete[] p_p3未执行，p_p3未被释放。
}
```

###### 内存泄漏的种类
1. 根据内存泄漏的来源

+ **堆内存泄漏**：
    - 当程序使用 `new` 或 `malloc` 等函数分配内存但没有使用 `delete` 或 `free` 释放内存时，就会发生堆内存泄漏。堆内存泄漏是最常见的内存泄漏类型。
+ **栈内存泄漏**：
    - 栈内存泄漏相对较少见，因为栈内存是由编译器自动管理的。但某些情况下，如递归调用过多导致栈溢出，也可以视为一种特殊形式的内存泄漏。

2. 根据内存泄漏的持续时间

+ **临时性泄漏**：
    - 发生在程序运行的特定时刻或条件下，一段时间后可能会被回收利用。通常是由于临时对象未能及时释放引起的。
+ **永久性泄漏**：
    - 内存一旦泄漏，就不会被程序回收，直到程序结束。通常发生在全局变量或长生命周期对象中。

3. 根据内存泄漏的影响范围

+ **直接内存泄漏**：
    - 程序分配了一块内存，但永远没有释放这块内存。泄漏的内存直接可以识别，并且与分配点关联明确。
+ **间接内存泄漏**：
    - 程序分配了一块内存，并通过指针或引用将其关联到另一个对象。当关联的对象被释放但内存未释放时，造成间接内存泄漏。

4. 根据内存泄漏的原因

+ **忘记释放内存**：
    - 程序员忘记在合适的时机释放内存，导致内存泄漏。
+ **双重释放**：
    - 程序在释放内存后再次尝试释放同一块内存，可能导致程序崩溃或未定义行为。
+ **错误的指针操作**：
    - 由于指针错误操作，如指针覆盖、野指针等，导致无法正确释放内存。
+ **循环引用**：
    - 在使用智能指针时，两个或多个对象相互引用，形成循环引用，导致内存无法释放。

```cpp
#include <iostream>

void memoryLeakExample() 
{
    int* p = new int[10]; // 分配10个int的数组
    // 忘记释放p指向的内存，导致内存泄漏
}

void cyclicReferenceExample() 
{
    struct Node 
    {
        Node* next;
        // 构造函数和其他成员
    };

    Node* node1 = new Node();
    Node* node2 = new Node();

    node1->next = node2;
    node2->next = node1; // 形成循环引用

    // 忘记释放node1和node2，导致内存泄漏
}

int main() 
{
    memoryLeakExample();
    cyclicReferenceExample();

    return 0;
}
```

###### 如何检测内存泄漏
+ _CrtDumpMemoryLeaks()

在`VS`下，可以使用Windows操作系统提供的`_CrtDumpMemoryLeaks()`函数进行简单检测，该函数只报出了大概泄露了多少个字节，没有更准确的泄漏点位置。

```cpp
int main()
{
     int* p = new int[10];
     // 将该函数放在main函数之后，每次程序退出的时候就会检测是否存在内存泄漏
     _CrtDumpMemoryLeaks();
        
     return 0;
}

////////////////////////////////////////////////////////
// 程序退出后，在输出窗口中可以检测到泄漏了多少字节，但是没有具体的位置
Detected memory leaks!
Dumping objects ->
{79} normal block at 0x00EC5FB8, 40 bytes long.
Data: <                > CD CD CD CD CD CD CD CD CD CD CD CD CD CD CD CD
Object dump complete.
```

+ 使用智能指针

 	使用C++11引入的智能指针，如 `std::unique_ptr` 和 `std::shared_ptr`可以自动管理内存，减少内存泄漏的风险。  

```cpp
#include <memory>

void example() 
{
    std::unique_ptr<int[]> p(new int[10]);
    // 不需要手动释放内存
}
```

+ 静态分析工具(Clang Static Analyzer、Cppcheck)
+ 动态分析工具(Valgrind、AddressSanitizer)
+ 自定义内存分析器

 实现自定义的内存分配器，通过重载 `new` 和 `delete` 操作符来跟踪内存分配和释放。例如：  

```cpp
#include <iostream>
#include <new>

void* operator new(size_t size) 
{
    void* p = malloc(size);
    std::cout << "Allocated " << size << " bytes at " << p << std::endl;
    
    return p;
}

void operator delete(void* p) noexcept 
{
    std::cout << "Deallocated memory at " << p << std::endl;
    free(p);
}

int main() 
{
    int* p = new int[10];
    delete[] p;
    
    return 0;
}
```

### 模板初阶
#### 泛型编程
如何实现一个通用的交换函数呢？

```cpp
void Swap(int& left, int& right)
{
    int tmp = left;
    left = right;
    right = tmp;
}

void Swap(double& left, double& right)
{
    double tmp = left;
    left = right;
    right = tmp;
}

void Swap(char& left, char& right)
{
    char tmp = left;
    left = right;
    right = tmp;
}

// ...
```

使用函数重载虽然可以实现，但是有以下几个不足的地方：

1. 重载的函数仅仅是类型不同，代码复用率比较低，只要有新类型出现时，就需要用户自己增加对应的函数。
2. 代码的可维护性较低，一个出错可能所有重载均出错。

那么能否**告诉编译器一个模子，让编译器根据不同的类型利用该模子来生成代码**呢？如果在C++中，存在这样一个模具，通过给这个模具中填充不同材料(类型)，来获得不同材料的铸件(即生成具体类型的代码)，那么在实际项目中会提高很多效率。

**泛型编程：编写与类型无关的通用代码，是代码复用的一种手段，模板是泛型编程的基础。**

#### 函数模板
##### 函数模板概念
**函数模板代表了一个函数家族，该函数模板与类型无关，在使用时被参数化，根据实参类型产生函数的特定类型版本。**

##### 函数模板格式
```cpp
template <typename T> 
返回类型 函数名(参数列表)
{
    // 函数体
}
```

+ `template <typename T>`：这是模板声明部分，表明接下来定义的是一个模板，其中`T`是一个类型参数。  
+ `T`：模板参数，可以在函数的返回类型和参数列表中使用。  
+ `返回类型`、`函数名`和`参数列表`：与普通函数定义类似，但可以使用模板参数`T`。  

例如以下简单的函数模板：

```cpp
template <typename T>
T Max(T a, T b)
{
    return (a > b) ? a : b;
}
```

上述模板定义了一个函数`Max`，它接受两个相同类型的餐宿并返回其中较大的一个。模板参数`T`可以是任何支持运算符的类型。

```cpp
template <typename T1, typename T2, ..., typename Tn>
T1 Add(T1 a, T2 b, ..., Tn n)
{
    return a + b + ... + n;
}
```

此模板定义类一个函数`Add`，它接受多个不同类型的参数并返回它们的和。模板参数`T1`、`T2`、... 、`Tn`可以是不同的类型。

```cpp
template <typename T, int size>
T Sum(const T (&array)[size]) 
{
    T total = 0;
    for (int i = 0; i < size; ++i)
    {
        total += array[i];
    }
    
    return total;
}
```

这个模板定义了一个函数`Sum`，它接受一个固定大小的数组并返回数组元素的和。模板参数`T`表示数组元素的类型，非类型参数`size`表示数组的大小。  

```cpp
#include <iostream>

// 函数模板定义
// Max函数模板：返回两个值中的较大者
template <typename T>
T Max(T a, T b)
{
    // 使用三元运算符判断并返回较大的值
    return (a > b) ? a : b;
}

// Add函数模板：将两个不同类型的值相加，并返回第一个参数类型的结果
template <typename T1, typename T2>
T1 Add(T1 a, T2 b)
{
    // 将两个值相加，并返回结果
    return a + b;
}

// Sum函数模板：计算数组的元素总和
// 参数T为数组的元素类型，size为数组的大小
template <typename T, int size>
T Sum(const T(&array)[size])
{
    T total = 0;  // 初始化总和为0

    // 遍历数组并累加每个元素的值
    for (int i = 0; i < size; ++i)
    {
        total += array[i];
    }

    // 返回累加的结果
    return total;
}

int main()
{
    // 使用 Max 函数模板
    std::cout << "Max of 3 and 5: " << Max(3, 5) << std::endl;  // 比较两个整数
    std::cout << "Max of 3.5 and 5.5: " << Max(3.5, 5.5) << std::endl;  // 比较两个浮点数

    // 使用 Add 函数模板
    std::cout << "Add of 3 and 2.5: " << Add(3, 2.5) << std::endl;  // 将整数和浮点数相加

    // 使用 Sum 函数模板
    int array[] = { 1, 2, 3, 4, 5 };  // 定义一个整数数组
    std::cout << "Sum of array: " << Sum(array) << std::endl;  // 计算数组元素的总和

    return 0;
}
```

##### 函数模板的原理
**函数模板是一个蓝图，它本身并不是函数，是编译器用使用方式产生特定具体类型函数的模具。所以其实模板就是将本来应该我们做的重复的事情交给了编译器。**

1. 模板定义。首先，定义一个函数模板，指定模板参数。模板参数通常是类型参数(用`typename`或`class`关键字声明)，也可以是非类型参数。

```cpp
template <typename T>
T Max(T a, T b)
{
    return (a > b) ? a : b;
}
```

2. 模板实例化。当调用一个模板函数时，编译器会根据调用时传递的参数类型实例化出具体的函数版本。例如：

```cpp
int main()
{
    int x = 3, y = 5;
    double a = 2.5, b = 3.7;

    int int_max = Max(x, y);     // 实例化为 int Max(int, int)
    double double_max = Max(a, b); // 实例化为 double Max(double, double)

    return 0;
}
```

在上述代码中，`Max`函数模板被实例化了两次：

+ 一次是`Max(int, int)`。
+ 一次是`Max(double, double)`。

编译器会生成这两种具体类型的`Max`函数实现。

3. 类型推导。编译器根据函数调用时传递的实参类型推导出模板参数类型。在上面的例子中：
+ 对于`Max(x, y)`，编译器推导出`T`为`int`。
+ 对于`Max(a, b)`，编译器推导出`T`为`double`。
4. 编译时检查。模板实例化是在编译时进行的，编译器会对实例化后的代码进行类型检查。如果模板代码中包含不适用于实例化类型的操作，编译会报错。例如：

```cpp
#include <iostream>

template <typename T>
T Add(T a, T b)
{
    return a + b;
}

int main()
{
    std::string s1 = "Hello, ";
    std::string s2 = "world!";
    std::string result = Add(s1, s2); // 正确，std::string 支持 + 操作

    int sum = Add(3, "world!");       // 错误，int 和 const char* 不支持 + 操作

    return 0;
}
```

5. 代码优化。由于模板是在编译时实例化的，因此没有运行时开销。模板代码生成的具体函数通常会进行内联扩展提高性能。然而，大量的模板实例化可能会导致代码膨胀，这是使用模板时需要注意的。

##### 函数模板的实例化
**用不同类型的参数使用函数模板时，称为函数模板的实例化。模板参数实例化分为：隐式实例化和显式实例化。**

+ **隐式实例化：让编译器根据实参推演模板参数的实际类型。**

```cpp
#include <iostream>

using namespace std;

template <class T>
T Add(const T& left, const T& right)
{
    return left + right;
}

int main()
{
    int a1 = 0, a2 = 20;
    double d1 = 10.0, d2 = 20.0;

    Add(a1, a2); // T 被推演为 int
    Add(d1, d2); // T 被推演为 double

    // 编译失败。当编译器看到该实例化时，需要推演其实参类型。
    // 通过实参 a1 将 T 推演为 int，通过实参 d1 将 T 推演为 double 类型，但模板参数列表中只有一个 T
    // 编译器无法确定此处到底该将 T 确定为 int 还是 double
    // 注意：在模板中，编译器一般不会进行类型转换操作，因为一旦转换出问题，编译器背锅
    // Add(a1, d1); // 这行代码会导致编译错误

    // 此时有两种处理方式：1. 用户自己强制转换 2. 使用显式实例化
    Add(a1, (int)d1); // 用户自己强制转换

    return 0;
}
```

函数模板在处理不同类型参数时，需要编译器推演模板参数的类型。如果传递的参数类型不一致且模板参数列表中只有一个类型参数，编译器无法确定类型推演，因此会导致编译错误。通过强制转换、显式实例化或使用支持不同类型参数的重载函数模板，可以解决这个问题。  

+ **显式实例化：在函数名后的**`**<>**`**中指定模板参数的实际类型。**

```cpp
#include <iostream>

using namespace std;

template <class T>
T Add(const T& left, const T& right)
{
    return left + right;
}

int main()
{
    int a = 10;
    double b = 20.0;

    // 显式实例化
    Add<int>(a, b);

    return 0;
}
```

如果类型不匹配，编译器会尝试进行隐式类型转换，如果无法转换成功编译器将会报错。

##### 模板参数的匹配原则
1. **一个非模板函数可以和一个同名的函数模板同时存在，而且该函数模板还可以被实例化为这个非模板函数。**

```cpp
#include <iostream>

using namespace std;

// 专门处理 int 类型的加法函数
int Add(int left, int right)
{
    return left + right;
}

// 通用加法函数模板
// 用于处理其他类型的加法操作
template <class T>
T Add(T left, T right)
{
    return left + right;
}

int main()
{
    // 调用专门处理 int 类型的 Add 函数
    // 由于参数类型完全匹配(int, int)，编译器选择调用非模板函数
    Add(1, 2);

    // 显式实例化模板函数
    // 即使传入的参数是 int 类型，编译器也会选择模板版本的 Add<int>(int, int)
    Add<int>(1, 2);  

    return 0;
}
```

2. **对于非模板函数和同名函数模板，如果其他条件都相同，在调用时会优先调用非模板函数而不会从该模板产生出一个实例。如果模板可以产生一个具有更好匹配的函数，那么将选择模板。**

```cpp
#include <iostream>

using namespace std;

// 专门处理 int 类型的加法函数
// 当参数为 int 类型时，调用此函数
int Add(int left, int right)
{
    return left + right;
}

// 通用加法函数模板
// 处理不同类型的加法操作，返回第一个参数类型的结果
template <class T1, class T2>
T1 Add(T1 left, T2 right)
{
    return left + right;
}

int main()
{
    // 调用专门处理 int 类型的 Add 函数
    // 由于参数类型完全匹配(int, int)，因此不会调用模板函数
    Add(1, 2);    

    // 调用模板 Add 函数
    // 由于参数类型不匹配(int, double)，因此编译器实例化模板函数生成 Add(int, double)
    Add(1, 2.0);  

    return 0;
}
```

3. **模板函数不允许自动类型转换，但普通函数可以进行自动类型转换。**

#### 类模板
##### 类模板的定义格式与实例化
```cpp
template <typename T>
class ClassName 
{
    // 类的成员变量和成员函数
};
```

+ `template <typename T>`：这是模板声明部分，表示接下来定义的是一个模板，其中`T`是一个类型参数。
+ `ClassName`：这是类的名称。
+ 类的成员变量和成员函数：可以使用模板参数`T`。

例如以下简单的类模板示例：

```cpp
#include <iostream>

using namespace std;

// 定义模板类 MyClass
template <typename T>
class MyClass
{
public:
    // 构造函数，接收一个类型为 T 的值并初始化成员变量 _value_
    MyClass(T value)
        : _value_(value)
    {}

    // 公共成员函数，返回成员变量 _value_ 的值
    T GetValue() const
    {
        return _value_;
    }

private:
    // 私有成员变量，类型为模板参数 T
    T _value_;
};

int main()
{
    // 实例化 MyClass<int> 对象，存储一个整数值
    // 必须显式指定模板参数类型
    MyClass<int> i_obj(10);

    // 实例化 MyClass<double> 对象，存储一个双精度浮点数值
    // 必须显式指定模板参数类型
    MyClass<double> d_obj(15.2);

    // 输出 i_obj 中存储的整数值
    cout << "Int value: " << i_obj.GetValue() << endl;

    // 输出 d_obj 中存储的双精度浮点数值
    cout << "Double value: " << d_obj.GetValue() << endl;

    return 0;
}
```

上述代码中，`MyClass`是一个模板类，它接受一个类型参数`T`。该类有一个构造函数和一个成员函数`GetValue`，它们都使用了模板参数`T`。

```cpp
#include <iostream>
#include <string>  // 包含string库以便使用std::string

using namespace std;

// 定义模板类 Pair，用于存储一对不同类型的值
template <typename T1, typename T2>
class Pair
{
public:
    // 构造函数，初始化成员变量 _first_ 和 _second_
    Pair(T1 first, T2 second)
        : _first_(first), _second_(second)
    {}

    // 获取第一个值
    T1 GetFirst() const
    {
        return _first_;
    }

    // 获取第二个值
    T2 GetSecond() const
    {
        return _second_;
    }

private:
    // 私有成员变量，用于存储一对值
    T1 _first_;
    T2 _second_;
};

int main()
{
    // 创建 Pair<int, double> 对象，存储一个整数和一个双精度浮点数
    // 必须显式指定模板参数类型
    Pair<int, double> p1(20, 20.5);

    // 创建 Pair<string, int> 对象，存储一个字符串和一个整数
    // 必须显式指定模板参数类型
    Pair<string, int> p2("Age", 30);

    // 输出 Pair 对象 p1 的内容
    cout << "Pair 1: (" << p1.GetFirst() << ", " << p1.GetSecond() << ")" << endl;

    // 输出 Pair 对象 p2 的内容
    cout << "Pair 2: (" << p2.GetFirst() << ", " << p2.GetSecond() << ")" << endl;

    return 0;
}
```

上述代码中，`Pair`类模板有两个模板参数`T1`和`T2`，分别表示一对值的类型。类的成员变量`_first_`好`_second_`使用了这些模板参数。

```cpp
#include <iostream>

using namespace std;

// 定义模板类 Array，用于创建一个固定大小的数组
template <typename T, int size>
class Array 
{
public:
    // 重载 [] 运算符，用于通过索引访问数组元素
    T& operator[](int index) 
    {
        return data[index];
    }

    // 获取数组的大小
    int GetSize() const 
    {
        return size;
    }

private:
    // 用于存储数组数据的私有成员变量
    T data[size];
};

int main()
{
    // 实例化 Array<int, 10> 对象，创建一个大小为 10 的整数数组
    Array<int, 10> int_array;

    // 将数组的每个元素设置为 i * 10
    for (int i = 0; i < int_array.GetSize(); ++i) 
    {
        int_array[i] = i * 10;
    }

    // 输出数组的每个元素
    for (int i = 0; i < int_array.GetSize(); ++i) 
    {
        cout << int_array[i] << " ";
    }

    cout << endl;

    return 0;
}
```

上述代码中，`Array` 类模板有一个类型模板参数`T`和一个非类型模板参数`size`，表示数组的大小。类的成员变量`data`是一个固定大小的数组。  

类模板实例化与函数模板实例化不同，**类模板实例化需要在类模板名后跟**`**<>**`**，然后将实例化的类型放在**`**<>**`**中即可，类模板名字不是真正的类，而实例化的结果才是真正的类。**

### 迭代器
#### 迭代器是什么
 在C++中，迭代器(Iterator)是一种用于遍历容器(如数组、链表、向量等)中的元素的对象。迭代器的概念类似于指针，但它们提供了一种统一的方式来访问不同类型容器的元素，从而提高了代码的通用性和可读性。  

#### 迭代器的作用
1. **遍历容器元素**：迭代器提供了在容器中逐个访问元素的方法。 
2. **统一接口**：不同的容器(如`vector`、`list`、`map`等)都有各自的内部实现，但通过迭代器，可以使用统一的方式来访问和操作它们的元素。 
3. **与算法结合**：C++标准模板库(`STL`)中的许多算法(如`sort`、`find`等)都依赖于迭代器来访问容器元素。  

#### 迭代器的种类
根据迭代器的功能和操作，它们可以分为以下几种类型：

1. **输入迭代器(Input Iterator)**：
    - 只能读取数据，不能修改数据。
    - 支持的操作：`==`, `!=`, `*`, `->`, `++`(前置和后置)。
    - 主要用于单向读取数据。
2. **输出迭代器(Output Iterator)**：
    - 只能写入数据，不能读取数据。
    - 支持的操作：`*`, `++`(前置和后置)。
    - 主要用于单向写入数据。
3. **前向迭代器(Forward Iterator)**：
    - 既可以读取数据，也可以写入数据。
    - 支持的操作：`==`, `!=`, `*`, `->`, `++`(前置和后置)。
    - 可以多次遍历相同的容器。
4. **双向迭代器(Bidirectional Iterator)**：
    - 既可以读取数据，也可以写入数据。
    - 支持的操作：`==`, `!=`, `*`, `->`, `++`(前置和后置)，`--`(前置和后置)。
    - 可以双向遍历容器。
5. **随机访问迭代器(Random Access Iterator)**：
    - 最强大的迭代器类型，支持所有前向和双向迭代器的操作，还可以直接跳转到容器内的任意元素。
    - 支持的操作：`==`, `!=`, `*`, `->`, `++`(前置和后置)，`--`(前置和后置)，`+`, `-`, `+=`, `-=`, `[]`。
    - 主要用于数组、`std::vector`等可以随机访问的容器。

#### 常见容器与迭代器类型对应关系
| 容器类型 | 迭代器类型 |
| :---: | :---: |
| `vector` | 随机访问迭代器 |
| `deque` | 随机访问迭代器 |
| `list` | 双向迭代器 |
| `forward_list` | 前向迭代器 |
| `set`/`multiset` | 双向迭代器 |
| `map`/`multimap` | 双向迭代器 |
| `unordered_set`/`unordered_map` | 前向迭代器 |


#### 常用迭代器操作
+ `**begin()**`**：返回指向容器第一个元素的迭代器。**
+ `**end()**`**：返回指向容器末尾的迭代器(不指向任何有效元素，表示遍历结束)。**
+ `**rbegin()**`**：返回指向容器最后一个元素的逆向迭代器。**
+ `**rend()**`**：返回指向容器第一个元素前的逆向迭代器。**
+ `**cbegin()**`**、**`**cend()**`**：返回常量迭代器，不能用于修改元素。**
+ `**++it**`**：将迭代器移动到下一个元素。**
+ `**--it**`**：将迭代器移动到上一个元素(双向迭代器和随机访问迭代器支持)。**
+ `***it**`**：解引用迭代器，获取当前元素的值。**
+ `**it->**`**：访问迭代器当前元素的成员(当元素是对象时)。**

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <forward_list>
#include <iterator>
#include <algorithm>
#include <sstream>

using namespace std;

// 示例1：输入迭代器
void InputIteratorExample()
{
    // 使用istringstream模拟输入流
    istringstream input("1 2 3 4 5");

    // 定义输入流迭代器，指向输入流的开始和结束
    istream_iterator<int> it(input);
    istream_iterator<int> end;

    // 使用输入迭代器读取数据并输出
    while (it != end)
    {
        cout << *it << " "; // 解引用迭代器并输出值
        ++it;               // 移动到下一个位置
    }
    cout << endl;
}

// 示例2：输出迭代器
void OutputIteratorExample()
{
    // 定义一个整数向量
    vector<int> vec = {1, 2, 3, 4, 5};

    // 定义输出流迭代器，指向标准输出
    ostream_iterator<int> out_it(cout, " ");

    // 使用copy算法将向量内容复制到输出流迭代器
    copy(vec.begin(), vec.end(), out_it);
    cout << endl;
}

// 示例3：前向迭代器
void ForwardIteratorExample()
{
    // 定义一个前向列表
    forward_list<int> flist = {1, 2, 3, 4, 5};

    // 使用前向迭代器遍历前向列表
    for (auto it = flist.begin(); it != flist.end(); ++it)
    {
        cout << *it << " "; // 解引用迭代器并输出值
    }
    cout << endl;
}

// 示例4：双向迭代器
void BidirectionalIteratorExample()
{
    // 定义一个双向列表
    list<int> lst = {1, 2, 3, 4, 5};

    // 使用双向迭代器反向遍历列表
    for (auto it = lst.rbegin(); it != lst.rend(); ++it)
    {
        cout << *it << " "; // 解引用迭代器并输出值
    }
    cout << endl;
}

// 示例5：随机访问迭代器
void RandomAccessIteratorExample()
{
    // 定义一个向量
    vector<int> vec = {1, 2, 3, 4, 5};

    // 使用随机访问迭代器遍历向量
    for (size_t i = 0; i < vec.size(); ++i)
    {
        cout << vec[i] << " "; // 通过下标访问向量元素
    }
    cout << endl;
}

int main()
{
    // 调用输入迭代器示例函数
    cout << "Input Iterator Example: ";
    InputIteratorExample();

    // 调用输出迭代器示例函数
    cout << "Output Iterator Example: ";
    OutputIteratorExample();

    // 调用前向迭代器示例函数
    cout << "Forward Iterator Example: ";
    ForwardIteratorExample();

    // 调用双向迭代器示例函数
    cout << "Bidirectional Iterator Example: ";
    BidirectionalIteratorExample();

    // 调用随机访问迭代器示例函数
    cout << "Random Access Iterator Example: ";
    RandomAccessIteratorExample();

    return 0;
}
```

#### 迭代器与算法
C++ `STL`中的许多算法都使用迭代器作为参数，例如以下：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    std::vector<int> vec = { 5, 2, 3, 1, 4 };

    // 使用sort算法对vector进行排序
    std::sort(vec.begin(), vec.end());

    // 使用find算法查找元素
    auto it = std::find(vec.begin(), vec.end(), 3);
    if (it != vec.end()) 
    {
        std::cout << "Found: " << *it << std::endl;
    }
    else
    {
        std::cout << "Not found" << std::endl;
    }

    return 0;
}
```

#### 自定义迭代器
有时候我们可能需要为自定义容器实现迭代器，以便使其能够与`STL`算法兼容。实现迭代器需要遵循迭代器的接口和特性，并定义必要的操作符，如`*`、`++`、`--`等。 以下是一个简单的自定义迭代器例子：

```cpp
#include <iostream>
#include <iterator>

// 自定义的整数数组迭代器类
class IntArrayIterator : public std::iterator<std::input_iterator_tag, int> 
{
    int* p; // 指向当前数组元素的指针

public:
    // 构造函数，初始化指针
    IntArrayIterator(int* x) : p(x) {}

    // 拷贝构造函数
    IntArrayIterator(const IntArrayIterator& it) : p(it.p) {}

    // 前置++运算符重载，将指针移动到下一个元素
    IntArrayIterator& operator++() 
    {
        ++p;
        return *this;
    }

    // 后置++运算符重载，将指针移动到下一个元素，但返回旧值
    IntArrayIterator operator++(int) 
    {
        IntArrayIterator tmp(*this); // 临时存储当前迭代器状态
        ++p;
        return tmp;
    }

    // 等号运算符重载，比较两个迭代器是否相等（指向同一位置）
    bool operator==(const IntArrayIterator& rhs) const 
    {
        return p == rhs.p;
    }

    // 不等号运算符重载，比较两个迭代器是否不相等
    bool operator!=(const IntArrayIterator& rhs) const
    {
        return p != rhs.p;
    }

    // 解引用运算符重载，获取当前指针指向的元素值
    int& operator*() 
    {
        return *p;
    }
};

int main() 
{
    // 创建一个整数数组
    int arr[] = { 1, 2, 3, 4, 5 };

    // 创建两个迭代器，分别指向数组的起始位置和结束位置
    IntArrayIterator begin(arr);
    IntArrayIterator end(arr + 5);

    // 使用自定义迭代器遍历数组元素
    for (IntArrayIterator it = begin; it != end; ++it) 
    {
        std::cout << *it << " "; // 输出当前元素值
    }
    std::cout << std::endl;

    return 0;
}
```

### string类
在C语言中，字符串是以`\0`结尾的一些字符的集合，为了操作方便，C标准库中提供了一些`str`系列的库函数，但是这些库函数与字符串是分离开的，不太符合OOP的思想，且底层空间需要用户自己管理，稍不留神可能还会越界访问。

#### 标准库中的string类
##### string类
1. `string`是管理字符数组的类。
2. `string`在底层实际是`basic_string`模板类的别名：`typedef basic_string<char, char_traits, allocator> string;`
3. 不能操作多字节或变长字符的序列。
4. 在使用`string`类时，必须包含`#include <string>`头文件，以及`using namespace std;`。

##### string类的常用接口说明
+ `s**tring**`**类对象的常见构造**

| 函数名称 | 功能说明 |
| :---: | :---: |
| `**string()**` | **构造空的**`**string**`**类对象，即空字符串。** |
| `**string(const char* s)**` | **用**`**C-string**`**来构造**`**string**`**类对象。** |
| `string(size_t n, char c)` | `string`类对象中包含n个字符c。 |
| `**string(const string& s)**` | **拷贝构造函数** |


```cpp
#include <iostream>
#include <string>

int main()
{
    std::string s1;  // 默认构造函数，创建一个空字符串
    std::string s2("hello");  // 使用C字符串构造一个std::string
    std::string s3(s2);  // 拷贝构造函数，使用另一个字符串s2来构造

    // 编译器通常会对这种情况进行优化，直接调用字符串类的构造函数，而不是先创建一个临时对象然后拷贝它
    std::string s4 = "hello";  // 拷贝初始化

    std::string s5 = s2;  // 拷贝构造，将s2的内容拷贝到s5
    std::string s6(5, 'c');  // 重复字符构造函数，创建包含5个字符‘c’的字符串
    std::string s7(s2, 1, 2);  // 子字符串构造函数，提取从索引1开始长度为2的子串
    std::string s8(s2, 1, 10);  // 子字符串构造函数，尝试提取从索引1开始长度为10的子串，但字符串结尾处停止
    std::string s9(s2, 1, std::string::npos);  // 从索引1开始，提取直到结尾的子串

    // 输出字符串内容
    std::cout << s1 << std::endl;  // (空字符串)
    std::cout << s2 << std::endl;  // hello
    std::cout << s3 << std::endl;  // hello
    std::cout << s4 << std::endl;  // hello
    std::cout << s5 << std::endl;  // hello
    std::cout << s6 << std::endl;  // ccccc
    std::cout << s7 << std::endl;  // el
    std::cout << s8 << std::endl;  // ello
    std::cout << s9 << std::endl;  // ello

    return 0;
}
```

+ `**string**`**类对象的容量操作**

| 函数名称 | 功能说明 |
| :---: | :---: |
| `**size**` | **返回字符串有效字符长度。** |
| `length` | 返回字符串有效字符长度。 |
| `capacity` | 返回空间总大小。 |
| `**empty**` | **字符串是否为空，空返回**`**true**`**，否则**`**false**`**。** |
| `**clear**` | **清空有效字符。** |
| `**reserve**` | **为字符串预留空间。** |
| `**resize(size_t n, char c)**` | **将有效字符的个数改为n个，多出的空间用字符**`**c**`**填充。** |


注意：

1. `size()`与`length()`方法底层实现原理完全相同，引入`size()`的原因是为了与其他容器的接口保持一致，一般情况下都是用`size()`。
2. `**clear()**`**只是将**`**string**`**中有效字符清空，不改变底层空间大小。**
3. `**resize(size_t n)**`**与**`**resize(size_t n, char c)**`**都是将字符串中有效字符的个数改变到n个，不同的是当字符个数增多时：**`**resize(size_t n)**`**用**`**0**`**来填充多出的元素空间，**`**resize(size_t n, char c)**`**用字符**`**c**`**来填充多出的元素空间。注意：**`**resize**`**在改变元素个数时，如果是将元素个数增多，可能会改变底层容量的大小，如果是将元素个数减少，底层空间总大小不变。**
4. `**reserve(size_t res_arg = 0)**`**：为**`**string**`**预留空间，不改变有效元素个数，当**`**reserve**`**的参数小于**`**string**`**底层空间总大小时，**`**reserve**`**不会改变容量大小。**

```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    // 初始化字符串s
    string s("hello, ccc!!!");
    cout << s.size() << endl;       // 打印字符串的大小(字符个数)
    cout << s.length() << endl;     // 打印字符串的长度(与size相同)
    cout << s.capacity() << endl;   // 打印字符串的容量(底层分配的空间)
    cout << s << endl;              // 打印字符串内容

    // 清空字符串内容，但不改变底层空间的大小
    s.clear();
    cout << s.size() << endl;       // 清空后大小为0
    cout << s.capacity() << endl;   // 容量保持不变

    // 调整字符串大小为10，不足部分用字符'a'填充
    s.resize(10, 'a');
    cout << s.size() << endl;       // 新大小为10
    cout << s.capacity() << endl;   // 容量可能会增加
    cout << s << endl;              // 打印新的字符串内容

    // 调整字符串大小为15，不足部分用字符'\0'填充
    s.resize(15);
    cout << s.size() << endl;       // 新大小为15
    cout << s.capacity() << endl;   // 容量可能会增加
    cout << s << endl;              // 打印新的字符串内容

    // 调整字符串大小为5，截断多余部分
    s.resize(5);
    cout << s.size() << endl;       // 新大小为5
    cout << s.capacity() << endl;   // 容量保持不变
    cout << s << endl;              // 打印新的字符串内容

    return 0;
}
```

+ `**string**`**类对象的访问及遍历操作**

| 函数名称 | 功能说明 |
| :---: | :---: |
| `operator[]` | 返回`pos`位置的字符，`const string`类对象调用。 |
| 正向迭代器`begin + end` | `begin`指向容器第一个元素，`end`指向容器最后一个元素后的虚拟位置。 |
| 反向迭代器`rbegin + rend` | `rbegin`指向容器最后一个元素，`rend`指向容器第一个元素之前的虚拟位置。 |
| 范围`for` | C++11支持更简洁的范围`for`的新遍历方式。 |


```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    // 初始化一个字符串s
    string s("hello ccc");

    // 3种遍历string对象的方式：
    // 需要注意的是以下三种方式不仅可以遍历string对象，
    // 还可以在遍历过程中修改string中的字符。
    // 另外，对于string而言，第一种方式(for + operator[])是最常用的。

    // 1. 使用for循环和operator[]遍历，推荐使用这种方式。
    for (size_t i = 0; i < s.size(); ++i) // 使用size_t类型来处理字符串的索引
    {
        cout << s[i] << endl; // 使用operator[]获取字符串中的每个字符并输出
    }

    // 2. 使用迭代器遍历字符串
    string::iterator it = s.begin(); // 定义一个迭代器，指向字符串的开头
    while (it != s.end()) // 当迭代器没有到达字符串的末尾时，继续循环
    {
        cout << *it << endl; // 输出迭代器指向的当前字符
        ++it; // 迭代器移动到下一个字符
    }

    // 3. 使用反向迭代器从字符串末尾向前遍历
    // C++11之后，使用auto自动推导迭代器的类型
    auto rit = s.rbegin(); // 定义一个反向迭代器，指向字符串的末尾
    while (rit != s.rend()) // 当反向迭代器没有到达字符串的开头时，继续循环
    {
        cout << *rit << endl; // 输出反向迭代器指向的当前字符
        ++rit; // 反向迭代器移动到前一个字符
    }

    // 4. 使用范围for循环遍历字符串
    for (auto ch : s) // 使用auto自动推导字符类型
    {
        cout << ch << endl; // 输出当前字符
    }

    return 0;
}
```

```cpp
#include <iostream>
#include <string>

using namespace std;

// 将字符串转换为整数的函数
int StringToInt(const string& str)
{
    int n_value = 0;  // 初始化整数值为0
    string::const_iterator it = str.begin();  // 获取字符串的迭代器

    // 遍历字符串中的每个字符
    while (it != str.end())
    {
        // 如果字符不是数字字符，抛出异常
        if (*it < '0' || *it > '9')
        {
            throw invalid_argument("输入字符串包含非数字字符");  // 抛出异常，提示字符串包含非数字字符
        }

        n_value *= 10;  // 当前整数值乘以10，为下一位数字留出空间
        n_value += *it - '0';  // 将当前字符转换为对应的数字，并加到整数值上
        ++it;  // 移动到下一个字符
    }

    return n_value;  // 返回转换后的整数值
}

int main()
{
    string s("1234");  // 要转换的字符串

    try
    {
        cout << StringToInt(s) << endl;  // 调用函数并输出结果
    }
    catch (const invalid_argument& e)
    {
        cout << "错误: " << e.what() << endl;  // 捕捉异常并输出错误信息
    }

    return 0;
}
```

+ `**string**`**类对象的修改操作**

| 函数名称 | 功能说明 |
| :---: | :---: |
| `push_back` | 在字符串后尾插字符`c`。 |
| `append` | 在字符串后追加一个字符串。 |
| `operator+=` | 在字符串后追加字符串`str`。 |
| `c_str` | 返回C格式字符串。 |
| `find + npos` | 从字符串`pos`位置开始往后找字符`c`，返回该字符在字符串中的位置。 |
| `rfind` | 从字符串`pos`位置开始往前找字符`c`，返回该字符在字符串中的位置。 |
| `substr` | 在`str`中从`pos`位置开始，截取n个字符，然后将其返回。 |


注意：

1. **在**`**string**`**尾部追加字符时，**`**s.push_back('c')**`**、**`**s.append(1, 'c')**`**、**`**s += 'c'**`**三种方法的实现方式差不多，一般情况下**`**string**`**类**`**+=**`**操作用的比较多，**`**+=**`**操作不仅可连接单个字符，还可以连接字符串。**
2. **对**`**string**`**操作时，如果能够大概估算到放多少字符，可以先通过**`**reserve**`**把空间预留好。**

```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    string str;               // 初始化一个空字符串
    str.push_back(' ');       // 在str后插入一个空格
    str.append("hello");      // 在str后追加一个字符串"hello"
    str += 't';               // 在str后追加一个字符't'
    str += "ex";              // 在str后追加一个字符串"ex"
    cout << str << endl;      // 输出str的内容
    cout << str.c_str() << endl; // 以C语言风格输出str的内容

    // 获取文件的后缀
    string file("string.cpp"); // 定义一个文件名字符串
    size_t pos = file.rfind('.'); // 查找最后一个'.'的位置
    string suffix(file.substr(pos, file.size() - pos)); // 提取文件后缀
    cout << suffix << endl;  // 输出文件后缀

    // string::npos 是一个常量，用于表示查找失败
    // static const size_t npos = -1;

    // 提取URL中的域名
    string url("http://www.cplusplus.com/reference/string/string/find/"); // 定义一个URL字符串
    cout << url << endl;         // 输出完整的URL
    size_t start = url.find("://"); // 查找"://"的位置
    if (start == string::npos)   // 如果没有找到"://"，则URL无效
    {
        cout << "invalid url" << endl; // 输出无效URL信息
        return 0;
    }
    start += 3;                  // 跳过"://"部分，指向域名开始位置
    size_t finish = url.find('/', start); // 查找域名后的第一个'/'的位置
    string address = url.substr(start, finish - start); // 提取域名
    cout << address << endl;     // 输出提取的域名

    // 删除URL的协议前缀
    pos = url.find("://");       // 查找"://"的位置
    url.erase(0, pos + 3);       // 删除从0到"://"之后的内容
    cout << url << endl;         // 输出删除协议后的URL

    return 0;
}

```

```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    string s("hello");
    s += '\0';
    s += " world";

    cout << s << endl;          // 将对象数组中所有字符都输出，hello world
    cout << s.c_str() << endl;  // 输出C风格，遇到\0就结束，hello

    return 0;
}
```

以上代码的输出结果，我们可以知道：

:::color2
1. `**std::string**`**对象可以存储空字符，并且不会将其视为字符串的终止符。**
2. `**c_str()**`**将**`**std::string**`**转换为以空字符结尾的C风格字符串，遇到第一个**`**\0**`**处停止输出。**

:::

+ `**string**`**类非成员函数**

| 函数 | 功能 |
| :---: | :---: |
| `operator+` | 尽量少用因为传值返回，导致深拷贝效率低。 |
| `operator>>` | 输入运算符重载。 |
| `operator<<` | 输出运算符重载。 |
| `getline` | 获取一行字符串。 |
| `relational operators` | 大小比较。 |


+ `**VS**`**与**`**g++**`**下**`**string**`**的结构(32位)**
    - `VS`下`string`的结构，`string`总共占28个字节，显式有一个联合体，联合体用来定义`string`中字符串的存储空间：当字符串长度小于16时，使用内部固定的字符数组来存放；当字符串长度大于等于16时，从堆上开辟空间。

```cpp
union _Bxty
{
    // storage for small buffer or pointer to larger one
    value_type _Buf[_BUF_SIZE];
    pointer _Ptr;
    char _Alias[_BUF_SIZE];  // to permit aliasing
} _Bx;
```

这种设计的想法是大多数情况下字符串的长度都小于16，那`string`对象创建好后，内部已经有了16个字符数组的固定空间，不需要通过堆创建，效率高。其次，还有一个`**size_t**`**字段保存字符串长度，一个**`**size_t**`**字段保存从堆上开辟空间的总容量**。最后，**一个指针**做其他事情处理。所以占用16+4+4+4=28个字节。例如`string s1("hello world");`，`s1`对象的结构为以下：

![](https://cdn.nlark.com/yuque/0/2024/png/36162499/1721787944625-1eb2ea66-eb2e-4c89-b6c7-d3c3c9b1e884.png)

其中，这里所见的结构并非是`string`真正的结构，只是`VS`为了方便大家理解而进行了优化，要查看真正的结构，是在原始视图中查看：

![](https://cdn.nlark.com/yuque/0/2024/png/36162499/1721788399989-e787f87a-2171-4f27-93e0-63fa8714bdb1.png)

其中，`_Myproxy`为指针类型`std::_Container_proxy *`，`_Bx`为联合体，`_Mysize`为字符串有效长度`size_t`，`_Myres`为空间容量`size_t`。

    - `g++`下，`string`是通过写时拷贝实现的，`string`对象总共占4个字节，内部只包含了一个指针，该指针将来指向一块堆空间，内容包含空间总大小、字符串有效长度、引用计数、指向堆空间的指针(存储字符串)：

```cpp
struct _Rep_base
{
    size_type     _M_length;
    size_type     _M_capacity;
    _Atomic_word  _M_refcount;
};
```

##### 练习
1. [仅仅反转字母。](https://leetcode.cn/problems/reverse-only-letters/description/)

```cpp
#include <iostream>
#include <string>
#include <algorithm> // 用于 swap 函数

using namespace std;

class Solution 
{
public:
    // 检查字符是否为字母
    bool IsChar(char ch)
    {
        return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
    }

    // 反转字符串中的字母，仅字母会被反转
    string reverseOnlyLetters(string s) 
    {
        int begin = 0; // 从字符串的开头开始
        int end = s.size() - 1; // 从字符串的结尾开始

        // 进行反转操作
        while (begin < end) 
        {
            // 找到下一个字母字符
            while (begin < end && !IsChar(s[begin]))
            {
                ++begin;
            }

            // 找到上一个字母字符
            while (begin < end && !IsChar(s[end])) 
            {
                --end;
            }

            // 交换字母
            swap(s[begin], s[end]);
            ++begin;
            --end;
        }

        return s;
    }
};

int main() 
{
    Solution sol;

    // 示例输入
    string s = "ab-cd";

    // 调用 reverseOnlyLetters 函数并输出结果
    string result = sol.reverseOnlyLetters(s);
    cout << "Reversed letters: " << result << endl; // 输出应为 "dc-ba"
    
    return 0;
}
```

2. [字符串中的第一个唯一字符。](https://leetcode.cn/problems/first-unique-character-in-a-string/description/)

```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Solution
{
public:
    // 返回字符串中第一个唯一字符的索引
    int firstUniqChar(string s) 
    {
        // 用于统计每个字符的出现次数，假设字符只包括小写字母
        int count[26] = { 0 };

        // 统计每个字符的出现次数
        for (auto ch : s)
        {
            count[ch - 'a']++;
        }

        // 查找第一个唯一字符的索引
        for (size_t i = 0; i < s.size(); ++i) 
        {
            // 如果字符的出现次数为 1，则返回其索引
            if (count[s[i] - 'a'] == 1) 
            {
                return i;
            }
        }

        // 如果没有唯一字符，则返回 -1
        return -1;
    }
};

int main()
{
    Solution sol;

    // 示例输入
    string s = "leetcode";

    // 调用 firstUniqChar 函数并输出结果
    int result = sol.firstUniqChar(s);
    cout << "Index of first unique character: " << result << endl; // 输出应为 0(字符 'l')

    // 另一个示例输入
    s = "loveleetcode";
    result = sol.firstUniqChar(s);
    cout << "Index of first unique character: " << result << endl; // 输出应为 2(字符 'v')

    // 另一个示例输入
    s = "aabb";
    result = sol.firstUniqChar(s);
    cout << "Index of first unique character: " << result << endl; // 输出应为 -1(没有唯一字符)

    return 0;
}
```

3. [字符串最后一个单词的长度。](https://www.nowcoder.com/practice/8c949ea5f36f422594b306a2300315da?tpId=37&&tqId=21224&rp=5&ru=/activity/oj&qru=/ta/huawei/question-ranking)

```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    string s;
    getline(cin, s);  // 从输入中读取整行字符串，包括空格和换行符，不能用cin >> s

    size_t pos = s.rfind(' ');  // 查找字符串中最后一个空格字符的位置
    cout << s.size() - (pos + 1) << endl;  // 输出最后一个单词的长度

    return 0;
}
```

4. [验证回文串。](https://leetcode.cn/problems/valid-palindrome/description/)

```cpp
#include <iostream>
#include <string>

using namespace std;

class Solution
{
public:
    // 判断字符是否为小写字母或数字
    bool IsCharOrNumber(char ch)
    {
        if ((ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9'))
        {
            return true;  // 如果是小写字母或数字，返回 true
        }
        else
        {
            return false; // 否则返回 false
        }
    }

    // 判断字符串是否为回文串
    bool IsPalindrome(string s)
    {
        // 将字符串中所有的大写字母转换为小写
        for (auto& ch : s)  // 使用引用，直接修改原字符串
        {
            if (ch >= 'A' && ch <= 'Z')
            {
                ch += 32;  // 将大写字母转换为对应的小写字母
            }
        }

        int begin = 0;  // 指向字符串的起始位置
        int end = s.size() - 1;  // 指向字符串的结束位置

        while (begin < end)
        {
            // 跳过字符串开头的非字母数字字符
            while ((begin < end) && !IsCharOrNumber(s[begin]))
            {
                ++begin;
            }

            // 跳过字符串结尾的非字母数字字符
            while ((begin < end) && !IsCharOrNumber(s[end]))
            {
                --end;
            }

            // 如果字符不相等，字符串不是回文串
            if (s[begin] != s[end])
            {
                return false;
            }
            else
            {
                ++begin;  // 移动起始指针
                --end;    // 移动结束指针
            }
        }

        return true;  // 如果所有字符都匹配，字符串是回文串
    }
};

int main()
{
    // 示例使用
    Solution sol;
    string testStr = "A man, a plan, a canal: Panama";
    cout << (sol.IsPalindrome(testStr) ? "Yes, it's a palindrome." : "No, it's not a palindrome.") << endl;

    return 0;
}
```

5. [字符串相加。](https://leetcode.cn/problems/add-strings/description/)

```cpp
#include <iostream>
#include <string>
#include <algorithm> // 用于 reverse 函数

using namespace std;

class Solution 
{
public:
    string addStrings(string num1, string num2) 
    {
        string answer;
        int cur = 0; // 用于存储每一位的和以及进位
        int len1 = num1.size() - 1; // num1 的索引，从最后一位开始
        int len2 = num2.size() - 1; // num2 的索引，从最后一位开始

        // 从两个字符串的末尾开始处理每一位数字
        while (len1 >= 0 || len2 >= 0 || cur > 0)
        {
            // 如果 num1 中还有数字，则将其加入当前和
            if (len1 >= 0) 
            {
                cur += num1[len1--] - '0'; // 将字符转为数字并加到 cur 中
            }
            // 如果 num2 中还有数字，则将其加入当前和
            if (len2 >= 0) 
            {
                cur += num2[len2--] - '0'; // 将字符转为数字并加到 cur 中
            }
            // 将当前和的个位数添加到结果字符串
            answer += to_string(cur % 10); // 结果字符串是逆序的
            cur = cur / 10; // 更新进位
        }
        // 逆序结果字符串以得到正确的结果
        reverse(answer.begin(), answer.end());
        return answer;
    }
};

int main() 
{
    Solution sol;

    // 示例输入
    string num1 = "123";
    string num2 = "456";

    // 调用 addStrings 函数并输出结果
    string result = sol.addStrings(num1, num2);
    cout << "Result: " << result << endl; // 输出应为 "579"

    return 0;
}
```

#### string类的模拟实现
##### 浅拷贝
:::color2
**浅拷贝也叫位拷贝，编译器只是将对象中的值拷贝过来。如果对象中管理资源，最后就会导致多个对象共享同一份资源，当一个对象销毁时就会将该资源释放掉，而此时另一些对象不知道该资源已经被释放，以为还有效，当继续对资源进行操作时，就会发生访问违规。浅拷贝的典型问题有：资源共享、悬空指针、多重释放。**

:::

```cpp
#include <iostream>
#include <cstring>

class ShallowCopyExample 
{
public:
    char* data;

    // 构造函数
    ShallowCopyExample(const char* initData)
    {
        data = new char[strlen(initData) + 1];
        strcpy(data, initData);
    }

    // 浅拷贝构造函数(编译器默认生成的)
    ShallowCopyExample(const ShallowCopyExample& other) 
    {
        data = other.data;
    }

    // 析构函数
    ~ShallowCopyExample() 
    {
        delete[] data;
    }

    void printData() const 
    {
        std::cout << data << std::endl;
    }
};

int main() 
{
    ShallowCopyExample obj1("Hello, World!");
    ShallowCopyExample obj2 = obj1; // 浅拷贝

    obj1.printData(); // 输出: Hello, World!
    obj2.printData(); // 输出: Hello, World!

    return 0; // 这里会导致问题
}
```

在这个示例中，当`main`函数结束时，`obj1`和`obj2`都会调用析构函数，导致`delete[] data`被调用两次，这就是双重释放错误。为了避免这些问题，需要实现深拷贝。  

##### 深拷贝
:::color2
 **深拷贝是在复制对象时，不仅复制对象的所有成员变量的值，还复制对象可能拥有的动态分配的资源。深拷贝确保每个对象都有自己独立的资源副本，而不是共享同一个资源。因此，深拷贝避免了浅拷贝所带来的资源管理问题，如悬空指针和多重释放。**

:::

在C++中，实现深拷贝的关键在于提供一个拷贝构造函数和一个重载的赋值运算符(如果对象可以被赋值)，以确保在复制对象时也会复制动态分配的内存或其他资源。如果一个类中涉及到资源的管理，其拷贝构造函数、赋值运算符重载以及析构函数必须要显式给出。

```cpp
#include <iostream>
#include <cstring>

class DeepCopyExample
{
public:
    char* data;

    // 构造函数
    DeepCopyExample(const char* initData)
    {
        data = new char[strlen(initData) + 1];
        strcpy(data, initData);
    }

    // 深拷贝构造函数
    DeepCopyExample(const DeepCopyExample& other)
    {
        data = new char[strlen(other.data) + 1];
        strcpy(data, other.data);
    }

    // 赋值运算符重载，确保赋值时也进行深拷贝
    DeepCopyExample& operator=(const DeepCopyExample& other)
    {
        if (this == &other)
        {
            return *this; // 处理自我赋值
        }
        delete[] data; // 释放已有资源
        data = new char[strlen(other.data) + 1];
        strcpy(data, other.data);
        return *this;
    }

    // 析构函数
    ~DeepCopyExample() 
    {
        delete[] data;
    }

    void printData() const 
    {
        std::cout << data << std::endl;
    }
};

int main() 
{
    DeepCopyExample obj1("Hello, World!");
    DeepCopyExample obj2 = obj1; // 深拷贝

    obj1.printData(); // 输出: Hello, World!
    obj2.printData(); // 输出: Hello, World!

    return 0;
}
```

在这个示例中，每次复制对象时，都会分配新的内存并复制实际的数据内容。这样，`obj1`和`obj2`分别拥有自己的内存空间，不会互相影响，避免了浅拷贝带来的资源管理问题。  

##### 模拟实现`string`类简化版
模拟实现`string`类，我们先写出大致框架，支持有参和无参的字符数组对象：

```cpp
namespace String
{
    class String
    {
    public:
        // 无参构造函数
        String()
            : _str_(nullptr)
        {}

        // 带参构造函数
        String(char* str)
            : _str_(str) // 将const char*转换为char*
        {}

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参
    }
}
```

```cpp
#include <iostream>
#include "String.hpp"

using namespace std;

int main()
{
    String::test_string1();

    return 0;
}
```

此时提示无法匹配参数列表，因为字符串`hello`是`const char*`类型，而构造函数参数列表的形参是`char*`，属于权限放大，所以改进`String.hpp`：

```cpp
namespace String
{
    class String
    {
    public:
        // 无参构造函数
        String()
            : _str_(nullptr)
        {}

        // 带参构造函数
        String(const char* str)
            : _str_(const_cast<char*>(str)) // const_cast<char*>(str)用于将const char*转换为char*
        {}

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参
    }
}
```

这样真的可以吗？我们继续增加两个成员函数，分别是获取字符数组长度的函数与返回数组中第`i`个字符的别名的函数，然后在测试函数`test_string1`中调用两个函数以遍历字符数组中的元素：

```cpp
namespace String
{
    class String
    {
    public:
        // 无参构造函数
        String()
            : _str_(nullptr)
        {}

        // 带参构造函数
        String(const char* str)
            : _str_(const_cast<char*>(str)) // const_cast<char*>(str)用于将const char*转换为char*
        {}

        // 获取字符数组的长度
        size_t size()
        { 
            return strlen(_str_);  
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，可读取也可修改  
        {
            return _str_[i];
        }

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        for (size_t i = 0; i < s1.size(); ++i)
        {
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;
    }
}
```

以上代码运行符合预期，但不存在其他问题了吗？若在遍历数组元素代码之前写入代码`s1[i] += 1`呢：

```cpp
namespace String
{
    class String
    {
    public:
        // 无参构造函数
        String()
            : _str_(nullptr)
        {}

        // 带参构造函数
        String(const char* str)
            : _str_(const_cast<char*>(str)) // const_cast<char*>(str)用于将const char*转换为char*
        {}

        // 获取字符数组的长度
        size_t size()
        { 
            return strlen(_str_);  
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2// 无参

        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;
    }
}
```

运行代码后崩溃了，调试运行到`s1[i] += 1`处时报内存错误："0x007F2BFB处引发的异常: 0xC0000005: 写入位置0x007F9B30时发生访问冲突"。原因为`s1`、`s2`对象是存储在栈上，而`string s1("hello")`要调用构造函数`String(const char* str)`，将`"hello"`传给了`str`，而`"hello"`常量字符串是存储在代码段中，`char& operator[](size_t i)`函数返回类型为`char&`，返回值为`_str_[i]`，即指向的是常量字符串`"hello"`的第`i`个位置的引用，而`s1[i] += 1`代码尝试让常量字符串的第`i`个位置修改，所以报错。还存在问题，如果想要在原字符串中插入字符，空间不够时应该扩容，但代码段无法扩容。解决方案是什么呢？在堆上开空间是我们可控的，`s1`、`s2`对象虽然存储在栈上，但对象中的指针指向的堆上的空间，将常量字符串`"hello"`拷贝进去。所以我们对构造函数进行修改：

```cpp
namespace String
{
    class String
    {
    public:
        // 无参构造函数
        String()
            : _str_(nullptr)
        {}

        // 带参构造函数
        String(const char* str)
        {
            // 如果传入的字符串指针非空(即str不为nullptr)
            if (str) 
            {
                // 为字符串分配新内存，大小为传入字符串的长度加1(用于存储终止符'\0')
                _str_ = new char[strlen(str) + 1];

                // 将传入的字符串内容复制到新分配的内存中
                strcpy(_str_, str);
            }

            // 如果传入的字符串指针为空(即str为nullptr)
            else 
            {
                // 将内部字符串指针设为nullptr
                _str_ = nullptr;
            }
        }

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参
    }
}
```

此时可以正常遍历字符数组内容，若对空字符数组对象`s2`进行遍历呢？

```cpp

```

运行发现，程序又崩溃！原因为遍历对象`s2`时，`s2`调用其成员函数`size()`，函数内部`strlen`函数要对`_str_`解引用直到遇到`\0`，但`_str_`为`nullptr`，所以为空指针！所以修改无参构造函数：

```cpp
namespace String
{
    class String
    {
    public:
        // 无参构造函数
        String()
            : _str_(new char[1])
        {
            _str_[0] = '\0';
        }

        // 带参构造函数
        String(const char* str)
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }
}
```

可以将无参构造函数和带参构造函数合并成全缺省构造函数：

```cpp
namespace String
{
    class String
    {
    public:
        //// 无参构造函数
        //String()
        //    : _str_(new char[1])
        //{
        //    _str_[0] = '\0';
        //}

        //// 带参构造函数
        //String(const char* str)
        //    : _str_(new char[strlen(str) + 1])
        //{
        //    strcpy(_str_, str);
        //}

        // 全缺省构造函数
        String(const char* str = "")
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }
}
```

最后还需要清理空间，完成析构函数的编写：

```cpp
namespace String
{
    class String
    {
    public:
        //// 无参构造函数
        //String()
        //    : _str_(new char[1])
        //{
        //    _str_[0] = '\0';
        //}

        //// 带参构造函数
        //String(const char* str)
        //    : _str_(new char[strlen(str) + 1])
        //{
        //    strcpy(_str_, str);
        //}

        // 全缺省构造函数
        String(const char* str = "")
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 析构函数
        ~String()
        {
            delete[] _str_;
            _str_ = nullptr;
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

    private:
        char* _str_;
    };

    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }
}
```

到此，我们完成了最基础的功能，在字符串对象的使用过程中，我们经常会用一个字符串对象拷贝构造出新的字符串对象。为了方便输出字符串内容，我们实现一个成员函数`c_str()`，然后尝试用拷贝构造方式获得新的字符串对象：

```cpp
namespace String
{
    class String
    {
    public:
        //// 无参构造函数
        //String()
        //    : _str_(new char[1])
        //{
        //    _str_[0] = '\0';
        //}

        //// 带参构造函数
        //String(const char* str)
        //    : _str_(new char[strlen(str) + 1])
        //{
        //    strcpy(_str_, str);
        //}

        // 全缺省构造函数
        String(const char* str = "")
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 析构函数
        ~String()
        {
            delete[] _str_;
            _str_ = nullptr;
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

        // 返回字符串
        const char* c_str()
        {
            return _str_;
        }

    private:
        char* _str_;
    };

    // 测试1：遍历
    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }

    // 测试2：拷贝构造
    void test_string2()
    {
        String s1("hello");
        String s2(s1);

        std::cout << s1.c_str() << std::endl;
        std::cout << s2.c_str() << std::endl;
    }
}
```

并且将`test.cc`中的测试代码注释，添加新的测试代码：

```cpp
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include "String.hpp"

using namespace std;

int main()
{
    // String::test_string1();
    String::test_string2();

    return 0;
}
```

运行崩溃，但字符串内容成功打印出来。崩溃的原因是浅拷贝，`s1`和`s2`对象公用同一块空间，当测试函数结束时，需要将`s1`和`s2`销毁，先销毁`s2`，后销毁`s1`，`s2`将其所指向的空间释放掉，`s2`对象成功销毁，但`s1`对象中的指针成为也指针，`s1`对象进行析构时，同一块空间被多次释放而引起程序崩溃。所以，应该再开一个同样大小的空间，将字符串拷贝到新空间，新的对象的指针是指向新开的空间，这样就能避免崩溃：

```cpp
namespace String
{
    class String
    {
    public:
        //// 无参构造函数
        //String()
        //    : _str_(new char[1])
        //{
        //    _str_[0] = '\0';
        //}

        //// 带参构造函数
        //String(const char* str)
        //    : _str_(new char[strlen(str) + 1])
        //{
        //    strcpy(_str_, str);
        //}

        // 全缺省构造函数
        String(const char* str = "")
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 拷贝构造string s2(s1)，深拷贝
        String(const String& s)
            : _str_(new char[strlen(s._str_) + 1])
        {
            strcpy(_str_, s._str_);
        }

        // 析构函数
        ~String()
        {
            delete[] _str_;
            _str_ = nullptr;
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

        // 返回字符串
        const char* c_str()
        {
            return _str_;
        }

    private:
        char* _str_;
    };

    // 测试1：遍历
    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }

    // 测试2：拷贝构造
    void test_string2()
    {
        String s1("hello");
        String s2(s1);

        std::cout << s1.c_str() << std::endl;
        std::cout << s2.c_str() << std::endl;
    }
}
```

如果想进行对象的赋值呢？能否正常赋值：

```cpp
namespace String
{
    class String
    {
    public:
        //// 无参构造函数
        //String()
        //    : _str_(new char[1])
        //{
        //    _str_[0] = '\0';
        //}

        //// 带参构造函数
        //String(const char* str)
        //    : _str_(new char[strlen(str) + 1])
        //{
        //    strcpy(_str_, str);
        //}

        // 全缺省构造函数
        String(const char* str = "")
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 拷贝构造string s2(s1)，深拷贝
        String(const String& s)
            : _str_(new char[strlen(s._str_) + 1])
        {
            strcpy(_str_, s._str_);
        }

        // 析构函数
        ~String()
        {
            delete[] _str_;
            _str_ = nullptr;
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

        // 返回字符串
        const char* c_str()
        {
            return _str_;
        }

    private:
        char* _str_;
    };

    // 测试1：遍历
    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }

    // 测试2：拷贝构造
    void test_string2()
    {
        String s1("hello");
        String s2(s1);

        std::cout << s1.c_str() << std::endl;
        std::cout << s2.c_str() << std::endl;
    }

    // 测试3：赋值
    void test_string3()
    {
        String s1("hello");
        String s2;
        s2 = s1;  // 赋值

        std::cout << s1.c_str() << std::endl;
        std::cout << s2.c_str() << std::endl;
    }
}
```

同样，更改`test.cc`的测试代码：

```cpp
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include "String.hpp"

using namespace std;

int main()
{
    // String::test_string1();
    // String::test_string2();
    String::test_string3();

    return 0;
}
```

运行后同样崩溃，原因为拷贝构造与赋值相同，默认为浅拷贝。我们需要自己手动实现赋值运算符重载：

```cpp
namespace String
{
    class String
    {
    public:
        //// 无参构造函数
        //String()
        //    : _str_(new char[1])
        //{
        //    _str_[0] = '\0';
        //}

        //// 带参构造函数
        //String(const char* str)
        //    : _str_(new char[strlen(str) + 1])
        //{
        //    strcpy(_str_, str);
        //}

        // 全缺省构造函数
        String(const char* str = "")
            : _str_(new char[strlen(str) + 1])
        {
            strcpy(_str_, str);
        }

        // 拷贝构造string s2(s1)，深拷贝
        String(const String& s)
            : _str_(new char[strlen(s._str_) + 1])
        {
            strcpy(_str_, s._str_);
        }

        // s2 = s1，赋值运算符重载operator=
        String& operator=(const String& s)
        {
            // 防止自我赋值
            if (this != &s)
            {
                char* tmp = new char[strlen(s._str_) + 1];  // 先开一个同样大小的空间s1
                strcpy(tmp, s._str_);  // 将值拷贝过去
                delete[] _str_;  // 释放s1空间
                _str_ = tmp;  // 指向新的空间
            }

            return *this;
        }

        // 析构函数
        ~String()
        {
            delete[] _str_;
            _str_ = nullptr;
        }

        // 获取字符数组的长度
        size_t size()
        {
            return strlen(_str_);
        }

        // 返回字符数组里第i个字符的别名
        char& operator[](size_t i) // 返回引用，便于修改  
        {
            return _str_[i];
        }

        // 返回字符串
        const char* c_str()
        {
            return _str_;
        }

    private:
        char* _str_;
    };

    // 测试1：遍历
    void test_string1()
    {
        String s1("hello");  // 带参
        String s2;           // 无参

        // 遍历s1
        for (size_t i = 0; i < s1.size(); ++i)
        {
            s1[i] += 1;
            std::cout << s1[i] << " ";
        }
        std::cout << std::endl;

        // 遍历s2
        for (size_t i = 0; i < s2.size(); ++i)
        {
            s2[i] += 1;
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;
    }

    // 测试2：拷贝构造
    void test_string2()
    {
        String s1("hello");
        String s2(s1);

        std::cout << s1.c_str() << std::endl;
        std::cout << s2.c_str() << std::endl;
    }

    // 测试3：赋值
    void test_string3()
    {
        String s1("hello");
        String s2;
        s2 = s1;  // 赋值

        std::cout << s1.c_str() << std::endl;
        std::cout << s2.c_str() << std::endl;
    }
}
```

我们模拟暂时进行到此，后续还有很多接口可扩展！

##### String类传统版
```cpp
#include <iostream>
#include <cstring>
#include <cassert>

class String
{
public:
    // 构造函数：根据传入的C字符串初始化String对象
    String(const char* str = "")
    {
        // 处理传递nullptr指针的情况
        if (nullptr == str)
        {
            assert(false); // 断言失败，提示错误
            return;
        }

        // 分配内存并复制传入的字符串
        _str_ = new char[strlen(str) + 1];
        strcpy(_str_, str);
    }

    // 拷贝构造函数：创建String对象的深拷贝
    String(const String& s)
        : _str_(new char[strlen(s._str_) + 1]) // 分配内存
    {
        strcpy(_str_, s._str_); // 复制字符串内容
    }

    // 赋值运算符重载：确保赋值操作时进行深拷贝
    String& operator=(const String& s)
    {
        if (this != &s) // 防止自我赋值
        {
            // 分配新的内存并复制字符串内容
            char* p_str = new char[strlen(s._str_) + 1];
            strcpy(p_str, s._str_);

            // 释放旧的内存
            delete[] _str_;

            // 更新指针指向新内存
            _str_ = p_str;
        }

        return *this; // 返回当前对象的引用
    }

    // 析构函数：释放动态分配的内存，防止内存泄漏
    ~String()
    {
        if (_str_)
        {
            delete[] _str_; // 释放内存
            _str_ = nullptr; // 防止悬空指针
        }
    }

private:
    char* _str_; // 字符串指针，用于存储字符串内容
};
```

##### String类现代版
```cpp
#include <iostream>
#include <cstring>
#include <cassert>
#include <utility> // for std::swap

class String
{
public:
    // 默认构造函数：根据传入的C字符串初始化String对象
    String(const char* str = "")
    {
        // 处理传递nullptr指针的情况
        if (nullptr == str)
        {
            assert(false); // 断言失败，提示错误
            return;
        }

        // 分配内存并复制传入的字符串
        _str_ = new char[strlen(str) + 1];
        strcpy(_str_, str);
    }

    // 拷贝构造函数：使用copy-and-swap习惯用法实现深拷贝
    String(const String& s)
        : _str_(nullptr) // 初始化为nullptr
    {
        String str_tmp(s._str_); // 使用传入的字符串创建临时对象
        std::swap(_str_, str_tmp._str_); // 交换临时对象的字符串指针和当前对象的字符串指针
    }

    // 赋值运算符重载：使用copy-and-swap习惯用法实现深拷贝赋值
    String& operator=(String s) // 使用传值方式传递参数
    {
        std::swap(_str_, s._str_); // 交换当前对象和传入对象的字符串指针
        return *this; // 返回当前对象的引用
    }

    // 使用标准的赋值运算符重载实现深拷贝赋值
    /*String& operator=(const String& s)
    {
        if (this != &s) // 防止自我赋值
        {
            String str_tmp(s); // 使用拷贝构造函数创建临时对象
            std::swap(_str_, str_tmp._str_); // 交换当前对象和临时对象的字符串指针
        }
        return *this; // 返回当前对象的引用
    }*/

    // 析构函数：释放动态分配的内存，防止内存泄漏
    ~String()
    {
        if (_str_)
        {
            delete[] _str_; // 释放内存
            _str_ = nullptr; // 防止悬空指针
        }
    }

private:
    char* _str_; // 字符串指针，用于存储字符串内容
};
```

+ `**String& operator=(String s)**`：
    - 这是现代C++中的常见技术，使用传值参数结合`swap`实现赋值运算符。
    - 优点：利用参数传值创建一个临时对象，避免显式的深拷贝，实现简单而且安全。
    - 缺点：在某些情况下，可能会有轻微的性能开销，因为涉及到额外的对象拷贝。
+ `**String& operator=(const String& s)**`：
    - 这是传统的实现方法，通过显式地检查自我赋值，然后使用拷贝构造函数创建临时对象。
    - 优点：直接明了。
    - 缺点：代码稍显冗长，现代C++社区更倾向于第一种方式。

##### 写时拷贝
 写时拷贝是一种优化技术，用于延迟或避免实际的对象复制，直到该对象被修改为止。这种技术在共享资源的情况下特别有用，可以提高性能并节省内存。写时拷贝的核心思想是多个对象可以共享同一个资源(如内存块)，直到其中一个对象需要修改该资源时，才进行实际的复制操作。   

写时拷贝的工作原理：

+ **初始化**：多个对象共享同一个资源，并且都指向同一个内存块。引用计数用于跟踪有多少对象共享这个资源。
+ **读取**：任何对象对资源的读取操作都是安全的，因为资源没有被修改。
+ **写入**：当某个对象需要修改资源时，会检查引用计数：
    - 如果引用计数大于1，表示资源被多个对象共享，此时进行实际的复制操作(深拷贝)，然后该对象修改其独立副本，引用计数减少。
    - 如果引用计数等于1，表示资源没有被其他对象共享，可以直接修改资源而无需复制。

```cpp
#include <iostream>
#include <cstring>
#include <cassert>

class String
{
public:
    // 默认构造函数：根据传入的C字符串初始化String对象
    String(const char* str = "")
    {
        if (nullptr == str) // 处理传递nullptr指针的情况
        {
            assert(false); // 断言失败，提示错误
            return;
        }

        // 分配内存并复制传入的字符串
        _str_ = new char[strlen(str) + 1];
        strcpy(_str_, str);
        _ref_count_ = new int(1); // 初始化引用计数为1
    }

    // 拷贝构造函数：增加引用计数，共享同一个字符串
    String(const String& s)
        : _str_(s._str_), _ref_count_(s._ref_count_)
    {
        ++(*_ref_count_); // 增加引用计数
    }

    // 赋值运算符重载：增加引用计数，共享同一个字符串
    String& operator=(const String& s)
    {
        if (this != &s) // 防止自我赋值
        {
            // 先减少当前对象的引用计数
            if (--(*_ref_count_) == 0)
            {
                delete[] _str_; // 如果引用计数为0，释放内存
                delete _ref_count_; // 释放引用计数指针
            }

            // 复制资源和引用计数
            _str_ = s._str_;
            _ref_count_ = s._ref_count_;
            ++(*_ref_count_); // 增加新的引用计数
        }
        return *this; // 返回当前对象的引用
    }

    // 修改字符串内容的方法：实现写时拷贝
    void set_value(const char* str)
    {
        if (--(*_ref_count_) == 0) // 先减少引用计数
        {
            delete[] _str_; // 如果引用计数为0，释放内存
            delete _ref_count_; // 释放引用计数指针
        }
        else // 如果引用计数大于0，表示有其他对象共享资源
        {
            _str_ = new char[strlen(str) + 1]; // 分配新的内存
            strcpy(_str_, str); // 复制新的字符串
            _ref_count_ = new int(1); // 初始化新的引用计数
        }
    }

    // 析构函数：减少引用计数，如果为0则释放资源
    ~String()
    {
        if (--(*_ref_count_) == 0) // 减少引用计数
        {
            delete[] _str_; // 如果引用计数为0，释放内存
            delete _ref_count_; // 释放引用计数指针
        }
    }

    // 打印字符串内容的方法
    void print() const
    {
        std::cout << _str_ << std::endl;
    }

private:
    char* _str_; // 字符串指针，用于存储字符串内容
    int* _ref_count_; // 引用计数指针，用于跟踪共享的对象数量
};

int main()
{
    String s1("Hello");
    String s2 = s1; // 共享资源，引用计数增加

    s1.print(); // 输出: Hello
    s2.print(); // 输出: Hello

    s2.set_value("World"); // s2 修改内容，触发写时拷贝

    s1.print(); // 输出: Hello
    s2.print(); // 输出: World

    return 0;
}
```

##### 模拟实现string类
```cpp
#pragma once
#include <iostream>
#include <cstring>
#include <cassert>

namespace String
{
    class String
    {
    public:
        // 迭代器类型定义
        typedef char* iterator;

        // 返回指向字符串起始位置的迭代器
        iterator begin()
        {
            return _str_;
        }

        // 返回指向字符串末尾(\0)的迭代器
        iterator end()
        {
            return _str_ + _size_;
        }

        // 默认构造函数和带参构造函数
        String(const char* str = "")
        {
            _size_ = strlen(str);              // 计算字符串长度
            _capacity_ = _size_;               // 设置容量为字符串长度
            _str_ = new char[_capacity_ + 1];  // 分配内存，多一个字节用于存放\0
            strcpy(_str_, str);                // 复制字符串内容到新分配的内存
        }

        // 拷贝构造函数：深拷贝另一个String对象
        String(const String& other)
        {
            _size_ = other._size_;                // 复制字符串长度
            _capacity_ = other._capacity_;        // 复制容量
            _str_ = new char[_capacity_ + 1];     // 分配内存
            strcpy(_str_, other._str_);           // 复制字符串内容
        }

        // 赋值运算符：处理自我赋值，并进行深拷贝
        String& operator=(const String& other)
        {
            if (this != &other)  // 防止自我赋值
            {
                delete[] _str_;  // 释放旧内存

                _size_ = other._size_;              // 复制字符串长度
                _capacity_ = other._capacity_;      // 复制容量
                _str_ = new char[_capacity_ + 1];   // 分配新内存
                strcpy(_str_, other._str_);         // 复制字符串内容
            }
            return *this;
        }

        // 返回字符串长度
        size_t size() const
        {
            return _size_;
        }

        // 返回字符串容量
        size_t capacity() const
        {
            return _capacity_;
        }

        // 下标运算符重载，返回可修改的字符引用
        char& operator[](size_t i)
        {
            assert(i < _size_);  // 确保索引有效
            return _str_[i];
        }

        // 下标运算符重载，返回不可修改的字符引用
        const char& operator[](size_t i) const
        {
            assert(i < _size_);  // 确保索引有效
            return _str_[i];
        }

        // 返回C风格的字符串
        const char* c_str() const
        {
            return _str_;
        }

        // 析构函数：释放内存
        ~String()
        {
            delete[] _str_;
            _str_ = nullptr;
            _size_ = _capacity_ = 0;
        }

        // 扩充容量至n
        void reserve(size_t n)
        {
            if (n > _capacity_)
            {
                char* new_str = new char[n + 1]; // 分配新内存
                strcpy(new_str, _str_);          // 复制旧数据到新内存
                delete[] _str_;                  // 释放旧内存
                _str_ = new_str;                 // 更新指针
                _capacity_ = n;                  // 更新容量
            }
        }

        // 调整字符串大小
        void resize(size_t n, char ch = '\0')
        {
            if (n < _size_)
            {
                _str_[n] = '\0';  // 截断字符串
                _size_ = n;       // 更新长度
            }
            else
            {
                if (n > _capacity_)
                {
                    reserve(n);  // 扩充容量
                }

                for (size_t i = _size_; i < n; ++i)
                {
                    _str_[i] = ch;  // 用指定字符填充
                }

                _size_ = n;
                _str_[_size_] = '\0';  // 添加字符串结束符
            }
        }

        // 在末尾增加一个字符
        void push_back(char ch)
        {
            if (_size_ == _capacity_)  // 如果容量已满
            {
                size_t new_capacity = _capacity_ == 0 ? 2 : _capacity_ * 2;
                reserve(new_capacity);  // 扩充容量
            }

            _str_[_size_] = ch;  // 添加字符
            ++_size_;            // 更新长度
            _str_[_size_] = '\0'; // 添加字符串结束符
        }

        // 在末尾增加一个字符串
        void append(const char* str)
        {
            size_t len = strlen(str);  // 获取新字符串的长度
            if (_size_ + len > _capacity_)
            {
                reserve(_size_ + len);  // 扩充容量
            }

            strcpy(_str_ + _size_, str);  // 追加字符串
            _size_ += len;  // 更新长度
        }

        // 重载+=操作符，追加单个字符
        String& operator+=(char ch)
        {
            this->push_back(ch);
            return *this;
        }

        // 重载+=操作符，追加字符串
        String& operator+=(const char* str)
        {
            this->append(str);
            return *this;
        }

        // 在指定位置插入单个字符
        String& insert(size_t pos, char ch)
        {
            assert(pos <= _size_);  // 确保位置有效
            if (_size_ == _capacity_)
            {
                size_t new_capacity = _capacity_ == 0 ? 2 : _capacity_ * 2;
                reserve(new_capacity);  // 扩充容量
            }

            // 移动字符为插入腾出空间
            for (size_t i = _size_; i > pos; --i)
            {
                _str_[i] = _str_[i - 1];
            }

            _str_[pos] = ch;  // 插入字符
            ++_size_;         // 更新长度
            _str_[_size_] = '\0';  // 更新字符串结束符

            return *this;
        }

        // 在指定位置插入字符串
        String& insert(size_t pos, const char* str)
        {
            assert(pos <= _size_);  // 确保位置有效

            size_t len = strlen(str);
            if (_size_ + len > _capacity_)
            {
                reserve(_size_ + len);  // 扩充容量
            }

            // 移动字符为插入腾出空间
            for (size_t i = _size_; i >= pos && i != static_cast<size_t>(-1); --i)
            {
                _str_[i + len] = _str_[i];
            }

            strncpy(_str_ + pos, str, len);  // 插入字符串
            _size_ += len;  // 更新长度

            return *this;
        }

        // 删除指定位置的字符或子字符串
        String& erase(size_t pos, size_t len = npos)
        {
            assert(pos < _size_);  // 确保位置有效

            if (len >= _size_ - pos)
            {
                _str_[pos] = '\0';  // 截断字符串
                _size_ = pos;       // 更新长度
            }
            else
            {
                for (size_t i = pos + len; i <= _size_; ++i)
                {
                    _str_[i - len] = _str_[i];
                }

                _size_ -= len;  // 更新长度
            }

            return *this;
        }

        // 查找字符的位置
        size_t find(char ch, size_t pos = 0) const
        {
            for (size_t i = pos; i < _size_; ++i)
            {
                if (_str_[i] == ch)
                {
                    return i;
                }
            }

            return npos;  // 找不到时返回npos
        }

        // 查找子字符串的位置
        size_t find(const char* str, size_t pos = 0) const
        {
            char* p = strstr(_str_ + pos, str);
            if (p == nullptr)
            {
                return npos;
            }
            else
            {
                return p - _str_;  // 返回相对位置
            }
        }

        // 重载<操作符，比较两个字符串
        bool operator<(const String& s) const
        {
            return strcmp(_str_, s._str_) < 0;
        }

        // 重载==操作符，判断两个字符串是否相等
        bool operator==(const String& s) const
        {
            return strcmp(_str_, s._str_) == 0;
        }

        // 重载<=操作符，判断是否小于或等于
        bool operator<=(const String& s) const
        {
            return *this < s || *this == s;
        }

        // 重载>操作符，判断是否大于
        bool operator>(const String& s) const
        {
            return !(*this <= s);
        }

        // 重载>=操作符，判断是否大于或等于
        bool operator>=(const String& s) const
        {
            return !(*this < s);
        }

        // 重载!=操作符，判断是否不相等
        bool operator!=(const String& s) const
        {
            return !(*this == s);
        }

    private:
        char* _str_;        // 指向字符数组的指针
        size_t _size_;      // 字符串的长度(不包括\0)
        size_t _capacity_;  // 字符串的容量

        static size_t npos;  // 静态常量，用于表示查找失败
    };

    size_t String::npos = -1;

    // 重载<<输出操作符
    std::ostream& operator<<(std::ostream& out, const String& s)
    {
        for (size_t i = 0; i < s.size(); ++i)
        {
            out << s[i];
        }

        return out;
    }

    // 重载>>输入操作符
    std::istream& operator>>(std::istream& in, String& s)
    {
        s = "";  // 清空现有内容

        while (true)
        {
            char ch = in.get();
            if (ch == ' ' || ch == '\n' || ch == '\t' || ch == '\0')
            {
                break;
            }
            else
            {
                s += ch;  // 添加字符到String对象
            }
        }

        return in;
    }

    // 测试基本功能
    void test_string1()
    {
        String s1;
        String s2("hello");

        std::cout << s1 << std::endl;
        std::cout << s2 << std::endl;

        // 遍历方式1
        for (size_t i = 0; i < s2.size(); ++i)
        {
            std::cout << s2[i] << " ";
        }
        std::cout << std::endl;

        // 遍历方式2
        String::iterator it2 = s2.begin();
        while (it2 != s2.end())
        {
            std::cout << *it2 << " ";
            ++it2;
        }
        std::cout << std::endl;

        // 遍历方式3
        for (auto e : s2)
        {
            std::cout << e << " ";
        }
        std::cout << std::endl;
    }

    // 测试增加字符(串)函数
    void test_string2()
    {
        String s1("hello");
        s1.push_back(' ');
        s1.push_back('w');
        s1.push_back('o');
        s1.push_back('r');
        s1.push_back('l');
        s1.push_back('d');
        std::cout << s1 << std::endl;

        s1.append(" I love C++");
        std::cout << s1 << std::endl;

        s1 += " and I love ";
        s1 += 'C';
        std::cout << s1 << std::endl;
    }

    // 测试insert函数
    void test_string3()
    {
        String s1("hello");
        s1.insert(1, 'x');
        s1.insert(1, "abc");

        std::cout << s1 << std::endl;
    }

    // 测试resize()
    void test_string4()
    {
        String s1("hello");
        s1.resize(10);

        std::cout << s1.size() << std::endl;
        std::cout << s1.capacity() << std::endl;

        s1.resize(5);
        std::cout << s1.size() << std::endl;
        std::cout << s1.capacity() << std::endl;

        s1.resize(20);
        std::cout << s1.size() << std::endl;
        std::cout << s1.capacity() << std::endl;
    }
}
```

```cpp
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include "String.hpp"

using namespace std;

int main()
{
    // String::test_string1();
    // String::test_string2();
    // String::test_string3();
    String::test_string4();

    return 0;
}
```

### vector
#### vector的介绍与使用
##### vector介绍
1. `vector`是表示可变大小数组的序列容器。
2. 像数组一样，`vector`也采用连续存储空间来存储元素。也就意味着可以采用下标对`vector`的元素进行访问，与数组一样高效。但不同于数组的是，它的大小可以动态改变，而且它的大小会被容器自动处理。
3. 本质上，`vector`使用动态分配数组来存储它的元素。当新元素插入时，数组需要重新分配大小，为了增加存储空间，其做法是分配一个新的数组，然后将全部元素移到这个数组。就时间而言，这是一个相对代价高的任务，因为每当一个新的元素加入到容器时，`vector`并不会每次都重新分配大小。
4. `vector`分配空间策略：会分配一些额外的空间以适应可能的增长，因为存储空间比实际需要的存储空间更大。不同的库采用不同的策略权衡空间的使用喝重新分配。但无论如何，重新分配都应该是对数组增长的间隔大小，以至于在末尾插入一个元素的时候是在常数时间的复杂度完成。
5. `vector`占用了更多的存储时间，为了获得管理存储空间的能力，并且以一种有效的方式动态增长。
6. 与其他动态序列容器相比(`deque`、`list`、`forward_list`)，`vector`在访问元素的时候更加高效，在末尾添加和删除元素相对高效。对于其他不在末尾的删除喝插入操作，效率更低。比起`list`与`forward_list`统一的迭代器和引用更好。

##### vector的使用
###### vector的定义
| **constructor** | **接口说明** |
| :---: | :---: |
| `**vector()**` | **无参构造** |
| `vector(size_type n, const value_type& val = value_type())` | 构造并初始化n个`val` |
| `**vector(const vector& x)**` | **拷贝构造** |
| `vector(InputIterator first, InputIterator last)` | 使用迭代器进行初始化构造 |


```cpp
#include <iostream>
#include <vector>

using namespace std;

int main() 
{
    vector<int> v1;   // 无参构造
    v1.push_back(1);  // 尾插
    v1.push_back(2);
    v1.push_back(3);
    v1.push_back(4);

    vector<int> v2(v1);  // 拷贝构造
    
    // 遍历打印v1
    for (size_t i = 0; i < v1.size(); ++i)
    {
        cout << v1[i] << " ";
    }
    
    cout << endl;

    // 遍历打印v2
    for (size_t i = 0; i < v2.size(); ++i)
    {
        cout << v2[i] << " ";
    }

    cout << endl;

    return 0;
}
```

###### vector迭代器
| `iterator`的使用 | 接口说明 |
| --- | :---: |
| ****<br/>`**begin**`**+ **`**end**` | **获取第一个数据位置的**`**iterator/const_iterator**`**，获取最后一个数据的下一个位置的**`**iterator/const_iterator**`**。** |
| <br/>`rbegin`+ `rend` | 获取最后一个数据位置的`reverse_iterator`，获取第一个数据前一个位置的`reverse_iterator`。 |


```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    vector<int> v;   // 无参构造
    v.push_back(1);
    v.push_back(2);
    v.push_back(3);
    v.push_back(4);

    // 遍历方法1：operator[] + size
    for (size_t i = 0; i < v.size(); ++i)
    {
        v[i] *= 2;
        cout << v[i] << " ";
    }

    cout << endl;

    // 遍历方法2：迭代器
    vector<int>::iterator it = v.begin();
    while (it != v.end())
    {
        *it *= 2;
        cout << *it << " ";
        ++it;
    }

    cout << endl;

    // 遍历方法3：范围for
    for (auto e : v)
    {
        e *= 2;
        cout << e << " ";
    }

    cout << endl;

    return 0;
}
```

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    vector<int> v1{1, 2, 3, 4};
    vector<int> v2{ 5, 6, 7, 8 };
    vector<int> v3{ 10, 20, 30, 40 };

    // 迭代器1：普通正向迭代器，可读可写
    vector<int>::iterator it = v1.begin();
    while (it != v1.end())
    {
        *it *= 2;
        cout << *it << " ";
        ++it;
    }

    cout << endl;

    // 迭代器2：const迭代器，不能写
    vector<int>::const_iterator cit = v2.begin();
    while (cit != v2.end())
    {
        // *it *= 2;  // const迭代器不能写
        cout << *cit << " ";
        ++cit;
    }

    cout << endl;

    // 迭代器3：反向迭代器，同理也有const反向迭代器
    vector<int>::reverse_iterator rit = v3.rbegin();
    while (rit != v3.rend())
    {
        cout << *rit << " ";
        ++rit;
    }

    cout << endl;

    return 0;
}
```

###### vector空间增长问题
| 容量空间 | 接口说明 |
| :---: | :---: |
| `size` | 获取数据个数 |
| `capacity` | 获取容量大小 |
| `empty` | 判断是否为空 |
| `**resize**` | **改变**`**vector**`**的**`**size**` |
| `**reserve**` | **改变**`**vector**`**的**`**capacity**` |


```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    // 定义一个变量 sz，用来保存 vector 的当前容量
    size_t sz;
    
    // 创建一个空的 vector，用于存储 int 型数据
    vector<int> v;
    
    // 初始时获取 vector 的容量，并将其存储在 sz 中
    sz = v.capacity();
    
    // 输出初始状态下的 vector 容量
    cout << "making v grow:\n";
    
    // 循环向 vector 中添加 100 个元素
    for (int i = 0; i < 100; ++i)
    {
        // 向 vector 尾部添加一个元素
        v.push_back(i);
        
        // 如果当前容量与之前存储的容量不同，表示 vector 进行了扩容
        if (sz != v.capacity())
        {
            // 更新 sz 为新的容量
            sz = v.capacity();
            
            // 输出容量改变后的值
            cout << "capacity changed: " << sz << '\n';
        }
    }

    return 0;
}
```

+ `VS`下`capacity`是按1.5倍增长的，`g++`是按2倍增长的(`VS`是`PJ`版`STL`，`g++`是`SGI`版`STL`)。
+ `resize`在开空间的同时还会进行初始化，影响`size`。
+ 如果已经确定`vector`中要存储元素大概个数，可以提前将空间设置足够，避免扩容导致效率低下。

```cpp
#include <iostream>   // 包含输入输出流库，用于使用 cout
#include <vector>     // 包含向量库，用于使用 vector 容器

using namespace std;  // 使用标准命名空间，避免使用标准函数时需要加上 std::

int main()
{
    vector<int> v;           // 声明一个整数类型的 vector
    size_t sz = v.capacity(); // 初始化容量变量为当前 vector 的容量
    v.reserve(100);           // 预留空间，确保 vector 能够容纳至少 100 个元素而不重新分配内存

    cout << "making bar grow:" << endl;  // 输出信息，表示 vector 将要增长

    // 循环向 vector 添加元素，并监控容量变化
    for (int i = 0; i < 100; ++i)
    {
        v.push_back(i);  // 向 vector 末尾添加一个元素
        if (sz != v.capacity())  // 检查 vector 的容量是否发生了变化
        {
            sz = v.capacity();   // 更新容量变量为新的容量

            cout << "capacity changed： " << sz << endl;  // 输出新的容量
        }
    }

    return 0;  
}
```

```cpp
#include <iostream>   // 包含输入输出流库，用于使用 cout
#include <vector>     // 包含向量库，用于使用 vector 容器

using namespace std;  // 使用标准命名空间，避免使用标准函数时需要加上 std::

int main()
{
    vector<int> v;

    // 1. 将 vector 的大小调整为 5，默认值为 0
    v.resize(5);

    // 输出当前 vector 的内容
    for (int i = 0; i < v.size(); i++)
    {
        cout << v[i] << " ";  // 此时 vector 中的元素应为 0 0 0 0 0
    }
    cout << endl;

    // 2. 将 vector 的大小调整为 8，多出的元素初始化为 100
    v.resize(8, 100);

    // 输出扩展后的 vector 内容
    for (int i = 0; i < v.size(); i++)
    {
        cout << v[i] << " ";  // 此时 vector 中的元素应为 0 0 0 0 0 100 100 100
    }
    cout << endl;

    // 3. 将 vector 的大小缩小为 3
    v.resize(3);

    // 输出缩小后的 vector 内容
    for (int i = 0; i < v.size(); i++)
    {
        cout << v[i] << " ";  // 此时 vector 中的元素应为 0 0 0
    }
    cout << endl;

    return 0;  
}
```

###### vector增删改查
| `vector`增删改查 | 接口说明 |
| :---: | :---: |
| `**push_back**` | **尾插。** |
| `**pop_back**` | **尾删。** |
| `find` | 查找(算法模块实现，并非`vector`成员接口)。 |
| `insert` | 在`position`前插入`val`。 |
| `erase` | 删除`position`位置的数据。 |
| `swap` | 交换两个`vector`的数据空间。 |
| `**operator[]**` | **像数组一样访问。** |


```cpp
#include <iostream>   // 包含输入输出流库，用于使用 cout
#include <vector>     // 包含向量库，用于使用 vector 容器
#include <algorithm>  // 包含算法库，用于使用 find 函数

using namespace std;  // 使用标准命名空间，避免使用标准函数时需要加上 std::

int main()
{
    // 初始化 vector v，包含元素 1, 2, 3, 4
    vector<int> v{1, 2, 3, 4};

    // 1. 在 vector 的头部插入元素 0
    v.insert(v.begin(), 0);  // 现在 v = {0, 1, 2, 3, 4}

    // 2. 删除 vector 头部的元素
    v.erase(v.begin());  // 删除第一个元素 0，v = {1, 2, 3, 4}

    // 3. 查找值为 3 的元素的位置
    auto pos = find(v.begin(), v.end(), 3);
    if (pos != v.end())
    {
        // 在找到的位置前插入元素 30
        v.insert(pos, 30);  // 现在 v = {1, 2, 30, 3, 4}
    }

    // 4. 遍历 vector 并输出所有元素
    vector<int>::iterator it = v.begin();
    while (it != v.end())
    {
        cout << *it << " ";  // 输出: 1 2 30 3 4
        ++it;
    }
    cout << endl;

    // 5. 再次查找值为 3 的元素的位置
    pos = find(v.begin(), v.end(), 3);
    if (pos != v.end())
    {
        // 删除找到的值为 3 的元素
        v.erase(pos);  // 删除元素 3，v = {1, 2, 30, 4}
    }

    // 6. 遍历 vector 并输出所有元素
    it = v.begin();
    while (it != v.end())
    {
        cout << *it << " ";  // 输出: 1 2 30 4
        ++it;
    }

    return 0;
}
```

###### vector迭代器失效问题
**迭代器的主要作用就是让算法能够不关心底层数据结构，其底层实际是一个指针，或者是对指针进行了封装，比如：**`**vector**`**的迭代器就是原生态指针**`**T***`**。因此迭代器失效，实际就是迭代器底层对应指针所指向的空间被销毁了，而继续使用一块已经被释放的空间，导致程序可能会崩溃。对于**`**vector**`**可能会导致其迭代器失效的操作有：**

1. **会引起其底层空间改变的操作，都有可能使迭代器失效，例如：**`**resize**`**、**`**reserve**`**等。**

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    vector<int> v{ 1, 2, 3, 4, 5, 6 };  // 初始化一个包含6个元素的 vector
    auto it = v.begin();                // 获取 vector 的起始迭代器

    // 将有效元素个数增加到100个，多出的位置用8填充，操作期间底层会扩容
    // v.resize(100, 8);

    // reserve的作用是改变容量大小，但不改变有效元素个数，操作期间可能会引起底层容量改变
    // v.reserve(100);

    // 插入元素期间，可能会引起扩容，导致原空间被释放
    // v.insert(v.begin(), 0);
    // v.push_back(8);

    // 给 vector 重新赋值，可能会引起底层容量改变
    v.assign(100, 8);

    /*
    以上操作，都有可能导致 vector 扩容，也就是说 vector 底层原来的旧空间被释放掉，
    而在打印时，it 还指向释放之前的旧空间。在对 it 迭代器操作时，实际上操作的是一块已经被释放的
    空间，这可能会导致代码运行时崩溃。
    解决方式：在以上操作完成之后，如果想要继续通过迭代器操作 vector 中的元素，只需给 it 重新赋值即可。
    */

    while (it != v.end())  // 遍历 vector 并输出其中的元素
    {
        cout << *it << " ";  // 打印当前迭代器指向的元素
        ++it;                // 移动迭代器到下一个元素
    }

    cout << endl;

    return 0;  // 程序成功结束
}
```

2. `**erase**`**指定位置元素的删除操作。**

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    int a[] = { 1, 2, 3, 4, 5 };
    vector<int> v(a, a + sizeof(a) / sizeof(int)); // 将数组 a 的元素复制到 vector v 中

    // 使用find查找3所在位置的iterator
    vector<int>::iterator pos = find(v.begin(), v.end(), 3);

    // 删除pos位置的数据，导致pos迭代器失效
    v.erase(pos);

    cout << *pos << endl;  // 此处会导致非法访问

    return 0;  // 程序成功结束
}
```

`**erase**`**删除**`**pos**`**位置元素后，**`**pos**`**位置之后的元素会往前移动，没有导致底层空间的改变，理论上讲迭代器不应该会失效，但是如果**`**pos**`**刚好是最后一个元素，删完之后**`**pos**`**刚好是**`**end**`**的位置，而**`**end**`**位置是没有元素的，那么**`**pos**`**就失效了。因此，删除**`**vector**`**中任意位置上元素时，**`**VS**`**就认为该位置迭代器失效了。**

以下代码的功能是删除`vector`中所有的偶数，请问哪段代码是正确的，为什么？

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    vector<int> v{ 1, 2, 3, 4 };
    auto it = v.begin();  // 初始化迭代器，指向 vector 的第一个元素

    while (it != v.end())
    {
        if (*it % 2 == 0)  // 如果当前元素是偶数
        {
            v.erase(it);  // 删除当前偶数元素，但不会更新 it，erase 操作导致 it 失效
            // 此时 it 指向的元素已经被删除，继续使用 it 是不安全的，可能会导致未定义行为
        }

        ++it;  // 即使 it 可能失效，依然递增它，这会跳过下一个元素，导致潜在的逻辑错误
        // 如果上一步 erase 了一个元素，it 实际上已经指向了删除元素之后的位置
        // 因此，递增 it 会跳过下一个元素，未检查或删除该元素
    }

    // 输出删除后的 vector
    for (int num : v)
    {
        cout << num << " ";  // 这里会打印出最终的 vector 状态，但由于前面的问题，可能不是预期的结果
    }
    cout << endl;

    return 0;
}
```

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    vector<int> v{1, 2, 3, 4};
    auto it = v.begin();

    while (it != v.end())
    {
        if (*it % 2 == 0)  // 如果当前元素是偶数
        {
            it = v.erase(it);  // 删除元素，并获取指向下一个元素的新迭代器
        }
        else
        {
            ++it;  // 如果没有删除元素，正常递增迭代器
        }
    }

    // 输出删除后的 vector
    for (int num : v)
    {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
```

3. **Linux下，**`**g++**`**编译器对迭代器失效的检测并不是很严格，处理也没有**`**VS**`**下极端。**

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    // 初始化一个包含 5 个元素的 vector
    vector<int> v{ 1, 2, 3, 4, 5 };

    // 输出 vector 中的所有元素
    for (size_t i = 0; i < v.size(); ++i)
    {
        cout << v[i] << " ";  // 输出 1 2 3 4 5
    }

    cout << endl;

    auto it = v.begin();  // 获取 vector 起始位置的迭代器
    cout << "扩容前，vector的容量为：" << v.capacity() << endl;

    // 调用 reserve 函数，将 vector 的容量设置为 100
    // 这会导致底层存储重新分配，所有原来的迭代器（包括 it）都会失效
    v.reserve(100);

    cout << "扩容后，vector的容量为：" << v.capacity() << endl;

    // 在 Linux 下，失效的迭代器可能不会立刻导致程序崩溃，但结果可能不正确
    // 在其他环境（如 VS）中，这种情况通常会导致程序崩溃
    while (it != v.end())
    {
        cout << *it << " ";  // 由于 it 迭代器已经失效，访问它可能会导致未定义行为
        ++it;  // 继续递增失效的迭代器，这也可能会导致不正确的结果或崩溃
    }

    cout << endl;

    return 0;
}
```

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    // 初始化一个包含 5 个元素的 vector
    vector<int> v{ 1, 2, 3, 4, 5 };

    // 使用 find 函数查找值为 3 的元素，返回指向该元素的迭代器
    vector<int>::iterator it = find(v.begin(), v.end(), 3);
    
    // 调用 erase 函数删除指向的元素，此时元素 3 被删除
    // 在删除元素后，后续的元素会向前移动以填补被删除元素的位置
    v.erase(it);

    // 尽管元素 3 已被删除，it 迭代器原本指向的位置现在指向原来的下一个元素（即 4）
    // 在 Linux 系统或其他实现中，空间没有被重新分配，所以 it 仍然有效
    cout << *it << endl;  // 输出 4（即元素 3 被删除后的位置上的新值）

    // 继续遍历 vector，it 现在从新位置（4）开始
    while (it != v.end())
    {
        cout << *it << " ";  // 输出 4 5
        ++it;  // 迭代器向前移动到下一个元素
    }
    
    cout << endl;

    return 0;
}
```

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main()
{
    // 初始化一个包含 5 个元素的 vector
    vector<int> v{ 1, 2, 3, 4, 5 };
    // vector<int> v{ 1, 2, 3, 4, 5, 6 };  
    auto it = v.begin();  // 获取 vector 的起始迭代器
    
    while (it != v.end())
    {
        if (*it % 2 == 0)  // 如果当前元素是偶数
        {
            v.erase(it);  // 删除当前元素，这会使迭代器 it 失效，指向已经删除的元素位置
            // 如果 it 是指向最后一个偶数元素（例如 4 或 6），删除后 it 会指向 vector 的末尾（即 end()）
            // 然而，下一个 ++it 操作会使 it 超过 end()，导致迭代器失效
        }

        ++it;  // 在 it 已经失效的情况下递增它，可能会导致程序崩溃或未定义行为
    }

    // 由于程序在删除最后一个元素时崩溃，下面的代码可能不会执行
    for (auto e : v)  // 遍历并输出 vector 中剩余的元素
    {
        cout << e << " ";  // 输出剩余的元素
    }

    cout << endl;

    return 0;
}
```

上述三个例子中可以发现：`SGI`版`STL`中，迭代器失效后，代码并不一定会崩溃，但是运行结果肯定不对，如果`it`不在`begin`和`end`范围内，肯定会崩溃。

4. **与**`**vector**`**类似，**`**string**`**在插入、扩容、**`**erase**`**之后，迭代器也会失效。**

```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    string s("hello");
    auto it = s.begin();

    // 放开之后代码会崩溃，因为resize到20后string会进行扩容
    // 扩容后，it指向之前旧空间已经被释放了，该迭代器就失效了
    // 后续打印时，再访问it指向的空间，程序就会崩溃
    // s.resize(20, 'c');
    while (it != s.end())
    {
        cout << *it;
        ++it;
    }

    cout << endl;

    it = s.begin();
    while (it != s.end())
    {
        it = s.erase(it);
        // 按照下面方式写，运行时程序会崩溃，因为erase(it)之后
        // it位置的迭代器就失效了
        // s.erase(it);
        ++it;
    }

    return 0;
}
```

**迭代器失效的解决办法：在使用前，对迭代器重新赋值即可。**

#### 深入理解vector与模拟实现
##### 模拟实现Vector::vector类
```cpp
#pragma once   // 防止头文件被重复包含
#include <assert.h>  // 包含断言库，用于调试时检查条件

namespace Vector  // 定义一个命名空间，避免与标准库中的 vector 名字冲突
{

    template<class T>  // 使用模板，支持存储任意类型的元素
    class vector
    {
    public:
        typedef T* iterator;  // 定义迭代器类型为指向 T 类型的指针
        typedef const T* const_iterator;  // 定义常量迭代器类型为指向常量 T 类型的指针

        // 默认构造函数，初始化指针成员为 nullptr
        vector()
            : _start_(nullptr)
            , _finish_(nullptr)
            , _endofstorage_(nullptr)
        {}

        // 预留指定容量的空间，如果 n 大于当前容量，则重新分配内存
        void reserve(size_t n)
        {
            if (n > capacity())
            {
                size_t sz = size();  // 获取当前有效元素的数量
                T* tmp = new T[n];   // 分配新的内存空间
                if (_start_)
                {
                    // memcpy(tmp, _start_, sizeof(T) * size()); // 按字节拷贝，浅拷贝
                    // 拷贝原有数据到新空间
                    for (size_t i = 0; i < sz; ++i)
                    {
                        tmp[i] = _start_[i];  // 调用operator= 深拷贝
                    }
                    delete[] _start_;  // 释放旧的内存空间
                }

                _start_ = tmp;  // 更新指针
                _finish_ = tmp + sz;
                _endofstorage_ = tmp + n;
            }
        }

        // 返回指向第一个元素的迭代器
        iterator begin()
        {
            return _start_;
        }

        // 返回指向最后一个元素的下一个位置的迭代器
        iterator end()
        {
            return _finish_;
        }

        // 向 vector 尾部添加元素，如果容量不够则扩容
        void push_back(const T& x)
        {
            //// 扩容
            //if (_finish_ == _endofstorage_)
            //{
            //    size_t new_capacity = capacity() == 0 ? 2 : capacity() * 2;
            //    reserve(new_capacity);
            //}

            //*_finish_ = x;
            //++_finish_;

            // 以上代码相当于是尾插
            insert(_finish_, x);  // 使用 insert 插入元素
        }

        // 删除 vector 尾部的元素
        void pop_back()
        {
            assert(_start_ < _finish_);  // 确保 vector 非空
            --_finish_;  // 将 finish 指针向前移动一个位置，相当于删除元素
        }

        // 在指定位置插入元素，如果容量不够则扩容
        void insert(iterator pos, const T& x)
        {
            assert(pos <= _finish_);  // 检查插入位置是否合法

            if (_finish_ == _endofstorage_)  // 检查是否需要扩容
            {
                size_t n = pos - _start_;  // 计算插入位置的偏移量
                size_t new_capacity = capacity() == 0 ? 2 : capacity() * 2;  // 计算新容量
                reserve(new_capacity);  // 扩容

                // 如果增容，原 pos 失效，需要重新计算位置
                pos = _start_ + n;
            }

            iterator end = _finish_ - 1;  // 从最后一个有效元素开始移动
            while (end >= pos)
            {
                *(end + 1) = *end;  // 将元素向后移动
                --end;
            }

            *pos = x;  // 在指定位置插入新元素
            ++_finish_;  // 更新 finish 指针
        }

        // 删除指定位置的元素，返回删除元素后的位置
        iterator erase(iterator pos)
        {
            assert(pos < _finish_);  // 检查删除位置是否合法
            iterator it = pos;
            while (it < _finish_ - 1)
            {
                *it = *(it + 1);  // 将后面的元素向前移动
                ++it;
            }

            --_finish_;  // 更新 finish 指针

            return pos;  // 返回删除元素后的位置
        }

        // 调整 vector 的大小，如果 n 大于当前大小，新增元素用 val 填充
        void resize(size_t n, const T& val = T())
        {
            if (n < size())
            {
                _finish_ = _start_ + n;  // 如果 n 小于当前大小，直接缩小范围
            }
            else
            {
                if (n > capacity())
                {
                    reserve(n);  // 如果 n 大于当前容量，先扩容
                }

                while (_finish_ < _start_ + n)
                {
                    *_finish_ = val;  // 用 val 填充新增的空间
                    ++_finish_;
                }
            }
        }

        // 拷贝构造函数，深拷贝另一个 vector
        vector(const vector<int>& v)
        {
            _start_ = new T[v.capacity()];  // 分配新的内存空间
            _finish_ = _start_;
            _endofstorage_ = _start_ + v.capacity();

            for (size_t i = 0; i < v.size(); ++i)
            {
                *_finish_ = v[i];  // 拷贝数据
                ++_finish_;
            }
        }

        // 赋值运算符重载，实现深拷贝
        vector<T>& operator=(const vector<T>& v)
        {
            if (this != &v)
            {
                delete[] _start_;  // 释放旧的内存空间
                _start_ = new T[v.capacity()];  // 分配新的内存空间
                memcpy(_start_, v._start_, sizeof(T) * v.size());  // 拷贝数据
                _finish_ = _start_ + v.size();  // 更新指针
                _endofstorage_ = _start_ + v.capacity();
            }

            return *this;
        }

        // 交换两个 vector 的内容
        void swap(vector<T>& v)
        {
            std::swap(_start_, v._start_);
            std::swap(_finish_, v._finish_);
            std::swap(_endofstorage_, v._endofstorage_);
        }

        // 析构函数，释放内存
        ~vector()
        {
            delete[] _start_;  // 释放动态分配的内存
            _start_ = _finish_ = _endofstorage_ = nullptr;  // 将指针置为 nullptr
        }

        // 下标运算符重载，返回指定位置的元素
        T& operator[](size_t i)
        {
            assert(i < size());  // 检查索引是否越界

            return _start_[i];
        }

        // 下标运算符重载，返回常量引用
        const T& operator[](size_t i) const
        {
            assert(i < size());  // 检查索引是否越界

            return _start_[i];
        }

        // 返回当前元素的数量
        size_t size() const
        {
            return _finish_ - _start_;
        }

        // 返回当前容量
        size_t capacity() const
        {
            return _endofstorage_ - _start_;
        }

    private:
        iterator _start_;  // 指向数据开始的指针
        iterator _finish_;  // 指向数据结束的指针
        iterator _endofstorage_;  // 指向已分配内存末尾的指针
    };
}
```

### list
#### list的介绍与使用
##### list介绍
1. `list`是可以在常数范围内在任意位置进行插入和删除的序列式容器，且该容器可以前后双向迭代。
2. `list`的底层是双向链表结构，双向链表中的每个元素存储在互不相关的独立节点中，在节点中通过指针指向其前一个元素和后一个元素。
3. `list`与`forward_list`非常相似：最主要的不同在于`forward_list`是单链表，只能向前迭代，让其更简单高效。
4. 与其他序列式容器相比(`array`、`vector`、`deque`)，`list`通常在任意位置进行插入、移除元素的执行效率更好。
5. 与其他序列式容器相比，`list`和`forward_list`最大的缺陷是不支持任意位置的随机访问，比如，要访问`list`的第6个元素，必须从已知的位置(例如头部或尾部)迭代到该位置，在这段位置上迭代需要线性的时间开销；`list`还需要一些额外的空间，以保存每个节点的相关联信息(对于存储类型较小元素的`list`来说，这可能是一个重要的因素)。

![](https://cdn.nlark.com/yuque/0/2024/png/36162499/1727749535334-c211e54f-9c6e-4bbc-b4ba-22c5702acd7c.png)

##### list的使用
###### list构造函数
| 构造函数(constructor) | 接口说明 |
| :---: | :---: |
| `**list(size_type n, const value_type& val = value_type())**` | **构造的**`**list**`**中包含**`**n**`**个值为**`**val**`**的元素** |
| `**list()**` | **构造空的**`**list**` |
| `**list(const list& x)**` | **拷贝构造函数** |
| `**list(InputIterator first, InputIterator last)**` | **用[first, last)区间中的元素构造**`**list**` |


```cpp
#include <iostream>
#include <list>
#include <vector>

using namespace std;

int main()
{
    list<int> l1;                         // 构造空的l1
    list<int> l2(4, 100);                 // l2中放4个值为100的元素
    list<int> l3(l2.begin(), l2.end());   // 用12的[begin(), end()]左闭右开的区间构造l3
    list<int> l4(l3);                     // 用l3拷贝构造l4

    // 以数组为迭代器区间构造l5
    int array[] = { 12, 1, 88, 19 };
    list<int> l5(array, array + sizeof(array) / sizeof(int));

    // 列表格式初始化(C++11)
    list<int> l6{ 1, 2, 3, 4, 5 };

    // 打印列表元素
    for (auto& e : l6)
    {
        cout << e << endl;
    }
    
    return 0;
}
```

###### list capacity
| 函数声明 | 接口说明 |
| :---: | :---: |
| `**empty**` | **检测**`**list**`**是否为空，是返回**`**true**`**，否则返回**`**false**`**。** |
| `**size**` | **返回**`**list**`**中有效节点的个数。** |
| `**max_size**` | **返回列表容器可以容纳的最大元素数。** |


```cpp
#include <iostream>
#include <list>

int main() 
{
    std::list<int> myList;  // 定义一个int类型的list容器

    // 1. 判断list是否为空
    if (myList.empty())
    {
        std::cout << "列表为空" << std::endl;  // 如果列表为空，输出信息
    }

    // 2. 向列表添加元素
    myList.push_back(10);   // 添加元素10
    myList.push_back(20);   // 添加元素20
    myList.push_back(30);   // 添加元素30

    // 3. 输出列表的当前大小
    std::cout << "列表大小为: " << myList.size() << std::endl;  // 输出元素个数

    // 4. 输出列表的最大容量
    std::cout << "列表最大容量为: " << myList.max_size() << std::endl;  // 输出系统支持的最大元素数量

    return 0;
}
```

###### list元素访问
| 函数声明 | 接口说明 |
| :---: | :---: |
| `front` |  返回列表的首元素的引用。   |
| `back` |  返回列表的末元素的引用。   |


```cpp
#include <iostream>
#include <list>

int main() 
{
    std::list<int> myList;  // 定义一个int类型的list容器

    // 向列表中添加元素
    myList.push_back(10);   // 添加元素10
    myList.push_back(20);   // 添加元素20
    myList.push_back(30);   // 添加元素30

    // 访问并输出列表的首元素和末元素
    std::cout << "列表首元素: " << myList.front() << std::endl;  // front() 返回首元素
    std::cout << "列表末元素: " << myList.back() << std::endl;   // back() 返回末元素

    // 修改列表的首元素和末元素
    myList.front() = 100;  // 通过front()修改首元素
    myList.back() = 300;   // 通过back()修改末元素

    // 再次输出修改后的首元素和末元素
    std::cout << "修改后的列表首元素: " << myList.front() << std::endl;
    std::cout << "修改后的列表末元素: " << myList.back() << std::endl;

    return 0;
}
```

###### list修饰符
| 函数声明 | 接口说明 |
| :---: | :---: |
| `push_front` |  在列表的前面插入一个元素。 |
| `pop_front` |  删除列表的第一个元素。   |
| `push_back` |  在列表的末尾插入一个元素。   |
| `pop_back` |  删除列表的最后一个元素。   |
| `insert` |  在指定位置插入一个或多个元素。   |
| `erase` |  删除一个或多个元素。   |
| `swap` |  交换两个列表的内容。   |
| `clear` |  清空列表中的所有元素。   |


```cpp
#include <iostream>
#include <list>

int main() 
{
    std::list<int> myList;

    // 使用 push_front 在前面插入元素
    myList.push_front(10);   // 列表: 10
    myList.push_front(20);   // 列表: 20, 10
    std::cout << "使用 push_front 后: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 20 10
    std::cout << std::endl;

    // 使用 push_back 在后面插入元素
    myList.push_back(30);    // 列表: 20, 10, 30
    myList.push_back(40);    // 列表: 20, 10, 30, 40
    std::cout << "使用 push_back 后: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 20 10 30 40
    std::cout << std::endl;

    // 使用 pop_front 移除前面的元素
    myList.pop_front();      // 列表: 10, 30, 40
    std::cout << "使用 pop_front 后: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 10 30 40
    std::cout << std::endl;

    // 使用 pop_back 移除最后面的元素
    myList.pop_back();       // 列表: 10, 30
    std::cout << "使用 pop_back 后: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 10 30
    std::cout << std::endl;

    // 使用 insert 插入元素
    auto it = myList.begin();  // 获取第一个元素的迭代器
    myList.insert(it, 5);      // 在第一个位置插入 5，列表: 5, 10, 30
    std::cout << "使用 insert 后: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 5 10 30
    std::cout << std::endl;

    // 使用 erase 删除元素
    it = myList.begin();
    myList.erase(it);          // 删除第一个元素，列表: 10, 30
    std::cout << "使用 erase 后: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 10 30
    std::cout << std::endl;

    // 使用 swap 交换两个列表
    std::list<int> anotherList = { 100, 200, 300 };
    myList.swap(anotherList);  // 交换后 myList: 100, 200, 300，anotherList: 10, 30
    std::cout << "使用 swap 后, myList: ";
    for (int val : myList) std::cout << val << " ";  // 输出: 100 200 300
    std::cout << std::endl;
    std::cout << "使用 swap 后, anotherList: ";
    for (int val : anotherList) std::cout << val << " ";  // 输出: 10 30
    std::cout << std::endl;

    // 使用 clear 清空列表
    myList.clear();            // 清空列表，myList 变为空
    std::cout << "使用 clear 后, myList 元素个数: " << myList.size() << std::endl;  // 输出: 0

    return 0;
}
```

###### list迭代器失效
**可以将迭代器暂时理解为指针，该指针指向**`**list**`**中的某个节点。迭代器失效即迭代器所指向的节点的无效，即该节点被删除了。因为**`**list**`**的底层结构为带头节点的双向循环链表，因此在**`**list**`**中进行插入时不会导致**`**list**`**的迭代器失效，只有在删除时才会失效，并且失效的只是指向被删除节点的迭代器，其他迭代器不会受影响。**迭代器失效代码如下：

```cpp
#include <iostream>
#include <list>

int main()
{
    int array[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 0 };
    std::list<int> myList(array, array + sizeof(array) / sizeof(array[0]));

    auto it = myList.begin();
    while (it != myList.end())
    {
        // erase()函数执行后，it所指向的节点已被删除，因此it无效
        // 在下一次使用it时，必须先给其赋值
        myList.erase(it);
        ++it;
    }

    return 0;
}
```

 当使用`erase()`删除一个元素时，`erase()`会返回指向下一个元素的迭代器。因此，正确的做法是将`it`赋值为`erase()`的返回值，而不是直接递增迭代器`it`。 修正代码为：

```cpp
#include <iostream>
#include <list>

int main()
{
    int array[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 0 };
    std::list<int> myList(array, array + sizeof(array) / sizeof(array[0]));

    auto it = myList.begin();
    while (it != myList.end())
    {
        // 正确做法：使用 erase() 的返回值更新迭代器
        // myList.erase(it++)
        it = myList.erase(it);  // erase() 返回指向被删除元素之后的迭代器
    }

    return 0;
}
```

`myList.erase(it)`代码`erase()`函数不仅会删除`it`所指向的元素，还会返回一个指向下一个元素的迭代器。通过将`it`赋值为`erase(it)`，确保了迭代器在每次删除操作后都指向正确的下一个元素，而不会失效。  

对于`vector`与`list`两者的底层数据结构不同，迭代器失效的原因：

1. `**vector**`**的迭代器，**`**insert**`**、**`**push_back**`**、**`**erase**`**等都会导致失效。**
2. `**list**`**的迭代器，**`**erase**`**会导致失效。**

#### list的深度剖析及模拟实现
##### list的模拟实现
```cpp
#pragma once
#include <iostream>
#include <assert.h>

using namespace std;

namespace bite
{
	// List的节点类
	template<class T>
	struct ListNode
	{
		ListNode(const T& val = T())
			: _prev(nullptr)
			, _next(nullptr)
			, _val(val)
		{}

		ListNode<T>* _prev;
		ListNode<T>* _next;
		T _val;
	};

	/*
	List 的迭代器
	迭代器有两种实现方式，具体应根据容器底层数据结构实现：
	  1. 原生态指针，比如：vector
	  2. 将原生态指针进行封装，因迭代器使用形式与指针完全相同，因此在自定义的类中必须实现以下方法：
		 1. 指针可以解引用，迭代器的类中必须重载operator*()
		 2. 指针可以通过->访问其所指空间成员，迭代器类中必须重载oprator->()
		 3. 指针可以++向后移动，迭代器类中必须重载operator++()与operator++(int)
			至于operator--()/operator--(int)释放需要重载，根据具体的结构来抉择，双向链表可以向前             移动，所以需要重载，如果是forward_list就不需要重载--
		 4. 迭代器需要进行是否相等的比较，因此还需要重载operator==()与operator!=()
	*/
	template<class T, class Ref, class Ptr>
	class ListIterator
	{
		typedef ListNode<T> Node;
		typedef ListIterator<T, Ref, Ptr> Self;

		// Ref 和 Ptr 类型需要重定义下，实现反向迭代器时需要用到
	public:
		typedef Ref Ref;
		typedef Ptr Ptr;
	public:
		//////////////////////////////////////////////
		// 构造
		ListIterator(Node* node = nullptr)
			: _node(node)
		{}

		//////////////////////////////////////////////
		// 具有指针类似行为
		Ref operator*()
		{
			return _node->_val;
		}

		Ptr operator->()
		{
			return &(operator*());
		}

		//////////////////////////////////////////////
		// 迭代器支持移动
		Self& operator++()
		{
			_node = _node->_next;
			return *this;
		}

		Self operator++(int)
		{
			Self temp(*this);
			_node = _node->_next;
			return temp;
		}

		Self& operator--()
		{
			_node = _node->_prev;
			return *this;
		}

		Self operator--(int)
		{
			Self temp(*this);
			_node = _node->_prev;
			return temp;
		}

		//////////////////////////////////////////////
		// 迭代器支持比较
		bool operator!=(const Self& l)const
		{
			return _node != l._node;
		}

		bool operator==(const Self& l)const
		{
			return _node != l._node;
		}

		Node* _node;
	};

	template<class Iterator>
	class ReverseListIterator
	{
		// 注意：此处typename的作用是明确告诉编译器，Ref是Iterator类中的一个类型，而不是静态成员变量
		// 否则编译器编译时就不知道Ref是Iterator中的类型还是静态成员变量
		// 因为静态成员变量也是按照 类名::静态成员变量名 的方式访问的
	public:
		typedef typename Iterator::Ref Ref;
		typedef typename Iterator::Ptr Ptr;
		typedef ReverseListIterator<Iterator> Self;
	public:
		//////////////////////////////////////////////
		// 构造
		ReverseListIterator(Iterator it)
			: _it(it)
		{}

		//////////////////////////////////////////////
		// 具有指针类似行为
		Ref operator*()
		{
			Iterator temp(_it);
			--temp;
			return *temp;
		}

		Ptr operator->()
		{
			return &(operator*());
		}

		//////////////////////////////////////////////
		// 迭代器支持移动
		Self& operator++()
		{
			--_it;
			return *this;
		}

		Self operator++(int)
		{
			Self temp(*this);
			--_it;
			return temp;
		}

		Self& operator--()
		{
			++_it;
			return *this;
		}

		Self operator--(int)
		{
			Self temp(*this);
			++_it;
			return temp;
		}

		//////////////////////////////////////////////
		// 迭代器支持比较
		bool operator!=(const Self& l)const
		{
			return _it != l._it;
		}

		bool operator==(const Self& l)const
		{
			return _it != l._it;
		}

		Iterator _it;
	};

	template<class T>
	class list
	{
		typedef ListNode<T> Node;

	public:
		// 正向迭代器
		typedef ListIterator<T, T&, T*> iterator;
		typedef ListIterator<T, const T&, const T&> const_iterator;

		// 反向迭代器
		typedef ReverseListIterator<iterator> reverse_iterator;
		typedef ReverseListIterator<const_iterator> const_reverse_iterator;
	public:
		///////////////////////////////////////////////////////////////
		// List的构造
		list()
		{
			CreateHead();
		}

		list(int n, const T& value = T())
		{
			CreateHead();
			for (int i = 0; i < n; ++i)
				push_back(value);
		}

		template <class Iterator>
		list(Iterator first, Iterator last)
		{
			CreateHead();
			while (first != last)
			{
				push_back(*first);
				++first;
			}
		}

		list(const list<T>& l)
		{
			CreateHead();

			// 用l中的元素构造临时的temp,然后与当前对象交换
			list<T> temp(l.begin(), l.end());
			this->swap(temp);
		}

		list<T>& operator=(list<T> l)
		{
			this->swap(l);
			return *this;
		}

		~list()
		{
			clear();
			delete _head;
			_head = nullptr;
		}

		///////////////////////////////////////////////////////////////
		// List的迭代器
		iterator begin()
		{
			return iterator(_head->_next);
		}

		iterator end()
		{
			return iterator(_head);
		}

		const_iterator begin()const
		{
			return const_iterator(_head->_next);
		}

		const_iterator end()const
		{
			return const_iterator(_head);
		}

		reverse_iterator rbegin()
		{
			return reverse_iterator(end());
		}

		reverse_iterator rend()
		{
			return reverse_iterator(begin());
		}

		const_reverse_iterator rbegin()const
		{
			return const_reverse_iterator(end());
		}

		const_reverse_iterator rend()const
		{
			return const_reverse_iterator(begin());
		}

		///////////////////////////////////////////////////////////////
		// List的容量相关
		size_t size()const
		{
			Node* cur = _head->_next;
			size_t count = 0;
			while (cur != _head)
			{
				count++;
				cur = cur->_next;
			}

			return count;
		}

		bool empty()const
		{
			return _head->_next == _head;
		}

		void resize(size_t newsize, const T& data = T())
		{
			size_t oldsize = size();
			if (newsize <= oldsize)
			{
				// 有效元素个数减少到newsize
				while (newsize < oldsize)
				{
					pop_back();
					oldsize--;
				}
			}
			else
			{
				while (oldsize < newsize)
				{
					push_back(data);
					oldsize++;
				}
			}
		}
		////////////////////////////////////////////////////////////
		// List的元素访问操作
		// 注意：List不支持operator[]
		T& front()
		{
			return _head->_next->_val;
		}

		const T& front()const
		{
			return _head->_next->_val;
		}

		T& back()
		{
			return _head->_prev->_val;
		}

		const T& back()const
		{
			return _head->_prev->_val;
		}

		////////////////////////////////////////////////////////////
		// List的插入和删除
		void push_back(const T& val)
		{
			insert(end(), val);
		}

		void pop_back()
		{
			erase(--end());
		}

		void push_front(const T& val)
		{
			insert(begin(), val);
		}

		void pop_front()
		{
			erase(begin());
		}

		// 在pos位置前插入值为val的节点
		iterator insert(iterator pos, const T& val)
		{
			Node* pNewNode = new Node(val);
			Node* pCur = pos._node;
			// 先将新节点插入
			pNewNode->_prev = pCur->_prev;
			pNewNode->_next = pCur;
			pNewNode->_prev->_next = pNewNode;
			pCur->_prev = pNewNode;
			return iterator(pNewNode);
		}

		// 删除pos位置的节点，返回该节点的下一个位置
		iterator erase(iterator pos)
		{
			// 找到待删除的节点
			Node* pDel = pos._node;
			Node* pRet = pDel->_next;

			// 将该节点从链表中拆下来并删除
			pDel->_prev->_next = pDel->_next;
			pDel->_next->_prev = pDel->_prev;
			delete pDel;

			return iterator(pRet);
		}

		void clear()
		{
			Node* cur = _head->_next;

			// 采用头删除删除
			while (cur != _head)
			{
				_head->_next = cur->_next;
				delete cur;
				cur = _head->_next;
			}

			_head->_next = _head->_prev = _head;
		}

		void swap(bite::list<T>& l)
		{
			std::swap(_head, l._head);
		}

	private:
		void CreateHead()
		{
			_head = new Node;
			_head->_prev = _head;
			_head->_next = _head;
		}
	private:
		Node* _head;
	};
}


///////////////////////////////////////////////////////
// 对模拟实现的list进行测试
// 正向打印链表
template<class T>
void PrintList(const bite::list<T>& l)
{
	auto it = l.begin();
	while (it != l.end())
	{
		cout << *it << " ";
		++it;
	}

	cout << endl;
}

// 测试List的构造
void TestBiteList1()
{
	bite::list<int> l1;
	bite::list<int> l2(10, 5);
	PrintList(l2);

	int array[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 0 };
	bite::list<int> l3(array, array + sizeof(array) / sizeof(array[0]));
	PrintList(l3);

	bite::list<int> l4(l3);
	PrintList(l4);

	l1 = l4;
	PrintList(l1);
}

// PushBack()/PopBack()/PushFront()/PopFront()
void TestBiteList2()
{
	// 测试PushBack与PopBack
	bite::list<int> l;
	l.push_back(1);
	l.push_back(2);
	l.push_back(3);
	PrintList(l);

	l.pop_back();
	l.pop_back();
	PrintList(l);

	l.pop_back();
	cout << l.size() << endl;

	// 测试PushFront与PopFront
	l.push_front(1);
	l.push_front(2);
	l.push_front(3);
	PrintList(l);

	l.pop_front();
	l.pop_front();
	PrintList(l);

	l.pop_front();
	cout << l.size() << endl;
}

// 测试insert和erase
void TestBiteList3()
{
	int array[] = { 1, 2, 3, 4, 5 };
	bite::list<int> l(array, array + sizeof(array) / sizeof(array[0]));

	auto pos = l.begin();
	l.insert(l.begin(), 0);
	PrintList(l);

	++pos;
	l.insert(pos, 2);
	PrintList(l);

	l.erase(l.begin());
	l.erase(pos);
	PrintList(l);

	// pos指向的节点已经被删除，pos迭代器失效
	cout << *pos << endl;

	auto it = l.begin();
	while (it != l.end())
	{
		it = l.erase(it);
	}
	cout << l.size() << endl;
}

// 测试反向迭代器
void TestBiteList4()
{
	int array[] = { 1, 2, 3, 4, 5 };
	bite::list<int> l(array, array + sizeof(array) / sizeof(array[0]));

	auto rit = l.rbegin();
	while (rit != l.rend())
	{
		cout << *rit << " ";
		++rit;
	}
	cout << endl;

	const bite::list<int> cl(l);
	auto crit = l.rbegin();
	while (crit != l.rend())
	{
		cout << *crit << " ";
		++crit;
	}
	cout << endl;
}
```

##### list的反向迭代器
我们知道，反向迭代器的`++`就是正向迭代器的`--`，反向迭代器的`--`就是正向迭代器的`++`，因此反向迭代器的实现可以借助正向迭代器，即：反向迭代器内部可以包装一个正向迭代器，对正向迭代器的接口进行包装即可：

```cpp
template<class Iterator>
class ReverseListIterator
{
    // 注意：此处typename的作用是明确告诉编译器，Ref是Iterator类中的类型，而不是静态成员变量
    // 则编译器编译时就不知道Ref是Iterator中的类型还是静态成员变量
    //  因为静态成员变量也是按照 类名::静态成员变量名 的方式访问的
public:
    typedef typename Iterator::Ref Ref;
    typedef typename Iterator::Ptr Ptr;
    typedef ReverseListIterator<Iterator> Self;

public:
    // 构造
    ReverseListIterator(Iterator it): _it(it) {}

    // 具有指针类似行为
    Ref operator*()
    {
        Iterator temp(_it);
        --temp;
        return *temp;
    }

    Ptr operator->() { return &(operator*()); }

    // 迭代器支持移动
    Self& operator++()
    {
        --_it;
        return *this;
    }

    Self operator++(int)
    {
        Self temp(*this);
        --_it;
        return temp;
    }

    Self& operator--()
    {
        ++_it;
        return *this;
    }

    Self operator--(int)
    {
        Self temp(*this);
        ++_it;
        return temp;
    }

    // 迭代器支持比较
    bool operator!=(const Self& l) const { return _it != l._it; }
    bool operator==(const Self& l) const { return _it != l._it; }
    Iterator _it;
};
```

#### list与vector的对比
| 不同场景 | `vector` | `list` |
| :---: | :---: | :---: |
| 底层结构 | 动态顺序表，一段连续空间 | 带头结点的双向循环链表 |
| 随机访问 | 支持随机访问，访问某个元素效率O(1)。 | 不支持随机访问，访问某个元素效率O(N)。 |
| 插入和删除 | 任意位置插入和删除效率低，需要搬移元素，时间复杂度O(N)，插入时有可能需要增容，增容：开辟新空间，拷贝元素，释放旧空间，导致效率更低。 | 任意位置插入和删除效率高，不需要搬移元素，时间复杂度为O(1)。 |
| 空间利用率 | 底层为连续空间，不容易造成内存碎片，空间利用率高，缓存利用率高。 | 底层节点动态开辟，小节点容易造成内存碎片，空间利用率低，缓存利用率低。 |
| 迭代器 | 原生态指针。 | 对原生态指针(节点指针)进行封装。 |
| 迭代器失效 | 在插入元素时，要给所有的迭代器重新赋值，因为插入元素有可能会导致重新扩容，致使原来迭代器失效，删除时，当前迭代器需要重新赋值否则会失效。 | 插入元素不会导致迭代器失效，删除元素时，只会导致当前迭代器失效，其他迭代器不受影响 。 |
| 使用场景 | 需要高效存储，支持随机访问，不关心插入删除效率。 | 大量插入和删除操作，不关心随机访问。 |


### stack与queue
#### stack的介绍与使用
##### stack的介绍
1. `stack`是一种容器适配器，专门用在具有后进先出操作的上下文环境中，<font style="color:rgb(0, 0, 0);">其中元素仅从容器的一端插入和提取。</font>
2. `<font style="color:rgb(0, 0, 0);">stack</font>`<font style="color:rgb(0, 0, 0);">是作为容器适配器被实现的，容器适配器即是对特定类封装作为其底层的容器，并提供一组特定的成员函数来访问其元素，将特定类作为其底层的，元素特定容器的尾部(即栈顶)被压入和弹出。</font>
3. `<font style="color:rgb(0, 0, 0);">stack</font>`<font style="color:rgb(0, 0, 0);">的底层容器可以是任何标准的容器类模板或者一些特定的容器类，这些容器类应该支持以下操作：</font>
+ `empty`：判空操作。
+ `back`：获取尾部元素操作。
+ `push_back`：尾部插入元素操作。
+ `pop_back`：尾部删除元素操作。
4. 标准容器`vector`、`queue`、`list`均符合这些需求，如果没有为`stack`指定特定的底层容器，默认使用`deque`。

##### stack的使用
| 函数 | 接口说明 |
| :---: | :---: |
| `stack` | 构造空的栈 |
| `empty` | 检测`stack`是否为空 |
| `size` | 返回`stack`种元素的个数 |
| `top` | 返回栈顶元素的引用 |
| `push` | 将元素压入栈中 |
| `pop` | 将尾部元素弹出 |


```cpp
#include <iostream>
#include <stack>

int main()
{
    // 构造空栈
    std::stack<int> s;

    // 判断是否为空栈
    if (s.empty())
    {
        std::cout << "栈为空" << std::endl;
    }

    // 将元素压入栈
    s.push(1);
    s.push(2);
    s.push(3);

    // 获取栈的大小
    std::cout << "栈中元素的个数：" << s.size() << std::endl;

    // 访问栈顶元素
    std::cout << "栈顶元素：" << s.top() << std::endl;

    // 弹出栈顶元素
    s.pop();
    std::cout << "弹出后的栈顶元素：" << s.top() << std::endl;

    return 0;
}
```

##### 打印栈中元素
`stack`是一个容器适配器，它是基于底层容器(如`deque`或`vector`)来实现的，但它并不直接提供迭代器访问元素的功能。这意味着不能像`vector`或`deque`一样使用迭代器来遍历`stack`的元素。可以通过逐个访问栈顶元素并弹出元素的方式来打印栈中的内容，但要注意这样会破坏栈的结构。因此，如果要保留栈中的元素，可以在打印时使用一个辅助栈来暂时存储弹出的元素。 例如以下代码：

```cpp
#include <iostream>
#include <stack>

void printStack(std::stack<int> s)
{
    // 打印并弹出栈中的每个元素
    while (!s.empty()) 
    {
        std::cout << s.top() << " ";
        s.pop();  // 弹出栈顶元素
    }
    std::cout << std::endl;
}

int main() 
{
    std::stack<int> s;

    // 压入元素
    s.push(10);
    s.push(20);
    s.push(30);

    // 打印栈中的元素
    std::cout << "栈中的元素为: ";
    printStack(s);  // 传递栈的副本进行打印

    return 0;
}
```

##### stack的模拟实现
```cpp
#include <vector>

namespace myStack
{
    template<class T>
    class stack
    {
    public:
        stack() {}
        void push(const T& x) { _c.push_back(x); }
        void pop() { _c.pop.back(); }
        T& top() { return _c.back(); }
        const T& top() const { return _c.back(); }
        size_t size() const { return _c.size(); }
        bool empty() const { return _c.empty(); }

    private:
        std::vector<T> _c;
    };
}
```

#### queue的介绍与使用
##### queue的介绍
1. 队列是一种容器适配器，专门用于先进先出中操作，从容器一端插入元素，另一端提取元素。
2. 队列作为容器适配器实现，容器适配器即将特定容器类封装作为其底层容器类，`queue`提供一组特定的成员函数来访问其元素。元素从队尾入队列，从队头出队列。
3. 底层容器可以是标准容器类模板之一，也可以是其他专门设计的容器类。该底层容器应至少支持以下操作：
+ `empty`：检测队列是否为空。
+ `size`：返回队列中有效元素的个数。
+ `front`：返回队头元素的引用。
+ `back`：返回队尾部入队列。
+ `pop_front`：在队列头部出队列。
4.  标准容器类`queue`和`list`满足了这些要求。默认情况下，如果没有为`queue`实例化指定容器类，则使用标准容器`deque`。

##### queue的使用
| 函数声明 | 接口说明 |
| :---: | :---: |
| `queue` | 构造空的队列。 |
| `empty` | 检测队列是否为空，空则返回`true`，否则返回`false`。 |
| `size` | 返回队列中有效元素的个数。 |
| `front` | 返回队头元素的引用。 |
| `back` | 返回队尾元素的引用。 |
| `push` | 在队尾将元素入队列。 |
| `pop` | 将队头元素出队列。 |


```cpp
#include <iostream>
#include <queue> 

int main() 
{
    // 创建一个空的队列，队列中存储int类型的元素
    std::queue<int> q;

    // 检查队列是否为空
    if (q.empty()) 
    {
        std::cout << "队列是空的" << std::endl;
    }

    // 向队列中添加元素
    q.push(10); // 队尾添加元素10
    q.push(20); // 队尾添加元素20
    q.push(30); // 队尾添加元素30

    // 输出队列的大小
    std::cout << "队列的大小: " << q.size() << std::endl;

    // 访问队头元素和队尾元素
    std::cout << "队头元素: " << q.front() << std::endl;
    std::cout << "队尾元素: " << q.back() << std::endl;

    // 将队头元素出队列
    q.pop(); // 移除队头元素

    // 再次访问队头元素和队尾元素
    std::cout << "移除队头后的队头元素: " << q.front() << std::endl;
    std::cout << "移除队头后的队尾元素: " << q.back() << std::endl;

    // 输出队列的大小
    std::cout << "移除队头后的队列大小: " << q.size() << std::endl;

    return 0;
}
```

##### queue的模拟实现
因为`queue`的接口中存在头删和尾插，因此使用`vector`来封装效率太低，故可以借助`list`来模拟实现`queue`，具体如下：

```cpp
#include <list>

namespace myQueue
{
    template<class T>
    class queue
    {
    public:
        queue() {}
        void push(const T& x) { _c.push_back(x); }
        void pop() { _c.pop_front(); }
        T& back() { return _c.back(); }
        const T& back() const { return _c.back(); }
        T& front() { return _c.front(); }
        const T& front() const { return _c.front(); }
        size_t size() const { return _c.size(); }
        bool empty() const { return _c.empty(); }

    private:
        std::list<T> _c;
    };
}
```

#### priority_queue的介绍与使用
##### priority_queue的介绍
1. 优先级队列是一种容器适配器，根据严格的弱排序标准，它的第一个元素总是元素中最大的。
2. 此上下文类似于堆，堆中可以随时插入元素，且只能检索最大堆元素(优先队列中位于顶部的元素)。
3. 优先队列被实现为容器适配器，即将特定容器类封装作为其底层容器类，`queue`提供一组特定的成员函数来访问其元素。元素从特定容器的"尾部"弹出，其称为优先队列的顶部。
4. 底层容器可以是任何标准容器类模板，也可以是其他特定设计的容器类。容器应该可以通过随机访问迭代器访问，并支持以下操作：
+ `empty`：检测容器是否为空。
+ `size`：返回容器中有效元素个数。
+ `front`：返回容器中第一个元素的引用。
+ `push_back`：在容器尾部插入元素。
+ `push_back`：删除容器尾部元素。
5. 标准容器类`vector`和`deque`满足这些需求。默认情况下，如果没有为特定的`priority_queue`类实例化指定容器类，则使用`vector`。
6. 需要支持随机访问迭代器，以便始终在内部保持堆结构。容器适配器通过在需要时自动调用算法函数`make_heap`、`push_heap`和`pop_heap`来自动完成此操作。 

##### priority_queue的使用
**优先级队列默认使用**`**vector**`**作为其底层存储数据的容器，在**`**vector**`**上又使用了堆算法将**`**vector**`**中元素构造成堆的结构，因此**`**priority_queue**`**就是堆，所有需要用到堆的位置，都可以考虑使用**`**priority_queue**`**。默认情况下**`**priority_queue**`**是大堆。**

| 函数声明 | 接口说明 |
| :---: | :---: |
| `priority_queue()/priority_queue(first, last)` | 构造一个空的优先级队列。 |
| `empty` | 检测优先级队列是否为空，是返回`true`，否则返回`false`。 |
| `top` | 返回优先级队列中最大(最小元素)，即堆顶元素。 |
| `push(x)` | 在优先级队列中插入元素`x`。 |
| `pop` | 删除优先级队列中最大(最小)元素，即堆顶元素。 |


```cpp
#include <iostream>
#include <queue> // 引入优先级队列的头文件
#include <vector> // 用于构造队列时传入区间

int main()
{
    // 构造一个默认的优先级队列（大顶堆，默认从大到小排序）
    std::priority_queue<int> pq;

    // 使用push插入元素
    pq.push(30);
    pq.push(10);
    pq.push(50);
    pq.push(20);

    // 输出当前队列的堆顶元素，即最大元素
    std::cout << "堆顶元素（最大元素）: " << pq.top() << std::endl;

    // pop操作，移除堆顶元素
    pq.pop();

    // 再次输出堆顶元素，此时最大元素是次大的元素
    std::cout << "移除堆顶后的堆顶元素: " << pq.top() << std::endl;

    // 检查队列是否为空
    if (pq.empty())
    {
        std::cout << "优先级队列是空的" << std::endl;
    }
    else 
    {
        std::cout << "优先级队列不是空的" << std::endl;
    }

    // 使用区间构造优先级队列（也可以用于初始化）
    std::vector<int> vec = { 100, 80, 60, 40, 20 };
    std::priority_queue<int> pq2(vec.begin(), vec.end());

    // 输出用区间构造的优先级队列的堆顶元素
    std::cout << "通过区间构造的堆顶元素: " << pq2.top() << std::endl;

    return 0;
}
```

注意：

1. **默认情况下，**`**priority_queue**`**是大堆。**

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <functional>

int main()
{
    // 默认情况下，创建的是大堆，其底层按照小于号比较
    std::vector<int> v{ 3, 2, 7, 6, 0, 4, 1, 9, 8, 5 };
    std::priority_queue<int> q1;

    // 将向量中的元素插入大顶堆
    for (auto& e : v)
    {
        q1.push(e);
    }

    // 输出堆顶元素
    std::cout << "大顶堆堆顶元素: " << q1.top() << std::endl;

    // 创建小顶堆，底层容器为vector，比较函数为greater<int>
    std::priority_queue<int, std::vector<int>, std::greater<int>> q2(v.begin(), v.end());

    // 输出小顶堆的堆顶元素
    std::cout << "小顶堆堆顶元素: " << q2.top() << std::endl;

    return 0;
}
```

2. 如果在`priority_queue`中放自定义类型的数据，用户需要在自定义类型中提供`>`或`<`的重载。

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <functional>

class Date
{
public:
    // 构造函数，带有默认参数，表示日期
    Date(int year = 1900, int month = 1, int day = 1)
        : _year_(year), _month_(month), _day_(day)
    {}

    // 重载小于运算符，用于比较日期
    bool operator<(const Date& d) const
    {
        // 比较年份，若年份相同则比较月份，若月份也相同则比较日期
        return (_year_ < d._year_) ||
            (_year_ == d._year_ && _month_ < d._month_) ||
            (_year_ == d._year_ && _month_ == d._month_ && _day_ < d._day_);
    }

    // 重载大于运算符，用于反向比较日期
    bool operator>(const Date& d) const
    {
        return (_year_ > d._year_) ||
            (_year_ == d._year_ && _month_ > d._month_) ||
            (_year_ == d._year_ && _month_ == d._month_ && _day_ > d._day_);
    }

    // 重载输出运算符，用于打印日期
    friend std::ostream& operator<<(std::ostream& _cout_, const Date& d)
    {
        _cout_ << d._year_ << "-" << d._month_ << "-" << d._day_;
        return _cout_;
    }

private:
    int _year_;  // 年份
    int _month_; // 月份
    int _day_;   // 日期
};

void TestPriorityQueue()
{
    // 创建大顶堆，使用默认的小于运算符
    std::priority_queue<Date> q1;
    q1.push(Date(2018, 10, 29));
    q1.push(Date(2018, 10, 28));
    q1.push(Date(2018, 10, 30));

    // 打印堆顶元素，应该是最大日期
    std::cout << "大顶堆堆顶: " << q1.top() << std::endl;

    // 创建小顶堆，使用大于运算符作为比较函数
    std::priority_queue<Date, std::vector<Date>, std::greater<Date>> q2;
    q2.push(Date(2018, 10, 29));
    q2.push(Date(2018, 10, 28));
    q2.push(Date(2018, 10, 30));

    // 打印堆顶元素，应该是最小日期
    std::cout << "小顶堆堆顶: " << q2.top() << std::endl;
}

int main()
{
    TestPriorityQueue();  // 测试大顶堆和小顶堆

    return 0;
}
```

##### priority_queue的模拟实现
`priority_queue`的底层结构是堆，因此只需对堆进行通用的封装即可：

```cpp
#pragma once
#include <iostream>

using namespace std;

#include <vector>

// priority_queue 模拟实现的命名空间
namespace my_priority_queue
{
    // less仿函数，用于实现小于号比较
    template<class T>
    struct less
    {
        bool operator()(const T& left, const T& right)
        {
            return left < right;  // 如果左边小于右边，则返回true
        }
    };

    // greater仿函数，用于实现大于号比较
    template<class T>
    struct greater
    {
        bool operator()(const T& left, const T& right)
        {
            return left > right;  // 如果左边大于右边，则返回true
        }
    };

    // priority_queue 类模板定义
    // T 为存储的数据类型，Container 为底层容器类型，默认使用 vector，Compare 为比较函数，默认为 less<T>
    template<class T, class Container = std::vector<T>, class Compare = less<T>>
    class priority_queue
    {
    public:
        // 构造函数，创建一个空的优先级队列
        priority_queue() : c() {}

        // 构造函数，使用迭代器范围初始化队列
        template<class Iterator>
        priority_queue(Iterator first, Iterator last)
            : c(first, last)  // 将区间内的元素存入容器c
        {
            // 将c中的元素调整成堆的结构
            int count = c.size();          // 元素数量
            int root = ((count - 2) >> 1); // 从最后一个非叶子节点开始向下调整
            for (; root >= 0; root--)
                AdjustDown(root);  // 调整每个节点使其符合堆的性质
        }

        // 向优先级队列中插入元素
        void push(const T& data)
        {
            c.push_back(data);      // 将新元素添加到容器末尾
            AdjustUP(c.size() - 1); // 调整新元素位置，确保堆的结构
        }

        // 删除堆顶元素
        void pop()
        {
            if (empty())  // 如果队列为空，直接返回
                return;

            swap(c.front(), c.back());  // 交换堆顶元素和最后一个元素
            c.pop_back();               // 删除最后一个元素（原堆顶）
            AdjustDown(0);              // 从堆顶开始向下调整堆
        }

        // 返回优先级队列中的元素个数
        size_t size()const
        {
            return c.size();
        }

        // 判断优先级队列是否为空
        bool empty()const
        {
            return c.empty();
        }

        // 返回堆顶元素的引用，堆顶元素不可修改
        const T& top()const
        {
            return c.front();
        }

    private:
        // 向上调整，将子节点向上移动到正确的位置
        void AdjustUP(int child)
        {
            int parent = ((child - 1) >> 1);  // 计算父节点索引
            while (child)
            {
                // 如果子节点比父节点优先级高，则交换它们
                if (Compare()(c[parent], c[child]))
                {
                    swap(c[child], c[parent]);  // 交换父子节点
                    child = parent;             // 更新子节点索引
                    parent = ((child - 1) >> 1); // 计算新的父节点索引
                }
                else
                {
                    return;  // 如果子节点已经在正确位置，结束调整
                }
            }
        }

        // 向下调整，将父节点向下移动到正确的位置
        void AdjustDown(int parent)
        {
            size_t child = parent * 2 + 1;  // 计算左子节点索引
            while (child < c.size())        // 当子节点在范围内
            {
                // 选择左右子节点中优先级更高的一个
                if (child + 1 < c.size() && Compare()(c[child], c[child + 1]))
                    child += 1;  // 选择右子节点

                // 如果父节点优先级比子节点低，则交换
                if (Compare()(c[parent], c[child]))
                {
                    swap(c[child], c[parent]);  // 交换父子节点
                    parent = child;             // 更新父节点索引
                    child = parent * 2 + 1;     // 计算新的子节点索引
                }
                else
                    return;  // 如果父节点已经在正确位置，结束调整
            }
        }

    private:
        Container c;  // 存储数据的容器
    };
}

// 测试自定义 priority_queue 类
void TestQueuePriority()
{
    // 创建一个默认的大顶堆
    my_priority_queue::priority_queue<int> q1;
    q1.push(5);
    q1.push(1);
    q1.push(4);
    q1.push(2);
    q1.push(3);
    q1.push(6);
    cout << q1.top() << endl;  // 输出堆顶元素（最大值）

    q1.pop();  // 删除堆顶
    q1.pop();  // 再次删除堆顶
    cout << q1.top() << endl;  // 输出新的堆顶元素

    // 创建一个小顶堆
    vector<int> v{ 5,1,4,2,3,6 };
    my_priority_queue::priority_queue<int, vector<int>, my_priority_queue::greater<int>> q2(v.begin(), v.end());
    cout << q2.top() << endl;  // 输出堆顶元素（最小值）

    q2.pop();  // 删除堆顶
    q2.pop();  // 再次删除堆顶
    cout << q2.top() << endl;  // 输出新的堆顶元素
}
```

#### 容器适配器
##### 什么是容器适配器
 C++中的容器适配器(Container Adapter)是一类特殊的容器，它们并不是从零开始设计的，而是基于已有的标准容器(如`vector`、`deque`、`list`)进行封装，为特定的操作模式提供简化的接口。容器适配器隐藏了底层容器的实现细节，并对外提供了一组有限的接口来操作容器。

常见的容器适配器有以下三种：

1. `**stack**`：栈，遵循后进先出的规则。
2. `**queue**`：队列，遵循先进先出的规则。
3. `**priority_queue**`：优先队列，元素根据优先级进行排序，最大元素优先被访问。

容器适配器的特点：

+ **有限的接口**：相比于标准容器，容器适配器通常只提供一部分功能。比如`stack`只允许对栈顶进行操作，而不允许遍历整个栈。
+ **基于底层容器实现**：容器适配器是基于其他标准容器(如`deque`、`vector`、`list`)来实现的。用户可以指定底层容器类型(默认是`deque`)，但不会直接操作底层容器的具体实现。
+ **不提供迭代器**：大部分容器适配器(如`stack`和`queue`)不支持迭代器，因此不能使用迭代器来遍历其中的元素。

##### 标准库中stack和queue的底层结构
虽然`stack`和`queue`中也可以存放元素，但在STL中并未将其划分在容器行列，而是将其称为容器适配器，这是因为`stack`和`queue`只是对其他容器的接口进行了包装，STL中的`stack`和`queue`默认使用`queue`，比如：

```c
// std:stack
template <class T, class Container = deque<T> > class stack;
// std::queue
template <class T, class Container = deque<T> > class queue;
// std::priority_queue
template <class T, class Container = vector<T>,  class Compare = less<typename Container::value_type> > class priority_queue;
```

### 模板进阶
#### 非类型模板参数
##### 非类型模板参数
 在C++中，模板参数分为**类型形参**和**非类型形参**，它们在模板定义中分别扮演不同的角色。  

+ **类型形参**：是指模板参数是一个类型(如`int`、`double`、`std::vector<int>`等)。类型形参用于让模板能够对不同的数据类型进行泛型编程。通过类型形参，用户可以在模板实例化时传递实际的类型。  
+ **非类型形参**：是指模板参数是一个常量值，而不是类型。非类型形参的值必须在编译时已知，常见的非类型形参有整型(如`int`、`char`、指针、引用等)。非类型形参用于传递常量值给模板，使模板能够根据这些常量值进行不同的实例化。**注意：浮点数、类对象以及字符串是不允许作为非类型模板参数的，非类型的模板参数必须在编译期就能确认结果。**

```cpp
#include <iostream>  

#define N 100  // 定义宏 N，表示数组的大小为 100

// 定义模板类 Array，其中 T 是类型模板参数
template<class T>  // 类型模板参数，用于指定数组元素的类型
class Array
{
public:
    // 可以在 public 区域定义一些操作数组的成员函数，例如获取数组大小或访问数组元素等
private:
    T _a_[N];  // 使用宏 N 来定义数组的大小，数组类型由模板参数 T 决定
};

int main()
{
    Array<int> a1;     // 创建一个元素类型为 int，大小为 100 的数组对象
    Array<double> a2;  // 创建一个元素类型为 double，大小为 100 的数组对象

    return 0;  // 程序正常结束
}

```

上述代码中，`T`是一个类型形参，我们可以用模板创建不同类型的数组对象`a1`与`a2`，现在如果有一个需求，`a1`为大小`100`元素类型为`int`的数组对象，`a2`为大小`1000`元素类型为`double`的数组对象，那么应该如何完成呢？

很显然，如果只是用类型模板参数，那么可以使用构造函数来传递数组大小，在运行时动态分配内存给数组：

```cpp
#include <iostream>

template<class T>  // 只使用类型模板参数
class Array
{
public:
    Array(int size) : _size_(size)  // 构造函数接收数组大小
    {
        _a_ = new T[_size_];  // 动态分配数组
    }

    ~Array()
    {
        delete[] _a_;  // 释放动态分配的内存
    }

private:
    T* _a_;  // 指向动态分配的数组
    int _size_;  // 存储数组大小
};

int main()
{
    Array<int> a1(100);  // 创建一个大小为 100 的 int 数组
    Array<double> a2(1000);  // 创建一个大小为 1000 的 double 数组

    return 0;
}
```

更加简单的方式为使用非类型模板参数，可以将`N`作为模板参数传入，以便在创建对象时指定数组大小：

```cpp
#include <iostream>

template<class T, int N>  // 类型模板参数 + 非类型模板参数
class Array
{
public:
    // 在这里可以实现一些数组的操作函数
private:
    T _a_[N];  // 数组的大小由 N 指定
};

int main()
{
    Array<int, 100> a1;  // 创建一个大小为 100 的 int 数组
    Array<double, 1000> a2;  // 创建一个大小为 1000 的 double 数组

    return 0;
}
```

##### 可作为非类型模板参数的类型  
 在 C++ 中，非类型模板参数是指模板参数可以是一个固定的值(非类型的)，而不仅仅是类型。这些非类型模板参数在编译时就要确定，并且它们受限于某些特定的类型。C++标准规定以下类型可以作为非类型模板参数：

+ **整型常量**(包括枚举类型)：可以是整数类型(`int`、`char`、`bool`、`unsigned` 等)或枚举类型。  
+ **指针或引用类型**：可以使用指向对象或函数的指针，也可以使用引用。 
+ **常量表达式的指针**：指向对象、函数或类成员的常量指针。
+ **函数指针或成员函数指针**：允许将函数指针作为模板参数。  
+ **常量引用**：可以使用对常量对象的引用作为模板参数。
+ `**std::nullptr_t**`：允许使用`nullptr`作为非类型模板参数。 

```cpp
// 整型常量 - 使用 int 类型的非类型模板参数来定义数组的大小
template<int N>
class Array
{
    int _data_[N];
};

// 整型常量 - 也可以使用 bool 作为非类型模板参数
template<bool flag>
class MyClass {};

// 指针或引用类型
template<int* ptr>
class PtrClass {};

// 常量表达式的指针
int x = 10;
template<const int* ptr>
class PointerClass {};

// 函数指针或成员函数指针
template<void(*Func)()>
class FuncWrapper {};

// 常量引用
template<const int& ref>
class RefClass {};

// std::nullptr_t
template<std::nullptr_t N>
class NullClass {};
```

##### 不可作为非类型模板参数的类型 
一些类型由于其动态性或不确定性，不能作为非类型模板参数：

+ **浮点类型(**`**float**`**、**`**double**`**)**： 由于精度问题和不同平台的表示差异，不能作为非类型模板参数。
+ **类类型(包括**`**std::string**`**等标准库类型)**：非类型模板参数不能是类类型的对象，因为类的对象需要运行时才能被创建和确定。
+ **非常量表达式**：非类型模板参数必须是编译时常量，任何运行时才能确定的表达式或变量都不能作为非类型模板参数。

```cpp
// 浮点类型
template<float N>
class FloatClass {};  // 错误，浮点类型不能作为非类型模板参数

// 类类型
template<std::string str>
class StringClass {};  // 错误，std::string 不能作为非类型模板参数

// 非常量表达式
int x = 10;
template<int N = x>  // 错误，x 是运行时变量，不能作为非类型模板参数
class MyClass {};
```

#### 类模板的特化
##### 概念
通常情况下，使用模板可以实现一些与类型无关的代码，但对于一些特殊类型的可能会得到一些错误的结果，需要特殊处理，例如实现了一个专门用来进行小于比较的函数模板：

```cpp
#include <iostream>

// 通用的模板函数，用于比较两者是否小于
template<typename T>
bool Less(const T& a, const T& b) 
{
    return a < b;  // 普通情况下比较a和b
}

int main() 
{
    int x = 5, y = 10;
    int* p1 = &x;
    int* p2 = &y;

    std::cout << "Comparing x and y: " << Less(x, y) << std::endl; 

    std::cout << "Comparing p1 and p2: " << Less(p1, p2) << std::endl; 

    return 0;
}
```

可以看到，`Less`绝对多数情况下都可以正常比较，但是在特殊场景下可能会得到错误的结果。上述示例中，`p1`指向的`x`显然小于`p2`指向的`y`，但是`Less`内部并没有比较`p1`和`p2`指向的对象内容，而比较的是`p1`和`p2`指针的地址，这就无法达到预期而错误。此时，就需要对模板进行特化，即**在原模板类的基础上，针对特殊类型所进行特殊化的实现方式。模板特化分为函数模板特化与类模板特化。**

当然，为了解决上述问题，这里也可以使用函数模板重载，根据传递的参数类型自动选择合适的函数版本，而无需显式指定类型：

```cpp
#include <iostream>

// 通用的模板函数，用于比较两者是否小于
template<typename T>
bool Less(const T& a, const T& b)
{
    return a < b;  // 普通情况下比较a和b
}

// 针对指针类型的模板重载，比较指针指向的对象
template<typename T>
bool Less(T* a, T* b)
{
    if (a && b)  // 检查指针是否有效
    {
        return *a < *b;  // 比较指针指向的对象
    }
    return false;  // 如果有空指针，返回false
}

int main()
{
    int x = 5, y = 10;
    int* p1 = &x;
    int* p2 = &y;

    // 使用通用模板版本比较x和y的值
    std::cout << "Comparing x and y: " << Less(x, y) << std::endl; // 输出: 1 (x < y)

    // 使用指针类型的重载版本比较p1和p2指向的对象的值
    std::cout << "Comparing p1 and p2: " << Less(p1, p2) << std::endl; // 输出: 1 (*p1 < *p2)

    return 0;
}
```

##### 函数模板特化
函数模板的特化步骤：

1. **定义通用模板**： 创建适用于所有类型的通用模板函数。
2. **声明模板特化**：使用`template<>`和特定类型进行模板特化声明。  
3. **定义特化版本**：函数名后跟一对尖括号，尖括号中指定需要特化的类型。
4. **函数形参表**<font style="color:rgb(119,119,119);">：</font>必须与模板函数的基础参数类型完全相同，否则编译器可能会报一些奇怪的错误。
5. **调用和选择**：编译器会根据参数类型自动选择合适的模板版本(通用或特化)。

##### 类模板特化
###### 全特化
类模板全特化是一种将模板类的所有实例化特化为某一特定类型的技术。意味着我们定义一个模板类，并为特定的类型提供完全不同的实现，而不依赖原始模板类中的任何内容。

在类模板全特化中，我们为特定类型重新定义整个类结构，而不再使用通用模板类的成员或函数。例如：通用类模板和指针类型的全特化。代码如下：

```cpp
#include <iostream>

// 通用模板类，用于比较两个对象是否相等
template<typename T>
struct Equal
{
    bool operator()(const T& a, const T& b) const
    {
        return a == b;  // 对于普通类型，直接比较值
    }
};

// 针对指针类型的全特化，比较指针指向的对象
template<>
struct Equal<int*>
{
    bool operator()(int* a, int* b) const
    {
        if (a && b)  // 检查指针是否有效
        {
            return *a == *b;  // 比较指针指向的对象是否相等
        }
        return false;  // 如果有空指针，返回false
    }
};

int main()
{
    int x = 5, y = 5;
    int* p1 = &x;
    int* p2 = &y;

    // 使用通用模板版本比较两个普通整数
    Equal<int> equalObj;
    std::cout << "Comparing x and y: " << equalObj(x, y) << std::endl; // 输出: 1 (x == y)

    // 使用全特化版本比较两个指针指向的对象
    Equal<int*> equalPtrObj;
    std::cout << "Comparing p1 and p2: " << equalPtrObj(p1, p2) << std::endl; // 输出: 1 (*p1 == *p2)

    return 0;
}
```

###### 偏特化
偏特化允许对模板的部分参数进行特化，而不是像全特化那样对所有参数特化。类模板偏特化是针对部分模板参数的特化，而不是全部参数，从而提供更灵活的实现方式。继上一个例子，比较两个对象是否相等，此例中，我们将指针类型进行偏特化，而不是只对`int*`特化。我们将为所有指针类型`T*`实现偏特化，比较它们指向的对象是否相等。代码如下：

```cpp
#include <iostream>

// 通用模板类，比较两个对象是否相等
template<typename T>
struct Equal
{
    bool operator()(const T& a, const T& b) const
    {
        return a == b;  // 普通情况下，比较a和b的值
    }
};

// 针对指针类型的偏特化，比较指针指向的对象是否相等
template<typename T>
struct Equal<T*>
{
    bool operator()(T* a, T* b) const
    {
        if (a && b)  // 检查指针是否有效
        {
            return *a == *b;  // 比较指针指向的对象
        }
        return false;  // 如果有空指针，返回false
    }
};

int main()
{
    int x = 5, y = 5;
    int* p1 = &x;
    int* p2 = &y;

    double d1 = 3.14, d2 = 3.14;
    double* pd1 = &d1;
    double* pd2 = &d2;

    // 使用通用模板比较普通类型
    Equal<int> equalObj;
    std::cout << "Comparing x and y: " << equalObj(x, y) << std::endl; // 输出: 1 (x == y)

    // 使用偏特化版本比较指针类型（int*）
    Equal<int*> equalPtrObj;
    std::cout << "Comparing p1 and p2: " << equalPtrObj(p1, p2) << std::endl; // 输出: 1 (*p1 == *p2)

    // 使用偏特化版本比较指针类型（double*）
    Equal<double*> equalDoublePtrObj;
    std::cout << "Comparing pd1 and pd2: " << equalDoublePtrObj(pd1, pd2) << std::endl; // 输出: 1 (*pd1 == *pd2)

    return 0;
}
```

#### 模板的分离编译
##### 什么是分离编译
**分离编译**是C++中一种编译方式，它允许程序的源代码被分割成多个源文件(通常是`.cpp`文件)，并分别编译成单独的目标文件(通常是`.o`或`.obj`文件)，最终通过**链接**将这些目标文件结合起来生成可执行文件或库。 

###### **分离编译的基本概念**
1. **头文件(Header Files，**`**.h**`**或**`**.hpp**`**文件)**：
+ 头文件通常包含类声明、函数声明、常量、宏定义和模板等信息。这些文件不会被单独编译，而是通过`#include`指令在源文件中进行包含，提供了必要的接口和声明。
2. **源文件(Source Files，**`**.cpp**`**文件)**：
+ 源文件包含函数或类的实现。每个源文件通常包含一个头文件，通过`#include`引入接口声明，然后实现具体的功能。
3. **目标文件(Object Files，**`**.o**`**或**`**.obj**`**文件)**：
+ 每个源文件可以独立编译为一个目标文件，目标文件是机器代码的中间形式，包含实现的函数和变量，但是还未被链接成完整的可执行程序。
4. **链接(Linking)**：
+ 将多个编译后的目标文件链接在一起，形成最终的可执行文件或静态/动态库。链接器负责解决各个源文件中相互依赖的符号和地址。

###### **分离编译的过程**
1. **编写头文件和源文件**：
+ 将声明和实现分离，例如在头文件中声明函数原型，在源文件中实现函数逻辑。
2. **独立编译源文件**：
+ 每个`.cpp`源文件会被单独编译成对应的目标文件(如`.o`或`.obj`)，这意味着你不必每次修改代码时都重新编译整个程序，只需编译修改的部分。
3. **链接目标文件**：
+ 将所有目标文件链接在一起，生成最终的可执行文件。

例如我们有一个简单的程序，它包含一个数学库和主程序，数学库`mathlib.h`代码如下：

```cpp
// mathlib.h
#ifndef MATHLIB_H
#define MATHLIB_H

// 函数声明
int add(int a, int b);
int subtract(int a, int b);

#endif // MATHLIB_H
```

源文件`mathlib.cpp`代码如下：

```cpp
// mathlib.cpp
#include "mathlib.h"

// 函数实现
int add(int a, int b)
{
    return a + b;
}

int subtract(int a, int b) 
{
    return a - b;
}
```

主程序文件`main.cpp`代码如下：

```cpp
// main.cpp
#include <iostream>
#include "mathlib.h"  // 包含头文件

int main() 
{
    int x = 10, y = 5;
    std::cout << "Add: " << add(x, y) << std::endl;
    std::cout << "Subtract: " << subtract(x, y) << std::endl;
    
    return 0;
}
```

###### **编译与链接**
在分离编译的方式下，编译和链接可以通过以下步骤完成：

1. **编译**`**mathlib.cpp**`：
+ `g++ -c mathlib.cpp -o mathlib.o`

这会将`mathlib.cpp`编译为目标文件`mathlib.o`。

2. **编译**`**main.cpp**`：
+ `g++ -c main.cpp -o main.o`

同样，将`main.cpp`编译为目标文件`main.o`。

3.  **链接目标文件**：
+ `g++ main.o mathlib.o -o my_program`

这一步将两个目标文件链接在一起，生成最终的可执行文件`my_program`。

4. **运行程序**：
+ `./my_program`

###### **分离编译的注意事项**
1. **多次包含保护**：头文件通常需要使用"包含保护"(如`#ifndef MATHLIB_H`、`#define MATHLIB_H`)以防止同一个头文件被多次包含，导致编译错误。  
2. **符号重定义**： 确保函数或变量定义只出现在一个源文件中，避免在多个源文件中重复定义同一个符号。  
3. **链接错误**：如果一个源文件使用了另一个源文件中定义的函数或变量，编译时可能不会出现问题，但在链接时可能会报错。需要确保所有相关的目标文件都参与链接。  

##### 模板的分离编译
在C++中，**模板的分离编译**与常规类和函数的分离编译有所不同，因为模板的具体实例化是在**编译时**完成的。模板的定义和使用通常是在同一个翻译单元(源文件)中进行的，否则会出现编译链接错误(如未定义引用的错误)。这是因为模板的**实例化**是延迟的，编译器只有在模板被使用时才会实例化它。 

在大型项目中，模板的定义和实现往往需要分开，以提高代码的可维护性和模块化。为了实现模块的分离编译，C++提供了几种常见的方式。

##### 模板的分离编译问题
 模板的定义通常放在头文件中，因为模板本质上是**编译器的代码生成器**。编译器在看到模板的定义时，不会立即生成代码，只有当模板在某处被具体使用时(即模板实例化时)，编译器才会生成对应类型的代码。因此，如果模板的实现与其声明分开，并且模板的实现不在同一个翻译单元中，编译器将无法实例化模板，导致链接错误。

有几种方法可以将模板的实现与其声明分离，同时避免模板的实例化问题。

###### **将模板的定义与实现放在同一个头文件**
这是最简单 也是最常见的方式，即将模板的声明和实现都放在头文件中。这样，所有包含该头文件的翻译单元都可以看到模板的定义，并在需要时进行实例化。例如以下，头文件中包含模板的定义与实现：

```cpp
// mytemplate.h
#ifndef MYTEMPLATE_H
#define MYTEMPLATE_H

// 模板函数声明和实现都在头文件中
template<typename T>
T add(const T& a, const T& b) 
{
    return a + b;
}

#endif // MYTEMPLATE_H
```

在这种方式下，任何包含`mytemplate.h`文件的源文件都会生成模板的实例化。

###### **将实现放在头文件的**`**.inl**`**文件中**
为了实现更好的代码组织结构，常见的做法是将模板的声明和实现分离，但依然将实现放在头文件中。具体来说，我们可以在头文件中声明模板，并将实现放在与头文件配对的`.inl`(内联)文件中。例如以下，头文件和`.inl`文件分离  ：

```cpp
// mytemplate.h
#ifndef MYTEMPLATE_H
#define MYTEMPLATE_H

// 模板函数声明
template<typename T>
T add(const T& a, const T& b);

// 包含实现的 .inl 文件
#include "mytemplate.inl"

#endif // MYTEMPLATE_H
```

```cpp
// mytemplate.inl
template<typename T>
T add(const T& a, const T& b) 
{
    return a + b;
}
```

通过这种方式，模板的实现被分离到`.inl`文件中，但由于头文件最终还是包含`.inl`文件，所以编译器仍然能看到模板的完整定义，从而可以进行实例化。

###### ** 显式实例化(Explicit Instantiation) **
 另一种方法是通过**显式实例化**来实现模板的分离编译。在这种方法中，模板的声明放在头文件中，而实现放在`.cpp`文件中。然后，在`.cpp`文件中，针对需要的模板参数进行显式实例化。这种方式的缺点是你必须明确知道你要实例化的模板类型。例如以下的显式实例化：

```cpp
// mytemplate.h
#ifndef MYTEMPLATE_H
#define MYTEMPLATE_H

// 模板函数声明
template<typename T>
T add(const T& a, const T& b);

#endif // MYTEMPLATE_H
```

```cpp
// mytemplate.cpp
#include "mytemplate.h"

// 模板函数的实现
template<typename T>
T add(const T& a, const T& b) {
    return a + b;
}

// 针对特定类型进行显式实例化
template T add<int>(const int& a, const int& b);
template T add<double>(const double& a, const double& b);
```

在这种情况下，`mytemplate.h`中包含的是模板的声明，而`mytemplate.cpp`中包含模板的实现和显式实例化。当编译器编译`mytemplate.cpp`文件时，它会生成针对`int`和`double`类型的`add`函数的实例。这种方式适用于只需要模板的某些特定类型的实例化时，可以避免重复实例化和过多代码膨胀。

###### 使用外部模板(C++11)
 C++11引入了`extern`关键字用于模板实例化。通过这个关键字，可以在某个翻译单元中实例化模板，而在其他翻译单元中声明使用它。这允许模板在单独的编译单元中实例化。例如以下：

```cpp
// mytemplate.h
#ifndef MYTEMPLATE_H
#define MYTEMPLATE_H

// 模板函数声明
template<typename T>
T add(const T& a, const T& b);

// 声明外部模板实例
extern template T add<int>(const int& a, const int& b);

#endif // MYTEMPLATE_H
```

```cpp
// mytemplate.cpp
#include "mytemplate.h"

// 模板函数实现
template<typename T>
T add(const T& a, const T& b) {
    return a + b;
}

// 定义外部模板实例
template T add<int>(const int& a, const int& b);
```

在这种方式下，模板的实例化只会在`mytemplate.cpp`中发生，而在其他包含了`mytemplate.h`的文件中，编译器知道`add<int>`已经在别处实例化了，它不会再次实例化该模板。  

###### 模板分离编译总结
+ **直接在头文件中实现模板**：这是最常见的做法，因为模板的实例化需要看到完整的实现。
+ **将实现分离到 **`**.inl**`** 文件中**：这种方法有助于代码的组织，使头文件更加简洁。
+ **显式实例化**：适用于只需要少量模板实例化的场景，有助于减少代码膨胀。
+ **外部模板**：使用 C++11 的 `extern` 关键字来控制模板实例化的翻译单元。

### 继承
#### 继承的概念及定义
##### 继承的基本概念
**继承**是面向对象编程中的一个核心概念，它允许一个类从另一个类中获取属性和方法，从而实现代码的复用和扩展。继承可以让子类(派生类)继承父类(基类)的成员函数和数据成员，并且子类可以根据需要添加新的成员或修改父类中的成员。 

**基类(Base Class)**也称为父类或超类，表示原始类，它提供了子类可以继承的成员。 

**派生类(Derived Class)**也称为子类或扩展类，表示从基类继承而来的类，派生类可以继承、扩展或重写基类中的属性和行为。  

继承的语法为：

```cpp
class 基类
{
    // 基类的成员
};

class 派生类 : 访问控制 基类 
{
    // 派生类的成员
};
```

其中，访问控制可以是`public`、`protected`、`private`，决定了基类成员在派生类中的访问权限。

```cpp
#include <iostream>  
#include <string>    

// 定义 Person 类，作为基类
class Person
{
public:
    // 定义一个公共成员函数 Print，用于打印 Person 对象的姓名和年龄
    void Print()
    {
        std::cout << "name: " << _name_ << std::endl;  // 输出姓名
        std::cout << "age: " << _age_ << std::endl;    // 输出年龄
    }

protected:
    // 定义受保护的成员变量，派生类可访问
    std::string _name_ = "job";  // 默认值为 "job" 的姓名
    int _age_ = 18;              // 默认值为 18 的年龄
};

// Student 类从 Person 类公有继承
// 继承后，Person 类的成员函数和成员变量都会成为 Student 类的一部分
class Student : public Person
{
protected:
    int _stuid_;  // 学生的学号，受保护的成员变量，仅派生类和自己可访问
};

// Teacher 类从 Person 类公有继承
// 同样继承了 Person 的成员函数和成员变量
class Teacher : public Person
{
protected:
    int _jobid_;  // 教师的工号，受保护的成员变量
};

int main()
{
    Student s;  // 创建 Student 类的对象 s
    Teacher t;  // 创建 Teacher 类的对象 t

    // 调用 Student 对象 s 的 Print 函数
    // 由于 Student 继承了 Person，所以可以调用 Person 的成员函数 Print
    s.Print();  // 输出默认的姓名 "job" 和年龄 18

    // 调用 Teacher 对象 t 的 Print 函数
    // 同样地，由于 Teacher 继承了 Person，也可以调用 Print
    t.Print();  // 输出默认的姓名 "job" 和年龄 18

    return 0;  // 程序正常结束
}
```

##### 继承的访问控制类型
1. **公有继承(public inheritance)**：
+ 基类的`public`成员在派生类中仍然是`public`。
+ 基类的`protected`成员在派生类中保持`protected`。
+ 基类的`private`成员不能被派生类直接访问，但可以通过基类的`public`或`protected`成员函数间接访问。

```cpp
class Base 
{
public:
    int x;

protected:
    int y;

private:
    int z;
};

class Derived : public Base 
{
public:
    void display() 
    {
        x = 1;  // 可访问 Base 的 public 成员
        y = 2;  // 可访问 Base 的 protected 成员
        // z = 3;  // 不可访问 Base 的 private 成员
    }
};
```

2. **保护继承(protected inheritance)**：
+ 基类的`public`成员在派生类中变为`protected`。
+ 基类的`protected`成员在派生类中保持`protected`。
+ 基类的`private`成员任然不可直接访问。

```cpp
class Base 
{
public:
    int x;

protected:
    int y;

private:
    int z;
};

class Derived : protected Base
{
public:
    void display() 
    {
        x = 1;  // 现在 x 是 protected 成员
        y = 2;  // y 仍然是 protected 成员
        // z = 3;  // 不可访问 Base 的 private 成员
    }
};
```

3. **私有继承(private inheritance)**：
+ 基类的`public`和`protected`成员在派生类中变为`private`。
+ 基类的`private`成员任然不可直接访问。

```cpp
class Base 
{
public:
    int x;

protected:
    int y;

private:
    int z;
};

class Derived : private Base 
{
public:
    void display() 
    {
        x = 1;  // 现在 x 是 private 成员
        y = 2;  // y 现在也是 private 成员
        // z = 3;  // 不可访问 Base 的 private 成员
    }
};
```

总结：

1. 基类`private`成员在派生类中无论以什么方式继承都是不可见的。**这里的不可见是指基类的私有成员还是被继承到了派生类对象中，但是语法上限制派生类对象不管在类里还是类外都不能去访问它。**
2. 基类`private`成员在派生类中不能被访问，如果基类成员不想在类外直接被访问，但需要在派生类中能访问，就定义为`protected`。**保护成员限定符是因继承才出现的。**
3. 基类的私有成员在派生类中均不可见，**基类的其他成员在派生类的访问方式为Min(成员在基类的访问限定符，继承方式)，其中**`**public**`**> **`**protected**`** > **`**private**`**。**
4. **使用关键字**`**class**`**时默认的继承方式是**`**private**`**，使用**`**struct**`**时默认的继承方式是**`**public**`**，但最好显式的写出继承方式。**
5. **实际中通常使用**`**public**`**继承，几乎很少也不提倡使用**`**protected**`**与**`**private**`**继承**，因为`protected`与`private`继承下来的成员都只能在派生类的类中使用，实际扩展维护较差。

#### 基类和派生类对象赋值转换
**基类和派生类对象赋值转换**是面向对象编程中非常重要的一个概念，它涉及到对象类型之间的转换。派生类对象可以被赋值给基类对象或基类指针，这种转换被称为**向上转换**(Upcasting)，而基类对象向派生类对象的转换则被称为**向下转换**(Downcasting)。  

##### 向上转换
+ **向上转换是指将派生类对象转换为基类类型，这种转换是安全的，不需要显式类型转换。**
+ **当进行向上转换时，派生类对象的基类部分被保留，而派生类新增的部分则无法通过基类访问。**
+ ** 派生类对象可以赋值给基类对象、指针和引用。**

```cpp
#include <iostream>

class Person
{
public:
    void Print()
    {
        std::cout << "This is a Person." << std::endl;
    }
};

class Student : public Person
{
public:
    void Study()
    {
        std::cout << "This is a Student studying." << std::endl;
    }
};

int main()
{
    Student s;  // 定义一个 Student 类的对象 s

    Person p = s;  // 向上转换，将 Student 对象 s 转换为 Person 类型对象 p
    // 由于是值赋值，基类对象 p 拷贝了派生类对象 s 的基类部分
    // 派生类中的新增部分（如 Study 函数）无法通过 p 访问

    Person* ptr = &s;  // 向上转换，将 Student 对象 s 的地址赋值给 Person* 类型的指针 ptr
    // 通过 ptr 指针，可以访问基类 Person 中的成员函数

    Person& ref = s;   // 向上转换，将 Student 对象 s 的引用赋值给 Person& 类型的引用 ref
    // 通过 ref 引用，可以访问基类 Person 中的成员函数

    p.Print();     // 调用基类的 Print 函数，输出 "This is a Person."
    // p.Study();  // 错误：基类对象无法访问派生类的成员函数 Study

    ptr->Print();  // 通过指针 ptr 调用基类的 Print 函数，输出 "This is a Person."
    ref.Print();   // 通过引用 ref 调用基类的 Print 函数，输出 "This is a Person."

    return 0;
}
```

注意：

+ **当**`**Student**`**对象**`**s**`**赋值给**`**Person**`**对象**`**p**`**时，只会保留**`**Person**`**部分，**`**Student**`**的扩展部分(如**`**Study**`**函数)将无法访问。**
+ **向上转换是隐式的，不需要显式类型转换。**

##### 向下转换
+ **向下转换是指将基类对象转换为派生类对象。这种转换通常不安全，可能会导致未定义行为，因此需要显式进行，并且通常需要借助C++的**`**dynamic_cast**`**。**
+ **向下转换通常涉及使用基类指针或引用指向派生类对象，然后尝试将其转换回派生类类型。**

```cpp
#include <iostream>  
   
class Person 
{
public:
    virtual void Print() 
    {
        std::cout << "This is a Person." << std::endl;
    }
};

class Student : public Person 
{
public:
    void Study() 
    {
        std::cout << "This is a Student studying." << std::endl;
    }
};

int main() 
{
    Student s;
    Person* p = &s;  // 向上转换：Student 指针转换为 Person 指针
    p->Print();      // 调用基类的 Print 函数

    // 向下转换：将 Person 指针转换为 Student 指针
    Student* sPtr = dynamic_cast<Student*>(p);
    if (sPtr) 
    {
        sPtr->Study();  // 安全调用派生类函数
    }

    return 0;
}
```

注意：

+ `**dynamic_cast**`**用于向下转换，它会在运行时检查转换是否成功。如果**`**p**`**实际上指向的是**`**Student**`**对象，则转换成功；否则返回**`**nullptr**`**。**
+ ** 只有基类中的成员函数被声明为**`**virtual**`**时，**`**dynamic_cast**`**才能正确运行。**
+ ** 向下转换需要小心，错误的向下转换可能导致运行时错误或未定义行为。**

#### 继承中的作用域
+ **在继承体系中基类和派生类都有独立的作用域。**
+ **子类和父类中有同名成员，子类成员将屏蔽父类对同名成员的直接访问，这种情况叫隐藏，也叫重定义。此时，派生类将直接使用自己的同名成员，除非显式指定使用基类的成员。通过**`**基类名::成员名**`**的方式，可以在派生类中访问基类的被隐藏成员。  **

```cpp
#include <iostream>  
   
class Base
{
public:
    void show()
    {
        std::cout << "Base show" << std::endl;
    }
};

class Derived : public Base
{
public:
    void show()
    {
        std::cout << "Derived show" << std::endl;
    }

    void accessBaseShow()
    {
        Base::show();  // 显式调用基类的 show()
    }
};

int main() 
{
    Derived obj;
    obj.show();  // 调用 Derived 的 show()
    obj.accessBaseShow();  // 显式调用 Base 的 show()

    return 0;
}
```

+ **需要注意，函数的隐藏不仅仅局限于函数签名的完全相同，只要函数名相同就会发生隐藏，无论参数是否相同。即使派生类中定义了同名但参数不同的函数，基类中所有同名的函数都会被隐藏。  **

```cpp
#include <iostream>  
   
class Base
{
public:
    void show(int x)
    {
        std::cout << "Base show whith int: " << x << std::endl;
    }
};

class Derived : public Base
{
public:
    void show()
    {
        std::cout << "Derived show without parameters" << std::endl;
    }
};

int main() 
{
    Derived obj;
    obj.show();  // 调用 Derived 的 show()
    // obj.show(10); // 编译错误，Base::show 被隐藏
    obj.Base::show(10);  // 显式调用 Base 的 show()

    return 0;
}
```

+ **在实际编程中，尽量避免基类和派生类中出现同名成员，以防止不必要的混淆和隐藏问题。如果设计需要，建议明确使用命名空间或通过 **`**基类名::成员名**`** 的方式解决。  **

#### 派生类的默认成员函数
##### 默认构造函数
+ **若基类有默认构造函数，派生类的默认构造函数会自动调用基类的默认构造函数来初始化基类部分。**
+ **若基类没有默认构造函数，而派生类不显式调用基类的构造函数，则编译报错，要求在派生类的构造函数中明确调用基类的构造函数。**

```cpp
#include <iostream>  
   
class Base
{
public:
    Base()
    {
        std::cout << "Base 默认构造函数" << std::endl;
    }
};

class Derived : public Base
{
public:
    Derived()
    {
        std::cout << "Derived 默认构造函数" << std::endl;
    }
};

int main() 
{
    Derived d;  // 调用顺序：Base() -> Derived()

    return 0;
}
```

注意：

+ **构造函数的调用顺序是：基类先于派生类。**
+ **如果基类有参数化构造函数，派生类的构造函数需要显式调用基类的构造函数。**

```cpp
#include <iostream>

// 基类 Base
class Base
{
public:
    // 带参数的构造函数，用来初始化 _x_
    Base(int val) 
        : _x_(val)  // 初始化成员变量 _x_
    {
        std::cout << "Base 带参构造函数，_x_ = " << _x_ << std::endl;
    }

private:
    int _x_;  // 基类中的私有成员变量 _x_
};

// 派生类 Derived，继承自 Base
class Derived : public Base
{
public:
    // 派生类构造函数，显式调用基类的带参构造函数
    Derived(int baseVal, int derivedVal)
        : Base(baseVal)  // 调用基类的构造函数初始化基类部分
        , _y_(derivedVal)  // 初始化派生类的成员变量 _y_
    {
        std::cout << "Derived 构造函数, _y_ = " << _y_ << std::endl;
    }

private:
    int _y_;  // 派生类中的私有成员变量 _y_
};

int main() 
{
    // 创建 Derived 对象，传入 10 和 20 作为构造函数参数
    Derived d(10, 20); 

    // 程序结束时，会自动调用析构函数
    return 0;
}
```

##### 拷贝构造函数
+ **如果派生类没有定义自己的拷贝构造函数，编译器会自动生成一个默认的拷贝构造函数。默认的拷贝构造函数会按成员进行逐一复制，并调用基类的拷贝构造函数来拷贝基类部分。**
+ **如果基类中含有资源管理，派生类可能需要重载拷贝构造函数以确保正确的资源管理。**

```cpp
#include <iostream>

// 基类 Base
class Base
{
public:
    // 默认构造函数
    Base()
        : _baseVal_(0)  // 初始化成员 _baseVal_ 为 0
    {
        std::cout << "Base 默认构造函数" << std::endl;
    }

    // 拷贝构造函数
    Base(const Base& other)
    {
        // 将 other 的 _baseVal_ 拷贝到当前对象
        _baseVal_ = other._baseVal_;
        std::cout << "Base 拷贝构造函数" << std::endl;
    }

private:
    int _baseVal_;  // 基类中的私有成员变量
};

// 派生类 Derived，继承自 Base
class Derived : public Base
{
public:
    // 默认构造函数
    Derived()
        : _derivedVal_(0)  // 初始化成员 _derivedVal_ 为 0
    {
        std::cout << "Derived 默认构造函数" << std::endl;
    }

    // 拷贝构造函数
    Derived(const Derived& other)
        : Base(other)  // 调用基类的拷贝构造函数，拷贝基类部分
    {
        // 拷贝派生类中的成员 _derivedVal_
        _derivedVal_ = other._derivedVal_;
        std::cout << "Derived 拷贝构造函数" << std::endl;
    }

private:
    int _derivedVal_;  // 派生类中的私有成员变量
};

int main()
{
    Derived d1;  // 调用派生类的默认构造函数，首先会调用基类的默认构造函数
    Derived d2 = d1;  // 调用派生类的拷贝构造函数，首先会调用基类的拷贝构造函数
    
    return 0;
}
```

##### 赋值运算符重载
+ **与拷贝构造函数类似，如果没有自定义赋值运算符，编译器会生成默认的赋值运算符，该运算符按成员赋值，并调用基类的赋值运算符。**
+ **如果基类中涉及到复杂的资源管理，如动态内存分配，派生类通常需要自定义赋值运算符来正确分配和释放资源。**

```cpp
#include <iostream>

// 基类 Base
class Base
{
public:
    // 默认构造函数
    Base()
        : _baseVal_(0)  // 初始化成员 _baseVal_ 为 0
    {
        std::cout << "Base 默认构造函数" << std::endl;
    }

    // 赋值运算符重载
    Base& operator=(const Base& other)
    {
        // 先检查自赋值情况
        if (this != &other)
        {
            _baseVal_ = other._baseVal_;  // 复制 _baseVal_
            std::cout << "Base 赋值运算符" << std::endl;
        }
        return *this;  // 返回当前对象，以支持链式赋值
    }

private:
    int _baseVal_;  // 基类中的私有成员
};

// 派生类 Derived，继承自 Base
class Derived : public Base
{
public:
    // 默认构造函数
    Derived()
        : _derivedVal_(0)  // 初始化派生类的成员
    {
        std::cout << "Derived 默认构造函数" << std::endl;
    }

    // 赋值运算符重载
    Derived& operator=(const Derived& other)
    {
        // 防止自赋值
        if (this != &other)
        {
            // 调用基类的赋值运算符
            Base::operator=(other);

            // 复制派生类的成员变量
            _derivedVal_ = other._derivedVal_;
            std::cout << "Derived 赋值运算符" << std::endl;
        }
        return *this;  // 返回当前对象，以支持链式赋值
    }

private:
    int _derivedVal_;  // 派生类中的私有成员
};

int main()
{
    Derived d1, d2;  // 调用默认构造函数创建两个对象
    d1 = d2;  // 调用赋值运算符，赋值 d2 到 d1

    return 0;
}
```

##### 析构函数
+ **派生类析构时，会先调用派生类的析构函数，然后再依次调用基类的析构函数。与构造函数相反，析构函数的调用顺序是从派生类到基类。**
+ 如果基类的析构函数不是虚函数，可能会导致资源管理问题，尤其是在多态情况下。因此，如果基类用于继承，且可能会通过基类指针删除派生类对象，基类析构函数应该声明为`virtual`。

```cpp
#include <iostream>

class Base 
{
public:
    virtual ~Base() 
    {
        std::cout << "Base 析构函数" << std::endl;
    }
};

class Derived : public Base 
{
public:
    ~Derived() 
    {
        std::cout << "Derived 析构函数" << std::endl;
    }
};

int main()
{
    Base* b = new Derived();
    delete b; // 调用顺序：Derived 析构函数 -> Base 析构函数

    return 0;
}
```

#### 继承与友元
##### 基类的友元不能自动访问派生类的成员
+ **如果一个函数或类是基类的友元，它只对基类的私有或保护成员有访问权限。**
+ **派生类的私有或保护成员并不会因为该函数或类是基类的友元而自动获取访问权限。如果想要友元访问派生类的成员，必须在派生类中重新声明该友元。**

```cpp
class Base 
{
    friend void friendFunc(Base&); // 基类友元函数

private:
    int _baseValue_;
};

class Derived : public Base 
{
    // friendFunc 不能访问 Derived 的私有成员

private:
    int _derivedValue_;
};

void friendFunc(Base& b) 
{
    // 只能访问 Base 类的成员
}
```

```cpp
#include <iostream>

// 基类 Base
class Base
{
public:
    // 带参数的构造函数，初始化基类私有成员 _baseVal_
    Base(int baseVal)
        : _baseVal_(baseVal)
    {
        std::cout << "Base 构造函数" << std::endl;
    }

    // 基类的友元函数，能够访问 Base 类的私有成员
    friend void showBaseFriend(Base& b);

private:
    int _baseVal_;  // 基类的私有成员
};

// 派生类 Derived，继承自 Base
class Derived : public Base
{
public:
    // 派生类构造函数，初始化基类部分并初始化派生类的私有成员 _derivedVal_
    Derived(int baseVal, int derivedVal)
        : Base(baseVal)  // 调用基类的构造函数，初始化基类成员
        , _derivedVal_(derivedVal)  // 初始化派生类私有成员
    {}

    // 派生类的成员函数，用于显示派生类的私有成员
    void show()
    {
        std::cout << "Derived value: " << _derivedVal_ << std::endl;
    }

private:
    int _derivedVal_;  // 派生类的私有成员
};

// 基类的友元函数
void showBaseFriend(Base& b)
{
    // 友元可以访问 Base 类的私有成员 _baseVal_
    std::cout << "Base friend accessing _baseVal_: " << b._baseVal_ << std::endl;

    // 无法访问派生类的私有成员 _derivedVal_，会导致编译错误
    // std::cout << "Trying to access _derivedVal_: " << b._derivedVal_ << std::endl;
    // 如果尝试访问上面这行代码，会编译报错，因为友元函数不能访问派生类的私有成员
}

int main()
{
    // 创建 Derived 类的对象，基类部分初始化为 100，派生类部分初始化为 200
    Derived d(100, 200);

    // 调用基类的友元函数 showBaseFriend，能够访问基类的私有成员
    showBaseFriend(d);

    // 调用派生类的成员函数 show，显示派生类的私有成员
    d.show();

    return 0;
}
```

##### 派生类的友元不能访问基类的私有成员
+ 派生类可以访问基类的保护成员，但私有成员对派生类是不可见的。
+ 派生类的友元(函数或类)也无权限访问基类的私有成员，除非基类明确将这些成员设为友元访问权限。

```cpp
class Base 
{
private:
    int _baseValue_;  // 对 Derived 的友元不可见
};

class Derived : public Base 
{
    friend void friendFunc(Derived&);  // Derived 的友元函数

private:
    int _derivedValue_;
};

void friendFunc(Derived& d) 
{
    // 只能访问 Derived 的成员，不能访问 Base 的私有成员
}
```

```cpp
#include <iostream>

// 基类 Base
class Base
{
public:
    // 带参数的构造函数，初始化基类私有成员 _baseVal_
    Base(int baseVal)
        : _baseVal_(baseVal)
    {
        std::cout << "Base 构造函数" << std::endl;
    }

private:
    int _baseVal_;  // 基类的私有成员
};

// 派生类 Derived，继承自 Base
class Derived : public Base
{
public:
    // 派生类构造函数，初始化基类部分并初始化派生类的私有成员 _derivedVal_
    Derived(int baseVal, int derivedVal)
        : Base(baseVal)  // 调用基类的构造函数，初始化基类成员
        , _derivedVal_(derivedVal)  // 初始化派生类私有成员
    {}

    // 声明友元函数，试图访问基类和派生类的私有成员
    friend void showDerivedFriend(Derived& d);

private:
    int _derivedVal_;  // 派生类的私有成员
};

// 派生类的友元函数
void showDerivedFriend(Derived& d)
{
    // 友元可以访问 Derived 类的私有成员 _derivedVal_
    std::cout << "Derived friend accessing _derivedVal_: " << d._derivedVal_ << std::endl;

    // 尝试访问基类的私有成员 _baseVal_，会导致编译错误
    // std::cout << "Trying to access _baseVal_: " << d._baseVal_ << std::endl;
    // 如果尝试访问上面这行代码，会编译报错，因为派生类的友元不能访问基类的私有成员
}

int main()
{
    // 创建 Derived 类的对象，基类部分初始化为 100，派生类部分初始化为 200
    Derived d(100, 200);

    // 调用派生类的友元函数 showDerivedFriend，访问派生类的私有成员
    showDerivedFriend(d);

    return 0;
}
```

##### 友元的继承问题
**友元关系不能继承**。如果基类的某个类或函数是其友元，该友元不会自动成为派生类的友元。同样，如果派生类需要友元访问权限，它必须在派生类中显式声明：

```cpp
class Base 
{
    friend class FriendClass;  // 只有 FriendClass 是 Base 的友元
};

class Derived : public Base 
{
    // FriendClass 不是 Derived 的友元，无法访问 Derived 的私有或保护成员
};
```

##### 友元函数与保护成员
友元函数可以访问类的保护成员。由于派生类能够访问基类的保护成员，友元函数如果在基类中被声明，可以访问基类的保护成员，但对于派生类保护成员的访问权限仍需要重新声明友元关系。

```cpp
class Base 
{
protected:
    int _baseValue_;  // 友元可以访问基类的保护成员
};

class Derived : public Base 
{
protected:
    int _derivedValue_;  // 需要重新声明友元函数才能访问
};

class FriendClass
{
public:
    void accessBase(Base& b)
    {
        // 可以访问 Base 的保护成员
        b.baseValue = 10;
    }

    void accessDerived(Derived& d) 
    {
        // 无法访问 Derived 的保护成员，除非 Derived 也将 FriendClass 声明为友元
    }
};
```

##### 友元类与多重继承
 在多重继承中，如果一个类继承了多个基类，每个基类的友元也只能访问该基类的成员，无法跨类访问其他基类的成员。派生类的友元类也是一样，不能访问其他基类的成员。  

```cpp
#include <iostream>

// 基类1：Base1
class Base1
{
public:
    Base1(int val1) : _base1Val_(val1)
    {
        std::cout << "Base1 构造函数" << std::endl;
    }

private:
    int _base1Val_;  // 基类1的私有成员

    // 声明 FriendClass1 为基类1的友元类
    friend class FriendClass1;
};

// 基类2：Base2
class Base2
{
public:
    Base2(int val2) : _base2Val_(val2)
    {
        std::cout << "Base2 构造函数" << std::endl;
    }

private:
    int _base2Val_;  // 基类2的私有成员

    // 声明 FriendClass2 为基类2的友元类
    friend class FriendClass2;
};

// 派生类 Derived，继承自 Base1 和 Base2
class Derived : public Base1, public Base2
{
public:
    Derived(int val1, int val2, int derivedVal)
        : Base1(val1), Base2(val2), _derivedVal_(derivedVal)
    {
        std::cout << "Derived 构造函数" << std::endl;
    }

private:
    int _derivedVal_;  // 派生类的私有成员

    // 声明 FriendClassDerived 为派生类的友元类
    friend class FriendClassDerived;
};

// 基类1的友元类 FriendClass1
class FriendClass1
{
public:
    void showBase1(Base1& b)
    {
        // 友元类可以访问 Base1 的私有成员
        std::cout << "FriendClass1 访问 Base1 的私有成员 _base1Val_: " << b._base1Val_ << std::endl;
    }

    // 无法访问 Base2 或 Derived 的私有成员
    // 不能访问 b._base2Val_ 或 b._derivedVal_，因为它们不是 Base1 的成员
};

// 基类2的友元类 FriendClass2
class FriendClass2
{
public:
    void showBase2(Base2& b)
    {
        // 友元类可以访问 Base2 的私有成员
        std::cout << "FriendClass2 访问 Base2 的私有成员 _base2Val_: " << b._base2Val_ << std::endl;
    }

    // 无法访问 Base1 或 Derived 的私有成员
};

// 派生类的友元类 FriendClassDerived
class FriendClassDerived
{
public:
    void showDerived(Derived& d)
    {
        // 友元类可以访问 Derived 的私有成员
        std::cout << "FriendClassDerived 访问 Derived 的私有成员 _derivedVal_: " << d._derivedVal_ << std::endl;

        // 无法访问 Base1 或 Base2 的私有成员
        // std::cout << "Cannot access Base1::_base1Val_ or Base2::_base2Val_" << std::endl;
    }
};

int main()
{
    // 创建 Derived 对象，初始化 Base1、Base2 和 Derived 的成员
    Derived d(10, 20, 30);

    FriendClass1 f1;
    f1.showBase1(d);  // 友元类 FriendClass1 可以访问 Base1 的私有成员

    FriendClass2 f2;
    f2.showBase2(d);  // 友元类 FriendClass2 可以访问 Base2 的私有成员

    FriendClassDerived fd;
    fd.showDerived(d);  // 友元类 FriendClassDerived 可以访问 Derived 的私有成员

    return 0;
}
```

综上可知：**友元类只能访问它被声明为友元的类的私有成员**，无法跨类访问其他基类的私有成员。即使在多重继承的情况下，不同基类的友元类也只能访问它们所属基类的私有成员。  

#### 继承与静态成员
##### 静态成员的继承
+ **静态成员变量和静态成员函数是可以被继承的**，派生类可以直接访问基类的静态成员，而无需创建基类对象。
+ **静态成员是类级别的成员，它们在所有对象之间共享**，同一个类或派生类的所有对象共享同一个静态变量。

```cpp
#include <iostream>

class Base
{
public:
    // 基类的静态成员变量
    static int baseStaticVar;

    // 基类的静态成员函数
    static void showBaseStatic()
    {
        std::cout << "Base 静态成员函数：baseStaticVar = " << baseStaticVar << std::endl;
    }

};

// 初始化基类的静态成员变量
int Base::baseStaticVar = 10;

class Derived : public Base
{

};

int main()
{
    // 通过派生类访问基类的静态成员变量和函数
    std::cout << "Derived 访问基类的静态变量：" << Derived::baseStaticVar << std::endl;
    Derived::showBaseStatic();  // 调用基类的静态成员函数

    return 0;
}
```

##### 静态成员变量的共享性
+ 无论是通过基类还是派生类访问静态成员，静态成员变量都只存在一个实例，并且由所有对象共享。
+ 派生类和基类访问同一个静态成员变量时，修改静态成员变量的值将影响所有类的实例。

```cpp
#include <iostream>

class Base
{
public:
    // 基类的静态成员变量
    static int baseStaticVar;

    // 基类的静态成员函数
    static void showBaseStatic()
    {
        std::cout << "Base 静态成员函数：baseStaticVar = " << baseStaticVar << std::endl;
    }

};

// 初始化基类的静态成员变量
int Base::baseStaticVar = 10;


int main()
{
    Base b1, b2;

    // 修改静态成员变量
    b1.baseStaticVar = 20;

    // 通过另一个对象查看静态成员变量
    std::cout << "b2 访问 baseStaticVar: " << b2.baseStaticVar << std::endl;

    // 再次通过类名查看静态成员变量
    Base::showBaseStatic();

    return 0;
}
```

##### 静态成员函数的访问
+ **静态成员函数没有隐藏的**`**this**`**指针，不能访问任何非静态成员。**
+ 派生类可以调用基类的静态成员函数，且静态成员函数可以通过类名或对象进行调用。

```cpp
#include <iostream>

class Base
{
public:
    int nonStaticVar;

    // 静态成员函数
    static void showStatic()
    {
        // 静态函数无法访问非静态成员
        // std::cout << "nonStaticVar = " << nonStaticVar << std::endl;  // 错误
        std::cout << "静态成员函数不能访问非静态成员" << std::endl;
    }
};

int main()
{
    Base b;
    b.nonStaticVar = 10;

    // 调用静态成员函数
    Base::showStatic();  // 通过类名调用
    b.showStatic();      // 通过对象调用

    return 0;
}
```

##### 隐藏规则
+ 如果派生类中声明了与基类静态成员同名的静态成员函数或静态变量，则基类的静态成员会被隐藏，派生类的静态成员优先被调用。
+ 基类的静态成员不会被自动重载或覆盖。如果希望调用基类的静态成员，可以通过`类名::静态成员`显式调用。

```cpp
#include <iostream>

class Base
{
public:
    static int staticVar;

    static void showStatic()
    {
        std::cout << "Base 静态成员函数: staticVar = " << staticVar << std::endl;
    }
};

// 初始化基类的静态成员变量
int Base::staticVar = 10;

class Derived : public Base
{
public:
    // 隐藏基类的静态成员
    static int staticVar;

    static void showStatic()
    {
        std::cout << "Derived 静态成员函数: staticVar = " << staticVar << std::endl;
    }
};

// 初始化派生类的静态成员变量
int Derived::staticVar = 20;

int main()
{
    // 调用派生类的静态成员函数和变量
    Derived::showStatic();  // 输出 Derived 的静态变量

    // 调用基类的静态成员变量和函数
    Base::showStatic();  // 仍然可以显式调用基类的静态函数

    return 0;
}
```

##### 静态成员与多态性
+ 静态成员函数不能是虚函数，因为静态成员函数不与对像绑定，而多态性依赖于对象的动态绑定。
+ 静态成员函数与类关联，而非与对象关联，因此它们不能通过虚函数机制来实现多态性。

```cpp
#include <iostream>

class Base
{
public:
    // 虚函数
    virtual void showVirtual()
    {
        std::cout << "Base 虚函数" << std::endl;
    }

    // 静态成员函数
    static void showStatic()
    {
        std::cout << "Base 静态成员函数" << std::endl;
    }
};

class Derived : public Base
{
public:
    // 重写虚函数
    void showVirtual() override
    {
        std::cout << "Derived 虚函数" << std::endl;
    }

    // 静态成员函数
    static void showStatic()
    {
        std::cout << "Derived 静态成员函数" << std::endl;
    }
};

int main()
{
    Base* basePtr = new Derived();

    // 虚函数调用，展示多态性
    basePtr->showVirtual();  // 输出 Derived 虚函数

    // 静态成员函数调用，静态成员函数不具备多态性
    basePtr->showStatic();   // 调用基类的静态成员函数
    Derived::showStatic();   // 显式调用派生类的静态成员函数

    return 0;
}
```

#### 菱形继承及菱形虚拟继承
##### 什么是菱形继承
在C++中，多重继承允许一个类从多个基类继承。菱形继承的概念来源于一种特定的继承模式：

1. 祖先类`Base`被两个派生类`Derived1`和`Derived2`继承。
2. 这两个派生类`Derive1`和`Derived2`继续被另一个派生类`Final`继承。

由于`Derived1`和`Derived2`都继承自`Base`，而`Final`又同时继承自`Derived1`和`Derived2`，这就导致`Base`类的成员会被继承两次。继承结构呈现出菱形的形状：

```cpp
       Base
      /    \
 Derived1  Derived2
      \    /
       Final
```

##### 菱形继承的典型问题
当`Final`类继承了两个派生类`Derived1`和`Derived2`时，实际上`Final`类中存在两个`Base`类的实例。会导致几个潜在问题。

###### 成员重复
在`Final`类中，由于`Base`类通过`Derived1`和`Derived2`被继承了两次，所以`Final`类中有两个`Base`类的副本。这意味着：

1. 如果`Base`类有成员变量，`Final`类中会有两份这些成员。
2. 如果`Base`类有成员函数(例如`display()`)，在`Final`类中使用这些函数时会产生二义性，即编译器不知道是调用`Derived1`继承下来的`Base`还是调用`Derived2`继承下来的`Base`。

###### 调用冲突
有以下代码：

```cpp
#include <iostream>

class Base
{
public:
    int x;
    Base() : x(0) {}
    void display() { std::cout << "Base class: x = " << x << std::endl; }
};

class Derived1 : public Base {};
class Derived2 : public Base {};

class Final : public Derived1, public Derived2 {};
```

在上述代码中，`Final`类继承了`Derived1`和`Derived2`，而`Derived1`和`Derived2`又都继承了`Base`。如果我们创建了`Final`的实例并尝试调用`display()`，则编译器不知道调用哪个`Base`类的`display()`，因为`Final`类包含两个`Base`类实例，分别来自`Derived1`和`Derived2`。编译器会产生二义性错误：

```cpp
Final f;
// f.display();  // 这会导致编译错误，二义性
```

 为了消除这个二义性，我们需要显式指定调用路径：  

```cpp
Final f;
f.Derived1::display();  // 指定通过 Derived1 继承的 Base
f.Derived2::display();  // 指定通过 Derived2 继承的 Base
```

通过这种方式，编译器明确知道你要调用的是哪个 `Base` 类的 `display()` 方法，因此可以解决冲突。同样的，对于基类中的成员变量，如果你需要访问`x`，也可以显式指定路径： 

```cpp
f.Derived1::x = 10;  // 访问通过 Derived1 继承的 Base 中的 x
f.Derived2::x = 20;  // 访问通过 Derived2 继承的 Base 中的 x
```

###### 内存浪费
 如果`Base`类中有一些较大的成员变量，那么在`Final`类中存储两个`Base`类的实例无疑是对内存的浪费。实际开发中，这种重复数据结构不仅占用更多的内存，而且也会导致管理的复杂性。  

##### 虚拟继承
为了解决菱形继承的二义性，C++提供了虚拟继承的机制。通过虚拟继承，确保在多重继承的情况下，派生类只继承一个基类实例，而非多个。

###### 虚拟继承的定义
 在类继承时使用`virtual`关键字标记基类的继承，使得派生类不会各自拥有独立的基类副本。相反，最终的派生类(即`Final`类)会只继承一个基类实例。  

###### 虚拟继承的实现
将前面的例子改为虚拟继承：

```cpp
class Base
{
public:
    int x;
    Base() : x(0) {}
    void display() { std::cout << "Base class: x = " << x << std::endl; }
};

class Derived1 : public virtual Base {};
class Derived2 : public virtual Base {};

class Final : public Derived1, public Derived2 {};
```

此时，`Derived1`和`Derived2`都是虚拟继承自`Base`。通过这种方式，`Final`类中只保留一个`Base`类的实例。

###### 虚拟继承的效果
```cpp
Final f;
f.display();  // 正常工作，不会再有二义性问题
```

由于`Derived1`和`Derived2`是虚拟继承`Base`的，`Final`类只会有一个`Base`实例。这意味着`display()`不再有二义性，`Final`类中也不会再存储多个`Base`的副本，从而避免了内存浪费。

###### 虚拟继承的底层实现原理
虚拟继承的底层实现依赖于**虚基类指针(vptr)**和**虚基类表(vtable)**，通过额外的指针将所有虚基类的实例指向同一个存储位置，从而避免菱形继承中的多次实例化。具体步骤如下：

+ **虚基类指针**：当类通过虚拟继承方式继承一个基类时，编译器会在该类对象的内存布局中增加一个**虚基类指针**，用于指向共享的基类实例。
+ **虚基类表**：虚基类指针指向一个由编译器维护的**虚基类表**，该表记录了虚基类在内存中的偏移量，使得派生类可以找到唯一的基类实例。
+ **共享基类实例**：当派生类被实例化时，虚基类只被实例化一次，并且所有通过虚拟继承的路径都指向这一个基类实例。这样，在菱形继承结构中，每个虚基类成员只存在一份，解决了二义性问题。

在虚拟继承结构中，编译器会在对象布局中引入偏移表，用于根据具体路径找到共享的基类实例。每次访问虚基类成员时，编译器通过偏移量调整访问地址，从而确保访问的是唯一的基类实例。  

###### 构造函数问题
虚拟继承虽然解决了二义性问题，但也带来了一个新的问题：构造函数的调用问题。由于基类`Base`在最终派生类`Final`中也只会被实例化一次，因此基类的构造函数只能由最"终端"的派生类即`Final`来负责调用，而不是由中间的派生类`Derived1`或`Derived2`来调用。代码演示如下：

```cpp
class Base
{
public:
    int x;
    Base(int val) : x(val)
    {
        std::cout << "Base class constructor called" << std::endl;
    }
};

class Derived1 : public virtual Base
{
public:
    Derived1() : Base(0)
    {
        std::cout << "Derived1 class constructo called" << std::endl;
    }
};

class Derived2 : public virtual Base
{
public:
    Derived2() : Base(0)
    {
        std::cout << "Derived2 class constructor called" << std::endl;
    }
};

class Final : public Derived1, public Derived2
{
public:
    Final() : Base(100)  // 由 Final 显式调用 Base 的构造函数
    {
        std::cout << "Final class constructor called" << std::endl;
    }
};
```

上述代码中，显然`Derived1`和`Derived2`都是虚拟继承`Base`的，但`Base`的构造函数并不会在它们的构造函数中被调用，而是由`Final`类负责调用。也就是说，当虚拟继承时，只有最终的派生类`Final`需要显式调用基类的构造函数。

### 多态
#### 多态的概念




#### 多态的定义及实现




#### 抽象类




#### 多态的原理




#### 单继承和多继承关系中的虚函数表




#### 继承和多态常见的面试题
