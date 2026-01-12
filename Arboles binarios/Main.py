import json
import os

# ===============================
#           NODE
# ===============================
class Node:
    def __init__(self, node_id, name, tipo, content=None):
        self.id = node_id
        self.name = name
        self.tipo = tipo        # carpeta | archivo
        self.content = content
        self.children = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tipo": self.tipo,
            "content": self.content,
            "children": [c.to_dict() for c in self.children]
        }

    @staticmethod
    def from_dict(data):
        n = Node(data["id"], data["name"], data["tipo"], data["content"])
        n.children = [Node.from_dict(c) for c in data["children"]]
        return n


# ===============================
#           TRIE
# ===============================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word.lower():
            node = node.children.setdefault(c, TrieNode())
        node.end = True

    def search_prefix(self, prefix):
        node = self.root
        for c in prefix.lower():
            if c not in node.children:
                return []
            node = node.children[c]
        return self._collect(prefix, node)

    def _collect(self, prefix, node):
        res = []
        if node.end:
            res.append(prefix)
        for c, n in node.children.items():
            res.extend(self._collect(prefix + c, n))
        return res


# ===============================
#           TREE
# ===============================
class FileTree:
    def __init__(self):
        self.root = Node("0", "root", "carpeta")
        self.map = {"0": self.root}
        self.trie = Trie()
        self.trash = []
        self.next_id = 1

    # ---------- UTIL ----------
    def _register(self, node):
        self.map[node.id] = node
        self.trie.insert(node.name)
        for c in node.children:
            self._register(c)

    def buscar_por_ruta(self, ruta):
        partes = [p for p in ruta.split("/") if p]
        actual = self.root
        for p in partes[1:]:
            actual = next((c for c in actual.children if c.name == p), None)
            if not actual:
                return None
        return actual

    # ---------- OPERACIONES ----------
    def insertar(self, ruta, nombre, tipo, contenido=None):
        padre = self.buscar_por_ruta(ruta)
        if not padre:
            print("Ruta invalida")
            return
        nuevo = Node(str(self.next_id), nombre, tipo, contenido)
        self.next_id += 1
        padre.children.append(nuevo)
        self._register(nuevo)
        print("Nodo creado")

    def listar(self, ruta):
        nodo = self.buscar_por_ruta(ruta)
        if not nodo:
            print("Ruta invalida")
            return
        for c in nodo.children:
            print(f"[{c.tipo}] {c.name} (id={c.id})")

    def mover(self, id_nodo, ruta_destino):
        if id_nodo not in self.map:
            print("ID invalido")
            return
        destino = self.buscar_por_ruta(ruta_destino)
        if not destino:
            print("Destino invalido")
            return

        nodo = self.map[id_nodo]
        padre = self._buscar_padre(self.root, nodo)
        if padre:
            padre.children.remove(nodo)
        destino.children.append(nodo)
        print("Nodo movido")

    def renombrar(self, id_nodo, nuevo_nombre):
        if id_nodo not in self.map:
            print("ID invalido")
            return
        self.map[id_nodo].name = nuevo_nombre
        self.trie.insert(nuevo_nombre)
        print("Nodo renombrado")

    def eliminar(self, id_nodo):
        if id_nodo not in self.map:
            print("ID invalido")
            return
        nodo = self.map[id_nodo]
        padre = self._buscar_padre(self.root, nodo)
        if padre:
            padre.children.remove(nodo)
        self.trash.append(nodo)
        del self.map[id_nodo]
        print("Nodo enviado a papelera")

    def _buscar_padre(self, actual, target):
        for c in actual.children:
            if c == target:
                return actual
            res = self._buscar_padre(c, target)
            if res:
                return res
        return None

    def ruta_completa(self, id_nodo):
        if id_nodo not in self.map:
            return None
        nodo = self.map[id_nodo]
        ruta = []

        def dfs(actual):
            if actual == nodo:
                ruta.append(actual.name)
                return True
            for c in actual.children:
                if dfs(c):
                    ruta.append(actual.name)
                    return True
            return False

        dfs(self.root)
        return "/" + "/".join(reversed(ruta))

    # ---------- RECORRIDOS ----------
    def preorden(self):
        res = []

        def dfs(n):
            res.append(n.name)
            for c in n.children:
                dfs(c)

        dfs(self.root)
        return res

    # ---------- MÉTRICAS ----------
    def altura(self, nodo=None):
        nodo = nodo or self.root
        if not nodo.children:
            return 1
        return 1 + max(self.altura(c) for c in nodo.children)

    def tamaño(self, nodo=None):
        nodo = nodo or self.root
        return 1 + sum(self.tamaño(c) for c in nodo.children)

    # ---------- PERSISTENCIA ----------
    def guardar(self, archivo="tree.json"):
        with open(archivo, "w") as f:
            json.dump(self.root.to_dict(), f, indent=4)
        print("Guardado")

    def cargar(self, archivo="tree.json"):
        if not os.path.exists(archivo):
            return
        with open(archivo, "r") as f:
            self.root = Node.from_dict(json.load(f))
        self.map = {}
        self.trie = Trie()
        self._register(self.root)
        self.next_id = max(int(k) for k in self.map.keys()) + 1


# ===============================
#           CONSOLA
# ===============================
def main():
    tree = FileTree()
    tree.cargar()

    while True:
        cmd = input("\n> ").split()
        if not cmd:
            continue

        if cmd[0] == "mkdir":
            tree.insertar(cmd[1], cmd[2], "carpeta")

        elif cmd[0] == "touch":
            tree.insertar(cmd[1], cmd[2], "archivo", " ".join(cmd[3:]))

        elif cmd[0] == "ls":
            tree.listar(cmd[1])

        elif cmd[0] == "mv":
            tree.mover(cmd[1], cmd[2])

        elif cmd[0] == "rename":
            tree.renombrar(cmd[1], cmd[2])

        elif cmd[0] == "rm":
            tree.eliminar(cmd[1])

        elif cmd[0] == "search":
            print(tree.trie.search_prefix(cmd[1]))

        elif cmd[0] == "pwd":
            print(tree.ruta_completa(cmd[1]))

        elif cmd[0] == "export":
            print(tree.preorden())

        elif cmd[0] == "save":
            tree.guardar()

        elif cmd[0] == "exit":
            tree.guardar()
            break

        else:
            print("Comando no reconocido")


if __name__ == "__main__":
    main()
