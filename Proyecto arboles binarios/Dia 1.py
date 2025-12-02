import json
import os


class Node:
    def __init__(self, node_id, name, tipo, content=None):
        self.id = node_id           # identificador unico
        self.name = name            # nombre del nodo
        self.tipo = tipo            # carpeta / archivo
        self.content = content      # solo para archivo
        self.children = []          # lista de hijos

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tipo": self.tipo,
            "content": self.content,
            "children": [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data):
        node = Node(data["id"], data["name"], data["tipo"], data["content"])
        node.children = [Node.from_dict(c) for c in data["children"]]
        return node


class FileTree:
    def __init__(self):
        self.root = Node("0", "root", "carpeta")
        self.map = {"0": self.root}  # hash map para búsqueda rápida


    def buscar_por_ruta(self, ruta):
        partes = [p for p in ruta.split("/") if p]

        # si la ruta es solo "/", devuelve root
        if len(partes) == 0:
            return self.root

        actual = self.root

        for p in partes[1:]:  # partes[0] es "root"
            encontrado = None
            for hijo in actual.children:
                if hijo.name == p:
                    encontrado = hijo
                    break
            if not encontrado:
                return None
            actual = encontrado

        return actual


    def insertar(self, ruta_padre, nombre, tipo, contenido=None):
        padre = self.buscar_por_ruta(ruta_padre)
        if padre is None:
            print("Ruta no encontrada:", ruta_padre)
            return

        nuevo_id = str(len(self.map))
        nuevo = Node(nuevo_id, nombre, tipo, contenido)

        padre.children.append(nuevo)
        self.map[nuevo_id] = nuevo
        print(f"Nodo '{nombre}' creado en {ruta_padre}")

    def listar_hijos(self, ruta):
        nodo = self.buscar_por_ruta(ruta)
        if nodo is None:
            print("Ruta no encontrada:", ruta)
            return
        print(f"Hijos de {ruta}:")
        for h in nodo.children:
            print(f"- ({h.tipo}) {h.name}")


    def obtener_ruta_id(self, node_id):
        if node_id not in self.map:
            return None

        nodo = self.map[node_id]

        def buscar_padre(actual, target):
            if actual == target:
                return []
            for hijo in actual.children:
                if hijo == target:
                    return [actual]
                resto = buscar_padre(hijo, target)
                if resto is not None:
                    return [actual] + resto
            return None

        ruta = buscar_padre(self.root, nodo)
        if ruta is None:
            return "/root"

        nombres = [n.name for n in ruta] + [nodo.name]
        return "/" + "/".join(nombres)


    # Guardar árbol en JSON
    def guardar(self, archivo="tree.json"):
        data = self.root.to_dict()
        with open(archivo, "w") as f:
            json.dump(data, f, indent=4)
        print("Árbol guardado en", archivo)

    # Cargar árbol desde JSON
    def cargar(self, archivo="tree.json"):
        if not os.path.exists(archivo):
            print("No existe el archivo, se crea árbol nuevo.")
            return

        with open(archivo, "r") as f:
            data = json.load(f)

        self.root = Node.from_dict(data)

        # reconstruir hash map
        self.map = {}

        def registrar(nodo):
            self.map[nodo.id] = nodo
            for c in nodo.children:
                registrar(c)

        registrar(self.root)
        print("Árbol cargado desde", archivo)


def menu():
    tree = FileTree()
    tree.cargar()

    while True:
        print("\n=== MENU ===")
        print("1. Crear carpeta (mkdir)")
        print("2. Crear archivo (touch)")
        print("3. Listar hijos (ls)")
        print("4. Obtener ruta completa de un nodo (pwd)")
        print("5. Guardar")
        print("6. Cargar")
        print("7. Salir")

        op = input("Opc: ")

        if op == "1":
            ruta = input("Ruta padre ej:/root : ")
            nombre = input("Nombre carpeta: ")
            tree.insertar(ruta, nombre, "carpeta")

        elif op == "2":
            ruta = input("Ruta padre: ")
            nombre = input("Nombre archivo: ")
            contenido = input("Contenido: ")
            tree.insertar(ruta, nombre, "archivo", contenido)

        elif op == "3":
            ruta = input("Ruta: ")
            tree.listar_hijos(ruta)

        elif op == "4":
            node_id = input("ID del nodo: ")
            ruta = tree.obtener_ruta_id(node_id)
            print("Ruta completa:", ruta)

        elif op == "5":
            tree.guardar()

        elif op == "6":
            tree.cargar()

        elif op == "7":
            print("Saliendo...")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
