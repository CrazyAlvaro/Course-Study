
# coding: utf-8

# ![Big Data University](https://ibm.box.com/shared/static/jvcqp2iy2jlx2b32rmzdt0tx8lvxgzkp.png)

# # <center> "Hello World" in TensorFlow  - Exercise Notebook</center>

# #### Before everything, let's import the TensorFlow library

# In[1]:

get_ipython().magic(u'matplotlib inline')
import tensorflow as tf


# ### First, try to add the two constants and print the result.

# In[2]:

a = tf.constant([5])
b = tf.constant([2])


# create another TensorFlow object applying the sum (+) operation:

# In[5]:

#Your code goes here
c = tf.add(a, b)


# <div align="right">
# <a href="#sum1" class="btn btn-default" data-toggle="collapse">Click here for the solution #1</a>
# <a href="#sum2" class="btn btn-default" data-toggle="collapse">Click here for the solution #2</a>
# </div>
# <div id="sum1" class="collapse">
# ```
# c=a+b
# ```
# </div>
# <div id="sum2" class="collapse">
# ```
# c=tf.add(a,b)
# ```
# </div>

# In[6]:

with tf.Session() as session:
    result = session.run(c)
    print "The addition of this two constants is: {0}".format(result)


# ---
# ### Now let's try to multiply them.

# In[7]:

# Your code goes here. Use the multiplication operator.

c = tf.multiply(a, b)


# <div align="right">
# <a href="#mult1" class="btn btn-default" data-toggle="collapse">Click here for the solution #1</a>
# <a href="#mult2" class="btn btn-default" data-toggle="collapse">Click here for the solution #2</a>
# </div>
# <div id="mult1" class="collapse">
# ```
# c=a*b
# ```
# </div>
# <div id="mult2" class="collapse">
# ```
# c=tf.multiply(a,b)
# ```
# </div>

# In[8]:

with tf.Session() as session:
    result = session.run(c)
    print "The Multiplication of this two constants is: {0}".format(result)


# ### Multiplication: element-wise or matrix multiplication
#
# Let's practice the different ways to multiply matrices:
# - **Element-wise** multiplication in the **first operation** ;
# - **Matrix multiplication** on the **second operation**  ;

# In[10]:

matrixA = tf.constant([[2,3],[3,4]])
matrixB = tf.constant([[2,3],[3,4]])


# In[12]:

# Your code goes here
first_operation = tf.multiply(matrixA, matrixB)
second_operation = tf.matmul(matrixA, matrixB)



# <div align="right">
# <a href="#matmul1" class="btn btn-default" data-toggle="collapse">Click here for the solution</a>
# </div>
# <div id="matmul1" class="collapse">
# ```
# first_operation=tf.multiply(matrixA, matrixB)
# second_operation=tf.matmul(matrixA,matrixB)
# ```
# </div>

# In[13]:

with tf.Session() as session:
    result = session.run(first_operation)
    print "Element-wise multiplication: \n", result

    result = session.run(second_operation)
    print "Matrix Multiplication: \n", result


# ---
# ### Modify the value of variable b to the value in constant a:

# In[15]:

a=tf.constant(1000)
b=tf.Variable(0)
init_op = tf.global_variables_initializer()


# In[16]:

# Your code goes here
update = tf.assign(b, a)
with tf.Session() as session:
    session.run(init_op)
    session.run(update)
    print(session.run(b))






# <div align="right">
# <a href="#assign" class="btn btn-default" data-toggle="collapse">Click here for the solution</a>
# </div>
# <div id="assign" class="collapse">
# ```
# a=tf.constant(1000)
# b=tf.Variable(0)
# init_op = tf.global_variables_initializer()
# update = tf.assign(b,a)
# with tf.Session() as session:
#     session.run(init_op)
#     session.run(update)
#     print(session.run(b))
# ```
# </div>

# ---
# ### Fibonacci sequence
#
# Now try to do something more advanced. Try to create a __fibonnacci sequence__ and print the first few values using TensorFlow:</b></h3>
#
# If you don't know, the fibonnacci sequence is defined by the equation: <br><br>
# $$F_{n} = F_{n-1} + F_{n-2}$$<br>
# Resulting in a sequence like: 1,1,2,3,5,8,13,21...
#
#
#

# In[20]:


fib_first = tf.Variable(1)
fib_second = tf.Variable(1)
temp = tf.Variable(1)
init_op = tf.global_variables_initializer()

update_1 = tf.assign(temp, fib_second)
update_2 = tf.assign(fib_second, fib_first + fib_second)
update_3 = tf.assign(fib_first, temp)



with tf.Session() as sess:
    sess.run(init_op)
    print(sess.run(fib_first))
    print(sess.run(fib_second))
    for _ in range(5):
        sess.run(update_1)
        sess.run(update_2)
        sess.run(update_3)
        print(sess.run(fib_second))




# <div align="right">
# <a href="#fibonacci-solution" class="btn btn-default" data-toggle="collapse">Click here for the solution #1</a>
# <a href="#fibonacci-solution2" class="btn btn-default" data-toggle="collapse">Click here for the solution #2</a>
# </div>
#
#
# <div id="fibonacci-solution" class="collapse">
# ```
# a=tf.Variable(0)
# b=tf.Variable(1)
# temp=tf.Variable(0)
# c=a+b
#
# update1=tf.assign(temp,c)
# update2=tf.assign(a,b)
# update3=tf.assign(b,temp)
#
# init_op = tf.initialize_all_variables()
# with tf.Session() as s:
# 	s.run(init_op)
# 	for _ in range(15):
# 		print(s.run(a))
# 		s.run(update1)
# 		s.run(update2)
# 		s.run(update3)
# ```
# </div>
#
#
# <div id="fibonacci-solution2" class="collapse">
# ```
# f = [tf.constant(1),tf.constant(1)]
#
# for i in range(2,10):
# 	temp = f[i-1] + f[i-2]
# 	f.append(temp)
#
# with tf.Session() as sess:
# 	result = sess.run(f)
# 	print result
# ```
# </div>

# ---
#
# ### Now try to create your own placeholders and define any kind of operation between them:
#
#

# In[21]:

# Your code goes here
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)

z = tf.multiply(x,y)

sess = tf.Session()
print(sess.run(z, feed_dict={x: 3.1, y: .2}))



# <div align="right">
# <a href="#placeholder" class="btn btn-default" data-toggle="collapse">Click here for the solution</a>
# </div>
#
#
# <div id="placeholder" class="collapse">
# ```
#
# a=tf.placeholder(tf.float32)
# b=tf.placeholder(tf.float32)
#
# c=2*a -b
#
# dictionary = {a:[2,2],b:[3,4]}
# with tf.Session() as session:
# 	print session.run(c,feed_dict=dictionary)
# ```
# </div>

# ### Try changing our example with some other operations and see the result.
#
# <div class="alert alert-info alertinfo">
# <font size = 3><strong>Some examples of functions:</strong></font>
# <br>
# tf.multiply(x, y)<br />
# tf.div(x, y)<br />
# tf.square(x)<br />
# tf.sqrt(x)<br />
# tf.pow(x, y)<br />
# tf.exp(x)<br />
# tf.log(x)<br />
# tf.cos(x)<br />
# tf.sin(x)<br /> <br>
#
# You can also take a look at [more operations]( https://www.tensorflow.org/versions/r0.9/api_docs/python/math_ops.html)
# </div>

# In[22]:

a = tf.constant(5.)
b = tf.constant(2.)


# create a variable named **`c`** to receive the result an operation (at your choice):

# In[23]:

#your code goes here
c = tf.pow(a,b)


#
# <div align="right">
# <a href="#operations" class="btn btn-default" data-toggle="collapse">Click here for the solution</a>
# </div>
#
#
# <div id="operations" class="collapse">
# ```
# c=tf.sin(a)
# ```
# </div>

# In[24]:

with tf.Session() as session:
    result = session.run(c)
    print "c =: {}".format(result)


# They're really similar to mathematical functions the only difference is that operations works over tensors.

# ## Want to learn more?
#
# Running deep learning programs usually needs a high performance platform. PowerAI speeds up deep learning and AI. Built on IBM's Power Systems, PowerAI is a scalable software platform that accelerates deep learning and AI with blazing performance for individual users or enterprises. The PowerAI platform supports popular machine learning libraries and dependencies including Tensorflow, Caffe, Torch, and Theano. You can download a [free version of PowerAI](https://cocl.us/ML0120EN_PAI).
#
# Also, you can use Data Science Experience to run these notebooks faster with bigger datasets. Data Science Experience is IBM's leading cloud solution for data scientists, built by data scientists. With Jupyter notebooks, RStudio, Apache Spark and popular libraries pre-packaged in the cloud, DSX enables data scientists to collaborate on their projects without having to install anything. Join the fast-growing community of DSX users today with a free account at [Data Science Experience](https://cocl.us/ML0120EN_DSX)This is the end of this lesson. Hopefully, now you have a deeper and intuitive understanding regarding the LSTM model. Thank you for reading this notebook, and good luck on your studies.

# ### Thanks for completing this lesson!
#
