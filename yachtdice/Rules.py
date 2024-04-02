from ..generic.Rules import set_rule
from BaseClasses import MultiWorld, CollectionState
from statistics import mean
import random

# This file doesn't seem to be able to read from external files, so here's weights (10 kilobytes).
weights = {('Ones', 1, 1): {0: 83239, 1: 16761}, ('Ones', 1, 2): {0: 69521, 1: 30479}, ('Ones', 1, 3): {0: 58042, 1: 41958}, ('Ones', 1, 4): {1: 51605, 0: 48395}, ('Ones', 1, 5): {1: 59869, 0: 40131}, ('Ones', 2, 1): {0: 69173, 1: 27944, 2: 2883}, ('Ones', 2, 2): {0: 48077, 1: 42561, 2: 9362}, ('Ones', 2, 3): {0: 33648, 1: 48807, 2: 17545}, ('Ones', 2, 4): {1: 49713, 0: 23353, 2: 26934}, ('Ones', 2, 5): {1: 48138, 0: 16166, 2: 35696}, ('Ones', 3, 1): {0: 57842, 1: 34681, 2: 7019, 3: 458}, ('Ones', 3, 2): {2: 19473, 1: 43905, 0: 33805, 3: 2817}, ('Ones', 3, 3): {2: 30933, 0: 19239, 1: 42247, 3: 7581}, ('Ones', 3, 4): {1: 36083, 2: 38625, 3: 13952, 0: 11340}, ('Ones', 3, 5): {3: 21123, 2: 43510, 1: 28912, 0: 6455}, ('Ones', 4, 1): {1: 38690, 0: 48091, 2: 11578, 3: 1549, 4: 92}, ('Ones', 4, 2): {1: 40794, 2: 27139, 0: 23040, 3: 8090, 4: 937}, ('Ones', 4, 3): {0: 11285, 1: 32876, 2: 35617, 3: 17049, 4: 3173}, ('Ones', 4, 4): {0: 5516, 2: 37241, 1: 23329, 4: 7098, 3: 26816}, ('Ones', 4, 5): {2: 34692, 0: 2576, 3: 34444, 4: 12901, 1: 15387}, ('Ones', 5, 1): {0: 40167, 1: 40088, 3: 3259, 2: 16162, 4: 315, 5: 9}, ('Ones', 5, 2): {1: 35513, 2: 31203, 0: 16110, 3: 13872, 4: 3041, 5: 261}, ('Ones', 5, 3): {1: 23521, 2: 34680, 3: 25027, 0: 6447, 4: 9036, 5: 1289}, ('Ones', 5, 4): {4: 17155, 2: 29967, 3: 32323, 5: 3774, 1: 14130, 0: 2651}, ('Ones', 5, 5): {0: 1011, 5: 7656, 3: 34454, 2: 23049, 4: 25945, 1: 7885}, ('Twos', 1, 1): {0: 83361, 2: 16639}, ('Twos', 1, 2): {0: 69433, 2: 30567}, ('Twos', 1, 3): {0: 57766, 2: 42234}, ('Twos', 1, 4): {0: 48040, 2: 51960}, ('Twos', 1, 5): {0: 40050, 2: 59950}, ('Twos', 2, 1): {0: 69418, 4: 2806, 2: 27776}, ('Twos', 2, 2): {4: 9247, 2: 42393, 0: 48360}, ('Twos', 2, 3): {4: 17766, 0: 33673, 2: 48561}, ('Twos', 2, 4): {2: 50127, 4: 26692, 0: 23181}, ('Twos', 2, 5): {2: 47982, 4: 35731, 0: 16287}, ('Twos', 3, 1): {2: 34704, 0: 57837, 4: 6969, 6: 490}, ('Twos', 3, 2): {0: 33400, 2: 43973, 6: 2947, 4: 19680}, ('Twos', 3, 3): {4: 30925, 0: 19282, 2: 42265, 6: 7528}, ('Twos', 3, 4): {4: 38771, 2: 36122, 6: 13811, 0: 11296}, ('Twos', 3, 5): {6: 21380, 0: 6525, 4: 43189, 2: 28906}, ('Twos', 4, 1): {2: 38796, 0: 48019, 6: 1551, 4: 11555, 8: 79}, ('Twos', 4, 2): {0: 23205, 2: 40934, 4: 27079, 8: 899, 6: 7883}, ('Twos', 4, 3): {2: 32465, 4: 35540, 6: 17366, 0: 11425, 8: 3204}, ('Twos', 4, 4): {4: 37398, 0: 5459, 6: 26883, 2: 22975, 8: 7285}, ('Twos', 4, 5): {4: 34889, 6: 34300, 8: 12690, 2: 15496, 0: 2625}, ('Twos', 5, 1): {0: 40432, 2: 40078, 4: 16002, 6: 3169, 8: 304, 10: 15}, ('Twos', 5, 2): {4: 31287, 0: 16192, 6: 13722, 2: 35470, 10: 260, 8: 3069}, ('Twos', 5, 3): {0: 6431, 6: 24855, 8: 9029, 4: 34718, 2: 23656, 10: 1311}, ('Twos', 5, 4): {4: 29913, 2: 14101, 8: 17181, 6: 32456, 0: 2666, 10: 3683}, ('Twos', 5, 5): {8: 25826, 10: 7738, 2: 7838, 4: 23216, 0: 989, 6: 34393}, ('Threes', 1, 1): {0: 83386, 3: 16614}, ('Threes', 1, 2): {0: 69267, 3: 30733}, ('Threes', 1, 3): {0: 57922, 3: 42078}, ('Threes', 1, 4): {3: 51839, 0: 48161}, ('Threes', 1, 5): {3: 60069, 0: 39931}, ('Threes', 2, 1): {0: 69551, 3: 27706, 6: 2743}, ('Threes', 2, 2): {3: 42487, 6: 9388, 0: 48125}, ('Threes', 2, 3): {3: 48780, 6: 17768, 0: 33452}, ('Threes', 2, 4): {3: 49882, 6: 26895, 0: 23223}, ('Threes', 2, 5): {3: 48048, 6: 35830, 0: 16122}, ('Threes', 3, 1): {0: 58112, 3: 34373, 6: 7068, 9: 447}, ('Threes', 3, 2): {3: 44379, 0: 33196, 6: 19596, 9: 2829}, ('Threes', 3, 3): {0: 19302, 6: 30948, 3: 42280, 9: 7470}, ('Threes', 3, 4): {9: 14015, 6: 38565, 3: 36006, 0: 11414}, ('Threes', 3, 5): {6: 43231, 9: 21335, 3: 28812, 0: 6622}, ('Threes', 4, 1): {3: 38475, 0: 48304, 6: 11591, 9: 1549, 12: 81}, ('Threes', 4, 2): {3: 40921, 0: 23282, 6: 26908, 9: 8028, 12: 861}, ('Threes', 4, 3): {9: 17403, 3: 32832, 6: 35428, 0: 11223, 12: 3114}, ('Threes', 4, 4): {12: 7259, 3: 23317, 9: 26777, 6: 37376, 0: 5271}, ('Threes', 4, 5): {12: 12996, 6: 34520, 9: 34409, 3: 15411, 0: 2664}, ('Threes', 5, 1): {6: 16018, 0: 40191, 9: 3214, 3: 40251, 12: 311, 15: 15}, ('Threes', 5, 2): {6: 31156, 9: 13826, 3: 35577, 0: 16082, 12: 3106, 15: 253}, ('Threes', 5, 3): {9: 24875, 3: 23557, 6: 34620, 0: 6489, 15: 1359, 12: 9100}, ('Threes', 5, 4): {6: 29975, 9: 32296, 12: 17378, 3: 13980, 15: 3779, 0: 2592}, ('Threes', 5, 5): {3: 7796, 9: 34312, 6: 23447, 12: 26056, 15: 7353, 0: 1036}, ('Fours', 1, 1): {0: 83344, 4: 16656}, ('Fours', 1, 2): {0: 69320, 4: 30680}, ('Fours', 1, 3): {0: 57704, 4: 42296}, ('Fours', 1, 4): {4: 51598, 0: 48402}, ('Fours', 1, 5): {4: 60105, 0: 39895}, ('Fours', 2, 1): {4: 27911, 0: 69267, 8: 2822}, ('Fours', 2, 2): {4: 42262, 0: 48491, 8: 9247}, ('Fours', 2, 3): {4: 48512, 0: 33666, 8: 17822}, ('Fours', 2, 4): {8: 26988, 0: 23304, 4: 49708}, ('Fours', 2, 5): {4: 48018, 8: 35825, 0: 16157}, ('Fours', 3, 1): {0: 57818, 8: 6984, 4: 34741, 12: 457}, ('Fours', 3, 2): {4: 44111, 0: 33555, 8: 19482, 12: 2852}, ('Fours', 3, 3): {4: 42473, 8: 30788, 0: 19266, 12: 7473}, ('Fours', 3, 4): {12: 13725, 4: 36284, 8: 38815, 0: 11176}, ('Fours', 3, 5): {8: 42976, 12: 21578, 4: 28881, 0: 6565}, ('Fours', 4, 1): {0: 48032, 12: 1509, 8: 11674, 4: 38717, 16: 68}, ('Fours', 4, 2): {8: 27200, 4: 40745, 12: 8060, 0: 23075, 16: 920}, ('Fours', 4, 3): {0: 11382, 8: 35497, 12: 17289, 4: 32735, 16: 3097}, ('Fours', 4, 4): {12: 26744, 4: 23199, 0: 5413, 8: 37451, 16: 7193}, ('Fours', 4, 5): {12: 34494, 8: 34634, 4: 15457, 16: 12752, 0: 2663}, ('Fours', 5, 1): {0: 40145, 4: 40078, 8: 16172, 12: 3278, 16: 320, 20: 7}, ('Fours', 5, 2): {16: 3009, 4: 35689, 12: 13847, 0: 16083, 8: 31076, 20: 296}, ('Fours', 5, 3): {8: 34277, 12: 24923, 0: 6539, 4: 23786, 16: 9129, 20: 1346}, ('Fours', 5, 4): {12: 32377, 8: 30256, 4: 13849, 16: 16978, 0: 2709, 20: 3831}, ('Fours', 5, 5): {8: 23080, 12: 34580, 4: 7856, 20: 7567, 16: 25841, 0: 1076}, ('Fives', 1, 1): {0: 83655, 5: 16345}, ('Fives', 1, 2): {0: 69141, 5: 30859}, ('Fives', 1, 3): {0: 57451, 5: 42549}, ('Fives', 1, 4): {0: 48174, 5: 51826}, ('Fives', 1, 5): {5: 59464, 0: 40536}, ('Fives', 2, 1): {0: 69460, 5: 27838, 10: 2702}, ('Fives', 2, 2): {0: 48340, 10: 9495, 5: 42165}, ('Fives', 2, 3): {0: 33394, 5: 48856, 10: 17750}, ('Fives', 2, 4): {5: 49905, 0: 23183, 10: 26912}, ('Fives', 2, 5): {5: 48196, 0: 15884, 10: 35920}, ('Fives', 3, 1): {5: 34633, 0: 58017, 10: 6863, 15: 487}, ('Fives', 3, 2): {0: 33539, 5: 44147, 10: 19527, 15: 2787}, ('Fives', 3, 3): {10: 30850, 5: 42258, 0: 19444, 15: 7448}, ('Fives', 3, 4): {15: 14005, 0: 10940, 10: 38917, 5: 36138}, ('Fives', 3, 5): {10: 43023, 15: 21619, 5: 28785, 0: 6573}, ('Fives', 4, 1): {5: 38259, 0: 48540, 10: 11586, 15: 1536, 20: 79}, ('Fives', 4, 2): {10: 27047, 5: 40972, 0: 22971, 15: 8110, 20: 900}, ('Fives', 4, 3): {5: 32526, 10: 35669, 15: 17370, 20: 3181, 0: 11254}, ('Fives', 4, 4): {10: 37008, 5: 23418, 15: 26844, 0: 5539, 20: 7191}, ('Fives', 4, 5): {15: 34495, 20: 12944, 0: 2533, 5: 15578, 10: 34450}, ('Fives', 5, 1): {0: 40009, 10: 16027, 5: 40445, 15: 3209, 20: 292, 25: 18}, ('Fives', 5, 2): {0: 15904, 5: 35792, 10: 31341, 15: 13711, 20: 3027, 25: 225}, ('Fives', 5, 3): {5: 23686, 15: 24850, 10: 34377, 25: 1339, 0: 6535, 20: 9213}, ('Fives', 5, 4): {10: 30086, 15: 32137, 25: 3834, 5: 14139, 20: 17154, 0: 2650}, ('Fives', 5, 5): {20: 25632, 15: 34567, 10: 23320, 25: 7652, 5: 7740, 0: 1089}, ('Sixes', 1, 1): {0: 83429, 6: 16571}, ('Sixes', 1, 2): {6: 30388, 0: 69612}, ('Sixes', 1, 3): {0: 57751, 6: 42249}, ('Sixes', 1, 4): {6: 51565, 0: 48435}, ('Sixes', 1, 5): {6: 59987, 0: 40013}, ('Sixes', 2, 1): {0: 69492, 6: 27656, 12: 2852}, ('Sixes', 2, 2): {6: 42600, 0: 48108, 12: 9292}, ('Sixes', 2, 3): {0: 33359, 6: 49005, 12: 17636}, ('Sixes', 2, 4): {6: 50132, 0: 23124, 12: 26744}, ('Sixes', 2, 5): {12: 35877, 6: 48049, 0: 16074}, ('Sixes', 3, 1): {0: 57807, 12: 7033, 6: 34675, 18: 485}, ('Sixes', 3, 2): {6: 44236, 0: 33721, 12: 19253, 18: 2790}, ('Sixes', 3, 3): {12: 31130, 6: 41932, 18: 7459, 0: 19479}, ('Sixes', 3, 4): {12: 39004, 6: 36097, 0: 11212, 18: 13687}, ('Sixes', 3, 5): {18: 21603, 6: 29010, 0: 6383, 12: 43004}, ('Sixes', 4, 1): {0: 48354, 6: 38391, 12: 11640, 18: 1543, 24: 72}, ('Sixes', 4, 2): {0: 23271, 12: 27097, 6: 40889, 18: 7874, 24: 869}, ('Sixes', 4, 3): {12: 35683, 6: 32745, 18: 17225, 0: 11197, 24: 3150}, ('Sixes', 4, 4): {6: 23145, 12: 37530, 18: 26840, 24: 7057, 0: 5428}, ('Sixes', 4, 5): {12: 34697, 18: 34555, 6: 15437, 24: 12741, 0: 2570}, ('Sixes', 5, 1): {6: 40144, 0: 40345, 12: 16040, 18: 3187, 24: 278, 30: 6}, ('Sixes', 5, 2): {6: 35724, 12: 31301, 0: 15907, 18: 13866, 30: 272, 24: 2930}, ('Sixes', 5, 3): {12: 34420, 18: 25185, 6: 23606, 0: 6399, 24: 9091, 30: 1299}, ('Sixes', 5, 4): {18: 32340, 12: 29826, 6: 14128, 30: 3777, 24: 17371, 0: 2558}, ('Sixes', 5, 5): {18: 34616, 12: 23218, 24: 25647, 30: 7594, 6: 7822, 0: 1103}, ('Choice', 1, 1): {2: 16561, 6: 16759, 1: 16707, 3: 16737, 4: 16563, 5: 16673}, ('Choice', 1, 2): {6: 27671, 1: 11148, 3: 11305, 5: 27776, 2: 10945, 4: 11155}, ('Choice', 1, 3): {6: 39775, 3: 9324, 4: 9206, 5: 23230, 2: 9235, 1: 9230}, ('Choice', 1, 4): {2: 7743, 6: 49767, 3: 7765, 1: 7782, 5: 19332, 4: 7611}, ('Choice', 1, 5): {2: 6407, 6: 58143, 3: 6435, 5: 16001, 4: 6477, 1: 6537}, ('Choice', 2, 1): {8: 14008, 7: 16633, 10: 8410, 12: 2783, 4: 8344, 6: 13916, 5: 10942, 9: 11192, 11: 5487, 3: 5451, 2: 2834}, ('Choice', 2, 2): {10: 14035, 12: 7852, 9: 12135, 5: 5042, 8: 13559, 7: 14689, 11: 15433, 6: 9888, 3: 2514, 4: 3650, 2: 1203}, ('Choice', 2, 3): {9: 11600, 11: 18548, 3: 1723, 5: 3389, 12: 15744, 8: 12726, 4: 2571, 7: 13221, 10: 12774, 6: 6856, 2: 848}, ('Choice', 2, 4): {3: 1186, 12: 24890, 7: 11797, 11: 19174, 6: 4818, 9: 10504, 5: 2433, 8: 11316, 10: 11497, 4: 1782, 2: 603}, ('Choice', 2, 5): {12: 33963, 8: 9920, 7: 10488, 4: 1277, 10: 9835, 11: 18691, 9: 9645, 6: 3232, 2: 420, 3: 857, 5: 1672}, ('Choice', 3, 1): {10: 12450, 9: 11536, 14: 6954, 5: 2781, 12: 11591, 7: 6859, 11: 12599, 15: 4585, 8: 9700, 13: 9724, 6: 4584, 3: 501, 16: 2811, 4: 1387, 17: 1479, 18: 459}, ('Choice', 3, 2): {9: 6481, 18: 2138, 10: 7974, 17: 6412, 14: 11422, 7: 2648, 15: 9771, 11: 10211, 13: 13457, 12: 12837, 16: 9017, 8: 4826, 4: 421, 6: 1387, 5: 866, 3: 132}, ('Choice', 3, 3): {16: 10624, 15: 10839, 13: 13577, 18: 6402, 12: 10786, 7: 1548, 14: 12198, 9: 4649, 17: 11047, 10: 5918, 11: 7672, 6: 806, 5: 439, 4: 239, 8: 3177, 3: 79}, ('Choice', 3, 4): {12: 8735, 16: 11202, 14: 11956, 18: 12544, 13: 13183, 15: 10793, 17: 14213, 11: 5674, 10: 4414, 9: 3367, 8: 2130, 5: 274, 7: 880, 4: 130, 6: 456, 3: 49}, ('Choice', 3, 5): {13: 12348, 15: 10462, 18: 19750, 16: 11098, 17: 16293, 8: 1412, 11: 4015, 9: 2378, 14: 11395, 10: 3114, 12: 6668, 4: 78, 6: 263, 7: 519, 5: 179, 3: 28}, ('Choice', 4, 1): {13: 10739, 14: 11286, 11: 8077, 12: 9695, 10: 6154, 16: 9683, 15: 10664, 18: 6231, 8: 2685, 21: 1544, 17: 8221, 19: 4316, 20: 2664, 9: 4214, 6: 742, 7: 1475, 5: 332, 23: 325, 22: 805, 24: 73, 4: 75}, ('Choice', 4, 2): {18: 11293, 16: 10316, 20: 7951, 15: 9294, 17: 11396, 19: 10041, 11: 2941, 12: 4311, 14: 7908, 13: 6275, 10: 2044, 22: 4601, 8: 599, 21: 6297, 9: 1212, 23: 2388, 24: 601, 7: 321, 5: 40, 6: 154, 4: 17}, ('Choice', 4, 3): {16: 8625, 18: 11648, 14: 5924, 22: 7550, 17: 9636, 20: 9991, 13: 4014, 21: 8336, 15: 7349, 23: 5909, 19: 11828, 10: 1131, 12: 2627, 6: 66, 9: 626, 24: 2490, 11: 1724, 8: 335, 7: 149, 4: 8, 5: 34}, ('Choice', 4, 4): {17: 8113, 22: 9299, 15: 5631, 23: 9637, 19: 12614, 18: 10757, 21: 9710, 20: 10743, 24: 6196, 14: 4194, 16: 6660, 12: 1591, 13: 2565, 9: 318, 11: 1061, 10: 629, 7: 77, 6: 36, 8: 153, 5: 13, 4: 3}, ('Choice', 4, 5): {20: 11379, 19: 12613, 15: 4107, 23: 12729, 22: 10342, 16: 5175, 21: 10216, 24: 11322, 13: 1602, 18: 9101, 17: 6280, 9: 199, 14: 2965, 10: 359, 11: 576, 12: 903, 8: 67, 7: 35, 6: 21, 5: 7, 4: 2}, ('Choice', 5, 1): {20: 8273, 18: 10091, 15: 8426, 25: 1664, 19: 9556, 27: 438, 17: 10106, 23: 3877, 12: 3911, 10: 1630, 24: 2523, 16: 9558, 21: 6848, 8: 460, 11: 2540, 14: 6965, 22: 5414, 28: 198, 13: 5364, 26: 919, 7: 184, 9: 898, 29: 59, 5: 14, 6: 70, 30: 14}, ('Choice', 5, 2): {21: 9780, 26: 4664, 16: 4586, 22: 9867, 18: 7336, 14: 2299, 23: 9595, 19: 8590, 25: 6430, 11: 508, 17: 5763, 27: 3301, 20: 9728, 24: 8389, 15: 3407, 13: 1401, 28: 2011, 29: 794, 12: 908, 10: 270, 30: 153, 9: 125, 8: 58, 6: 11, 7: 26}, ('Choice', 5, 3): {30: 978, 17: 3666, 14: 1175, 25: 9241, 16: 2707, 28: 4512, 27: 5942, 24: 10150, 20: 7889, 18: 5000, 21: 8899, 19: 6530, 26: 7389, 23: 9959, 29: 2917, 22: 9588, 15: 1896, 13: 645, 12: 443, 11: 262, 7: 13, 10: 105, 8: 26, 9: 60, 6: 6, 5: 2}, ('Choice', 5, 4): {26: 9428, 17: 2241, 30: 3081, 22: 8349, 20: 6065, 21: 7344, 28: 7007, 25: 11042, 24: 10913, 27: 7761, 23: 9239, 18: 3163, 29: 5892, 14: 653, 19: 4497, 11: 110, 13: 339, 8: 10, 12: 217, 16: 1603, 15: 972, 10: 46, 9: 20, 7: 6, 6: 2}, ('Choice', 5, 5): {27: 9206, 24: 10214, 14: 275, 26: 10430, 30: 6785, 29: 9253, 28: 8722, 20: 4454, 25: 11922, 23: 8103, 21: 5645, 22: 6723, 17: 1473, 19: 2938, 11: 53, 18: 1990, 16: 956, 12: 102, 13: 189, 15: 522, 10: 31, 9: 9, 7: 1, 8: 4}, ('Pair', 1, 1): {0: 100000}, ('Pair', 1, 2): {0: 100000}, ('Pair', 1, 3): {0: 100000}, ('Pair', 1, 4): {0: 100000}, ('Pair', 1, 5): {0: 100000}, ('Pair', 2, 1): {10: 16659, 0: 83341}, ('Pair', 2, 2): {0: 69607, 10: 30393}, ('Pair', 2, 3): {0: 57963, 10: 42037}, ('Pair', 2, 4): {0: 48274, 10: 51726}, ('Pair', 2, 5): {10: 59554, 0: 40446}, ('Pair', 3, 1): {0: 55377, 10: 44623}, ('Pair', 3, 2): {10: 69057, 0: 30943}, ('Pair', 3, 3): {10: 82991, 0: 17009}, ('Pair', 3, 4): {10: 90480, 0: 9520}, ('Pair', 3, 5): {10: 94775, 0: 5225}, ('Pair', 4, 1): {10: 72290, 0: 27710}, ('Pair', 4, 2): {0: 7919, 10: 92081}, ('Pair', 4, 3): {10: 97809, 0: 2191}, ('Pair', 4, 4): {10: 99407, 0: 593}, ('Pair', 4, 5): {10: 99843, 0: 157}, ('Pair', 5, 1): {10: 90763, 0: 9237}, ('Pair', 5, 2): {10: 99110, 0: 890}, ('Pair', 5, 3): {10: 99919, 0: 81}, ('Pair', 5, 4): {10: 99992, 0: 8}, ('Pair', 5, 5): {10: 100000}, ('ThreeOfAKind', 1, 1): {0: 100000}, ('ThreeOfAKind', 1, 2): {0: 100000}, ('ThreeOfAKind', 1, 3): {0: 100000}, ('ThreeOfAKind', 1, 4): {0: 100000}, ('ThreeOfAKind', 1, 5): {0: 100000}, ('ThreeOfAKind', 2, 1): {0: 100000}, ('ThreeOfAKind', 2, 2): {0: 100000}, ('ThreeOfAKind', 2, 3): {0: 100000}, ('ThreeOfAKind', 2, 4): {0: 100000}, ('ThreeOfAKind', 2, 5): {0: 100000}, ('ThreeOfAKind', 3, 1): {0: 97256, 20: 2744}, ('ThreeOfAKind', 3, 2): {0: 88749, 20: 11251}, ('ThreeOfAKind', 3, 3): {20: 21698, 0: 78302}, ('ThreeOfAKind', 3, 4): {0: 67629, 20: 32371}, ('ThreeOfAKind', 3, 5): {20: 42286, 0: 57714}, ('ThreeOfAKind', 4, 1): {0: 90286, 20: 9714}, ('ThreeOfAKind', 4, 2): {0: 68611, 20: 31389}, ('ThreeOfAKind', 4, 3): {0: 49008, 20: 50992}, ('ThreeOfAKind', 4, 4): {20: 65374, 0: 34626}, ('ThreeOfAKind', 4, 5): {20: 76116, 0: 23884}, ('ThreeOfAKind', 5, 1): {0: 78777, 20: 21223}, ('ThreeOfAKind', 5, 2): {0: 45759, 20: 54241}, ('ThreeOfAKind', 5, 3): {0: 25652, 20: 74348}, ('ThreeOfAKind', 5, 4): {20: 85598, 0: 14402}, ('ThreeOfAKind', 5, 5): {20: 91973, 0: 8027}, ('FourOfAKind', 1, 1): {0: 100000}, ('FourOfAKind', 1, 2): {0: 100000}, ('FourOfAKind', 1, 3): {0: 100000}, ('FourOfAKind', 1, 4): {0: 100000}, ('FourOfAKind', 1, 5): {0: 100000}, ('FourOfAKind', 2, 1): {0: 100000}, ('FourOfAKind', 2, 2): {0: 100000}, ('FourOfAKind', 2, 3): {0: 100000}, ('FourOfAKind', 2, 4): {0: 100000}, ('FourOfAKind', 2, 5): {0: 100000}, ('FourOfAKind', 3, 1): {0: 100000}, ('FourOfAKind', 3, 2): {0: 100000}, ('FourOfAKind', 3, 3): {0: 100000}, ('FourOfAKind', 3, 4): {0: 100000}, ('FourOfAKind', 3, 5): {0: 100000}, ('FourOfAKind', 4, 1): {0: 99524, 30: 476}, ('FourOfAKind', 4, 2): {0: 96231, 30: 3769}, ('FourOfAKind', 4, 3): {30: 10262, 0: 89738}, ('FourOfAKind', 4, 4): {0: 81691, 30: 18309}, ('FourOfAKind', 4, 5): {0: 72936, 30: 27064}, ('FourOfAKind', 5, 1): {0: 97987, 30: 2013}, ('FourOfAKind', 5, 2): {0: 86815, 30: 13185}, ('FourOfAKind', 5, 3): {30: 28994, 0: 71006}, ('FourOfAKind', 5, 4): {30: 44588, 0: 55412}, ('FourOfAKind', 5, 5): {30: 58383, 0: 41617}, ('TinyStraight', 1, 1): {0: 100000}, ('TinyStraight', 1, 2): {0: 100000}, ('TinyStraight', 1, 3): {0: 100000}, ('TinyStraight', 1, 4): {0: 100000}, ('TinyStraight', 1, 5): {0: 100000}, ('TinyStraight', 2, 1): {0: 100000}, ('TinyStraight', 2, 2): {0: 100000}, ('TinyStraight', 2, 3): {0: 100000}, ('TinyStraight', 2, 4): {0: 100000}, ('TinyStraight', 2, 5): {0: 100000}, ('TinyStraight', 3, 1): {0: 91611, 20: 8389}, ('TinyStraight', 3, 2): {20: 21023, 0: 78977}, ('TinyStraight', 3, 3): {0: 66656, 20: 33344}, ('TinyStraight', 3, 4): {0: 55864, 20: 44136}, ('TinyStraight', 3, 5): {0: 46988, 20: 53012}, ('TinyStraight', 4, 1): {0: 78861, 20: 21139}, ('TinyStraight', 4, 2): {0: 55094, 20: 44906}, ('TinyStraight', 4, 3): {0: 38207, 20: 61793}, ('TinyStraight', 4, 4): {20: 73382, 0: 26618}, ('TinyStraight', 4, 5): {20: 81796, 0: 18204}, ('TinyStraight', 5, 1): {20: 35085, 0: 64915}, ('TinyStraight', 5, 2): {20: 63342, 0: 36658}, ('TinyStraight', 5, 3): {20: 79598, 0: 20402}, ('TinyStraight', 5, 4): {20: 88363, 0: 11637}, ('TinyStraight', 5, 5): {20: 93408, 0: 6592}, ('SmallStraight', 1, 1): {0: 100000}, ('SmallStraight', 1, 2): {0: 100000}, ('SmallStraight', 1, 3): {0: 100000}, ('SmallStraight', 1, 4): {0: 100000}, ('SmallStraight', 1, 5): {0: 100000}, ('SmallStraight', 2, 1): {0: 100000}, ('SmallStraight', 2, 2): {0: 100000}, ('SmallStraight', 2, 3): {0: 100000}, ('SmallStraight', 2, 4): {0: 100000}, ('SmallStraight', 2, 5): {0: 100000}, ('SmallStraight', 3, 1): {0: 100000}, ('SmallStraight', 3, 2): {0: 100000}, ('SmallStraight', 3, 3): {0: 100000}, ('SmallStraight', 3, 4): {0: 100000}, ('SmallStraight', 3, 5): {0: 100000}, ('SmallStraight', 4, 1): {0: 94527, 30: 5473}, ('SmallStraight', 4, 2): {0: 82668, 30: 17332}, ('SmallStraight', 4, 3): {0: 68088, 30: 31912}, ('SmallStraight', 4, 4): {0: 53760, 30: 46240}, ('SmallStraight', 4, 5): {0: 42284, 30: 57716}, ('SmallStraight', 5, 1): {0: 84711, 30: 15289}, ('SmallStraight', 5, 2): {0: 60618, 30: 39382}, ('SmallStraight', 5, 3): {30: 60478, 0: 39522}, ('SmallStraight', 5, 4): {30: 75184, 0: 24816}, ('SmallStraight', 5, 5): {30: 84465, 0: 15535}, ('LargeStraight', 1, 1): {0: 100000}, ('LargeStraight', 1, 2): {0: 100000}, ('LargeStraight', 1, 3): {0: 100000}, ('LargeStraight', 1, 4): {0: 100000}, ('LargeStraight', 1, 5): {0: 100000}, ('LargeStraight', 2, 1): {0: 100000}, ('LargeStraight', 2, 2): {0: 100000}, ('LargeStraight', 2, 3): {0: 100000}, ('LargeStraight', 2, 4): {0: 100000}, ('LargeStraight', 2, 5): {0: 100000}, ('LargeStraight', 3, 1): {0: 100000}, ('LargeStraight', 3, 2): {0: 100000}, ('LargeStraight', 3, 3): {0: 100000}, ('LargeStraight', 3, 4): {0: 100000}, ('LargeStraight', 3, 5): {0: 100000}, ('LargeStraight', 4, 1): {0: 100000}, ('LargeStraight', 4, 2): {0: 100000}, ('LargeStraight', 4, 3): {0: 100000}, ('LargeStraight', 4, 4): {0: 100000}, ('LargeStraight', 4, 5): {0: 100000}, ('LargeStraight', 5, 1): {0: 96934, 40: 3066}, ('LargeStraight', 5, 2): {0: 87111, 40: 12889}, ('LargeStraight', 5, 3): {40: 25054, 0: 74946}, ('LargeStraight', 5, 4): {0: 63466, 40: 36534}, ('LargeStraight', 5, 5): {40: 46913, 0: 53087}, ('FullHouse', 1, 1): {0: 100000}, ('FullHouse', 1, 2): {0: 100000}, ('FullHouse', 1, 3): {0: 100000}, ('FullHouse', 1, 4): {0: 100000}, ('FullHouse', 1, 5): {0: 100000}, ('FullHouse', 2, 1): {0: 100000}, ('FullHouse', 2, 2): {0: 100000}, ('FullHouse', 2, 3): {0: 100000}, ('FullHouse', 2, 4): {0: 100000}, ('FullHouse', 2, 5): {0: 100000}, ('FullHouse', 3, 1): {0: 100000}, ('FullHouse', 3, 2): {0: 100000}, ('FullHouse', 3, 3): {0: 100000}, ('FullHouse', 3, 4): {0: 100000}, ('FullHouse', 3, 5): {0: 100000}, ('FullHouse', 4, 1): {0: 100000}, ('FullHouse', 4, 2): {0: 100000}, ('FullHouse', 4, 3): {0: 100000}, ('FullHouse', 4, 4): {0: 100000}, ('FullHouse', 4, 5): {0: 100000}, ('FullHouse', 5, 1): {0: 96166, 25: 3834}, ('FullHouse', 5, 2): {0: 81548, 25: 18452}, ('FullHouse', 5, 3): {0: 64060, 25: 35940}, ('FullHouse', 5, 4): {25: 50017, 0: 49983}, ('FullHouse', 5, 5): {0: 38111, 25: 61889}, ('Yacht', 1, 1): {0: 100000}, ('Yacht', 1, 2): {0: 100000}, ('Yacht', 1, 3): {0: 100000}, ('Yacht', 1, 4): {0: 100000}, ('Yacht', 1, 5): {0: 100000}, ('Yacht', 2, 1): {0: 100000}, ('Yacht', 2, 2): {0: 100000}, ('Yacht', 2, 3): {0: 100000}, ('Yacht', 2, 4): {0: 100000}, ('Yacht', 2, 5): {0: 100000}, ('Yacht', 3, 1): {0: 100000}, ('Yacht', 3, 2): {0: 100000}, ('Yacht', 3, 3): {0: 100000}, ('Yacht', 3, 4): {0: 100000}, ('Yacht', 3, 5): {0: 100000}, ('Yacht', 4, 1): {0: 100000}, ('Yacht', 4, 2): {0: 100000}, ('Yacht', 4, 3): {0: 100000}, ('Yacht', 4, 4): {0: 100000}, ('Yacht', 4, 5): {0: 100000}, ('Yacht', 5, 1): {0: 99949, 50: 51}, ('Yacht', 5, 2): {0: 98731, 50: 1269}, ('Yacht', 5, 3): {0: 95425, 50: 4575}, ('Yacht', 5, 4): {0: 89885, 50: 10115}, ('Yacht', 5, 5): {0: 82836, 50: 17164}}

simulationCount = 0
scores = []
previousState = None

GAMES_TO_PROGRESS = 100
ITERATIONS_PER_GANE_TO_PROGRESS = 5

class Category:
    def __init__(self, name):
        self.name = name

    def maxScore(self, weights, nbDice, nbRolls):
        return max(weights[self.name, nbDice, nbRolls])

    def meanScore(self, weights, nbDice, nbRolls):
        meanScore = 0
        for key in weights[self.name, nbDice, nbRolls]:
            meanScore += key*weights[self.name, nbDice, nbRolls][key]/100000
        return meanScore

    def simulateRolls(self, nbDice, nbRolls):
        return \
            random.choices(list(weights[self.name, nbDice, nbRolls].keys()),
                           weights[self.name, nbDice, nbRolls].values(), k=1)[0]

def canReachScore(state: CollectionState, player, scoretarget: int, options):
    global previousState
    categories, number_of_rerolls, number_of_dice, score_mult = extractProgression(state, player, options)
    diceSimulation(categories, number_of_rerolls, number_of_dice, score_mult)
    if False:
        if previousState is None:
            categories, number_of_rerolls, number_of_dice, score_mult=extractProgression(state, player, options)
            diceSimulation(categories, number_of_rerolls, number_of_dice, score_mult)
        elif state != previousState:
            categories, number_of_rerolls, number_of_dice, score_mult=extractProgression(state, player, options)
            diceSimulation(categories, number_of_rerolls, number_of_dice, score_mult)
        previousState = state
    if scoretarget == 500:
        print(verifyAccessibility(scoretarget))
        print(max(scores))
    return verifyAccessibility(scoretarget)

def verifyAccessibility(score):
    global scores
    wins = len(list(filter(lambda s:s>=score, scores)))
    if wins == 0:
        return False
    return max(scores)>score
    return len(scores)/wins <= GAMES_TO_PROGRESS

def extractProgression(state, player, options):
    number_of_dice = state.count("Dice", player) + state.count("Dice Fragment", player) // options.number_of_dice_fragments_per_dice.value

    number_of_rerolls = state.count("Roll", player) + state.count("Roll Fragment", player) // options.number_of_roll_fragments_per_roll.value

    number_of_mults = state.count("Score Multiplier", player)
    score_mult = 0.02 *  number_of_mults

    categories = []

    if state.has("Category Choice", player, 1):
        categories.append(Category("Choice"))
    if state.has("Category Inverse Choice", player, 1):
        categories.append(Category("Choice"))
    if state.has("Category Sixes", player, 1):
        categories.append(Category("Sixes"))
    if state.has("Category Fives", player, 1):
        categories.append(Category("Fives"))
    if state.has("Category Tiny Straight", player, 1):
        categories.append(Category("TinyStraight"))
    if state.has("Category Threes", player, 1):
        categories.append(Category("Threes"))
    if state.has("Category Fours", player, 1):
        categories.append(Category("Fours"))
    if state.has("Category Pair", player, 1):
        categories.append(Category("Pair"))
    if state.has("Category Three of a Kind", player, 1):
        categories.append(Category("ThreeOfAKind"))
    if state.has("Category Four of a Kind", player, 1):
        categories.append(Category("FourOfAKind"))
    if state.has("Category Ones", player, 1):
        categories.append(Category("Ones"))
    if state.has("Category Twos", player, 1):
        categories.append(Category("Twos"))
    if state.has("Category Small Straight", player, 1):
        categories.append(Category("SmallStraight"))
    if state.has("Category Large Straight", player, 1):
        categories.append(Category("LargeStraight"))
    if state.has("Category Full House", player, 1):
        categories.append(Category("FullHouse"))
    if state.has("Category Yacht", player, 1):
        categories.append(Category("Yacht"))

    return categories, number_of_rerolls, number_of_dice, score_mult
    
def diceSimulation(categories, nbRolls, nbDice, multiplier):
    global weights
    global simulationCount
    global scores

    scores = []

    categories.sort(key=lambda category: category.maxScore(weights, nbDice, nbRolls))
    for i in range(GAMES_TO_PROGRESS * ITERATIONS_PER_GANE_TO_PROGRESS):
        total = 0
        for j in range(len(categories)):
            roll = round(categories[j].simulateRolls(nbDice, nbRolls) * (1 + j * multiplier))
            total += roll
        scores.append(total)

    simulationCount += 250

# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int, options):
    for i in range(1, options.goal_score.value):
        if i < 20 or (i < 100 and i % 2 == 0) or (i % 10 == 0):
            set_rule(world.get_location(f"{i} score", player), lambda state, i=i, player=player: canReachScore(state, player, i, options))
    

# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int, options):
    print("A")
    if scores:
        if max(scores) >500:
            print("B")
    world.completion_condition[player] = lambda state: canReachScore(state, player, options.goal_score.value, options)
