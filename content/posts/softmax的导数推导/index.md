---
date: '2025-08-21T17:07:30+08:00'
draft: false
title: 'Softmax的反向传播推导'
tags: ["深度学习","数学"]
---

softmax是一个经典的多分类概率分布的公式，有n个类，softmax公式如下，
$$
\text{softmax}(z)_j = \frac{e^{z_j}}{\sum_{i=1}^n  e^{z_i}}, \quad j = 1, 2, \dots, n
$$
首先，考虑一个样本每个类的预测分数做一个softmax，转换成每类预测的概率形式。

$$
a^{[L]} = \text{softmax}(z^{[L]})
$$

$$
\hat{y} = a^{[L]}\quad
$$

然后，利用样本标签，结合极大似然估计的损失函数如下。
$$
L(\hat{y}, y) = - \sum_{i=1}^{n} y_i \log(\hat{y}_i)
$$

由于需要做反向传播，我们想求 $\frac{\partial L}{\partial z^{[L]}}$，也就是做完softmax的前的偏导数。

假设 $y$ 的分类为 $1$，则 $y_1 = 1$，其余 $y_j = 0\ (j\neq 1)$，$y=[1,0,.....,0]$ 
则有，
$$
L(\hat{y}, y) = -\log(\hat{y}_1)
$$

$$
L(\hat{y}, y) = - \ln \left( \frac{e^{z_1^{[L]}}}{e^{z_1^{[L]}} + e^{z_2^{[L]}} + \cdots + e^{z_n^{[L]}}} \right),
\quad S = e^{z_1^{[L]}} + e^{z_2^{[L]}} + \cdots + e^{z_n^{[L]}}
$$

接下来求 $Z^{[L]}$ 的偏导，
$$
\frac{\partial L}{\partial z^{[L]}_1} 
= -\frac{S}{e^{z^{[L]}_1}} \cdot \frac{e^{z^{[L]}_1} \cdot S - \big(e^{z^{[L]}_1}\big)^2}{S^2} 
= \frac{e^{z^{[L]}_1}}{S} - 1
$$

$$
\frac{\partial L}{\partial z^{[L]}_j} 
= - \frac{S}{e^{z^{[L]}_1}} \cdot \frac{-e^{z^{[L]}_1} \cdot e^{z^{[L]}_j}}{S^2} 
= \frac{e^{z^{[L]}_j}}{S}, 
\quad j \neq 1
$$

因为，
$$
a_j^{[L]} = \frac{e^{z_j^{[L]}}}{S},
$$
所以，
$$
\frac{\partial L}{\partial z^{[L]}_1} = a_1^{[L]} - 1
$$

$$
\frac{\partial L}{\partial z^{[L]}_j} = a_j^{[L]}, \quad (j \neq 1)
$$

由于不同分类标签的对称性，从而得到最终化简结果，
$$
\frac{\partial L}{\partial z^{[L]}} = \hat{y} - y
$$
对于多样本，每个样本间独立，则有，
$$
\frac{\partial L}{\partial Z^{[L]}} = \hat{Y} - Y
$$

