import json
import uuid

# ===================== NODO =====================
class Node:
    def __init__(self, name, tipo, contenido=None):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.tipo = tipo  # carpeta / archivo
        self.contenido = contenido
        self.children = []
        self.parent = None

# ===================== TRIE =====================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insertar(self, palabra):
        nodo = self.root
        for c in palabra:
            if c not in nodo.children:
                nodo.children[c] = TrieNode()
            nodo = nodo.children[c]
        nodo.end = True

    def buscar_prefijo(self, prefijo):
        nodo = self.root
        for c in prefijo:
            if c not in nodo.children:
                return []
            nodo = nodo.children[c]
        return self._dfs(nodo, prefijo)

    def _dfs(self, nodo, prefijo):
        resultados = []
        if nodo.end:
            resultados.append(prefijo)
        for c, hijo in nodo.children.items():
            resultados.extend(self._dfs(hijo, prefijo + c))
        return resultados

# ===================== ÁRBOL =====================
class FileTree:
    def __init__(self):
        self.root = Node("root", "carpeta")
        self.nodes = {self.root.id: self.root}
        self.trie = Trie()
        self.trie.insertar("root")
        self.trash = []

    def buscar_por_ruta(self, ruta):
        if ruta == "/":
            return self.root
        partes = ruta.strip("/").split("/")
        actual = self.root
        for p in partes:
            encontrado = False
            for h in actual.children:
                if h.name == p:
                    actual = h
                    encontrado = True
                    break
            if not encontrado:
                return None
        return actual

    def insertar(self, ruta, nombre, tipo, contenido=None):
        padre = self.buscar_por_ruta(ruta)
        if not padre or padre.tipo != "carpeta":
            print("Ruta invalida")
            return
        nuevo = Node(nombre, tipo, contenido)
        nuevo.parent = padre
        padre.children.append(nuevo)
        self.nodes[nuevo.id] = nuevo
        self.trie.insertar(nombre)
        print(f"{tipo} creado con ID {nuevo.id}")

    def listar(self, ruta):
        nodo = self.buscar_por_ruta(ruta)
        if not nodo:
            print("Ruta no encontrada")
            return
        for h in nodo.children:
            print(f"{h.name} ({h.tipo}) [{h.id}]")

    def mover(self, node_id, ruta_destino):
        if node_id not in self.nodes:
            print("ID no valido")
            return
        destino = self.buscar_por_ruta(ruta_destino)
        if not destino or destino.tipo != "carpeta":
            print("Destino invalido")
            return
        nodo = self.nodes[node_id]
        nodo.parent.children.remove(nodo)
        nodo.parent = destino
        destino.children.append(nodo)
        print("Nodo movido")

    def eliminar(self, node_id):
        if node_id not in self.nodes or node_id == self.root.id:
            print("No se puede eliminar")
            return
        nodo = self.nodes[node_id]
        nodo.parent.children.remove(nodo)
        self.trash.append(nodo)
        del self.nodes[node_id]
        print("Nodo enviado a papelera")

    def export_preorden(self):
        def dfs(n, nivel=0):
            print("  " * nivel + f"{n.name} ({n.tipo})")
            for h in n.children:
                dfs(h, nivel + 1)
        dfs(self.root)

    def guardar(self):
        def serializar(n):
            return {
                "id": n.id,
                "name": n.name,
                "tipo": n.tipo,
                "contenido": n.contenido,
                "children": [serializar(h) for h in n.children]
            }
        with open("tree.json", "w") as f:
            json.dump(serializar(self.root), f, indent=2)

# ===================== CONSOLA =====================
def main():
    tree = FileTree()
    print("Arboles - Si necesitas ayuda escribe: 'help'")

    while True:
        cmd = input("> ").strip().split()
        if not cmd:
            continue

        if cmd[0] == "help":
            print("""
mkdir <ruta> <nombre>
touch <ruta> <nombre> [contenido]
ls <ruta>
mv <id> <ruta_destino>
rm <id>
search <prefijo>
export
exit
""")

        elif cmd[0] == "mkdir":
            if len(cmd) != 3:
                print("Uso: mkdir <ruta> <nombre>")
                continue
            tree.insertar(cmd[1], cmd[2], "carpeta")

        elif cmd[0] == "touch":
            if len(cmd) < 3:
                print("Uso: touch <ruta> <nombre> [contenido]")
                continue
            tree.insertar(cmd[1], cmd[2], "archivo", " ".join(cmd[3:]))

        elif cmd[0] == "ls":
            if len(cmd) != 2:
                print("Uso: ls <ruta>")
                continue
            tree.listar(cmd[1])

        elif cmd[0] == "mv":
            if len(cmd) != 3:
                print("Uso: mv <id> <ruta_destino>")
                continue
            tree.mover(cmd[1], cmd[2])

        elif cmd[0] == "rm":
            if len(cmd) != 2:
                print("Uso: rm <id>")
                continue
            tree.eliminar(cmd[1])

        elif cmd[0] == "search":
            if len(cmd) != 2:
                print("Uso: search <prefijo>")
                continue
            print(tree.trie.buscar_prefijo(cmd[1]))

        elif cmd[0] == "export":
            tree.export_preorden()
            tree.guardar()

        elif cmd[0] == "exit":
            break

        else:
            print("Comando desconocido")

if __name__ == "__main__":
    main()
