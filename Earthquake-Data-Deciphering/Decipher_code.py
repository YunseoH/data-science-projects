#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import struct

# Define the format of data in the file
data_format1 = 'iffh'  # recnum(4B), latitude(4B), longtitude(4B), numvals(2B)
data_format2 = 'ffxx'  # SS(4B), S1(4B), paddings(2B)

# Define the column names
column_names = ['Recnum', 'Latitude', 'Longitude', 'Numvals', 'SS', 'S1']

# Initialize an empty list to hold the data
data = []

# Open the file in binary mode
with open('./1997-AK-MCE-R1a.rnd', 'rb') as f:
    while True:
        # Read 14 bytes: recnum(4B), latitude(4B), longtitude(4B), numvals(2B)
        record1 = f.read(14)
        if len(record1) != 14:  # If less than 14 bytes are read, it's the end of the file
            break
        # Read 10 bytes: SS(4B), S1(4B), paddings(2B)
        record2 = f.read(10)
        if len(record2) != 10:
            break

        # Unpack the binary data and append to the list according to the pre-defined format
        data.append(struct.unpack(data_format1, record1) + struct.unpack(data_format2, record2))

# Convert the list into a pandas DataFrame
df = pd.DataFrame(data, columns=column_names)

# Show dataframe
print(df)


# In[5]:


# Histogram of numvals

import matplotlib.pyplot as plt

plt.hist(df['Numvals'], bins=2, color='blue', alpha=0.7)
plt.xlabel('Numvals')
plt.ylabel('Frequency')
plt.title('Histogram of Numvals')
plt.show()


# In[6]:


# Remove data having 0 numvals to have histograms with valid values only

df = df[(df["Numvals"] != 0)]


# In[7]:


# Histograms of SS and S1
fig, axs = plt.subplots(2)

# Plot histogram of 'SS'
axs[0].hist(df['SS'], bins=50, color='blue', alpha=0.7)
axs[0].set_title('Histogram of SS')
axs[0].set_xlabel('SS')
axs[0].set_ylabel('Frequency')

# Plot histogram of 'S1'
axs[1].hist(df['S1'], bins=50, color='red', alpha=0.7)
axs[1].set_title('Histogram of S1')
axs[1].set_xlabel('S1')
axs[1].set_ylabel('Frequency')

# Display the figure
plt.tight_layout()
plt.show()


# In[8]:


# Box plots of SS and S1

import matplotlib.pyplot as plt

# Create a figure and a set of subplots
fig, axs = plt.subplots(1,2)

# Plot box plot of 'SS'
axs[0].boxplot(df['SS'])
axs[0].set_title('Box plot of SS')
axs[0].set_ylabel('SS')

# Plot box plot of 'S1'
axs[1].boxplot(df['S1'])
axs[1].set_title('Box plot of S1')
axs[1].set_ylabel('S1')

# Display the figure
plt.tight_layout()
plt.show()


# In[9]:


# Correlation matrix of Longtitude, Latitude, SS, and S1

import seaborn as sns

corr = df[["Longitude", "Latitude", "SS", "S1"]].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Heatmap of Correlation Matrix')
plt.show()


# In[10]:


# Scatter plot colored by SS and S1

# Create a figure and a set of subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 16))

# Create a scatter plot for 'SS'
sc1 = axs[0].scatter(df['Longitude'], df['Latitude'], c=df['SS'], cmap='viridis')
fig.colorbar(sc1, ax=axs[0], label='SS')
axs[0].set_title('Scatter plot colored by SS')
axs[0].set_xlabel('Longitude')
axs[0].set_ylabel('Latitude')

# Create a scatter plot for 'S1'
sc2 = axs[1].scatter(df['Longitude'], df['Latitude'], c=df['S1'], cmap='viridis')
fig.colorbar(sc2, ax=axs[1], label='S1')
axs[1].set_title('Scatter plot colored by S1')
axs[1].set_xlabel('Longitude')
axs[1].set_ylabel('Latitude')

# Display the plots
plt.tight_layout()
plt.show()

