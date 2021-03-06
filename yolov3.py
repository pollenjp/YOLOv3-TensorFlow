import numpy as np
np.random.seed(101)
import tensorflow as tf
import os
import utils

class YOLOv3(object):
    """Structure of reseau neural YOLO3"""

    # def __init__(self, x, num_classes, trainable=True, strategie_training=False, is_training=False):
    def __init__(self, x, num_classes, cfg_filepath, weight_filepath, trainable=True):
        """
        Create the graph ofthe YOLOv3 model
        | Parameters
        | input          | tf.Tensor |
        | trainable      | bool      |
        :param x: Placeholder for the input tensor: (normalised image (416, 416, 3)/255.)
        :param num_classes: Number of classes in the dataset
               if it isn't in the same folder as this code
        """
        self.X = x
        self.NUM_CLASSES = num_classes
        self.cfg_parser = utils.read_cfg_file(config_filepath=cfg_filepath)
        self.weight_h5_filepath = weight_h5_filepath
        self.trainable=trainable

    #===================================================================================================================
    def __call__(self, input):
        """
        Create the network graph
        |-Parameters
        | input          | tf.Tensor |
        | fine_tuning    | bool      |
        |
        |-Returns
        | feature maps 5+80 in 3 grid (13,13), (26,26), (52, 52)
        """
        features_odict, scale_0_odict, scale_1_odict, scale_2_odict = \
            utils.split_layer_structure(config_parser=self.cfg_parser)
        
        print("YOLOv3, let's go!!!!!!!")
        layer = input
        self.layer_idx = 0
        self.layers_list = []
        #===========================================================================================
        with tf.name_scope("Features"):
            for _section, _proxy in features_odict.items():
                assert len(_section.split("_")) == 2
                select_layer(section=_section, proxy=_proxy, inputs=layer)
                layer_idx += 1
                self.layers_list.append(layer)

        #===========================================================================================
        with tf.name_scope("Features"):
            conv_1 = self.conv2d(self.X, 1)
            # Downsample#############################################
            conv_2 = self.conv2d(conv_1, 2, stride=2)

            # resblock
            conv_3 = self.conv2d(conv_2, 3)
            conv_4 = self.conv2d(conv_3, 4)
            resn_1 = self.resnet(conv_2, conv_4, 1)

            # Downsample#############################################
            conv_5 = self.conv2d(resn_1, 5, stride=2)

            # resblock
            conv_6 = self.conv2d(conv_5, 6)
            conv_7 = self.conv2d(conv_6, 7)
            resn_2 = self.resnet(conv_5, conv_7, 2)

            # resblock
            conv_8 = self.conv2d(resn_2, 8)
            conv_9 = self.conv2d(conv_8, 9)
            resn_3 = self.resnet(resn_2, conv_9, 3)

            # Downsample#############################################
            conv_10 = self.conv2d(resn_3, 10, stride=2)

            # resblock
            conv_11 = self.conv2d(conv_10, 11)
            conv_12 = self.conv2d(conv_11, 12)
            resn_4 = self.resnet(conv_10, conv_12, 4)

            # resblock
            conv_13 = self.conv2d(resn_4, 13)
            conv_14 = self.conv2d(conv_13, 14)
            resn_5 = self.resnet(resn_4, conv_14, 5)

            # resblock
            conv_15 = self.conv2d(resn_5, 15)
            conv_16 = self.conv2d(conv_15, 16)
            resn_6 = self.resnet(resn_5, conv_16, 6)

            # resblock
            conv_17 = self.conv2d(resn_6, 17)
            conv_18 = self.conv2d(conv_17, 18)
            resn_7 = self.resnet(resn_6, conv_18, 7)

            # resblock
            conv_19 = self.conv2d(resn_7, 19)
            conv_20 = self.conv2d(conv_19, 20)
            resn_8 = self.resnet(resn_7, conv_20, 8)

            # resblock
            conv_21 = self.conv2d(resn_8, 21)
            conv_22 = self.conv2d(conv_21, 22)
            resn_9 = self.resnet(resn_8, conv_22, 9)

            # resblock
            conv_23 = self.conv2d(resn_9, 23)
            conv_24 = self.conv2d(conv_23, 24)
            resn_10 = self.resnet(resn_9, conv_24, 10)

            # resblock
            conv_25 = self.conv2d(resn_10, 25)
            conv_26 = self.conv2d(conv_25, 26)
            resn_11 = self.resnet(resn_10, conv_26, 11)

            # Downsample#############################################
            conv_27 = self.conv2d(resn_11, 27, stride=2)

            # resblock
            conv_28 = self.conv2d(conv_27, 28)
            conv_29 = self.conv2d(conv_28, 29)
            resn_12 = self.resnet(conv_27, conv_29, 12)

            # resblock
            conv_30 = self.conv2d(resn_12, 30)
            conv_31 = self.conv2d(conv_30, 31)
            resn_13 = self.resnet(resn_12, conv_31, 13)

            # resblock
            conv_32 = self.conv2d(resn_13, 32)
            conv_33 = self.conv2d(conv_32, 33)
            resn_14 = self.resnet(resn_13, conv_33, 14)

            # resblock
            conv_34 = self.conv2d(resn_14, 34)
            conv_35 = self.conv2d(conv_34, 35)
            resn_15 = self.resnet(resn_14, conv_35, 15)

            # resblock
            conv_36 = self.conv2d(resn_15, 36)
            conv_37 = self.conv2d(conv_36, 37)
            resn_16 = self.resnet(resn_15, conv_37, 16)

            # resblock
            conv_38 = self.conv2d(resn_16, 38)
            conv_39 = self.conv2d(conv_38, 39)
            resn_17 = self.resnet(resn_16, conv_39, 17)

            # resblock
            conv_40 = self.conv2d(resn_17, 40)
            conv_41 = self.conv2d(conv_40, 41)
            resn_18 = self.resnet(resn_17, conv_41, 18)

            # resblock
            conv_42 = self.conv2d(resn_18, 42)
            conv_43 = self.conv2d(conv_42, 43)
            resn_19 = self.resnet(resn_18, conv_43, 19)

            # Downsample##############################################
            conv_44 = self.conv2d(resn_19, 44, stride=2)

            # resblock
            conv_45 = self.conv2d(conv_44, 45)
            conv_46 = self.conv2d(conv_45, 46)
            resn_20 = self.resnet(conv_44, conv_46, 20)

            # resblock
            conv_47 = self.conv2d(resn_20, 47)
            conv_48 = self.conv2d(conv_47, 48)
            resn_21 = self.resnet(resn_20, conv_48, 21)

            # resblock
            conv_49 = self.conv2d(resn_21, 49)
            conv_50 = self.conv2d(conv_49, 50)
            resn_22 = self.resnet(resn_21, conv_50, 22)

            # resblock
            conv_51 = self.conv2d(resn_22, 51)
            conv_52 = self.conv2d(conv_51, 52)
            resn_23 = self.resnet(resn_22, conv_52, 23)  # [None, 13,13,1024]

        #===========================================================================================
        with tf.name_scope('SCALE'):
            with tf.name_scope('scale_1'):
                conv_53 = self.conv2d(resn_23, 53)
                conv_54 = self.conv2d(conv_53, 54)
                conv_55 = self.conv2d(conv_54, 55)  # [None,14,14,512]
                conv_56 = self.conv2d(conv_55, 56)
                conv_57 = self.conv2d(conv_56, 57)
                conv_58 = self.conv2d(conv_57, 58)  # [None,13 ,13,1024]
                conv_59 = self.conv2d(conv_58, 59, batch_norm_and_activation=False, trainable=self.trainable)
                # [yolo layer] 6,7,8 # 82  --->predict    scale:1, stride:32, detecting large objects => mask: 6,7,8
                # 13x13x255, 255=3*(80+1+4)
            with tf.name_scope('scale_2'):
                route_1 = self.route1(conv_57, name="route_1")
                conv_60 = self.conv2d(route_1, 60)
                upsam_1 = self.upsample(conv_60, 2, name="upsample_1")
                route_2 = self.route2(upsam_1, resn_19, name="route_2")
                conv_61 = self.conv2d(route_2, 61)
                conv_62 = self.conv2d(conv_61, 62)
                conv_63 = self.conv2d(conv_62, 63)
                conv_64 = self.conv2d(conv_63, 64)
                conv_65 = self.conv2d(conv_64, 65)
                conv_66 = self.conv2d(conv_65, 66)
                conv_67 = self.conv2d(conv_66, 67, batch_norm_and_activation=False, trainable=self.trainable)
                # [yolo layer] 3,4,5 # 94  --->predict   scale:2, stride:16, detecting medium objects => mask: 3,4,5
                # 26x26x255, 255=3*(80+1+4)
            with tf.name_scope('scale_3'):
                route_3 = self.route1(conv_65, name="route_3")
                conv_68 = self.conv2d(route_3, 68)
                upsam_2 = self.upsample(conv_68, 2, name="upsample_2")
                route_4 = self.route2(upsam_2, resn_11, name="route_4")
                conv_69 = self.conv2d(route_4, 69)
                conv_70 = self.conv2d(conv_69, 70)
                conv_71 = self.conv2d(conv_70, 71)
                conv_72 = self.conv2d(conv_71, 72)
                conv_73 = self.conv2d(conv_72, 73)
                conv_74 = self.conv2d(conv_73, 74)
                conv_75 = self.conv2d(conv_74, 75, batch_norm_and_activation=False, trainable=self.trainable)
                # [yolo layer] 0,1,2 # 106 --predict scale:3, stride:8, detecting the smaller objects => mask: 0,1,2
                # 52x52x255, 255=3*(80+1+4)
                # Bounding Box:  YOLOv2: 13x13x5
                #                YOLOv3: 13x13x3x3, 3 for each scale

        return conv_59, conv_67, conv_75

    #===================================================================================================================
    def select_layer(self, section, proxy, inputs):
        """
        | section | str                       |
        | proxy   | configparser.SectionProxy |
        | inputs  | tf.Tensor                 |
        """
        section_name, order_idx = section.split("_")
        if section_name == "convolutional":
            #====================
            layer = self.conv2d(inputs         =inputs,
                                order_idx      =int(order_idx),
                                batch_normalize=int(proxy["batch_normalize"]),
                                filters        =int(proxy["filters"]),
                                kernel_size    =int(proxy["kernel_size"]),
                                stride         =int(proxy["stride"]),
                                pad            =int(proxy["pad"]),
                                activation     =int(proxy["activation"]),
                                fine_tuning    =self.trainable)
        elif section_name == "route":
            #====================
            proxy["layers"].split
            layers = [int(a) for a in layers]
            # "-1, 4"
            layers = list(map(int, config_parser_proxy["layers"].split(",")))
            assert 0 < len(layers) and len(layers) <= 2

            # 現在のindexからの「負の相対的な数値」で表す
            layers = list(map(check_positive, layer))
            def check_positive(a)
                return a - self.layer_idx if a > 0 else a

            with tf.name_scope(name=section):
                if len(layers) == 1:
                    # 値が1つのときはその値と一つ前のレイヤ
                    layer = self.layers_list[i + (layers[0])]
                else:
                    # 値が2つのときはそれらをchannel軸でconcatenate
                    in_idx1, in_idx2 = self.layer_idx + layers[0], self.layer_idx + layers[1]
                    layer = tf.concat(values=[self.layers_list[in_idx1], self.layers_list[in_idx2]],
                                       axis=-1, name='concatenate')
        elif section_name == "shortcut":
            #====================
            _input = self.layers_list[self.layer_idx-1]
            with tf.name_scope(section):
                # 同じサイズ同士のテンソルを足す
                _from = int(proxy["from"])
                _acti = proxy["activation"]
                assert _acti == "linear"
                layer = _input + self.layers_list[self.layer_idx-_from]
        elif section_name == "upsample":
            #====================
            _input = self.layers_list[self.layer_idx-1]
            with tf.name_scope(section):
                _, h, w, _ = tf.shape(_input)  # [batch, height, width, channels]
                _size = proxy["stride"]
                layer = tf.image.resize_images(images=_input, size=[_size * h, _size * w],  # [new_height, new_width]
                                               method=ResizeMethod.NEAREST_NEIGHBOR, align_corners=False)
        elif section_name == "yolo":
            #====================
            pass
        elif section_name == "net"
            #====================
            pass
        else:
            #====================
            raise ValueError('Unsupported section header type: {}'.format(section))

        return layer

    #===================================================================================================================
    def conv2d(self,
               inputs,
               order_idx,
               batch_normalize
               filters,
               kernel_size,
               stride,
               pad,
               activation,
               fine_tuning=False):
        """
        batch_normalize=1 True
        filters=32
        size=3 (kernel_size)
        stride=1 True
        pad=1 True
        activation=leaky

        Convolutional layer
        |-Parameters
        | inputs          | tf.Tensor | size = (batch, channel, height, width)
        | order_idx       | int       | conv layer's number
        | batch_normalize | int       | 0 or 1
        | filters         | int       |
        | kernel_size     | int       | [kernel_size, kernel_size]
        | stride          | int       |
        | pad             | int       | 0(False) or 1(True)
        | activation      | str       | "leaky", "linear"
        | fine_tuning     | bool      | default False
        |
        |-Returns
        """
        name_dict = {
            "conv"     : "conv_{}".format(order_idx),
            "weights"  : "weights_{}".format(order_idx),
            "biases"   : "biases_{}".format(order_idx),
            "mov_mean" : "moving_mean_{}".format(order_idx),
            "mov_vari" : "moving_variance_{}".format(order_idx),
            "beta"     : "beta_{}".format(order_idx),
            "gamma"    : "gamma_{}".format(order_idx),
        }
        with tf.variable_scope(name_dict["conv"]):
            #===============================================
            if trainable == True:
                # we will initialize weights by a Gaussian distribution with mean 0 and variance 1/sqrt(n)
                # don't set all = 0 or =
                if order_idx == 59:  # scale1
                    weights_shape = [1, 1, 1024, 3 * (self.NUM_CLASSES + 1 + 4)]
                elif order_idx == 67:  # scale2
                    weights_shape = [1, 1,  512, 3 * (self.NUM_CLASSES + 1 + 4)]
                else:  # scalse3
                    weights_shape = [1, 1,  256, 3 * (self.NUM_CLASSES + 1 + 4)]
                weights = tf.Variable(initial_value=tf.random_normal(shape=weights_shape, mean=0.0, stddev=0.01),
                                      trainable=True, dtype=tf.float32, name="weights")
                #weights = tf.Variable(
                #    initial_value=np.random.normal(loc=0.0, scale=0.01, size=weights_shape),
                #    trainable=True, dtype=np.float32, name="weights")
            else:
                weights = tf.Variable(initial_value=self.W(number_conv=order_idx, weight_h5_filepath=self.weight_h5_filepath),
                                      trainable=False, dtype=tf.float32, name="weights")
  
            tf.summary.histogram(name=name_dict["weights"], values=weights)

            #===============================================
            if stride == 2:
                # > Darknet uses left and top padding instead of 'same' mode
                # > https://github.com/qqwweee/keras-yolo3/blob/e6598d13c703029b2686bc2eb8d5c09badf42992/convert.py#L165-L167
                paddings = tf.constant([[0, 0], [1, 0], [1, 0], [0, 0]])
                inputs_pad = tf.pad(tensor=inputs, paddings=paddings, mode="CONSTANT")
                conv = tf.nn.conv2d(input=inputs_pad, filter=weights, strides=[1, stride, stride, 1], padding='VALID', name="conv")
            else:
                conv = tf.nn.conv2d(input=inputs, filter=weights, strides=[1, stride, stride, 1], padding='SAME', name="conv")

            if batch_norm_and_activation:  # TODO
                # conv_1 ---> conv_75 EXCEPT conv_59, conv_67, conv_75
                with tf.variable_scope("BatchNorm"):
                    variance_epsilon = tf.constant(0.0001, name="epsilon")  # small float number to avoid dividing by 0

                    # batch_mean, batch_var = tf.nn.moments(inputs, [0, 1, 2], name='moments')
                    # ema = tf.train.ExponentialMovingAverage(decay=0.5)
                    #
                    # def mean_var_with_update():
                    #     ema_apply_op = ema.apply([batch_mean, batch_var])
                    #     with tf.control_dependencies([ema_apply_op]):
                    #         return tf.identity(batch_mean), tf.identity(batch_var)
                    #
                    # mean, var = tf.cond(self.is_training,
                    #                     mean_var_with_update,
                    #                     lambda: (ema.average(batch_mean), ema.average(batch_var)))

                    moving_mean, moving_variance, beta, gamma = self.B(number_conv=order_idx, weight_h5_filepath=self.weight_h5_filepath)

                    moving_mean     = tf.Variable(initial_value=moving_mean,     trainable=False, dtype=tf.float32, name="moving_mean")
                    moving_variance = tf.Variable(initial_value=moving_variance, trainable=False, dtype=tf.float32, name="moving_variance")
                    beta            = tf.Variable(initial_value=beta,            trainable=False, dtype=tf.float32, name="beta")
                    gamma           = tf.Variable(initial_value=gamma,           trainable=False, dtype=tf.float32, name="gamma")

                    tf.summary.histogram(name=name_dict["mov_mean"], value=moving_mean)
                    tf.summary.histogram(name=name_dict["mov_vari"], value=moving_variance)
                    tf.summary.histogram(name=name_dict["beta"],     value=beta)
                    tf.summary.histogram(name=name_dict["gamma"],    value=gamma)

                    conv = tf.nn.batch_normalization(x=conv, mean=moving_mean, variance=moving_variance, offset=beta,
                                                     scale=gamma, variance_epsilon=variance_epsilon, name='BatchNorm')
                with tf.name_scope('Activation'):
                    # leaky relu : https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6
                    alpha = tf.constant(value=0.1, name="alpha")  # Slope of the activation function at x < 0
                    acti = tf.maximum(alpha * conv, conv)
                return acti

            else:
                # for conv_59, conv67, conv_75
                if trainable == True:
                    # biases may be  init =0
                    biases = tf.Variable(
                        np.random.normal(size=[3 * (self.NUM_CLASSES + 1 + 4), ], loc=0.0, scale=0.01),
                        trainable=True,
                        dtype=np.float32, name="biases")
                else:
                    biases = tf.Variable(initial_value=self.B(number_conv=order_idx, weight_h5_filepath=self.weight_h5_filepath),
                                         trainable=False, dtype=tf.float32, name="biases")
                tf.summary.histogram(name=name_dict["biases"], values=biases)  # add summary
                conv = tf.add(conv, biases)
                return conv

    @staticmethod
    def W(number_conv, weight_h5_filepath):
        # Charger weights from the pre-trained in COCO
        import h5py
        with h5py.File(name=weight_h5_filepath, mode="r") as f:
            name = 'conv2d_' + str(number_conv)
            w = f['model_weights'][name][name]['kernel:0']
            weights = tf.cast(w, tf.float32)
        return weights

    @staticmethod
    def B(number_conv, weight_h5_filepath):
        # Charger biases, bat_norm from the pre-trained in COCO
        import h5py
        with h5py.File(name=weight_h5_filepath, mode="r") as f:
            if (number_conv == 59) or (number_conv == 67) or (number_conv == 75):
                name = 'conv2d_' + str(number_conv)
                b = f['model_weights'][name][name]['bias:0']
                biases = tf.cast(b, tf.float32)
                return biases
            else:
                if 68 <= number_conv <= 74:
                    name = 'batch_normalization_' + str(number_conv-2)
                    if number_conv==74:
                        print("Finir de charger les poids!")
                elif 66 >= number_conv >= 60:
                    name = 'batch_normalization_' + str(number_conv - 1)
                elif 0 < number_conv <= 58:
                    name = 'batch_normalization_' + str(number_conv)
                beta = f['model_weights'][name][name]['beta:0']
                beta = tf.cast(beta, tf.float32)

                gamma = f['model_weights'][name][name]['gamma:0']
                gamma = tf.cast(gamma, tf.float32)

                moving_mean = f['model_weights'][name][name]['moving_mean:0']
                moving_mean = tf.cast(moving_mean, tf.float32)

                moving_variance = f['model_weights'][name][name]['moving_variance:0']
                moving_variance = tf.cast(moving_variance, tf.float32)

                return moving_mean, moving_variance, beta, gamma

    @staticmethod
    def route1(inputs, name):
        """
        :param inputs: [5, 500, 416, 3]
        :param name: name in graph
        :return: output = input [5, 500, 416, 3]
        """
        # [route]-4
        with tf.name_scope(name):
            output = inputs
            return output

    @staticmethod
    def route2(input1, input2, name):
        """
        :param input1: [5, 500, 416, 3]
        :param input2: [5, 500, 416, 32]
        :param name: name in graph
        :return: concatenate{input1, input2} [5, 500, 416, 3+32]
                 (nối lại)
        """
        # [route]-1, 36
        # [route]-1, 61
        with tf.name_scope(name):
            output = tf.concat([input1, input2], -1, name='concatenate')  # input1:-1, input2: 61
            return output

    @staticmethod
    def upsample(inputs, size, name):
        """
        :param inputs: (5, 416, 416, 3) par ex
        :param size: 2 par ex
        :param name: name in graph
        :return: Resize images to size using nearest neighbor interpolation. (5, 832, 832, 3) par ex
        """
        with tf.name_scope(name):
            w = tf.shape(inputs)[1]  # 416
            h = tf.shape(inputs)[2]  # 416
            output = tf.image.resize_nearest_neighbor(inputs, [size * w, size * h])
            return output

    @staticmethod
    def resnet(a, b, idx):
        """
        :param a: [5, 500, 416, 32]
        :param b: [5, 500, 416, 32]
        :param name: name in graph
        :return: a+b [5, 500, 416, 32]
        """
        name_res = 'resn' + str(idx)
        with tf.name_scope(name_res):
            resn = a + b
            return resn

    @staticmethod
    def yolo_predict():
        """
        | Parameters
        """
        name = "predict_
        with tf.name_scope(name):
            _boxes, _box_scores = yolo_boxes_and_scores(yolo_outputs[mask],
                                                        anchors[anchor_mask[mask]],
                                                        num_classes,
                                                        input_shape,
                                                        image_shape)

            boxes.append(_boxes)  # list(3 array): [3, None*13*13*3, 4]
            box_scores.append(_box_scores)  # list(3 array): [3, None*13*13*3, 80]
