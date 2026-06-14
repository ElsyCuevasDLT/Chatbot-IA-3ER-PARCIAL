from motor import responder

print("ReciclaBot listo. Escribe un residuo o 'salir' para terminar.\n")

while True:
    mensaje = input("Tú: ").strip()
    if mensaje.lower() in {"salir", "exit", "adios"}:
        print("ReciclaBot: Gracias por separar tus residuos.")
        break
    resultado = responder(mensaje)
    print(f"ReciclaBot [{resultado['categoria']}]: {resultado['respuesta']}")
