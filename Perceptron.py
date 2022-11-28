import numpy as np
import random

class Perceptron():
    digit_codes = {
        0x0: [1,1,1,1,-1,1,1,1],         # 0  first element = constant bias input
        0x1: [1,-1,-1,1,-1,-1,1,-1],     # 1
        0x2: [1,1,-1,1,1,1,-1,1],        # 2
        0x3: [1,1,-1,1,1,-1,1,1],        # 3
        0x4: [1,-1,1,1,1,-1,1,-1],       # 4
        0x5: [1,1,1,-1,1,-1,1,1],        # 5
        0x6: [1,1,1,-1,1,1,1,1],         # 6
        0x7: [1,1,-1,1,-1,-1,1,-1],      # 7
        0x8: [1,1,1,1,1,1,1,1],          # 8 
        0x9: [1,1,1,1,1,-1,1,1],         # 9
        # 0xA: [1,1,1,1,1,1,1,-1],         # A
        # 0xB: [1,-1,1,-1,1,1,1,1],        # B
        # 0xC: [1,-1,-1,1,1,1,-1,1],       # C
        # 0xD: [1,-1,-1,1,1,1,1,1],        # D
        # 0xE: [1,1,1,-1,1,1,-1,1],        # E
        # 0xF: [1,1,1,-1,1,1,-1,-1]        # F
    }      

    a_learning_rate = 0.05
    number_of_features = 8
    w_weights = np.random.randint(np.arange(0, number_of_features), number_of_features)/10
    weigths_are_correct = False

    def get_train_sample(self):
        rand_int = random.randrange(0,8,1)
        tq_target_value = -1 if rand_int % 2 else 1
        x_input = np.asarray(self.digit_codes[rand_int])
        return x_input, tq_target_value


    def sign_fct(self, inputs):
        weighted_sum = np.dot(inputs, self.w_weights)
        return 1 if weighted_sum > 0 else -1


    def adapt_weights(self, x_input, tq_target, pred_output):
        deltaW_weight_change = 0.5 * (tq_target - pred_output) * x_input
        self.w_weights = self.w_weights + self.a_learning_rate * deltaW_weight_change
        print(self.w_weights)

    def are_weights_correct(self):
        for digit, input in self.digit_codes.items():
            tq_target_value = -1 if digit % 2 else 1
            y_pred_output = self.sign_fct(input)
            if tq_target_value != y_pred_output:
                self.adapt_weights(np.asarray(input), tq_target_value, y_pred_output)
                return False
        print("Correct weights were found: ", self.w_weights)
        return True

    def learn(self):
        iteration = 0
        while not self.weigths_are_correct:
            iteration += 1
            print("iteration: ", iteration)
            x_input, tq_target_value = self.get_train_sample()
            y_pred_output = self.sign_fct(x_input)
            if y_pred_output != tq_target_value:
                self.adapt_weights(x_input, tq_target_value, y_pred_output)
            else:
                self.weigths_are_correct = self.are_weights_correct()

if __name__ == "__main__":
    perceptron = Perceptron()
    perceptron.learn()
    print("Done!")