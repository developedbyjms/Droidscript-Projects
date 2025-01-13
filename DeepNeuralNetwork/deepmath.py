from native import app
import random, math, json

def sigmoid(data_x):
    if typeOf(data_x)==0: #Array
       return list(map(lambda x: 1/(1+math.exp(-x)), data_x))
    elif typeOf(data_x)==1: #Matrix
       result = []
       for rows in data_x:
           result.append(list(map(lambda x: 1/(1+math.exp(-x)), rows)))
       return result
    else: return "<the object> must be an array or matrix"
    
def dsigmoid(data_x):
    if typeOf(data_x)==0: #Array
       return list(map(lambda x: x*(1-x), data_x))
    elif typeOf(data_x)==1: #Matrix
       result = []
       for rows in data_x:
           result.append(list(map(lambda x: x*(1-x), rows)))
       return result
    else: return "<the object> must be an array or matrix"



def add(m1, m2):
    # Escalar addition: Matrix + Number
    if typeOf(m1)==1 and (typeOf(m2)==2 or typeOf(m2)==3 or typeOf(m2)==4):
       matrix = zeros(len(m1), len(m1[0]))
       for rows in range(len(m1)):
           for cols in range(len(m1[0])):
               matrix[rows][cols] = m1[rows][cols] + m2
       return matrix
    # Escalar addition: Number + Matrix
    elif typeOf(m2)==1 and (typeOf(m1)==2 or typeOf(m1)==3 or typeOf(m1)==4):
       matrix = zeros(len(m2), len(m2[0]))
       for rows in range(len(m2)):
           for cols in range(len(m2[0])):
               matrix[rows][cols] = m1 + m2[rows][cols]
       return matrix
    # Escalar addition: Array + Number
    elif typeOf(m1)==0 and (typeOf(m2)==2 or typeOf(m2)==3 or typeOf(m2)==4):
         added = zeros(len([m1]), len([m1][0]))
         for rows in range(len([m1])):
             for cols in range(len([m1][0])):
                 added[rows][cols] = [m1][rows][cols] + m2
         return from_matrix(added)
         #return added
    # Escalar addition: Number + Array
    elif typeOf(m2)==0 and (typeOf(m1)==2 or typeOf(m1)==3 or typeOf(m1)==4):
         added = zeroz(len([m2]), len([m2][0]))
         for rows in range(len([m2])):
             for cols in range(len([m2][0])):
                 added[rows][cols] = [m2][rows][cols] + m1
         return from_matrix(added)
         #return added
    # Array + Array
    elif typeOf(m1)==0 and typeOf(m2)==0: #It's an array
         added = zeros(len([m1]), len([m1][0]))
         for rows in range(len([m1])):
             for cols in range(len([m1][0])):
                 added[rows][cols] = [m1][rows][cols] + [m2][rows][cols]
         return from_matrix(added)
         #return added
    # The real addition of two matrix: Matrix + Matrix
    elif typeOf(m1)==1 and typeOf(m2)==1: # Matrix + Matrix
         if len(m1)!=len(m2) and len(m1[0])!=len(m2[0]): return []
         matrix = zeros(len(m1), len(m2[0]))
         for rows in range(len(m1)):
             for cols in range(len(m2[0])):
                 matrix[rows][cols] = m1[rows][cols] + m2[rows][cols]
         return matrix
    else: return []
    
def array(nelements):
    return [0]*nelements

def transpose(matrix):
    """Transpose a matrix, turn rows into cols."""
    if typeOf(matrix)==1:
       transposed = zeros(len(matrix[0]), len(matrix))
       for rows in range(len(matrix)):
           for cols in range(len(matrix[0])):
               transposed[cols][rows] = matrix[rows][cols]
       return transposed
    elif typeOf(matrix)==0:
         return [matrix]
    return "The <object> isn't an array or a matrix"
    
def oppose(matrix):
    """Oppose a matrix value, turn all positive values into negate and vice verse."""
    matrix_type = typeOf(matrix)
    try:
       if matrix_type==1:
          opposed = zeros(len(matrix), len(matrix[0]))
          for rows in range(len(matrix)):
              for cols in range(len(matrix[0])):
                  opposed[rows][cols] = -matrix[rows][cols]
          return opposed
       else:
           opposed = zeros(len([matrix]), len([matrix][0]))
           for rows in range(len([matrix])):
               for cols in range(len([matrix][0])):
                   opposed[rows][cols] = -[matrix][rows][cols]
           return fromMatrix(opposed)
    except Exception as error:
          return "The <object> isn't an array or a matrix"
          
def typeOf(obj):
    """Verify if obj is an array, a matrix, a number, or a string."""
    try:
        n_cols = len(obj[0]) # Try take the number of cols of the obj
        if type(obj)==str: return 5 # If the obj is a string
        else: return 1 # If the obj is a Matrix
    except Exception as error:
        if type(obj)==list: return 0 # If the obj is an array
        elif type(obj)==int: return 2 # If the obj is an Integer number
        #elif type(obj)==long: return 3 # If the obj is a long number
        elif type(obj)==float: return 4 # If the obj is a float number
        else: return -1 # If the obj is an Float number
               
def from_matrix(matrix):
    """Turn a matrix into an Array."""
    if typeOf(matrix) != 1: return "The <object> isn't a matrix"
    array = []
    for rows in range(len(matrix)):
        for cols in range(len(matrix[0])):
            array.append(matrix[rows][cols])
    return array

def from_array(array):
    """Turn an array into a matrix."""
    if typeOf(array) != 0: return "The <object> isn't an array"
    matrix = zeros(len([array][0]), len([array]))
    for rows in range(len([array])):
        for cols in range(len([array][0])):
            matrix[cols][rows] = [array][rows][cols]
    return matrix
                      
def show(matrix):
    """Print a matrix with '|' as bracket."""
    if typeOf(matrix) == 1:
       for rows in matrix:
           m = str(rows).replace("[","|")
           m = m.replace("]","|")
           print(m)
       print("\n")
       
def zeros(nrows, ncols):
    matrix = []
    for rows in range(nrows):
        newline = [0]*ncols
        matrix.append(newline)
    return matrix
    

def hadamard_product(m1, m2):
    if typeOf(m1)==0 and typeOf(m2)==0: #Array
       if len(m1)==len(m2):
          hadamardArray = array(len(m1))
          for i in range(len(m1)):
              hadamardArray[i] = m1[i] * m2[i]
          return hadamardArray
       return []
           
    elif typeOf(m1)==1 and typeOf(m2)==1: #Matrix
         if len(m1)==len(m2) and len(m1[0])==len(m2[0]):
            hadamardMatrix = zeros(len(m1), len(m1[0]))
            for rows in range(len(m1)):
                for cols in range(len(m1[0])):
                    hadamardMatrix[rows][cols] = m1[rows][cols] * m2[rows][cols]
            return hadamardMatrix
         return []
    else: return []
    
def multiply(m1, m2):
    # Escalar multiplication: Matrix * Number
    if typeOf(m1)==1 and (typeOf(m2)==2 or typeOf(m2)==3 or typeOf(m2)==4):
       matrix = zeros(len(m1), len(m1[0]))
       for rows in range(len(m1)):
           for cols in range(len(m1[0])):
               matrix[rows][cols] = m1[rows][cols] * m2
       return matrix
    # Escalar multiplication: Number * Matrix
    elif typeOf(m2)==1 and (typeOf(m1)==2 or typeOf(m1)==3 or typeOf(m1)==4):
       matrix = zeros(len(m2), len(m2[0]))
       for rows in range(len(m2)):
           for cols in range(len(m2[0])):
               matrix[rows][cols] = m1 * m2[rows][cols]
       return matrix
    
    # The real multiplication
    elif typeOf(m1)==1 and typeOf(m2)==1: # Matrix * Matrix
         if len(m1[0]) != len(m2): return "number of cols <matrix1> must be equal to number of rows of <matrix2>"
         multiplied = zeros(len(m1), len(m2[0]))
         for rows in range(len(m1)):
             for cols in range(len(m2[0])):
               for i in range(len(m1[0])):
                   multiplied[rows][cols] += m1[rows][i] * m2[i][cols]
         return multiplied
    else: return []

   
def subtract(m1, m2):
    """Subtract two matrix."""
    if typeOf(m1)==1 and typeOf(m2)==1: #Matrix - Matrix
       return add(m1, oppose(m2))
    elif typeOf(m1)==0 and typeOf(m2)==0: #Array - Array
         return add(m1, oppose(m2))
    return "The <object> isn't an array or a matrix"



def random_matrix(nrows, ncols):
    result = []
    for rows in range(nrows):
        line = [random.random()]*ncols
        result.append(line)
    return result

def fromReadFile(content):
       # Remover os colchetes externos e separar os elementos manualmente
       content = content.strip()  # Remove espaços em branco extras
       content = content[1:-1]  # Remove os colchetes externos: [[0, 1], [3, 4]] -> [0, 1], [3, 4]
       # Transformar o conteúdo em uma lista de listas
       data_list = []
       for item in content.split('],'):  # Dividir pelos colchetes das listas internas
            item = item.replace('[', '').replace(']', '').strip()  # Remove os colchetes restantes
            inner_list = [int(x) for x in item.split(',')]  # Converte os elementos para inteiros
            data_list.append(inner_list)
       return data_list
      
 
def verificarTipo(x):
    if isinstance(x, list):
        if all(isinstance(i, list) for i in x):  # Verifica se todos os elementos são listas
            return "matriz"
        return "array"
    elif isinstance(x, str):
        return "string"
    elif isinstance(x, (int, float, complex)):
        return "número"
    else:
        return "tipo desconhecido"
        
def extrairSufixo(lista, startwth):
    resultado = []
    for elemento in lista:
        if elemento.startswith(startwth) and "_" in elemento:
            prefixo, sufixo = elemento.split("_", 1)
            resultado.append([prefixo, sufixo])
    return resultado

def loadModel(data):
       try:
          r = json.loads(str(data))
          return [ r["dataset"], r["modelName"], r["weights"], r["biases"], r["hidden"] ]
       except Exception as e:
              return False
              
def doesFileExist(path):
       exists = app.FileExists( path )
       if exists == True: return True
       else: return False
       
def is_array(obj):
    try:
        obj[0]  # Testa indexação
        iter(obj)  # Testa se é iterável
        return True
    except (TypeError, IndexError):
        return False 
       
def is_matrix(x):
        try:
             x[0][0]
             return is_array(x)
        except Exception as error:
                      return error
  
def feedforward(weights, inputs, biases):
    return sigmoid(add(multiply(weights, inputs), biases))


def output_error(targets, outputs):
    return subtract(targets, outputs)

def hidden_error(forward_weights, forward_error):
    return multiply(transpose(forward_weights), forward_error)


def graddient(error, result, learning_rate):
    return multiply(hadamard_product(error, dsigmoid(result)), 	learning_rate)

def delta_weights(graddient, inputs):
    return multiply(graddient, transpose(inputs))

def adjust_weights(old_weights, delta_weights):
    return add(old_weights, delta_weights)
    