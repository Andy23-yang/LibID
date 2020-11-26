#!/usr/bin/env python3

import json
import os
import re
from enum import Enum
from pathlib import Path

import glob2

OUTPUT_DIR = 'outputs'
GROUND_TRUTH_FILE = 'data/ground_truth.txt'

GROUND_TRUTH = dict()
LIBPECKER_THRESHOLD = dict()
LIB_INFO = json.load(open('lib_info.json'))

MATCH_RESULT = dict()


def is_valid_tpl(lib):
    if lib.startswith(('com.android.', 'support', 'internal_')):
        # These are all Android Support libraries
        return False
    elif LIB_INFO[lib]['cls_num'] <= 5:
        # The mimumum number of classes required to make a meaningful decision
        return False

    return True


def build_ground_truth():
    with open(GROUND_TRUTH_FILE) as fd:
        lines = fd.read().splitlines()
        for line in lines:
            app_name = line.split(':')[0][:-4]
            lib_list = line.split(':')[1].split(',')[:-1]
            lib_list = [l[:-4] if l.endswith('.jar') else l for l in lib_list]
            lib_list = [l for l in lib_list if is_valid_tpl(l)]

            GROUND_TRUTH[app_name] = lib_list


class Detector(Enum):
    LIBIDS = "LibID/LibID-S"
    LIBIDA = "LibID/LibID-A"
    ORLIS = "Orlis"
    LIBPECKER = "LibPecker"
    LIBSCOUT = "LibScout"


class Obfuscator(Enum):
    ALLATORI = "allatori"
    DASHO = "dasho"


class Metric(Enum):
    # Explained in the paper
    PIN_POINT = "pin_point"
    IN_RANGE = "in_range"


class Evaluator:

    def __init__(self, detector=Detector.LIBIDS, obfuscator=Obfuscator.ALLATORI, metric=Metric.PIN_POINT, debug=False):
        self.detector = detector
        self.obfuscator = obfuscator
        self.debug = debug
        self.metric = metric

        self.output_files = glob2.glob(
            # f'{OUTPUT_DIR}/{self.detector.value}/{self.obfuscator.value}/*')
            f'{OUTPUT_DIR}/*')

    def evaluate(self):
        if not GROUND_TRUTH:
            build_ground_truth()

        true_positive_libs = 0
        reported_libs = 0
        total_libs = 0

        for output_file in self.output_files:
            app_name = Path(output_file).stem

            if app_name in GROUND_TRUTH:
                matched_libs = self._get_matched_libs(output_file)
                matched_libs = [l for l in matched_libs if is_valid_tpl(l)]

                true_positive_lib_set = set(matched_libs).intersection(
                    set(GROUND_TRUTH[app_name]))

                if self.metric == Metric.IN_RANGE:
                    matched_keys = set([LIB_INFO[l]['name']
                                        for l in matched_libs])
                    reported_libs += len(matched_keys)
                    reported_libs += len(true_positive_lib_set) - len(
                        set([LIB_INFO[l]['name'] for l in true_positive_lib_set]))
                else:
                    reported_libs += len(matched_libs)

                true_positive_libs += len(true_positive_lib_set)
                total_libs += len(GROUND_TRUTH[app_name])

                self._print_debug_information(app_name, matched_libs)

        self._print_results(true_positive_libs, reported_libs, total_libs)

    def _get_matched_libs(self, output_file):
        # Each detector reports results in different formats, so we parse the results differently
        if self.detector == Detector.ORLIS:
            return self._get_matched_libs_for_orlis(output_file)
        elif self.detector == Detector.LIBPECKER:
            return self._get_matched_libs_for_libpecker(output_file)
        elif self.detector == Detector.LIBSCOUT:
            return self._get_matched_libs_for_libscout(output_file)
        else:
            return self._get_matched_libs_for_libid(output_file)

    def _get_matched_libs_for_orlis(self, output_file):
        with open(output_file) as fd:
            content = fd.read()

        matched_libs = set(re.findall(r'\[(.*)\]', content))
        matched_libs = [l[:-4] for l in matched_libs]

        return matched_libs

    def _get_matched_libs_for_libscout(self, output_file):
        json_data = json.load(open(output_file))
        matched_libs = []

        for l in json_data['pMatches']:
            r = re.compile(f"{l['libName']}.*{l['libVersion']}")
            matched_libs.append(list(filter(r.match, LIB_INFO.keys()))[0])

        return matched_libs

    def _get_matched_libs_for_libpecker(self, output_file):
        with open(output_file) as fd:
            content = fd.read()

        matched_libs_raw = re.findall(r' -> (.*) \((.*)\)', content)
        matched_lib_dict = dict()

        for l in matched_libs_raw:
            lib_name = LIB_INFO[l[0]]['name']

            if lib_name not in matched_lib_dict:
                if float(l[1]) >= self._get_libpecker_threshold(l[0]):
                    matched_lib_dict[lib_name] = {
                        'match': [l[0]], 'similarity': float(l[1])}
            else:
                if float(l[1]) > matched_lib_dict[lib_name]['similarity']:
                    matched_lib_dict[lib_name] = {
                        'match': [l[0]], 'similarity': float(l[1])}
                elif float(l[1]) == matched_lib_dict[lib_name]['similarity']:
                    matched_lib_dict[lib_name]['match'].append(l[0])

        matched_libs = []
        for k in matched_lib_dict:
            matched_libs.extend(matched_lib_dict[k]['match'])

        return matched_libs

    def _get_matched_libs_for_libid(self, output_file):
        json_data = json.load(open(output_file))

        matched_lib_dict = dict()

        for l in json_data['libraries']:
            lib_full_name = [l['name'] + "_" + v for v in l['version']
                             ] if l['version'][0] != "" else [l['name']]
            for n in lib_full_name:
                key_name = LIB_INFO[n]['name'] + "|" + \
                    str(l['matched_root_package'])

                if key_name not in matched_lib_dict:
                    # If this library has not been reported, choose it
                    matched_lib_dict[key_name] = {
                        'match': [n], 'similarity': l['similarity']}
                else:
                    # If another version of this library has been reported, choose the one with highest similarity
                    if l['similarity'] > matched_lib_dict[key_name]['similarity']:
                        matched_lib_dict[key_name] = {
                            'match': [n], 'similarity': l['similarity']}
                    elif l['similarity'] == matched_lib_dict[key_name]['similarity']:
                        matched_lib_dict[key_name]['match'].append(n)

        matched_libs = []
        for k in matched_lib_dict:
            matched_libs.extend(matched_lib_dict[k]['match'])

        return matched_libs

    def _get_libpecker_threshold(self, lib):
        # Threshold is set based on the LibPecker paper
        class_num = LIB_INFO[lib]['cls_num']

        if class_num >= 5 and class_num < 10:
            return 0.9
        elif class_num >= 10 and class_num < 15:
            return 0.8
        elif class_num >= 15 and class_num < 20:
            return 0.7
        elif class_num >= 20 and class_num < 25:
            return 0.6
        elif class_num >= 25:
            return 0.5
        else:
            return 1

    def _print_results(self, true_positive_libs, reported_libs, total_libs):
        recall = float(true_positive_libs) / total_libs
        precision = float(true_positive_libs) / reported_libs
        F1 = 2 * precision * recall / (precision + recall)

        print(f"""
        {self.detector.name} {self.metric.value} performance [{self.obfuscator.name} dataset]
        -----------------
        Apps: {len(self.output_files)}
        TP: {true_positive_libs}
        Reported: {reported_libs}
        Total: {total_libs}
        Precision: {precision * 100:.2f}\\%
        Recall: {recall * 100:.2f}\\%
        F1: {F1:.4f}
        """)

    def _print_debug_information(self, app_name, matched_libs):
        if self.debug:
            false_negative_libs = set(
                GROUND_TRUTH[app_name]) - set(matched_libs)
            if false_negative_libs:
                print(
                    f'{self.detector.name} [{self.obfuscator}] missed: {app_name} -> {false_negative_libs}')


if __name__ == "__main__":
    for obfuscator in Obfuscator:
        for metric in Metric:
            for detector in Detector:
                Evaluator(detector=detector, obfuscator=obfuscator, metric=metric).evaluate()
