#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetLab Educacional — Instalador Multiplataforma
Autor: Sistema de Build
Versão: 5.0.0
"""

import os
import sys
import shutil
import json
import winreg
from pathlib import Path
from tkinter import Tk, messagebox, ttk
import tkinter as tk
from threading import Thread

class NetLabInstalador:
    def __init__(self):
        self.versao = "5.0.0"
        self.nome_app = "NetLab Educacional"
        self.guid = "A3F8C2D1-77E4-4B9A-9F2E-C8D5B1A6E034"
        self.pasta_programa = None
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / "dist"
        self.exe_principal = "NetLab Educacional.exe"
        self.sucesso = False
        
    def get_programa_files(self):
        """Obtém o caminho correto do Program Files"""
        if sys.maxsize > 2**32:  # 64 bits
            return Path(os.environ.get("ProgramFiles"))
        else:  # 32 bits
            return Path(os.environ.get("ProgramFiles(x86)"))
    
    def criar_layout_instalador(self):
        """Cria a janela de instalação"""
        self.root = Tk()
        self.root.title(f"{self.nome_app} v{self.versao} — Instalador")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Ícone (se disponível)
        try:
            ico_path = self.root_dir / "installer" / "assets" / "icone.ico"
            if ico_path.exists():
                self.root.iconbitmap(str(ico_path))
        except:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Título
        title = ttk.Label(
            main_frame,
            text=f"{self.nome_app} v{self.versao}",
            font=("Arial", 14, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Descrição
        desc = ttk.Label(
            main_frame,
            text="Plataforma de Análise de Redes para Ensino\n© 2026 Yuri Gonçalves Pavão — Instituto Federal Farroupilha",
            font=("Arial", 10),
            justify="center"
        )
        desc.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Localização da instalação
        ttk.Label(main_frame, text="Localização da instalação:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", pady=10
        )
        
        self.pasta_programa = self.get_programa_files() / self.nome_app
        self.local_var = tk.StringVar(value=str(self.pasta_programa))
        
        entry_local = ttk.Entry(main_frame, textvariable=self.local_var, width=50)
        entry_local.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Opções
        ttk.Label(main_frame, text="Opções de instalação:", font=("Arial", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=10
        )
        
        self.criar_atalho_desktop = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Criar atalho na Área de Trabalho", variable=self.criar_atalho_desktop).grid(
            row=5, column=0, sticky="w", padx=20
        )
        
        self.criar_atalho_iniciar = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Criar atalho no Menu Iniciar", variable=self.criar_atalho_iniciar).grid(
            row=6, column=0, sticky="w", padx=20
        )
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=300)
        self.progress.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.status_label = ttk.Label(main_frame, text="Pronto para instalar", foreground="blue")
        self.status_label.grid(row=8, column=0, columnspan=2)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Instalar", command=self.iniciar_instalacao).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.root.quit).pack(side="left", padx=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
    
    def iniciar_instalacao(self):
        """Inicia o processo de instalação em thread"""
        thread = Thread(target=self.instalar, daemon=True)
        thread.start()
    
    def instalar(self):
        """Executa a instalação"""
        try:
            self.progress['value'] = 0
            self.pasta_programa = Path(self.local_var.get())
            
            # Verificar permissões de administrador
            if not self.eh_admin():
                self.atualizar_status("Erro: Privilégios de Administrador necessários!", "red")
                messagebox.showerror("Erro", "Este instalador requer privilégios de Administrador.\nPor favor, execute novamente como Administrador.")
                return
            
            # 1. Verificar arquivo executável
            self.atualizar_status("Verificando arquivos...", "blue")
            exe_path = self.dist_dir / self.exe_principal
            if not exe_path.exists():
                raise FileNotFoundError(f"Executável não encontrado: {exe_path}")
            self.progress['value'] = 10
            self.root.update()
            
            # 2. Criar pasta de destino
            self.atualizar_status("Criando pasta de instalação...", "blue")
            self.pasta_programa.mkdir(parents=True, exist_ok=True)
            self.progress['value'] = 20
            self.root.update()
            
            # 3. Copiar executável
            self.atualizar_status("Copiando executável...", "blue")
            shutil.copy2(exe_path, self.pasta_programa / self.exe_principal)
            self.progress['value'] = 30
            self.root.update()
            
            # 4. Copiar pasta dados (se existir)
            self.atualizar_status("Copiando dados...", "blue")
            dados_src = self.dist_dir / "dados"
            if dados_src.exists():
                dados_dst = self.pasta_programa / "dados"
                if dados_dst.exists():
                    shutil.rmtree(dados_dst)
                shutil.copytree(dados_src, dados_dst)
            self.progress['value'] = 40
            self.root.update()
            
            # 5. Copiar ícone
            self.atualizar_status("Copiando recursos...", "blue")
            ico_src = self.root_dir / "installer" / "assets" / "icone.ico"
            if ico_src.exists():
                shutil.copy2(ico_src, self.pasta_programa / "icone.ico")
            self.progress['value'] = 50
            self.root.update()
            
            # 6. Criar atalhos
            self.atualizar_status("Criando atalhos...", "blue")
            self.criar_atalhos()
            self.progress['value'] = 70
            self.root.update()
            
            # 7. Registrar no Windows
            self.atualizar_status("Registrando no sistema...", "blue")
            self.registrar_windows()
            self.progress['value'] = 90
            self.root.update()
            
            # 8. Sucesso!
            self.progress['value'] = 100
            self.atualizar_status("Instalação concluída com sucesso!", "green")
            self.sucesso = True
            self.root.update()
            
            messagebox.showinfo(
                "Sucesso",
                f"{self.nome_app} foi instalado com sucesso!\n\n"
                f"Localização: {self.pasta_programa}\n\n"
                f"Você pode iniciar o programa através do Menu Iniciar ou da Área de Trabalho."
            )
            self.root.quit()
            
        except Exception as e:
            self.atualizar_status(f"Erro: {str(e)}", "red")
            messagebox.showerror("Erro na Instalação", f"Ocorreu um erro durante a instalação:\n\n{str(e)}")
    
    def atualizar_status(self, texto, cor="black"):
        """Atualiza o label de status"""
        self.status_label.config(text=texto, foreground=cor)
        self.root.update()
    
    def eh_admin(self):
        """Verifica se tem privilégios de administrador"""
        try:
            return os.getuid() == 0  # Linux/Mac
        except AttributeError:
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()  # Windows
            except:
                return False
    
    def criar_atalhos(self):
        """Cria atalhos no Windows"""
        try:
            import winshell
            
            # Atalho no Menu Iniciar
            if self.criar_atalho_iniciar.get():
                pasta_menu = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / self.nome_app
                pasta_menu.mkdir(parents=True, exist_ok=True)
                
                atalho_path = pasta_menu / f"{self.nome_app}.lnk"
                winshell.CreateShortCut(
                    str(atalho_path),
                    str(self.pasta_programa / self.exe_principal),
                    icon_file=str(self.pasta_programa / "icone.ico")
                )
            
            # Atalho na Área de Trabalho
            if self.criar_atalho_desktop.get():
                desktop = Path(os.environ['USERPROFILE']) / "Desktop"
                atalho_path = desktop / f"{self.nome_app}.lnk"
                winshell.CreateShortCut(
                    str(atalho_path),
                    str(self.pasta_programa / self.exe_principal),
                    icon_file=str(self.pasta_programa / "icone.ico")
                )
        except ImportError:
            # Fallback: criar usando VBScript
            self.criar_atalhos_vbscript()
    
    def criar_atalhos_vbscript(self):
        """Cria atalhos usando VBScript (fallback)"""
        try:
            import tempfile
            
            ico_path = str(self.pasta_programa / "icone.ico")
            exe_path = str(self.pasta_programa / self.exe_principal)
            
            if self.criar_atalho_desktop.get():
                desktop = Path(os.environ['USERPROFILE']) / "Desktop"
                vbs_content = f"""
Set objShell = CreateObject("WScript.Shell")
Set objLink = objShell.CreateShortcut("{desktop}\\{self.nome_app}.lnk")
objLink.TargetPath = "{exe_path}"
objLink.IconLocation = "{ico_path}"
objLink.Save
"""
                with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
                    f.write(vbs_content)
                    vbs_path = f.name
                
                os.system(f'cscript.exe "{vbs_path}"')
                os.unlink(vbs_path)
        except Exception as e:
            print(f"Aviso: Não foi possível criar atalhos de forma automática: {e}")
    
    def registrar_windows(self):
        """Registra a aplicação no Windows (Adicionar/Remover Programas)"""
        try:
            chave = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                0,
                winreg.KEY_WRITE
            )
        except:
            # Fallback para HKEY_CURRENT_USER se não tiver acesso HKLM
            chave = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            )
        
        try:
            subchave = winreg.CreateKey(chave, f"{self.guid}_is1")
            
            winreg.SetValueEx(subchave, "DisplayName", 0, winreg.REG_SZ, self.nome_app)
            winreg.SetValueEx(subchave, "DisplayVersion", 0, winreg.REG_SZ, self.versao)
            winreg.SetValueEx(subchave, "InstallLocation", 0, winreg.REG_SZ, str(self.pasta_programa))
            winreg.SetValueEx(subchave, "UninstallString", 0, winreg.REG_SZ, str(self.pasta_programa / self.exe_principal))
            winreg.SetValueEx(subchape, "Publisher", 0, winreg.REG_SZ, "Yuri Gonçalves Pavão / IFFar")
            winreg.SetValueEx(subchave, "URLInfoAbout", 0, winreg.REG_SZ, "https://yurigonpav.github.io/NetLab-Site")
            
            winreg.CloseKey(subchave)
        finally:
            winreg.CloseKey(chave)
    
    def executar(self):
        """Executa o instalador"""
        self.criar_layout_instalador()
        self.root.mainloop()
        return self.sucesso

if __name__ == "__main__":
    instalador = NetLabInstalador()
    sucesso = instalador.executar()
    sys.exit(0 if sucesso else 1)
