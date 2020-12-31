import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
import sys
#read input data


class DataFrame(pd.DataFrame):
    __params_dict = {'cqi': 'lte_cqi_cw0_1', 'rsrp': 'lte_inst_rsrp_1', 'rsrq': 'lte_inst_rsrq_1',
                     'pci': 'lte_physical_cell_id_1', 'snr': 'lte_sinr_1', 'lat': 'positioning_lat', 'lon': 'positioning_lon'}
    
    def __init__(self, data):
        super().__init__()
        self.data = data

    def remove_empty(self, columnname, npnan):
        self.data[columnname].replace('', npnan, inplace=True)
        self.data.dropna(subset=[columnname], inplace=True)

    def drop_duplicate(self, columnname):
        self.data2 = self.data.drop_duplicates([columnname])

    def read_data(self):
        return self.data2

    def params_list(self):
        self.dict_items = self.__params_dict.items()
        self.dict_keys = self.__params_dict.keys()
        self.names_list = []
        g = globals()
        for x in self.dict_items:
            listname = str(x[0])
            print(listname)
            self.listname = listname
            print(self.listname)
            colname = x[1]
            self.names_list.append(self.listname)
            print(self.names_list)
            g['li_{0}'.format(x[0])] = [y for y in self.data2[colname]]
        return self.names_list

    def get_cqi_percentage(self):
        self.low_cqi = [x for x in li_cqi if 0 < x < 7]
        self.high_cqi = [x for x in li_cqi if 7 <= x <= 15]
        __low_per = round((len(self.low_cqi)/len(li_cqi))*100, 2)
        __high_per = round((len(self.high_cqi)/len(li_cqi))*100, 2)
        return __low_per, __high_per


class Plot():

    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def scatterplot(self, x, y, col):
        self.c = np.where(col < 7, 'r', 'g')
        self.scatter = self.ax.scatter(x, y, c=self.c, picker=1)

    def set_xlabel(self, label):
        plt.xlabel(label)

    def set_ylabel(self, label):
        plt.ylabel(label)

    def set_title(self, title):
        plt.title(title + '\n' + str(len(li_cqi)) + " samples")

    def set_legend(self, lowper, highper):
        red = mpatches.Patch(color='red', label="0 to 7 (" + str(lowper) + "%)")
        green = mpatches.Patch(color='green', label="7 to 15 (" + str(highper) + "%)")
        plt.legend(handles=[red, green ])

    def plt_show(self):
        plt.show()

    def createannot(self):
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

    def update_annot(self, ind):
        pos = self.scatter.get_offsets()[ind]
        self.annot.xy = pos
        # text = " CQI {}".format(" ".join([str(round(li[ind],2))]))
        text = " CQI {}\n RSRP {}\n RSRQ {}\n PCI {}\n SINR {}".format(" ".join([str(round(li_cqi[ind], 2))]),
                                                                       " ".join(
                                                                           [str(round(li_rsrp[ind], 2))]),
                                                                       " ".join(
                                                                           [str(round(li_rsrq[ind], 2))]),
                                                                       " ".join([str(li_pci[ind])]),
                                                                       " ".join(
                                                                           [str(round(li_snr[ind], 2))]))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_facecolor((self.c[ind]))
        self.annot.get_bbox_patch().set_alpha(0.4)
        return text


class Events():
    def __init__(self, annot, fig):
        self.annot = annot
        self.fig = fig

    def onpick(self, event):
    # vis = annot.get_visible()
    # annot.set_visible(True)
        global ind
        ind = event.ind[-1]
        print("first value ind"+str(ind))
        pltt.update_annot(ind)
        self.annot.set_visible(True)
        self.fig.canvas.draw_idle()
        # print (len(ind))
        # print('onpick points:', update_annot(ind))

    def press(self, event):
        key = event.key
        sys.stdout.flush()
        global ind
        if key == 'left':
            ind += 1
            print("2nd value ind" + str(ind))
            pltt.update_annot(ind)
            self.annot.set_visible(True)
            self.fig.canvas.draw_idle()
        elif key == 'right':
            ind -= 1
            print("3rd value ind" + str(ind))
            pltt.update_annot(ind)
            self.annot.set_visible(True)
            self.fig.canvas.draw_idle()

    def connect(self):
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.fig.canvas.mpl_connect('key_press_event', self.press)


if __name__=='__main__':
    npnan = np.nan
    npwhere = np.where
    df = pd.read_csv('tmp_export.csv')
    dfm = DataFrame(df)
    dfm.remove_empty('lte_cqi_cw0_1', npnan)
    dfm.drop_duplicate('positioning_lon')
    li = dfm.params_list()
    low, high = dfm.get_cqi_percentage()
    col = dfm.read_data()
    pltt = Plot()
    pltt.scatterplot(li_lon, li_lat, col.lte_cqi_cw0_1)
    pltt.set_xlabel('Longitude')
    pltt.set_ylabel('Latitude')
    pltt.set_title('CQI plot')
    pltt.set_legend(low, high)
    pltt.createannot()
    evt = Events(pltt.annot, pltt.fig)
    evt.connect()
    pltt.plt_show()
