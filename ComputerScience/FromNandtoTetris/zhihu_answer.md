<!--
[]Module 0
[]Module 1
[]Module 2
[]Module 3
[]Module 4
[]Module 5
[]Module 6
[]Module 7

汇编语言

从VM code translate到assembly code

Compiler，Tokenizer，Parser如何运作，Grammer是语言的核心，了解语言是怎么设计的

Stack和Heap，静态编译的时候，构建起了哪些参数
编程语言从高级语言到机器语言是怎么一个流程
OOP是怎么让计算机理解的
Array，Object在内存中是如何表现的

OS


NandTetris：从“与非门”到“俄罗斯方块”
Part 1: 没有任何前置要求
Part 2: 需要上过一门计算机入门的课程，以及有高级语言的编程经验（Java，C++，Python，Javascript)

教师/作者介绍
Noam Nisan
Shimon Schocken


材料：

课程视频
Shimon Schocken Ted 演讲 B站
项目网站：包含所有的项目材料，软件工具，所有都是免费和开源的！
教材: The Elements of Computing Systems(MIT Press) 英文 中文 （教学视频和网站上的课件已经非常完整和深入，教材个人认为非必须）

参考知乎答题样式：h
-->
## From Nand to Tetris / 从与非门到俄罗斯方块
>*Building a Modern Computer From First Principles* / *从第一原理构建现代计算机*

这门课程已经在之前的回答中有提及，但是我觉得有必要单独拿出来回答，因为我认为这门课程对于 **非科班** 出生的开发人员来说，是一门非常好，且极其重要的课程。  
<!-- 如果将广义上的计算机工程开发比做武功招式的话，那这门课程学得就是 **武功心法**。学完了这门课程，动手完成项目之后，相当于修炼了《**易筋经**》。 -->
TODO 图片

#### Hello World

这段简单的代码相信只要学过一点编程，都知道是做什么，但是计算机是怎么把它转化成屏幕上的“Hello World”字符串的？这就是这门课程要教你的知识，不仅如此，它还要求你自己从0开始，来搭建这个*计算机*

```Java
Class Main {
  function void main() {
    do Output.printString("Hello World");
    do Output.println(); // New Line
    return;
  }
}
```

### 此课程的特点
- 课程资料**完全公开免费**：
  - 项目资料，课件，作业代码工具都在[项目网站][1]，
  - 课程视频: [B站][2], [Coursera Part I][3], [Coursera Part II][4]
- 无需太多的前置课程知识要求
  - Part I: 第一部分没有前置课程要求
  - Part II: 第二部分只要求使用过高级语言
- **项目中心/Project Centereed**: 每周都有一个项目，能够很好的都收实现
- 内容涵盖丰富，包含了：
  - 操作系统，编程语言，计算机体系结构，编译原理，电路原理，数据结构，算法设计，软件工程

TODO 拼图

### 你将从这门课程学到什么
1. 软件和硬件之间是如何协同工作的?
2. 操作系统，算法，编译，体系结构，面向对象语言，这些计算机专业核心课程之间的关系是什么?
3. 高级语言是如何在计算机里运行的，如何设计一门编程语言?
4. C++和Java的编译方式有什么不同，为什么C++运行速度比Java快？Java虚拟机是一个什么东西？
5. 写程序编译高级语言到汇编语言再到机器语言。
6. 字符串，数组，对象，在内存中是如何通过Stack和Heap实现的。
7. 如何设计研发一个大型的工程项目，什么样的设计是一个好的设计?
8. 能够在你自己构建的计算机上，自己写一个俄罗斯方程玩。  
........ 

TODO 图片 链接

我想，不论你是刚开始接触计算机学科的学生，还是已经在业界工作多年，但是因为没有经过所谓”科班训练“，而仍旧在某些方面感觉到自己的认知不够，都能从这门课程中学到很多。

PS. Coursera上评论中一个来自加州的13岁小孩都已经学了这门课程了，后生可畏啊!

#### Reference:
项目网站：https://www.nand2tetris.org/  

Coursera链接：

  - Part I: https://www.coursera.org/learn/build-a-computer
  - Part II: https://www.coursera.org/learn/nand2tetris2


<!-- #### 这门课程讲了什么，为什么如此重要？: -->
<!-- 从逻辑门到高级编程语言，把计算机是怎么构造起来的，翻了个底朝天，而且让你在每一个部分都亲身参与，动手操作。入门计算机科学，掌握一张地图，为日后的深入研究学习打下基础 -->
<!-- ####  为什么觉得相见恨晚，觉得他好 -->
<!-- #### 学了这门课程有什么用？ -->
<!-- 很多时候，没有编译器的知识，对于语言的理解是表层的，该课程从第一性原理出发，首先极大的满足了对于计算机运行机制的好奇，并且能够让你成为一个更加“富有”richer 的Programmer，（原话）。实际课程中Part2，写一个VMcode到汇编语言的翻译器，再写一个高级语言到vmcode的编译器，能够深入理解stack，heap在语言编译和运行时候的机制，并且对很多之前不甚了解的原理有了非常深入的认识（如何显示字符，如何画图，键盘输入是怎么获取的，数组，字符串，对象到底是怎么构造的） -->
<!-- 核心：对编程语言的理解：为学习语言打下坚实的理论基础，掌握了语言的内功心法，所有的语言都知识武功套路了。 -->
<!-- 软件工程，操作系统，数据结构，算法设计 -->
<!-- 总而言之，就是为之后的每一个部分的课程打下了坚实的基础，知道每一个细分主题在整一个计算机系统中起到了什么作用，甚至于对于理解软件，硬件都有了一个大致的概念。 -->
<!-- 体系结构，电路原理）为Part 1内容，之后补充 -->
<!-- #### 材料 -->
<!--  -->
<!-- 为什么推荐这门课程？ -->
<!--  -->
<!-- Top-down vs bottom-up -->
<!--  -->
<!-- Topic Oriented Approach, -->
<!--  -->
<!-- 每一个topic都是一门课程，配合着几百页的教材，这样的问题是每一个主题都有深入的了解，但是却不知到如何联系，即所谓的只见树木不见森林 -->

[1]: <https://www.nand2tetris.org/> "项目网站"
[2]: <https://www.bilibili.com/video/BV1KJ411s7QJ> "Bilibili 视频"
[3]: <https://www.coursera.org/learn/nand2tetris1> "Coursera Part 1"
[4]: <https://www.coursera.org/learn/nand2tetris2> "Coursera Part 2"

<!-- Refeerence -->
[8]: <https://www.youtube.com/watch?v=JtXvUoPx4Qs&t=51s>
[9]: <https://www.youtube.com/watch?v=wTl5wRDT0CU&feature=youtu.be>