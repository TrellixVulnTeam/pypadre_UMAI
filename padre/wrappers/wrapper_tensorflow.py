import torch
import copy
import numpy as np
import json
import importlib
import os
import random

class WrapperTensorFlow:
    """
    This class wraps the whole Tensorflow network and exposes an easy to use interface to the user
    """

    network = None

    def __init__(self, params:dict):
        """
        Function for initializing the wrapper, creating the network and setting all the necessary parameters

        :param params: Parameters of the network, shape of the network
        """

        with open('mappings_tensorflow.json') as f:
            framework_dict = json.load(f)

        self.layers_dict = framework_dict.get('layers', None)

        if self.layers_dict is None:
            return

        self.params = copy.deepcopy(params)
        self.steps = params.get('steps', 1000)
        self.checkpoint = params.get('checkpoint', self.steps)
        self.batch_size = params.get('batch_size', 1)
        self.resume = params.get('resume', False)
        self.pre_trained_model_path = params.get('model', None)
        self.model_prefix = params.get('model_prefix', "")

        architecture = params.get('architecture', None)
        layer_order = params.get('layer_order', None)
        shape = self.create_network_shape(architecture=architecture, layer_order=layer_order)

        if shape is None:
            return

        self.model = shape

    def create_network_shape(self, architecture=None, layer_order=None):
        """
        This function creates the network from the architecture specified in the config file

        :param architecture: The shape of the network
        :param layer_order: The ordering of the layers

        :return: The network object if the function succeeded else None
        """

        if architecture is None or layer_order is None:
            return None

        layers = []

        for layer_name in layer_order:

            layer = architecture.get(layer_name, None)
            if layer is None:
                return None

            layer_type = layer.get('type')
            params = layer.get('params')

            layer_obj = self.create_layer_object(layer_type, params)

            if layer_obj is not None:
                layers.append(layer_obj)

            else:
                layers = None
                break

        return layers

    def create_layer_object(self, layer_type=None, layer_params=None):
        """
        The function creates a layer object from the type and the params
        Reference: https://pytorch.org/docs/stable/nn.html

        :param layer_type:
        :param layer_params:

        :return: A layer object
        """

        if layer_type is None:
            return None

        layer_type = str(layer_type).upper()

        if layer_params is None:
            layer_params = dict()

        # Verify params for the module
        layer = self.layers_dict.get(layer_type, None)

        if layer is None:
            return None

        path = layer.get('path', None)

        if path is None:
            return None

        # Some layers have no parameters while some layers might have not defined any parameters.
        # The latter case is an error and the string is used to distinguish between both cases.
        params = layer.get('params', "PARAMSNOTDEFINED")
        if params == 'PARAMSNOTDEFINED':
            return None

        curr_params = dict()
        for param in params:
            param_value = layer_params.get(param, None)
            print(param)
            if param_value is None and params.get(param).get('optional') is False:
                curr_params = None
                break

            else:
                if param_value is not None:
                    curr_params[param] = param_value

        obj = None
        if curr_params is not None:
            split_idx = path.rfind('.')
            import_path = path[:split_idx]
            class_name = path[split_idx + 1:]
            module = importlib.import_module(import_path)
            class_ = getattr(module, class_name)
            obj = class_(**curr_params)

        return copy.deepcopy(obj)

    def create_loss_function(self, name, params):
        """
        Function to create the loss function and set all the corresponding params in a dictionary

        :param params: Parameters of the loss function

        :return: The loss function and a dictionary containing all the required parameters
        """

        if params is None:
            params = dict()

        loss = None

        name = str(name).upper()

        loss_function_details = self.loss_dict.get(name, None)

        if loss_function_details is not None:
            path = loss_function_details.get('path', None)

            if path is not None:

                curr_params = dict()

                loss_params= loss_function_details.get('params', None)
                if loss_params is None:
                    loss_params = dict()

                for param in loss_params:
                    # Get the corresponding parameter value from the input param list

                    param_value = params.get(param, None)

                    if param_value is None and loss_params.get(param).get('optional') is False:
                        curr_params = None
                        break

                    else:
                        if param_value is not None:
                            curr_params[param] = param_value

                split_idx = path.rfind('.')
                import_path = path[:split_idx]
                class_name = path[split_idx + 1:]
                module = importlib.import_module(import_path)
                loss = getattr(module, class_name)

                if curr_params is None:
                    curr_params = dict()

        return copy.deepcopy(loss), copy.deepcopy(curr_params)