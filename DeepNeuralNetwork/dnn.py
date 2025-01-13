from native import app
import deepmath as dm
import random as rm, ast

class DeepNeuralNetwork:
      def __init__(self, model_name = "xor"):
          #Orginize model name
          self.path = "/sdcard/aidata/"+model_name
          self.model_name = model_name
          self.dataset = ast.literal_eval(  app.ReadFile( self.path+"/dataset.json")   )
          
          self.layers = [len(self.dataset[0][0])]
          self.input_nodes = [len(self.dataset[0][0])]
          self.hidden_nodes = ast.literal_eval(  app.ReadFile( self.path+"/hidden.json") )
          self.output_nodes = [len(self.dataset[0][1])]
          for n in  ast.literal_eval(  app.ReadFile( self.path+"/hidden.json") ):
                self.layers.append(n)
          self.layers.append(len(self.dataset[0][1]))
          
          try:
               weights = ast.literal_eval(  app.ReadFile( self.path+"/weights.txt")   )
               biases = ast.literal_eval(  app.ReadFile( self.path+"/biases.txt")   )
          except Exception as error:
                        weights = []; biases = []
          
          if weights==[] or biases==[] or dm.doesFileExist(self.path+"/weights.txt") == False or dm.doesFileExist(self.path+"/biases.txt") == False or dm.doesFileExist(self.path+"/hidden.json") == False or  dm.doesFileExist(self.path+"/dataset.json") == False or dm.doesFileExist(self.path+"/epoch.json") == False:                                   
              self.weights = []; self.biases = []
              for i in range(len(self.layers)-1):
                    self.weights.append(dm.random_matrix(self.layers[i+1], self.layers[i]))
                    self.biases.append(dm.random_matrix(self.layers[i+1], 1))
                    #app.ShowPopup( "Foram inicializados novos pesos" )
          else:
                  self.weights = weights
                  self.biases = biases
                  #app.ShowPopup( "Foram inicializados pesos do arquivo" )
               
             
      def feedforward(self, inputs):
             try:
                results = [dm.feedforward(self.weights[0], dm.from_array(inputs), self.biases[0])]
                for i in range(len(self.layers)-2):
                      results.append(dm.feedforward(self.weights[i+1], results[i], self.biases[i+1]))
                return results[len(results)-1]
             except:
                       return []

      def backPropagation(self, inputs, targets, learning_rate = 0.10):
                 #FeedForward
                 results = [dm.feedforward(self.weights[0], dm.from_array(inputs), self.biases[0])]
                 for i in range(len(self.layers)-2):
                       results.append(dm.feedforward(self.weights[i+1], results[i], self.biases[i+1]))
                 #Errors
                 errors = [dm.output_error(dm.from_array(targets), results[len(results)-1])]
                 for i in range(len(results)-1):
                       errors.append(dm.hidden_error(self.weights[len(self.weights)-1-i], errors[i]))
                 #Graddients
                 graddients = []
                 for i in range(len(results)):
                       graddients.append(dm.graddient(errors[i], results[len(results)-1-i], learning_rate))
                 #DeltaWeights
                 delta_weights = []
                 for i in range(len(self.weights)-1):
                      delta_weights.append(dm.delta_weights(graddients[i], results[len(results)-2-i]))
                 delta_weights.append(dm.delta_weights(graddients[len(graddients)-1], dm.from_array(inputs)))
                 #AdjustWeights
                 for i in range(len(self.weights)):
                       self.weights[len(self.weights)-1-i] = dm.adjust_weights(self.weights[len(self.weights)-1-i], delta_weights[i])
                 return [results[len(results)-1], results, errors[0], errors, graddients, delta_weights, self.weights, self.biases]
      

"""
    Coded-by: Jose Sixpenze
    E-mail  : josesixpenze@yahoo.com
    Github  : CODEDBYBYJMSIXPENZE
"""