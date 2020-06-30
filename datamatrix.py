import math
import glob
import os, sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.backends.backend_qt5agg import FigureCanvasQT


class DataMatrix:
    num_probs = 0
    num_pairs = 0
    tol_diff_num_values = 0
    count_annos = 0
    count_skipped = 0
    count_error = 0
    A_data = []
    anno_list = []
    image_list = []
    image_names_list = []
    matr_list = []
    age_list = []
    score_list = []
    num_value_0_with_large_sc = []
    num_value_1_with_small_sc = []
    table_annodata = None   # course, name, nr, age, sex, 5 percent,
                            # 6 status, diverse0, diverse1, divers0p, divers1p, 11 amount
    tolerance = 100
    image_path = ''
    output_dir = ''
    anno_dat = ''
    age_dat = ''
    anno_files = ''
    output_log = ''
    hist1_canvas = None
    hist2_canvas = None
    attr_canvas = None
    attr_per_age = None
    avg_attr_per_age = None
    var_attr_per_age = None
    min_age = 0
    max_age = 100

    def __init__(self, anno_dat, anno_files, image_path, output_dir, ages_dat, tolerance):
        self.count_annos = 0
        self.count_skipped = 0
        self.count_error = 0
        self.A_data = []
        self.anno_list = []
        self.image_list = []
        self.image_names_list = []
        self.matr_list = []
        self.age_list = []
        self.score_list = []
        self.num_value_0_with_large_sc = []
        self.num_value_1_with_small_sc = []
        self.tolerance = tolerance
        self.anno_dat = anno_dat
        self.anno_files = anno_files
        self.image_path = image_path
        self.output_dir = output_dir
        self.age_dat = ages_dat
        self.load_dataset()
        self.generate_datamatrix()
        self.estimate_images()
        self.normal_rank_graph()

    def load_dataset(self):
        """
        Load the dataset from annotations dat file

        :param filename: usually ends with .dat and includes the list of images
        :return: number of images, filenames of images
        """
        file = open(self.anno_dat, 'r')
        line_count = 0
        data = []
        for line in file:
            if line.strip().rstrip('\n') != '':
                line_count += 1
                data.append(line.rstrip('\n'))
        file.close()

        self.num_probs = line_count
        self.num_pairs = math.floor(line_count/2)
        self.image_names_list = data

        file = open(self.age_dat)
        for line in file:
            if line.strip().rstrip('\n') != '':
                self.age_list.append(int(line.rstrip('\n')))

        return line_count, data

    def load_annotations(self, path):
        randomized = []
        values = []
        is_randomized = False
        is_values = False
        p = None
        f = None
        for filename in glob.glob(str(path) + "\\*.*"):
            p, f = os.path.split(filename)
            if f == 'randomized.txt':
                is_randomized = True
                with open(filename) as rand:
                    for line in rand:
                        if line.strip() != '':
                            randomized.append( int(line.strip()))
            elif f == 'values.txt':
                is_values = True
                with open(filename) as value:
                    for line in value:
                        a, b = line.split(' ')
                        values.append([int(a.strip()), int(b.strip())])
            elif 'randomized' in f:
                print("Error in path " + str(p) + ": There is a randomized file, but not usable")
        if p is not None and not is_randomized:
            print("Error in path " + str(p) + ": randomized.txt file not found - skipping")
        if p is not None and not is_values:
            print("There is no values.txt file")

        return randomized, values

    def generate_datamatrix(self):
        output_log = ''
        count = [0, 0, 0]  # number of annotations, number of skipped, number of errors
        amount = len(list(os.walk(self.anno_files)))-1
        ta = np.empty((amount, 11), dtype="S10")
        i = 0
        for subpath in glob.glob(str(self.anno_files + "/*")):
            if os.path.isdir(subpath):
                # subpath is annotations folder, which contains students matricle number
                rand, value = self.load_annotations(subpath)
                _, f = os.path.split(subpath)
                print(str(i) + " - " + str(f))
                try:
                    ta[i][0], ta[i][1], ta[i][2], ta[i][3], ta[i][4] = f.split('_', 4)
                    ta[i][3] = ta[i][3][:1]
                except:
                    print("error in anno_list: " + str(f))

                if len(rand) <= 1 or len(value) <= 1:
                    ta[i][6] = 'error'
                    count[0] += 1  # total
                    count[2] += 1  # error
                    print("Error in folder: " + str(f))
                    i += 1
                else:
                    valneu = np.full((self.num_probs), 2)
                    for val in value:
                        if val[0] < 1 or val[0] > self.num_pairs:
                            print("warning: unvalid index 0 < val(%d,1)=%d < num_pairs(%d) => ignore value")
                        if val[1] < 0 or val[1] > 1:
                            print("warning: value(%d)~= 0 or 1 => set to value and pair to -1 and go on")
                        try:
                            valneu[rand[val[0]-1]] = val[1]
                            index = val[0]+self.num_pairs-1  # index of randomized.txt
                            idx = rand[index]-1  # index of value.txt
                            valneu[idx] = not val[1]
                        except IndexError as err:
                            print(str(err) + ' in folder ' + str(f))
                            output_log += str(err) + ' in folder ' + str(f) + '\n'
                            count[2] += 1
                            ta[i][6] = 'error'
                            break

                    if ta[i][6] != b'error':
                        done = 100 - (np.sum(valneu) - self.num_pairs) / 3.0 / self.num_pairs * 100
                        count[0] += 1
                        output_log += str(count[0]) + '  ' + (str(f) + f" \t - Annotations: {done:3.1f}%")
                        ta[i][5] = f"{done:2.1f}"

                        if done >= self.tolerance:
                            self.A_data.append(valneu)
                            self.anno_list.append(str(f))
                            ta[i][6] = 'pass'
                        elif ta[i][6] != b'error':
                            count[1] += 1
                            output_log += " - skipped"
                            ta[i][6] = 'skip'
                        output_log += '\n'
                    i += 1

        self.table_annodata = ta
        self.count_annos = count[0] - count[1] - count[2]
        self.count_skipped = count[1]
        self.count_error = count[2]
        output_log += f'{count[0]:d} Annotations scanned, {count[1]:d} skipped, {count[0] - count[1]:d} Annotations in Datamatrix\n'
        self.output_log = output_log

        np.savetxt((str(self.output_dir)+'/datamatrix.txt'), self.A_data, fmt='%d', delimiter=' ', )

    def compute_score(self, datamatrix):
        # 3.2.a) Miss Diversity;
        # compute scores(avg attractiveness per probant( == valid annos per col))
        V = np.asanyarray(datamatrix)
        B = (V == 1).astype(int)
        valid_per_col = np.sum(V < 2, axis=0)
        sum_per_col_valid = np.sum(B, axis=0)
        sc = 1.0 * sum_per_col_valid / valid_per_col
        self.score_list = sc
        self.hist1_canvas = valid_per_col
        self.hist2_canvas = sc
        return V

    def estimate_images(self):
        print(self.image_path)
        print(self.count_annos)
        num_all_pairs = (self.num_probs-1)*self.num_probs / math.factorial(2)
        print('number of all possible pairs: {:g} by {:d} images -> {:d}({:1.3f}%) annotated of {:g} poss. pairs.\n'.format(
            num_all_pairs, self.num_probs, self.num_pairs, self.num_pairs/num_all_pairs*100, num_all_pairs))
        print(self.anno_list)
        for anno in self.anno_list:
            try:
                match = re.search(r'_\d\d\d\d\d\d_', anno)
                match = str(match.group(0)).rstrip('_').lstrip('_')
            except AttributeError as err:
                match = None
            if not match:
                print(str(anno) + " ERROR: not correct anno-name (no 6 digits, too long, too short or not unique)")
            else:
                if match in [x[0] for x in self.matr_list]:
                    for i in range(0, len(self.matr_list)):
                        if self.matr_list[i][0] == match:
                            self.matr_list[i][1] += 1
                else:
                    self.matr_list.append([match, 1])
        self.matr_list = sorted(self.matr_list, key=lambda l: l[1], reverse=True)

        V = self.compute_score(self.A_data)

        num_value_0_with_large_sc = []
        num_value_1_with_small_sc = []
        num_value_0 = []
        num_value_1 = []
        delete_rows = []
        n = 0
        k = 0
        for row in V:
            num_value_0_with_large_sc.append(0)
            num_value_1_with_small_sc.append(0)
            num_value_0.append(0)
            num_value_1.append(0)
            for i in range(0, len(row)):
                score = self.score_list[i]
                if row[i] == 1 and score < 0.5:
                    num_value_1_with_small_sc[-1] += (0.5 - score)**4 * 10000
                elif row[i] == 0 and score > 0.5:
                    num_value_0_with_large_sc[-1] += (score - 0.5)**4 * 10000
            while self.table_annodata[n+k][6] != b'pass':
                k += 1

            self.table_annodata[n+k][7] = f"{num_value_0_with_large_sc[n]:1.1f}"
            self.table_annodata[n+k][8] = f"{num_value_1_with_small_sc[n]:1.1f}"
            d0 = num_value_0_with_large_sc[n] * 100 / self.num_probs / float(self.table_annodata[n + k][5])
            self.table_annodata[n+k][9] = f"{d0:.2f}"
            num_value_0[-1] += d0
            d1 = num_value_1_with_small_sc[n] * 100 / self.num_probs / float(self.table_annodata[n + k][5])
            self.table_annodata[n+k][10] = f"{d1:.2f}"
            num_value_1[-1] += d1
            if d1 > 4.0:
                delete_rows.append(n)
                self.table_annodata[n+k][6] = 't.div'
            n += 1
        datamatrix_2 = V
        for row in reversed(delete_rows):
            datamatrix_2 = np.delete(datamatrix_2, row, 0)
        np.savetxt((str(self.output_dir) + '/datamatrix2.txt'), datamatrix_2, fmt='%d', delimiter=' ', )
        self.num_value_1_with_small_sc = num_value_1
        self.num_value_0_with_large_sc = num_value_0

        V = self.compute_score(datamatrix_2)
        sc = self.score_list

        anno_list = ""
        for row in self.table_annodata:
            if row[6] == b'pass':
                for item in row[:5]:
                    anno_list += item.decode('utf8') + '_'
                anno_list += '\n'

        print(anno_list)
        print(np.argmax(sc))
        sc_sort = np.argsort(sc)
        miss_attr = self.image_path + os.sep + self.image_names_list[sc_sort[-1]].split(' ')[0]
        print(miss_attr)
        self.image_list = []
        for i in range(len(sc)):
            self.image_list.append(self.image_names_list[sc_sort[-1-i]])
            path, fname = (self.image_names_list[sc_sort[-1-i]].split(' ')[0]).split('/')
            img_load = self.image_path + os.sep + self.image_names_list[sc_sort[-1-i]].split(' ')[0]
            img = Image.open(img_load)
            if not os.path.exists(self.output_dir + "/sc_images/"):
                os.mkdir(self.output_dir + "/sc_images/")
            img_save = self.output_dir + "/sc_images/{:.3f}".format(sc[sc_sort[-1-i]]) + "_" + fname.split('dummy')[0] + ".jpg"
            # print(img_save)
            img.save(img_save)

        miss2_attr = self.image_path + os.sep + self.image_names_list[sc_sort[-2]].split(' ')[0]
        print(miss2_attr)
        miss3_attr = self.image_path + os.sep + self.image_names_list[sc_sort[-3]].split(' ')[0]
        print(miss3_attr)
        img0 = Image.open(miss_attr)
        img1 = Image.open(miss2_attr)
        img2 = Image.open(miss3_attr)
        img = self.get_concat_h(img0, img1)
        img = self.get_concat_h(img, img2)
        img.save('tmp.png')

        self.attr_canvas = plt.imread('tmp.png')

    def get_concat_h(self, im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    def normal_rank_graph(self):
        avg_attr_per_age = []
        var_attr_per_age = []
        B = np.asarray(self.age_list)
        min_age = min(B[B > 0])
        max_age = max(B)
        print(min_age)
        print(max_age)
        x = min_age
        attr_per_age = []

        while x < max_age:
            age = []
            for i in range(0, self.num_probs):
                if self.age_list[i] == x:
                    age.append(self.score_list[i])
            attr_per_age.append(age)
            x += 1

        for element in attr_per_age:
            if element:
                avg_attr_per_age.append(np.nanmean(np.asarray(element)))
                var_attr_per_age.append(np.nanvar(np.asarray(element)))
            else:
                avg_attr_per_age.append(None)
                var_attr_per_age.append(None)

        self.attr_per_age = attr_per_age
        self.avg_attr_per_age = avg_attr_per_age
        self.var_attr_per_age = var_attr_per_age
        self.min_age = min_age
        self.max_age = max_age

    def get_dataset_properties(self):
        ret_str = 'Images:\t' + str(self.num_probs) + '\nPairs:\t' + str(self.num_pairs)
        ret_str += '\n\nAnnotations\ntotal:\t' + str(self.count_annos + self.count_skipped + self.count_error)
        ret_str += '\nvalid:\t' + str(self.count_annos)
        ret_str += '\nskipped:\t' + str(self.count_skipped)
        ret_str += '\nerror:\t' + str(self.count_error)
        ret_str += '\n\nTop Annotators:'
        for matr in self.matr_list[:40]:
            ret_str += '\n' + str(matr[0]) + ':\t' + str(matr[1])
        return ret_str

    def get_age_data(self):
        return self.min_age, self.max_age, self.attr_per_age, self.avg_attr_per_age, self.var_attr_per_age
