import customtkinter as tk
import re

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.configuraLoyout()
        self.configuraWidget()
        self.configuraGridWidget()

    def destroiTela(self,evento):
        self.destroy()

    def verificaCampoVazio(self):
        nome=self.inputNome.get()
        email=self.inputEmail.get()
        senha1=self.inputPrimeiraSenha.get()
        senha2=self.inputSegundaSenha.get()
        if len(nome)!=0:
            if len(email)!=0:
                if len(senha1)!=0:
                    self.verificaSenhaRobusta()
                    if len(senha2)!=0:
                        print(f'Campos preenchidos!')
                    else:
                        print(f'Campo confirma senha está vazio!')
                else:
                    print(f'Campo senha está vazio!')
            else:
                print(f'Campo email está vazio!')
        else:
            print(f'Campo nome está vazio!')

    def verificaSenhaRobusta(self):
        maiusculo=re.compile(r"\w*[A-Z]\w*")
        minusculo=re.compile(r"\w*[a-z]\w*")
        numeral=re.compile(r"\w*[0-9]\w*")
        especial=re.compile(r"\w*[!@#$_]\w*")

        senha1=self.inputPrimeiraSenha.get()
        if re.match(maiusculo,senha1):
            print(f'{senha1} possui caractere maiúsculo.')
            if re.match(minusculo,senha1):
                print(f'{senha1} possui caractere minúsculo.')
                if re.match(numeral,senha1):
                    print(f'{senha1} possui caractere numeral.')
                    if re.match(especial,senha1):
                        print(f'{senha1} possui caractere especial.')
                        if len(senha1)>=8:
                            print(f'{senha1} possui 8 ou mais caracteres.')
                            senha2=self.inputSegundaSenha.get()
                            if senha1==senha2:
                                print(f'Senhas conferem.')
                            else:
                                print(f'Senhas não conferem.')
                        else:
                            print(f'{senha1} não possui 8 caracteres.')
                    else:
                        print(f'{senha1} não possui caractere especial.')
                else:
                    print(f'{senha1} não possui caractere numeral.')
            else:
                print(f'{senha1} não possui caractere minúsculo.')
        else:
            print(f'{senha1} não possui caractere maiúsculo.')
    
    def configuraLoyout(self):
        # self.winfo_toplevel()
        alturaTela=self.winfo_screenheight()
        larguraTela=self.winfo_screenwidth()
        umQuartoLargura=larguraTela//4
        metadeAltura=alturaTela//2
        larguraTelaLogin=300
        alturaTelaLogin=400
        self.title('Cadastrar')
        self.geometry(f'{larguraTelaLogin}x{alturaTelaLogin}+{(umQuartoLargura*3)-(larguraTelaLogin//2)}+{metadeAltura-(alturaTelaLogin//2)}')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.sextoContainer=tk.CTkFrame(self)
        self.sextoContainer.grid(row=0,column=0,padx=20,pady=20,sticky='nswe')
        self.sextoContainer.columnconfigure(0,weight=1)

        self.primeiroContainer=tk.CTkFrame(self.sextoContainer)
        self.primeiroContainer.grid(row=0,column=0,padx=10,pady=(10,0),sticky='nswe')
        self.primeiroContainer.columnconfigure(0,weight=1)
        self.segundoContainer=tk.CTkFrame(self.sextoContainer)
        self.segundoContainer.grid(row=1,column=0,padx=10,pady=(10,0),sticky='nswe')
        self.segundoContainer.columnconfigure(0,weight=1)
        self.terceiroContainer=tk.CTkFrame(self.sextoContainer)
        self.terceiroContainer.grid(row=2,column=0,padx=10,pady=(10,0),sticky='nswe')
        self.terceiroContainer.columnconfigure(0,weight=1)

    def configuraWidget(self):
        self.labelCadastro=tk.CTkLabel(self.primeiroContainer,text='Cadastrar',font=tk.CTkFont(size=16,weight='bold'))
        self.inputNome=tk.CTkEntry(self.segundoContainer,placeholder_text='Nome',width=200)
        self.inputEmail=tk.CTkEntry(self.segundoContainer,placeholder_text='Email',width=200)
        self.inputPrimeiraSenha=tk.CTkEntry(self.segundoContainer,placeholder_text='Senha',width=200)
        self.inputSegundaSenha=tk.CTkEntry(self.segundoContainer,placeholder_text='Confirme a senha',width=200)
        self.botaoCadastro=tk.CTkButton(self.segundoContainer,text='Cadastrar',width=200,command=self.verificaCampoVazio)
        self.labelPossuiCadastro=tk.CTkLabel(self.terceiroContainer,text='Já possui cadastro?')
        self.labelLinkEntrar=tk.CTkLabel(self.terceiroContainer,text='Entrar',font=tk.CTkFont(size=12,weight='bold'), cursor="hand2")
        self.labelLinkEntrar.bind('<Button-1>',self.destroiTela)

    def configuraGridWidget(self):
        self.labelCadastro.grid(row=0,column=0,padx=10,pady=10,sticky='we')
        self.inputNome.grid(row=0,column=0,padx=10,pady=(10,0))
        self.inputEmail.grid(row=1,column=0,padx=10,pady=(10,0))
        self.inputPrimeiraSenha.grid(row=2,column=0,padx=10,pady=(10,0))
        self.inputSegundaSenha.grid(row=3,column=0,padx=10,pady=(10,0))
        self.botaoCadastro.grid(row=4,column=0,padx=10,pady=10)
        self.labelPossuiCadastro.grid(row=0,column=0,padx=10,pady=(10,0))
        self.labelLinkEntrar.grid(row=1,column=0,padx=10,pady=10)