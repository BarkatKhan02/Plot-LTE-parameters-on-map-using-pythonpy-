import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
import sys
#read input data
data = pd.read_csv('tmp_export.csv')

#remove nan values
data['lte_cqi_cw0_1'].replace('', np.nan, inplace=True)

data.dropna(subset=['lte_cqi_cw0_1'], inplace=True)
data2=data.drop_duplicates(['positioning_lon'])

#create list of parameters in desired format

li = []
rsrp = []
rsrq = []
pci = []
snr = []

for x in data2.lte_cqi_cw0_1:
    li.append(float(x))

for x in data2.lte_inst_rsrp_1:
    rsrp.append(float(x))
    
for x in data2.lte_inst_rsrq_1:
    rsrq.append(float(x))
    
for x in data2.lte_physical_cell_id_1:
    pci.append(int(x))
    
for x in data2.lte_sinr_1:
    snr.append(float(x))
    
x1=[]
x2=[]
for x in li:
    if 0<x<7:
        x1.append(x)
    elif 7<=x<=15:
        x2.append(x)
        
#create x and y axis data
x = []
y = []
for a in data2.positioning_lon:
    x.append(float(a))
for a in data2.positioning_lat:
    y.append(float(a))


low_per = round((len(x1)/len(li)*100),2)
high_per = round((len(x2)/len(li)*100),2)

#set color condition
c = np.where(data2.lte_cqi_cw0_1 < 7, 'r', 'g')
#plot the map
fig, ax=plt.subplots()
scatter=ax.scatter(x,y,c=c,picker=1)
 
#give labels and title
plt.xlabel('Longitude')
plt.ylabel('lattitude')
plt.title('CQI plot\n' + str(len(li))+" samples")

# to show values of each point
#for i, value in enumerate(li):
 #   
  #  annot = ax.annotate(value,(x[i], y[i]))
   # 
    #annot.set_visible(False)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):
    pos = scatter.get_offsets()[ind]
    annot.xy = pos
    text = " CQI {}".format(" ".join([str(round(li[ind],2))]))
    text = " CQI {}\n RSRP {}\n RSRQ {}\n PCI {}\n SINR {}".format(" ".join([str(round(li[ind], 2))]),
                                                                   " ".join(
                                                                       [str(round(rsrp[ind], 2))]),
                                                                   " ".join(
                                                                       [str(round(rsrq[ind], 2))]),
                                                                   " ".join([str(pci[ind])]),
                                                                   " ".join(
                                                                       [str(round(snr[ind], 2))]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor((c[ind]))
    annot.get_bbox_patch().set_alpha(0.4)
    return text

def onpick(event):
    #vis = annot.get_visible()
    #annot.set_visible(True)
    global ind
    ind = event.ind[-1]
    #print("first value ind"+str(ind))

    update_annot(ind)
    annot.set_visible(True)
    fig.canvas.draw_idle()
    #print (len(ind))
    #print('onpick points:', update_annot(ind))
def press(event):
    key = event.key
    sys.stdout.flush()
    global ind
    if key == 'left':

        ind += 1
        #print("2nd value ind" + str(ind))
        update_annot(ind)
        annot.set_visible(True)
        fig.canvas.draw_idle()
    elif key == 'right':

        ind -= 1
        #print("3rd value ind" + str(ind))
        update_annot(ind)
        annot.set_visible(True)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('key_press_event', press)
#set legend
red = mpatches.Patch(color='red', label="0 to 7 (" + str(low_per) + "%)")
green = mpatches.Patch(color='green', label="7 to 15 (" + str(high_per) + "%)")
plt.legend(handles=[red , green ])
        
#Display the map
plt.show()
