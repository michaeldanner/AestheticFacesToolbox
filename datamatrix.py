import math
import glob
import os, sys
import re
import numpy as np
import matplotlib.pyplot as plt
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
    tolerance = 100
    limit_div_0_with_large = 304
    limit_div_1_with_small = 344  # Threshold for too_divers, if > limit_divers (on LFW)
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

    def load_image_list(self):
        with open(self.image_path) as image:
            self.image_list.append(image)

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
        for subpath in glob.glob(str(self.anno_files + "\\*")):
            # subpath is annotations folder, which is students matricle number
            rand, value = self.load_annotations(subpath)
            if len(rand) > 1 and len(value) > 1:
                valneu = np.full((self.num_probs), 2)
                _, f = os.path.split(subpath)
                for val in value:
                    if val[0] < 1 or val[0] > self.num_pairs:
                        print("warning: unvalid index 0 < val(%d,1)=%d < num_pairs(%d) => ignore value")
                    if val[1] < 0 or val[1] > 1:
                        print("warning: value(%d)~= 0 or 1 => set to value and pair to -1 and go on")
                    try:
                        valneu[rand[val[0]-1]] = val[1]
                        valneu[rand[val[0]+self.num_pairs-1]] = not val[1]
                    except IndexError as err:
                        print(str(err) + ' in folder ' + str(f))
                        output_log += str(err) + ' in folder ' + str(f) + '\n'
                        count[2] += 1
                # print(valneu)
                done = 100 - (np.sum(valneu) - self.num_pairs) / 3.0 / self.num_pairs * 100
                count[0] += 1
                output_log += str(count[0]) + '  ' + (str(f) + f" \t - Annotations: {done:3.1f}%")

                if done >= self.tolerance:
                    self.A_data.append(valneu)
                    self.anno_list.append(str(f))
                else:
                    count[1] += 1
                    output_log += " - skipped"
                output_log += '\n'
        self.count_annos = count[0] - count[1] - count[2]
        self.count_skipped = count[1]
        self.count_error = count[2]
        output_log += f'{count[0]:d} Annotations scanned, {count[1]:d} skipped, {count[0] - count[1]:d} Annotations in Datamatrix\n'
        self.output_log = output_log

        np.savetxt((str(self.anno_files)+'/datamatrix.txt'), self.A_data, fmt='%d', delimiter=' ', )

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

        # 3.2.a) Miss Diversity;
        # compute scores(avg attractiveness per probant( == valid annos per col))
        V = np.asanyarray(self.A_data)
        B = (V == 1).astype(int)
        valid_per_col = np.sum(V < 2, axis=0)
        sum_per_col_valid = np.sum(B, axis=0)
        sc = 1.0 * sum_per_col_valid / valid_per_col
        self.score_list = sc
        miss_attr = self.image_path + os.sep + self.image_names_list[np.argmax(sc)].split(' ')[0]
        print(miss_attr)

        self.hist1_canvas = valid_per_col
        self.hist2_canvas = sc
        self.attr_canvas = plt.imread(miss_attr)

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
        ret_str += '\n\nAnnotations\ntotal:\t' + str(self.count_annos + self.count_skipped)
        ret_str += '\nvalid:\t' + str(self.count_annos)
        ret_str += '\nskipped:\t' + str(self.count_skipped)
        ret_str += '\nerror:\t' + str(self.count_error)
        ret_str += '\n\nTop Annotators:'
        for matr in self.matr_list[:40]:
            ret_str += '\n' + str(matr[0]) + ':\t' + str(matr[1])
        return ret_str

    def get_age_data(self):
        return self.min_age, self.max_age, self.attr_per_age, self.avg_attr_per_age, self.var_attr_per_age
