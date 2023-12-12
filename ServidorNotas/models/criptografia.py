import random
from models.tabelacaracteres import tabela as tb

class Criptografia:
    def __init__(self):
        self.tabela_valores = tb

    def criar_numero_primo_aleatorio(self)  -> int:
        numero_primo_aleatorio = 0
        verificador = False
        while not verificador:
            numero_primo_aleatorio = random.randint(10, 100)
            for i in range(2, numero_primo_aleatorio):
                if numero_primo_aleatorio % i == 0:
                    verificador = False
                    break
                else:
                    verificador = True
        return numero_primo_aleatorio

    def calcular_mdc(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def calcular_e(self, phi_n) -> int:
        e_aleatorio = 0
        verificador = False
        while not verificador:
            e_aleatorio = self.criar_numero_primo_aleatorio()
            if 1 < e_aleatorio < phi_n:
                calcular_mdc_e = self.calcular_mdc(phi_n, e_aleatorio)
                if calcular_mdc_e == 1:
                    verificador = True
        return e_aleatorio
    
    def encriptar_base_dados(self, texto):
        p = self.criar_numero_primo_aleatorio()
        q = self.criar_numero_primo_aleatorio()
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = self.calcular_e(phi_n)

        texto_usuario = texto
        array_caracteres_criptografados = []

        for caractere in texto_usuario:
            for item_tabela in self.tabela_valores:
                if caractere == item_tabela[0]:
                    valor_letra = item_tabela[1]
                    caractere_codificado = (valor_letra ** e) % n
                    array_caracteres_criptografados.append(caractere_codificado)
                    break

        loop_d = 0
        calc = 0
        while calc != 1:
            loop_d += 1
            calc = loop_d * e % phi_n
        d = loop_d

        class CriptografiaBD:
            def __init__(self, d, n, texto_criptografado: str):
                self.d = d
                self.n = n
                self.texto_criptografado = texto_criptografado

        resultado_rsa = CriptografiaBD(d, n, array_caracteres_criptografados)
        return resultado_rsa

    def desencriptar_base_dados(self, chaves: str, caracteres_criptografados: str) -> str:
        chaves = chaves.strip().replace(' ', '').split("-")
        d = int(chaves[0])
        n = int(chaves[1])

        array_descriptografado = []

        for caractere_criptografado in caracteres_criptografados:
            caractere_descriptografado = int(caractere_criptografado) ** d % n
            array_descriptografado.append(caractere_descriptografado)

        mensagem_final_descriptografada = ''

        for caractere in array_descriptografado:
            for item_tabela in self.tabela_valores:
                if caractere == item_tabela[1]:
                    mensagem_final_descriptografada += item_tabela[0]
                    break

        return mensagem_final_descriptografada
    
    @staticmethod
    def encriptar_cliente(texto: str) -> str:
        chave=5
        return "".join([chr(ord(algo) + chave) for algo in texto])
    
    @staticmethod
    def desencriptar_cliente(texto: str) -> str:
        chave=5
        return "".join([chr(ord(algo) - chave) for algo in texto])