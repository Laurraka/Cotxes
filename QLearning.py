from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense
import random
import numpy as np
import collections

from joc import *

class QAgent:
    def __init__(self, params):
        self.reward = 0  # recompensa
        self.gamma = 0.9  # parametro de confianza
        self.short_memory = np.array([])  # memoria de estados a corto plazo
        self.agent_target = 1  # inicializacion del target
        self.agent_predict = 0  # inicializacion de las predicciones
        self.learning_rate = params['learning_rate']  # tasa de aprendizaje de la red
        self.epsilon = 1  # parametro que controla la aleatoriedad de las acciones
        self.first_layer = params['first_layer_size']  # neuronas 1ra capa oculta
        self.second_layer = params['second_layer_size']  # neuronas 2ra capa oculta
        self.memory = collections.deque(maxlen=params['memory_size'])  # para guardar estados y acciones en memoria
        self.weights = params['weights_path']  # pesos de la red
        self.load_weights = params['load_weights']  # para cargar red pre-entrenada
        self.model = self.network()  # iniciamos el modelo

    def network(self):
        model = Sequential()
        model.add(Dense(activation="relu", input_dim=15, units=self.first_layer))
        model.add(Dense(activation="relu", units=self.second_layer))
        model.add(Dense(activation="softmax", units=3))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if self.load_weights:
            model.load_weights(self.weights)
        return model

    def get_state(self, joc, car):
        state = []

        p=WPoint(car.x+car.w/2, car.y+car.h/2) #Centre del cotxe obstacle

        p1=WPoint(rotar_respecte_x0_y0(car.x,car.y+car.h/2, car.angle, car.x+car.w/2, car.y+car.h/2)[0],
                  rotar_respecte_x0_y0(car.x,car.y+car.h/2, car.angle, car.x+car.w/2, car.y+car.h/2)[1])
        
        p2=WPoint(rotar_respecte_x0_y0(car.x, car.y, car.angle, car.x+car.w/2, car.y+car.h/2)[0],
                  rotar_respecte_x0_y0(car.x, car.y, car.angle, car.x+car.w/2, car.y+car.h/2)[1])
        
        p3=WPoint(rotar_respecte_x0_y0(car.x+car.w/2, car.y, car.angle, car.x+car.w/2, car.y+car.h/2)[0],
                  rotar_respecte_x0_y0(car.x+car.w/2, car.y, car.angle, car.x+car.w/2, car.y+car.h/2)[1])
        
        p4=WPoint(rotar_respecte_x0_y0(car.x+car.w, car.y, car.angle, car.x+car.w/2, car.y+car.h/2)[0],
                  rotar_respecte_x0_y0(car.x+car.w, car.y, car.angle, car.x+car.w/2, car.y+car.h/2)[1])
        
        L1=LinearEquation(p, p1)

        return np.array(state)
    
    