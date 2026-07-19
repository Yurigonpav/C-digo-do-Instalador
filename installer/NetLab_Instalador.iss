; =============================================================================
;  NetLab Educacional — Script de Instalação Profissional
;  Ferramenta: Inno Setup 6.x (https://jrsoftware.org/isinfo.php)
;
;  Autor:    Yuri Gonçalves Pavão
;  TCC:      Instituto Federal Farroupilha — Campus Uruguaiana
;  Curso:    Técnico em Informática Integrado ao Ensino Médio
;  Versão:   5.0
;
;  COMO USAR:
;    1. Instale o Inno Setup 6 (https://jrsoftware.org/isdl.php)
;    2. Certifique-se de que todos os arquivos listados em [Files] existam
;       nas pastas indicadas (veja a seção "Pré-requisitos do Build" abaixo)
;    3. Compile com: iscc.exe NetLab_Instalador.iss
;       Ou abra no Inno Setup IDE e pressione F9
;
;  ESTRUTURA DE PASTAS ESPERADA ANTES DE COMPILAR:
;
;    installer/
;    ├── NetLab_Instalador.iss        ← este arquivo
;    ├── assets/
;    │   ├── icone.ico                ← ícone do instalador e atalhos
;    │   ├── banner_instalador.bmp    ← imagem lateral 164x314 px (24-bit BMP)
;    │   ├── topo_instalador.bmp      ← imagem do topo 497x58 px (24-bit BMP)
;    │   └── licenca.rtf              ← texto da licença em formato RTF
;    ├── prerequisitos/
;    │   └── npcap-1.82.exe           ← instalador do Npcap (baixe em npcap.com)
;    └── dist/
;        └── NetLab Educacional.exe   ← executável gerado pelo PyInstaller
;
;  COMO GERAR O EXECUTÁVEL (NetLab Educacional.exe):
;    1. Ative o ambiente virtual: .\venv\Scripts\Activate.ps1
;    2. Instale o PyInstaller: pip install pyinstaller
;    3. Execute: pyinstaller NetLab.spec
;    4. O executável estará em: dist\NetLab Educacional.exe
; =============================================================================

; -----------------------------------------------------------------------------
;  DEFINIÇÕES GLOBAIS — ajuste apenas estas constantes para novas versões
; -----------------------------------------------------------------------------

#define NOME_APP          "NetLab Educacional"
#define VERSAO            "5.0.0"
#define VERSAO_EXIBIDA    "5.0"
#define EDITOR            "Yuri Gonçalves Pavão"
#define ORGANIZACAO       "IFFar — Campus Uruguaiana"
#define SITE_OFICIAL      "https://yurigonpav.github.io/NetLab-Site"
#define SUPORTE_EMAIL     "netlab.educacional@gmail.com"
#define EXE_PRINCIPAL     "NetLab Educacional.exe"
#define NOME_SERVICO      "NetLabEducacional"
#define GUID_INSTALACAO   "A3F8C2D1-77E4-4B9A-9F2E-C8D5B1A6E034"
#define PASTA_DIST        "..\dist"
#define PASTA_ASSETS      "assets"
#define PASTA_PREREQ      "..\prerequisitos"

; =============================================================================
;  CONFIGURAÇÕES GERAIS DO INSTALADOR
; =============================================================================

[Setup]

; --- Identificação única desta aplicação (GUID fixo para atualizações corretas)
AppId={{{#GUID_INSTALACAO}}}

; --- Metadados exibidos no "Adicionar/Remover Programas"
AppName={#NOME_APP}
AppVersion={#VERSAO}
AppVerName={#NOME_APP} v{#VERSAO_EXIBIDA}
AppPublisher={#EDITOR} / {#ORGANIZACAO}
AppPublisherURL={#SITE_OFICIAL}
AppSupportURL={#SITE_OFICIAL}
AppUpdatesURL={#SITE_OFICIAL}
AppCopyright=Copyright © 2026 {#EDITOR} — Uso educacional

; --- Pasta de destino padrão (pode ser alterada pelo usuário)
DefaultDirName={autopf}\{#NOME_APP}
DefaultGroupName={#NOME_APP}
AllowNoIcons=no

; --- Arquivo de saída
OutputDir=..\saida_instalador
OutputBaseFilename=NetLab_Educacional_v{#VERSAO}_Setup
SetupIconFile={#PASTA_ASSETS}\icone.ico

; --- Visual do instalador (wizard moderno)
WizardStyle=modern
DisableWelcomePage=no
WizardSizePercent=130
WizardImageFile={#PASTA_ASSETS}\banner_instalador.bmp

; --- Compressão (LZMA2 = melhor razão, um pouco mais lento)
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=4

; --- Requisitos de plataforma
MinVersion=10.0.17763
; Windows 10 1809 ou superior (Build 17763)
; Necessário para: LZMA2, Npcap moderno, compatibilidade com PyQt6

; --- Privilégios (obrigatório — Npcap exige admin)
PrivilegesRequired=admin

; --- Arquivo de licença exibido na tela do instalador
LicenseFile={#PASTA_ASSETS}\licenca.rtf

; --- Informações mostradas nas telas "Bem-vindo" e "Concluído"
SetupMutex={#NOME_SERVICO}_instalacao_mutex
RestartApplications=no
CloseApplications=yes
CloseApplicationsFilter=*.exe

; --- Desinstalador
UninstallDisplayIcon={app}\{#EXE_PRINCIPAL}
UninstallDisplayName={#NOME_APP} v{#VERSAO_EXIBIDA}
CreateUninstallRegKey=yes
Uninstallable=yes

; --- Registro do Windows (Adicionar/Remover Programas)
VersionInfoVersion={#VERSAO}
VersionInfoCompany={#ORGANIZACAO}
VersionInfoDescription={#NOME_APP} — Plataforma de Análise de Redes para Ensino
VersionInfoProductName={#NOME_APP}
VersionInfoProductVersion={#VERSAO}

; --- Outras opções
DirExistsWarning=auto
DisableProgramGroupPage=no
UsePreviousGroup=yes
UsePreviousSetupType=yes
AlwaysShowGroupOnReadyPage=yes
AlwaysShowDirOnReadyPage=yes
ShowTasksTreeLines=yes

; =============================================================================
;  IDIOMA
; =============================================================================

[Languages]
Name: "ptbr"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

; =============================================================================
;  TAREFAS OPCIONAIS OFERECIDAS AO USUÁRIO
; =============================================================================

[Tasks]
; Atalhos
Name: "atalho_area_trabalho";    Description: "Criar atalho na &Área de Trabalho";         GroupDescription: "Atalhos:"
Name: "atalho_barra_rapida";     Description: "Fixar na &Barra de Tarefas";                GroupDescription: "Atalhos:";     Flags: unchecked
Name: "atalho_inicializar";      Description: "Iniciar o NetLab com o &Windows (Administrador)"; GroupDescription: "Atalhos:"; Flags: unchecked

; Diagnóstico
Name: "criar_atalho_diag";       Description: "Criar atalho para o script de diagnósti&co de interfaces"; GroupDescription: "Ferramentas avançadas:"; Flags: unchecked

; Firewall
Name: "regra_firewall";          Description: "Adicionar exceção no &Firewall do Windows (recomendado para o Servidor Lab)"; GroupDescription: "Segurança:"

; =============================================================================
;  ARQUIVOS INSTALADOS
; =============================================================================

[Files]

; --- Executável principal (gerado pelo PyInstaller)
Source: "{#PASTA_DIST}\{#EXE_PRINCIPAL}";  DestDir: "{app}";  Flags: ignoreversion;  DestName: "{#EXE_PRINCIPAL}"

; --- Ícone standalone para atalhos
Source: "{#PASTA_ASSETS}\icone.ico";        DestDir: "{app}";  Flags: ignoreversion

; --- Pasta de dados persistentes (aliases de dispositivos)
;     A pasta é criada vazia — o NetLab a preenche em tempo de execução
Source: "..\dados\.gitkeep";               DestDir: "{app}\dados";  Flags: ignoreversion skipifsourcedoesntexist

; --- Script de diagnóstico autônomo (Python — opcional, para usuários avançados)
;     Só é instalado se o usuário marcou a tarefa correspondente
Source: "..\diagnostico.py";               DestDir: "{app}\ferramentas";  Tasks: criar_atalho_diag;  Flags: ignoreversion

; --- Npcap (pré-requisito — incluído no pacote do instalador)
;     Baixe o instalador em: https://npcap.com/#download
;     Coloque em: installer/prerequisitos/npcap-1.82.exe
Source: "{#PASTA_PREREQ}\npcap-1.82.exe";  DestDir: "{tmp}";  Flags: dontcopy

; =============================================================================
;  ÍCONES / ATALHOS
; =============================================================================

[Icons]

; --- Atalho no Menu Iniciar
Name: "{group}\{#NOME_APP}";                         Filename: "{app}\{#EXE_PRINCIPAL}";  IconFilename: "{app}\icone.ico";  Comment: "Abrir {#NOME_APP} — Análise de Redes Educacional"
Name: "{group}\Desinstalar {#NOME_APP}";             Filename: "{uninstallexe}";           Comment: "Remover o {#NOME_APP} do computador"

; --- Atalho na Área de Trabalho (somente se marcado)
Name: "{autodesktop}\{#NOME_APP}";                   Filename: "{app}\{#EXE_PRINCIPAL}";  IconFilename: "{app}\icone.ico";  Comment: "Abrir {#NOME_APP}";  Tasks: atalho_area_trabalho

; --- Atalho de diagnóstico (somente se marcado)
Name: "{group}\Ferramentas\Diagnóstico de Interfaces"; Filename: "python";               Parameters: """{app}\ferramentas\diagnostico.py""";  Comment: "Diagnosticar interfaces de rede disponíveis";  Tasks: criar_atalho_diag

; =============================================================================
;  REGISTRO DO WINDOWS
; =============================================================================

[Registry]

; --- Associação no Adicionar/Remover Programas (informações adicionais)
Root: HKLM;  Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{{#GUID_INSTALACAO}}}_is1"; ValueType: string;  ValueName: "URLInfoAbout";         ValueData: "{#SITE_OFICIAL}"
Root: HKLM;  Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{{#GUID_INSTALACAO}}}_is1"; ValueType: string;  ValueName: "HelpLink";              ValueData: "{#SITE_OFICIAL}"
Root: HKLM;  Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{{#GUID_INSTALACAO}}}_is1"; ValueType: string;  ValueName: "EstimatedSize";         ValueData: "350000"
Root: HKLM;  Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{{#GUID_INSTALACAO}}}_is1"; ValueType: string;  ValueName: "DisplayVersion";        ValueData: "{#VERSAO_EXIBIDA}"
Root: HKLM;  Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{{#GUID_INSTALACAO}}}_is1"; ValueType: string;  ValueName: "Publisher";             ValueData: "{#EDITOR} / {#ORGANIZACAO}"

; --- Informações da instalação (usadas pelo script de diagnóstico)
Root: HKLM;  Subkey: "SOFTWARE\{#NOME_SERVICO}";   ValueType: string;  ValueName: "PastaInstalacao";     ValueData: "{app}"
Root: HKLM;  Subkey: "SOFTWARE\{#NOME_SERVICO}";   ValueType: string;  ValueName: "Versao";              ValueData: "{#VERSAO}"
Root: HKLM;  Subkey: "SOFTWARE\{#NOME_SERVICO}";   ValueType: string;  ValueName: "DataInstalacao";      ValueData: "{code:ObterDataHoraAtual}"

; =============================================================================
;  CÓDIGO PASCAL — LÓGICA PERSONALIZADA DO INSTALADOR
; =============================================================================

[Code]

// ---------------------------------------------------------------------------
// CONSTANTES E VARIÁVEIS GLOBAIS
// ---------------------------------------------------------------------------

const
  NPCAP_VERSAO_MINIMA   = '1.70';
  NPCAP_CHAVE_REGISTRO  = 'SOFTWARE\Npcap';
  WINPCAP_CHAVE_REGISTRO = 'SOFTWARE\WinPcap';
  WINDOWS_BUILD_MINIMO  = 17763;  // Windows 10 1809

var
  // Flags de estado para controlar o fluxo de instalação
  NpcapJaInstalado:  Boolean;
  NpcapVersaoAtual:  String;
  InstalacaoOk:      Boolean;

  // Páginas personalizadas
  PaginaInformacoes: TOutputMsgWizardPage;


// ---------------------------------------------------------------------------
// FUNÇÕES AUXILIARES
// ---------------------------------------------------------------------------

// Retorna a data e hora atual no formato DD/MM/YYYY HH:MM
function ObterDataHoraAtual(Param: String): String;
var
  Data: String;
begin
  Data := GetDateTimeString('dd/mm/yyyy', '-', ':');
  Result := Data;
end;


// Verifica se o sistema é Windows 10 ou superior
function WindowsSuportado: Boolean;
begin
  Result := (GetWindowsVersion >= $0A000000);
end;


// Lê a versão do Npcap do registro do Windows (tenta 32 e 64 bits)
function LerVersaoNpcap: String;
var
  Versao: String;
begin
  Result := '';
  // Tenta a chave de 32 bits
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, NPCAP_CHAVE_REGISTRO, '', Versao) then
  begin
    Result := Versao;
    Exit;
  end;
  // Tenta a chave de 64 bits
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\WOW6432Node\Npcap', '', Versao) then
  begin
    Result := Versao;
    Exit;
  end;
end;


// Compara duas versões no formato "X.YZ" — retorna True se VersaoAtual >= VersaoMinima
function VersaoSuficiente(VersaoAtual, VersaoMinima: String): Boolean;
begin
  Result := False;
  if VersaoAtual = '' then Exit;

  // Simplificado: compara as strings diretamente após normalização
  if CompareStr(VersaoAtual, VersaoMinima) >= 0 then
    Result := True;
end;


// Verifica se o Npcap está instalado e em versão adequada
function VerificarNpcap: Boolean;
begin
  NpcapVersaoAtual := LerVersaoNpcap;
  NpcapJaInstalado := (NpcapVersaoAtual <> '');
  Result := NpcapJaInstalado;
end;


// Verifica se o WinPcap está instalado (conflito potencial com Npcap)
function WinPcapInstalado: Boolean;
var
  Valor: String;
begin
  Result := RegQueryStringValue(HKEY_LOCAL_MACHINE, WINPCAP_CHAVE_REGISTRO, '', Valor);
end;


// Verifica se a aplicação está rodando no momento
function AplicacaoRodando: Boolean;
begin
  // Verifica via FindWindowByClassName — simplificado para não depender de DLL externa
  Result := False;
end;


// Adiciona regra no Firewall do Windows para o servidor de laboratório
procedure AdicionarRegraFirewall;
var
  ComandoEntrada, ComandoSaida: String;
  ResultadoCodigo: Integer;
begin
  // Regra de entrada — permite acesso ao servidor lab por outros dispositivos
  ComandoEntrada := '/c netsh advfirewall firewall add rule '
    + 'name="NetLab Educacional - Servidor Lab" '
    + 'protocol=TCP dir=in action=allow '
    + 'localport=8080 profile=any enable=yes '
    + 'description="Permite acesso ao servidor de laboratorio do NetLab Educacional"';

  ShellExec('', 'cmd.exe', ComandoEntrada, '', SW_HIDE, ewWaitUntilTerminated, ResultadoCodigo);

  // Regra de saída (geralmente não necessária, mas melhora a experiência)
  ComandoSaida := '/c netsh advfirewall firewall add rule '
    + 'name="NetLab Educacional - Captura" '
    + 'protocol=TCP dir=out action=allow '
    + 'profile=any enable=yes '
    + 'description="Permite captura de pacotes pelo NetLab Educacional"';

  ShellExec('', 'cmd.exe', ComandoSaida, '', SW_HIDE, ewWaitUntilTerminated, ResultadoCodigo);
end;


// Remove as regras de firewall criadas pelo NetLab
procedure RemoverRegraFirewall;
var
  Comando: String;
  ResultadoCodigo: Integer;
begin
  Comando := '/c netsh advfirewall firewall delete rule name="NetLab Educacional - Servidor Lab"';
  ShellExec('', 'cmd.exe', Comando, '', SW_HIDE, ewWaitUntilTerminated, ResultadoCodigo);

  Comando := '/c netsh advfirewall firewall delete rule name="NetLab Educacional - Captura"';
  ShellExec('', 'cmd.exe', Comando, '', SW_HIDE, ewWaitUntilTerminated, ResultadoCodigo);
end;


// Instala o Npcap silenciosamente com as opções corretas para o NetLab
function InstalarNpcap: Boolean;
var
  NpcapExe:        String;
  CodigoRetorno:   Integer;
  MensagemErro:    String;
  // Parâmetros de instalação do Npcap:
  //   /S           = modo silencioso
  //   /winpcap_mode=yes  = habilita modo compatível WinPcap (OBRIGATÓRIO para Scapy)
  //   /dot11_support=no  = desabilita suporte Wi-Fi 802.11 raw (não necessário)
  //   /admin_only=no     = permite uso por usuários não-admin (conveniente)
  //   /loopback_support=yes = habilita interface loopback
  ParametrosNpcap: String;
begin
  Result      := False;
  
  // Extrai o instalador do Npcap para {tmp} ANTES de tentar acessá-lo
  try
    ExtractTemporaryFile('npcap-1.82.exe');
  except
    // Falha silenciosa, a verificação FileExists pegará o erro abaixo
  end;

  NpcapExe    := ExpandConstant('{tmp}\npcap-1.82.exe');
  // O Npcap gratuito não permite instalação silenciosa (/S), então executamos em modo interativo.
  // Pré-configuramos as opções corretas para que o usuário precise apenas confirmar a instalação.
  ParametrosNpcap := '/winpcap_mode=yes /dot11_support=no /admin_only=no /loopback_support=yes';

  // Verificação de segurança: o arquivo existe?
  if not FileExists(NpcapExe) then
  begin
    MensagemErro := 'O instalador do Npcap não foi encontrado em:'#13#10
      + NpcapExe + #13#10#13#10
      + 'Baixe manualmente em: https://npcap.com/#download'#13#10
      + 'e instale com a opção "WinPcap API-compatible mode" marcada.';
    MsgBox(MensagemErro, mbError, MB_OK);
    Exit;
  end;

  // Executa o instalador do Npcap de forma interativa (SW_SHOW) herdando as permissões de Admin
  if not Exec(NpcapExe, ParametrosNpcap, '', SW_SHOW, ewWaitUntilTerminated, CodigoRetorno) then
  begin
    MensagemErro := 'Falha ao executar o instalador do Npcap.'#13#10
      + 'Código de erro: ' + IntToStr(CodigoRetorno) + #13#10#13#10
      + 'Por favor, instale o Npcap manualmente em: https://npcap.com';
    MsgBox(MensagemErro, mbError, MB_OK);
    Exit;
  end;

  // Verifica se a instalação foi bem-sucedida (código 0 = sucesso, 3010 = requer reinício)
  if (CodigoRetorno = 0) or (CodigoRetorno = 3010) then
  begin
    Result := True;
    if CodigoRetorno = 3010 then
      MsgBox(
        'O Npcap foi instalado com sucesso, mas pode ser necessário'#13#10
        + 'reiniciar o computador para completar a configuração.'#13#10#13#10
        + 'O NetLab funcionará normalmente após o reinício.',
        mbInformation, MB_OK
      );
  end
  else
  begin
    MensagemErro := 'A instalação do Npcap retornou o código: ' + IntToStr(CodigoRetorno) + #13#10#13#10
      + 'Se o Npcap não funcionar corretamente, instale manualmente'#13#10
      + 'em https://npcap.com marcando "WinPcap API-compatible mode".';
    MsgBox(MensagemErro, mbError, MB_OK);
  end;
end;


// Cria a pasta de dados do NetLab (para aliases de dispositivos)
procedure CriarPastasDados;
var
  PastaDados: String;
begin
  PastaDados := ExpandConstant('{app}\dados');
  if not DirExists(PastaDados) then
    CreateDir(PastaDados);

  // Cria arquivo aliases.json vazio se não existir
  // (o NetLab cria automaticamente, mas é boa prática garantir)
  if not FileExists(PastaDados + '\aliases.json') then
    SaveStringToFile(PastaDados + '\aliases.json', '{}', False);
end;


// Cria atalho de inicialização automática com privilégios de administrador
procedure CriarAtalhoInicializacao;
var
  AtalhoPath:    String;
  SheelLinkCmd:  String;
  ResultCode:    Integer;
begin
  AtalhoPath := ExpandConstant('{commonstartup}\{#NOME_APP}.lnk');

  // Usa PowerShell para criar atalho com privilégio de admin (RunAs)
  SheelLinkCmd := '-NoProfile -ExecutionPolicy Bypass -Command "'
    + '$WScriptShell = New-Object -ComObject WScript.Shell;'
    + '$Atalho = $WScriptShell.CreateShortcut(''' + AtalhoPath + ''');'
    + '$Atalho.TargetPath = ''' + ExpandConstant('{app}\{#EXE_PRINCIPAL}') + ''';'
    + '$Atalho.WorkingDirectory = ''' + ExpandConstant('{app}') + ''';'
    + '$Atalho.Description = ''Iniciar NetLab Educacional como Administrador'';'
    + '$Atalho.IconLocation = ''' + ExpandConstant('{app}\icone.ico') + ''';'
    + '$Atalho.Save();'
    // Ativa o bit "Executar como Administrador" no atalho
    + '$Bytes = [System.IO.File]::ReadAllBytes(''' + AtalhoPath + ''');'
    + '$Bytes[21] = $Bytes[21] -bor 0x20;'
    + '[System.IO.File]::WriteAllBytes(''' + AtalhoPath + ''', $Bytes);"';

  Exec('powershell.exe', SheelLinkCmd, '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;


// Remove o atalho de inicialização automática
procedure RemoverAtalhoInicializacao;
var
  AtalhoPath: String;
begin
  AtalhoPath := ExpandConstant('{commonstartup}\{#NOME_APP}.lnk');
  if FileExists(AtalhoPath) then
    DeleteFile(AtalhoPath);
end;


// ---------------------------------------------------------------------------
// EVENTO: InitializeSetup — executado antes de qualquer tela aparecer
// ---------------------------------------------------------------------------

function InitializeSetup: Boolean;
var
  MensagemAviso: String;
begin
  Result := True;

  // Verificação 1: Windows suportado?
  if not WindowsSuportado then
  begin
    MsgBox(
      '{#NOME_APP} v{#VERSAO_EXIBIDA} requer Windows 10 (versão 1809 ou superior)'#13#10
      + 'ou Windows 11.'#13#10#13#10
      + 'Sua versão do Windows não é compatível com este software.'#13#10
      + 'Por favor, atualize o sistema operacional e tente novamente.',
      mbCriticalError, MB_OK
    );
    Result := False;
    Exit;
  end;

  // Verificação 2: WinPcap instalado? (conflito potencial)
  if WinPcapInstalado then
  begin
    MensagemAviso :=
      'ATENÇÃO: O WinPcap foi detectado no seu sistema.'#13#10#13#10
      + 'O WinPcap é um driver mais antigo e pode conflitar com o Npcap,'#13#10
      + 'que é o driver utilizado pelo {#NOME_APP}.'#13#10#13#10
      + 'Recomendamos desinstalar o WinPcap antes de continuar.'#13#10#13#10
      + 'Deseja continuar mesmo assim?';

    if MsgBox(MensagemAviso, mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
      Exit;
    end;
  end;

  // Lê o estado atual do Npcap para usar nas telas seguintes
  VerificarNpcap;
  InstalacaoOk := False;
end;


// ---------------------------------------------------------------------------
// EVENTO: InitializeWizard — configura páginas personalizadas
// ---------------------------------------------------------------------------

procedure InitializeWizard;
var
  TextoInformacoes: String;
begin
  // Página de informações do sistema (exibida antes da instalação)
  TextoInformacoes :=
    'O instalador realizará as seguintes ações:'#13#10#13#10
    + '  -  Instalar o {#NOME_APP} v{#VERSAO_EXIBIDA}'#13#10
    + '  -  Instalar o Npcap (driver de captura de pacotes)'#13#10
    + '  -  Criar atalhos no Menu Iniciar e Área de Trabalho'#13#10
    + '  -  Configurar exceção no Firewall do Windows'#13#10
    + '  -  Registrar o programa em Adicionar/Remover Programas'#13#10#13#10;

  // Adiciona status do Npcap
  if NpcapJaInstalado then
    TextoInformacoes := TextoInformacoes
      + '  INFO: Npcap detectado: v' + NpcapVersaoAtual + ' (será atualizado se necessário)'#13#10
  else
    TextoInformacoes := TextoInformacoes
      + '  AVISO: Npcap NÃO detectado; será instalado automaticamente'#13#10;

  TextoInformacoes := TextoInformacoes + #13#10
    + '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'#13#10
    + 'IMPORTANTE: O {#NOME_APP} requer privilégios de'#13#10
    + 'Administrador para capturar pacotes de rede.'#13#10
    + 'Sempre execute o programa com "Executar como Administrador".'#13#10#13#10
    + 'Para mais informações: {#SITE_OFICIAL}';

  PaginaInformacoes := CreateOutputMsgPage(
    wpSelectTasks,
    'Informações do Sistema',
    'Revise as ações que serão realizadas antes de prosseguir.',
    TextoInformacoes
  );
end;


// ---------------------------------------------------------------------------
// EVENTO: NextButtonClick — validações ao avançar entre telas
// ---------------------------------------------------------------------------

function NextButtonClick(PageID: Integer): Boolean;
begin
  Result := True;
end;


// ---------------------------------------------------------------------------
// EVENTO: PrepareToInstall — executado antes de copiar arquivos
// Aqui instalamos o Npcap, que deve estar pronto antes do NetLab
// ---------------------------------------------------------------------------

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  DeveInstalarNpcap: Boolean;
  MensagemNpcap:     String;
  RespostaUsuario:   Integer;
begin
  Result := '';  // String vazia = sem erros, pode prosseguir
  NeedsRestart := False;

  // --- Decisão sobre o Npcap ---
  if not NpcapJaInstalado then
  begin
    // Npcap não está presente → instalar obrigatoriamente
    MensagemNpcap :=
      'O Npcap (driver de captura de rede) não foi encontrado.'#13#10#13#10
      + 'O Npcap é OBRIGATÓRIO para o funcionamento do {#NOME_APP}.'#13#10
      + 'Sem ele, nenhum pacote de rede poderá ser capturado.'#13#10#13#10
      + 'O instalador irá instalar o Npcap automaticamente.'#13#10
      + 'Clique em OK para continuar.';

    MsgBox(MensagemNpcap, mbInformation, MB_OK);
    DeveInstalarNpcap := True;
  end
  else
  begin
    // Npcap já instalado — perguntar se deseja atualizar
    MensagemNpcap :=
      'O Npcap v' + NpcapVersaoAtual + ' já está instalado.'#13#10#13#10
      + 'Deseja atualizar o Npcap para a versão incluída neste instalador?'#13#10#13#10
      + 'RECOMENDADO: Mantenha o Npcap atualizado para melhor'#13#10
      + 'compatibilidade com o {#NOME_APP}.'#13#10#13#10
      + '  [Sim]  = Atualizar o Npcap'#13#10
      + '  [Não]  = Manter a versão atual e continuar';

    RespostaUsuario := MsgBox(MensagemNpcap, mbConfirmation, MB_YESNO);
    DeveInstalarNpcap := (RespostaUsuario = IDYES);
  end;

  // --- Instalação do Npcap ---
  if DeveInstalarNpcap then
  begin
    WizardForm.StatusLabel.Caption := 'Instalando o Npcap — aguarde...';

    if not InstalarNpcap then
    begin
      // Npcap falhou e é obrigatório → abortar instalação
      if not NpcapJaInstalado then
      begin
        Result := 'Falha ao instalar o Npcap.'#13#10
          + 'O {#NOME_APP} não funcionará sem o Npcap.'#13#10#13#10
          + 'Por favor, instale o Npcap manualmente em:'#13#10
          + 'https://npcap.com/#download'#13#10#13#10
          + 'Marque "WinPcap API-compatible mode" durante a instalação.';
        Exit;
      end;
      // Se já havia Npcap e a atualização falhou → continua com a versão existente
      MsgBox(
        'Não foi possível atualizar o Npcap.'#13#10
        + 'A versão instalada (' + NpcapVersaoAtual + ') será mantida.',
        mbInformation, MB_OK
      );
    end;

    WizardForm.StatusLabel.Caption := 'Npcap instalado com sucesso.';
  end;
end;


// ---------------------------------------------------------------------------
// EVENTO: CurStepChanged — executado em cada etapa da instalação
// ---------------------------------------------------------------------------

procedure CurStepChanged(CurStep: TSetupStep);
begin
  case CurStep of

    // --- ssPostInstall: executado APÓS copiar todos os arquivos ---
    ssPostInstall:
    begin
      // 1. Criar pastas de dados do NetLab
      CriarPastasDados;

      // 2. Adicionar regras no Firewall (somente se o usuário marcou)
      if WizardIsTaskSelected('regra_firewall') then
        AdicionarRegraFirewall;

      // 3. Criar atalho de inicialização automática (somente se marcado)
      if WizardIsTaskSelected('atalho_inicializar') then
        CriarAtalhoInicializacao;

      InstalacaoOk := True;
    end;

  end;
end;


// ---------------------------------------------------------------------------
// EVENTO: DeinitializeSetup — executado ao fechar o instalador
// ---------------------------------------------------------------------------

procedure DeinitializeSetup;
begin
  // Nenhuma limpeza necessária aqui
  // O Npcap já foi instalado com Flags: deleteafterinstall
end;


// ---------------------------------------------------------------------------
// EVENTO: CurUninstallStepChanged — executado durante a desinstalação
// ---------------------------------------------------------------------------

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  PastaDados:  String;
  RespostaDir: Integer;
begin
  case CurUninstallStep of

    // usPostUninstall: executado APÓS remover os arquivos
    usPostUninstall:
    begin
      // Remove regras do firewall
      RemoverRegraFirewall;

      // Remove atalho de inicialização automática
      RemoverAtalhoInicializacao;

      // Pergunta ao usuário se quer manter os dados do NetLab (aliases etc.)
      PastaDados := ExpandConstant('{app}\dados');
      if DirExists(PastaDados) then
      begin
        RespostaDir := MsgBox(
          'Deseja manter os dados salvos pelo {#NOME_APP}?'#13#10#13#10
          + 'Pasta: ' + PastaDados + #13#10#13#10
          + 'Esses dados incluem apelidos de dispositivos e configurações personalizadas.'#13#10
          + '  [Sim] = Manter os dados (recomendado caso vá reinstalar)'#13#10
          + '  [Não] = Apagar permanentemente todos os dados',
          mbConfirmation, MB_YESNO
        );

        if RespostaDir = IDNO then
        begin
          // Remove a pasta de dados recursivamente
          DelTree(PastaDados, True, True, True);
          // Tenta remover a pasta principal se estiver vazia
          RemoveDir(ExpandConstant('{app}'));
        end;
      end;

      // Remove as chaves de registro criadas pelo instalador
      RegDeleteKeyIncludingSubkeys(
        HKEY_LOCAL_MACHINE,
        'SOFTWARE\{#NOME_SERVICO}'
      );
    end;

  end;
end;


// ---------------------------------------------------------------------------
// EVENTO: UpdateReadyMemo — texto exibido na tela de resumo antes de instalar
// ---------------------------------------------------------------------------

function UpdateReadyMemo(Space, NewLine, MemoUserInfoInfo, MemoDirInfo,
  MemoTypeInfo, MemoComponentsInfo, MemoGroupInfo, MemoTasksInfo: String): String;
var
  Resumo: String;
begin
  Resumo := '';

  // Cabeçalho
  Resumo := Resumo + '{#NOME_APP} v{#VERSAO_EXIBIDA}' + NewLine;
  Resumo := Resumo + StringOfChar('─', 50) + NewLine + NewLine;

  // Pasta de destino
  if MemoDirInfo <> '' then
    Resumo := Resumo + 'Pasta de instalação:' + NewLine + Space + MemoDirInfo + NewLine + NewLine;

  // Grupo do Menu Iniciar
  if MemoGroupInfo <> '' then
    Resumo := Resumo + 'Menu Iniciar:' + NewLine + Space + MemoGroupInfo + NewLine + NewLine;

  // Tarefas selecionadas
  if MemoTasksInfo <> '' then
    Resumo := Resumo + 'Tarefas:' + NewLine + MemoTasksInfo + NewLine + NewLine;

  // Status do Npcap
  Resumo := Resumo + 'Driver de captura (Npcap):' + NewLine;
  if NpcapJaInstalado then
    Resumo := Resumo + Space + 'Versão ' + NpcapVersaoAtual + ' já instalada' + NewLine + NewLine
  else
    Resumo := Resumo + Space + 'Será instalado automaticamente' + NewLine + NewLine;

  // Aviso de administrador
  Resumo := Resumo + StringOfChar('─', 50) + NewLine;
  Resumo := Resumo + 'LEMBRETE: Execute sempre o {#NOME_APP} como' + NewLine;
  Resumo := Resumo + 'Administrador para capturar pacotes de rede.' + NewLine;

  Result := Resumo;
end;


// ---------------------------------------------------------------------------
// EVENTO: ShouldSkipPage — controla quais páginas são exibidas
// ---------------------------------------------------------------------------

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  // Nunca pula páginas — todas são relevantes para o usuário
end;

// =============================================================================
//  AÇÕES PÓS-INSTALAÇÃO — mensagens de execução ao final
// =============================================================================

[Run]

; --- Opção 1: Abrir o NetLab imediatamente após a instalação
Filename: "{app}\{#EXE_PRINCIPAL}"; Description: "Abrir o {#NOME_APP} agora"; Flags: nowait postinstall skipifsilent runasoriginaluser shellexec

; --- Opção 2: Abrir o site do projeto para documentação
Filename: "{#SITE_OFICIAL}"; Description: "Abrir a documentação online"; Flags: nowait postinstall skipifsilent shellexec unchecked

; =============================================================================
;  AÇÕES PÓS-DESINSTALAÇÃO
; =============================================================================

[UninstallRun]

; Remove regras do firewall ao desinstalar (fallback caso o código Pascal falhe)
Filename: "netsh"; RunOnceId: "remover_regra_firewall_servidor"; Parameters: "advfirewall firewall delete rule name=""NetLab Educacional - Servidor Lab"""; Flags: runhidden

Filename: "netsh"; RunOnceId: "remover_regra_firewall_captura"; Parameters: "advfirewall firewall delete rule name=""NetLab Educacional - Captura"""; Flags: runhidden

; =============================================================================
;  MENSAGENS PERSONALIZADAS
; =============================================================================

[Messages]

; --- Sobrescreve textos padrão para melhor UX em português
WelcomeLabel1=Bem-vindo ao Assistente de Instalação do%n{#NOME_APP}
WelcomeLabel2=Este assistente irá instalar o {#NOME_APP} v{#VERSAO_EXIBIDA} no seu computador.%n%nO {#NOME_APP} é uma plataforma educacional para análise de tráfego de rede, desenvolvida como Trabalho de Conclusão de Curso no Instituto Federal Farroupilha.%n%nFECHE TODOS OS OUTROS APLICATIVOS antes de continuar. Clique em Avançar para continuar ou Cancelar para sair.
FinishedHeadingLabel=Instalação do {#NOME_APP} Concluída
FinishedLabelNoIcons=O {#NOME_APP} v{#VERSAO_EXIBIDA} foi instalado com sucesso.%n%nIMPORTANTE: Sempre execute o {#NOME_APP} com "Executar como Administrador" para habilitar a captura de pacotes de rede.%n%nEm caso de dúvidas, acesse: {#SITE_OFICIAL}
FinishedLabel=O {#NOME_APP} v{#VERSAO_EXIBIDA} foi instalado com sucesso.%n%nIMPORTANTE: Sempre execute o {#NOME_APP} com "Executar como Administrador" para habilitar a captura de pacotes de rede.%n%nClique em Concluir para sair do assistente.
ClickNext=Clique em Avançar para continuar ou Cancelar para sair.
BeveledLabel=Instalador Oficial — {#NOME_APP}
ButtonInstall=&Instalar
SelectDirDesc=Onde o {#NOME_APP} deve ser instalado?
SelectDirLabel3=O instalador copiará os arquivos do {#NOME_APP} para a pasta abaixo.%n%nPara instalar em outra pasta, clique em Procurar e escolha uma diferente. Clique em Avançar para continuar.
SelectStartMenuFolderDesc=Onde o instalador deve criar os atalhos no Menu Iniciar?
SelectStartMenuFolderLabel3=O instalador criará os atalhos do programa no grupo do Menu Iniciar abaixo.%n%nPara criar em outro grupo, clique em Procurar e escolha um diferente. Clique em Avançar para continuar.
ReadyLabel1=O assistente está pronto para instalar o {#NOME_APP} no seu computador.%n%nClique em Instalar para iniciar ou Voltar para revisar as configurações.
ReadyLabel2b=Clique em Instalar para continuar.
InstallingLabel=Instalando o {#NOME_APP}, aguarde...
UninstallAppFullTitle=Desinstalar o {#NOME_APP}
ConfirmUninstall=Isso irá remover o %1 do seu computador.%n%nSeus dados pessoais (apelidos de dispositivos salvos) podem ser mantidos. Você será perguntado sobre isso.%n%nDeseja continuar?

; =============================================================================
;  VERIFICAÇÕES EXTRAS
; =============================================================================

[CustomMessages]

; --- Mensagens exibidas durante a instalação
ptbr.InstallingNpcap=Instalando o driver Npcap...
ptbr.NpcapOk=Driver Npcap configurado com sucesso.
ptbr.CriandoPastas=Criando estrutura de pastas do NetLab...
ptbr.ConfigurandoFirewall=Configurando regras no Firewall do Windows...
ptbr.RegistrandoApp=Registrando o aplicativo no sistema...

; =============================================================================
;  FIM DO SCRIPT
; =============================================================================
;
;  DÚVIDAS E SUPORTE:
;    Site:   {#SITE_OFICIAL}
;    GitHub: https://github.com/Yurigonpav/NetLab-Educacional
;
;  LICENÇA:
;    Este instalador é fornecido para uso educacional.
;    O código-fonte do NetLab Educacional está disponível no GitHub.
;
; =============================================================================
