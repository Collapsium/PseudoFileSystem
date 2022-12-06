import textwrap
import itertools

class Node:
    id = itertools.count()

    def __init__(self, value, child = None, isDirectory = 0):
        self.value = value
        self.child = child or [] #Nodo inicializado con arreglo de hijos
        self.isDirectory = isDirectory # 1 si es directory
        self.id = next(self.id)
class Arbol:

    def __init__(self):
        self.root = Node("root", None, 1)
        self.pwd = ["root"]

    def findNode(self, node, key) -> Node : 
        if node == None or node.value == key:
            return node
        for child in node.child:
            return_node = self.findNode(child,key)
            if return_node:
                return return_node
        return None

       
    def touch(self, key): #crea archivo en el wd
        new_node = Node(key)
        wd_node =  self.findNode(self.root, self.pwd[-1])
        #print(wd_node.value)
        wd_node.child.append(new_node) #Accedo al nodo, y le agrego un hijo
        print(f"Creado el nodo plano con valor: {new_node.value}")
        print(f'{new_node.id}')
        return new_node

    def mkdir(self,key): #crea directorio en el wd
        new_node = Node(key, None, 1)
        wd_node =  self.findNode(self.root, self.pwd[-1])
        #print(wd_node.value)
        wd_node.child.append(new_node) #Accedo al nodo, y le agrego un hijo
        print(f"Creado el nodo directorio con valor: {new_node.value}")
        return new_node 

    def ls(self):
        wd_val = self.findNode(self.root, self.pwd[-1])
        files = ""
        for x in wd_val.child:
            files = files + " " + x.value 
        return files

    def lsi(self):
        wd_val = self.findNode(self.root, self.pwd[-1])
        files = ""
        for x in wd_val.child:
            id = str(x.id)
            files =  files + "  " + id + " " + x.value 
        return files

    def lsr(self):
        wd_node = self.findNode(self.root, self.pwd[-1])
 
        files = ""
        for x in wd_node.child:
             files = x.value  + "  " + files
        return files

    def rename(self, old_key, new_key):
        wd_node = self.findNode(self.root, self.pwd[-1])
        for x in wd_node.child:
            if( x.value == old_key ):
                x.value = new_key
                return f"{old_key} Cambiado a {x.value}"
        return None

    def remove(self, key): 
        wd_node = self.findNode(self.root, self.pwd[-1])

        for x in wd_node.child:
            if(x.value == key):
                if(x.isDirectory == 1 and wd_node.child != None):
                    print("Solo se pueden eliminar carpetas vacias")
                    return None
                
                if(x.isDirectory == 1):
                    wd_node.child.remove(x)
                    x.value = None
                    return print("Carpeta eliminada")
                
                if(x.isDirectory == 0):
                    x.value = None
                    wd_node.child.remove(x)
                    return print("Archivo eliminado")
        return print("No se encuentra el archivo en el directorio")

    def move(self,key, parent_key): #nodo a mover, carpeta de destino
        #addfile: (hijo, nuevo padre)
        #borrar enlace padre con el hijo a mover
        if(key == None):
            return None
        wd_node = self.findNode(self.root, self.pwd[-1])
        new_father = self.findNode(self.root, parent_key)
        son = self.findNode(self.root, key)
        
        if(new_father.isDirectory != 1):
            print("No se puede mover a la ubicacion especificada.")
            return None
        
        new_father.child.append(son)
        wd_node.child.remove(son)
        return print(f'{son.value} movido a carpeta {new_father.value}')
       
    def cd(self, key):
        wd_node = self.findNode(self.root, self.pwd[-1])
        node_key = self.findNode(self.root, key)

        if(node_key.isDirectory == 0):
            return print("Comando solo funciona sobre carpetas")
        for x in wd_node.child:
            if(x.value == key):
                self.pwd.append(key)
                return self.printPwd()
        return print("Está mal escrito")

    def cdDotDot(self):
        self.pwd.pop()
        return self.printPwd()

    def preorder(self, root: 'Node', ans: list = None):
        if not root: return ans
        if ans == None: ans = []
        ans.append(root.value)
        for child in root.child:
            self.preorder(child, ans)
        return ans
        
    def printPwd(self):
        l = ""
        for x in self.pwd:
           l = l + f'/{x}'
        return l 

arbol = Arbol()

# arbol.touch("sex.txt")
# arbol.mkdir("sex, la carpeta")
# arbol.ls()
# arbol.rename("sex.txt", "amongus.sex")
# arbol.move("amongus.sex", "sex, la carpeta")
# arbol.remove("amongus.sex")#print(arbol.remove("amongus.sex")
# arbol.touch("amongus2.sex")
# arbol.remove("amongus2.sex")
# arbol.pwd()
# arbol.mkdir("amongus3.carpeta")
# arbol.cd("amongus3.carpeta")
# arbol.cdDotDot()


help = textwrap.dedent(""" 

    Lista de comandos:

    touch <<nombre_archivo>> : crea archivo dentro del working directory
    mkdir <<nombre_archivo>> : crea carpeta dentro del working directory
    ls: lista de archivos dentro del working directory
    ls -i : lista de archivos con identificador de nodo
    ls -R : lista invertida de archivos
    rename <<nombre_archivo>> : Renombra archivo (Dentro del working directory)
    remove <<nombre_archivo>> : Elimina archivo (Dentro del working directory)
    pwd : imprime working directory
    cd <<nombre_archivo>> : dirige working directory al archivo seleccionado
    cd.. : dirige working directory un directorio anterior
    exit: sale de la pestaña de comandos
    """)

print("Presiona h para acceder a la lista de comandos ")

while True:
    print(arbol.printPwd(), end=" ")

    input_value = input()

    inputs = input_value.split(' ')

    if(inputs[0] == "exit"):
        break

  
    
    if len(inputs) == 3:
        try:
            funcion = getattr(arbol, inputs[0])(inputs[1], inputs[2])
            continue
        except:
            print("Comando no valido")
            continue
    if len(inputs) == 2 :

        if(inputs[0] == "ls" and inputs[1] == "-i"):
            print(arbol.lsi())
            continue
        if(inputs[0] == "ls" and inputs[1] == "-R"):
            print(arbol.lsr())
            continue
        try:
            funcion = getattr(arbol, inputs[0])(inputs[1])
            continue
        except:
            print("Comando no valido")
            continue

    if len(inputs) == 1 :

        if(inputs[0] == "h"):
            print(help)
            continue
        if(inputs[0] == "ls"):
            print(arbol.ls())
            continue
        if(inputs[0] == "pwd"):
            print(arbol.printPwd())
            continue
        if(inputs[0] == "cd.."):
            arbol.cdDotDot()
            continue

        try:
            funcion = getattr(arbol, inputs[0])()
            continue
        except:
            print("Commando no valido")
            continue

    print("comando no valido")
