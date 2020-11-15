import matplotlib.pyplot as plt


age_labels = '13-17', '18', '19', '20', '21', '22', '23', '24', '25-30', '31-50', '> 50'
ages = [8, 6, 11, 14, 10, 7, 3, 10, 9, 6, 7]

labels = 'male', 'female'
sizes = [156, 51]
explode = (0.01, 0.01)
col = ('xkcd:medium blue', 'xkcd:pale red')
age_col = ('xkcd:medium blue',
           'xkcd:yellowgreen',
           'xkcd:lightgreen',
           'xkcd:lime',
           'xkcd:green',
           'xkcd:chartreuse',
           'xkcd:darkgreen',
           'xkcd:olive',
           'xkcd:pale red',
           'xkcd:violet',
           'xkcd:yellow',
           )
fig1, (ax1,  ax3) = plt.subplots(1, 2, figsize=(10, 5))

ax1.pie(ages, labels=age_labels, autopct='%1.1f%%',
        shadow=False, startangle=90, colors=age_col)
ax1.axis('equal')

ax3.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90, colors=col)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
plt.savefig("d:/anno_gender.svg")
