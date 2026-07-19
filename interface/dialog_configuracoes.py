"""
interface/dialog_configuracoes.py
Janela de configurações avançadas do NetLab.

Organizada em 4 abas:
  - Geral        : limite de hosts, timers, modo Wi-Fi
  - Filtros       : sub-redes priorizadas/excluídas, apenas local, OUI
  - Gerenciamento : adicionar/remover hosts manuais e excluídos
  - Avançado      : parâmetros ARP, exportar/importar configurações
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Optional

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QIcon, QPalette
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QDoubleSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from utils.config_manager import ConfigManager


# ── Helpers visuais ──────────────────────────────────────────────────────────

_ESTILO_DIALOG = """
QDialog {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}
QTabWidget::pane {
    border: 1px solid #30363d;
    border-radius: 6px;
    background: #161b22;
    top: -1px;
}
QTabBar::tab {
    background: #0d1117;
    color: #8b949e;
    padding: 8px 18px;
    border: 1px solid #30363d;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    min-width: 100px;
}
QTabBar::tab:selected {
    background: #161b22;
    color: #58a6ff;
    border-color: #30363d;
    border-bottom: 1px solid #161b22;
}
QTabBar::tab:hover:!selected {
    background: #21262d;
    color: #c9d1d9;
}
QGroupBox {
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    color: #8b949e;
    font-size: 11px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #58a6ff;
    font-weight: bold;
}
QLabel {
    color: #c9d1d9;
}
QLabel.subtitulo {
    color: #8b949e;
    font-size: 10px;
}
QSpinBox, QDoubleSpinBox, QLineEdit {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 4px;
    color: #c9d1d9;
    padding: 4px 8px;
    selection-background-color: #1f6feb;
}
QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
    border-color: #58a6ff;
}
QCheckBox {
    color: #c9d1d9;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid #30363d;
    border-radius: 3px;
    background: #0d1117;
}
QCheckBox::indicator:checked {
    background: #1f6feb;
    border-color: #58a6ff;
    image: none;
}
QListWidget {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 4px;
    color: #c9d1d9;
    outline: none;
}
QListWidget::item {
    padding: 4px 8px;
    border-bottom: 1px solid #21262d;
}
QListWidget::item:selected {
    background: #1f6feb;
    color: #fff;
}
QListWidget::item:hover:!selected {
    background: #21262d;
}
QPushButton {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 5px;
    color: #c9d1d9;
    padding: 5px 14px;
    font-size: 11px;
}
QPushButton:hover {
    background: #30363d;
    border-color: #58a6ff;
    color: #58a6ff;
}
QPushButton:pressed {
    background: #0d1117;
}
QPushButton#btn_primario {
    background: #1f6feb;
    border-color: #1f6feb;
    color: #fff;
    font-weight: bold;
}
QPushButton#btn_primario:hover {
    background: #388bfd;
    border-color: #388bfd;
    color: #fff;
}
QPushButton#btn_perigo {
    background: #da3633;
    border-color: #da3633;
    color: #fff;
}
QPushButton#btn_perigo:hover {
    background: #f85149;
    border-color: #f85149;
}
QPushButton#btn_sucesso {
    background: #238636;
    border-color: #238636;
    color: #fff;
}
QPushButton#btn_sucesso:hover {
    background: #2ea043;
    border-color: #2ea043;
}
QDialogButtonBox QPushButton {
    min-width: 90px;
}
QScrollArea {
    border: none;
    background: transparent;
}
"""


def _separador() -> QFrame:
    linha = QFrame()
    linha.setFrameShape(QFrame.Shape.HLine)
    linha.setStyleSheet("color: #30363d;")
    return linha


def _label_secao(texto: str, cor: str = "#58a6ff") -> QLabel:
    lbl = QLabel(texto)
    lbl.setStyleSheet(f"color: {cor}; font-weight: bold; font-size: 12px; margin-top: 4px;")
    return lbl


def _label_ajuda(texto: str) -> QLabel:
    lbl = QLabel(texto)
    lbl.setStyleSheet("color: #6e7681; font-size: 10px; font-style: italic;")
    lbl.setWordWrap(True)
    return lbl


def _grupo(titulo: str) -> QGroupBox:
    g = QGroupBox(titulo)
    return g


# ── Aba: Geral ───────────────────────────────────────────────────────────────

class _AbaGeral(QWidget):
    def __init__(self, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self._cfg = cfg
        self._montar_ui()
        self._carregar_valores()

    def _montar_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        conteudo = QWidget()
        layout = QVBoxLayout(conteudo)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        # ── Hosts ─────────────────────────────────────────────────────────────
        g_hosts = _grupo("Limite de Dispositivos")
        v_hosts = QVBoxLayout(g_hosts)
        v_hosts.setSpacing(8)

        h_limite = QHBoxLayout()
        lbl_limite = QLabel("Máximo de hosts a exibir/analisar:")
        lbl_limite.setFixedWidth(230)
        self._spin_limite = QSpinBox()
        self._spin_limite.setRange(10, 4096)
        self._spin_limite.setSuffix(" hosts")
        self._spin_limite.setFixedWidth(130)
        self._spin_limite.setToolTip(
            "Define quantos dispositivos serão processados durante a varredura ARP.\n"
            "Aumente para redes maiores. O padrão é 100."
        )
        h_limite.addWidget(lbl_limite)
        h_limite.addWidget(self._spin_limite)
        h_limite.addStretch()
        v_hosts.addLayout(h_limite)
        v_hosts.addWidget(_label_ajuda(
            "Atenção: valores muito altos podem tornar a varredura mais lenta. "
            "Recomenda-se até 500 para redes comuns e até 4096 para redes corporativas."
        ))
        layout.addWidget(g_hosts)

        # ── Timers ────────────────────────────────────────────────────────────
        g_timer = _grupo("Timers de Redescoberta")
        v_timer = QVBoxLayout(g_timer)
        v_timer.setSpacing(8)

        h_timer = QHBoxLayout()
        lbl_timer = QLabel("Intervalo de redescoberta automática:")
        lbl_timer.setFixedWidth(230)
        self._spin_timer = QSpinBox()
        self._spin_timer.setRange(10, 600)
        self._spin_timer.setSuffix(" segundos")
        self._spin_timer.setFixedWidth(130)
        self._spin_timer.setToolTip("Intervalo entre varreduras ARP automáticas.")
        h_timer.addWidget(lbl_timer)
        h_timer.addWidget(self._spin_timer)
        h_timer.addStretch()
        v_timer.addLayout(h_timer)

        h_timeout = QHBoxLayout()
        lbl_timeout = QLabel("Timeout de resposta ARP:")
        lbl_timeout.setFixedWidth(230)
        self._spin_timeout = QDoubleSpinBox()
        self._spin_timeout.setRange(0.2, 10.0)
        self._spin_timeout.setSingleStep(0.2)
        self._spin_timeout.setSuffix(" s")
        self._spin_timeout.setDecimals(1)
        self._spin_timeout.setFixedWidth(130)
        h_timeout.addWidget(lbl_timeout)
        h_timeout.addWidget(self._spin_timeout)
        h_timeout.addStretch()
        v_timer.addLayout(h_timeout)

        v_timer.addWidget(_label_ajuda(
            "Timeout maior aumenta a chance de detectar hosts lentos, "
            "mas prolonga a varredura."
        ))
        layout.addWidget(g_timer)

        # ── Modo de operação ─────────────────────────────────────────────────
        g_modo = _grupo("Modo de Operação")
        v_modo = QVBoxLayout(g_modo)
        self._chk_apenas_local = QCheckBox(
            "Mostrar apenas hosts da sub-rede local (filtrar sub-redes externas)"
        )
        self._chk_apenas_local.setToolTip(
            "Quando ativado, hosts de outras sub-redes detectados via ARP passivo\n"
            "não serão adicionados à topologia. Útil em redes com múltiplos segmentos."
        )
        v_modo.addWidget(self._chk_apenas_local)
        v_modo.addWidget(_label_ajuda(
            "Recomendado para ambientes de laboratório onde a interface captura tráfego "
            "de múltiplas sub-redes (ex.: VLANs, VPNs)."
        ))
        layout.addWidget(g_modo)

        layout.addStretch()
        scroll.setWidget(conteudo)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def _carregar_valores(self):
        self._spin_limite.setValue(self._cfg.obter("limite_hosts", 100))
        self._spin_timer.setValue(self._cfg.obter("timer_redescoberta_s", 30))
        self._spin_timeout.setValue(self._cfg.obter("timeout_arp_s", 1.8))
        self._chk_apenas_local.setChecked(self._cfg.obter("apenas_subrede_local", False))

    def coletar_valores(self) -> dict:
        return {
            "limite_hosts":         self._spin_limite.value(),
            "timer_redescoberta_s": self._spin_timer.value(),
            "timeout_arp_s":        round(self._spin_timeout.value(), 1),
            "apenas_subrede_local": self._chk_apenas_local.isChecked(),
        }


# ── Aba: Filtros ─────────────────────────────────────────────────────────────

class _AbaFiltros(QWidget):
    def __init__(self, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self._cfg = cfg
        self._montar_ui()
        self._carregar_valores()

    def _montar_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        conteudo = QWidget()
        layout = QVBoxLayout(conteudo)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        # ── Sub-redes priorizadas ─────────────────────────────────────────────
        g_prio = _grupo("Sub-redes Priorizadas")
        v_prio = QVBoxLayout(g_prio)
        v_prio.addWidget(_label_ajuda(
            "Hosts dessas sub-redes serão varridos primeiro, garantindo que "
            "apareçam na topologia mesmo quando o limite for atingido."
        ))
        self._lista_prio = QListWidget()
        self._lista_prio.setMaximumHeight(120)
        v_prio.addWidget(self._lista_prio)
        h_prio = QHBoxLayout()
        self._edit_prio = QLineEdit()
        self._edit_prio.setPlaceholderText("ex.: 192.168.1.0/24")
        btn_add_prio = QPushButton("+ Adicionar")
        btn_add_prio.setObjectName("btn_sucesso")
        btn_rem_prio = QPushButton("− Remover")
        btn_rem_prio.setObjectName("btn_perigo")
        btn_add_prio.clicked.connect(self._adicionar_priorizada)
        btn_rem_prio.clicked.connect(lambda: self._remover_item(self._lista_prio))
        h_prio.addWidget(self._edit_prio, 1)
        h_prio.addWidget(btn_add_prio)
        h_prio.addWidget(btn_rem_prio)
        v_prio.addLayout(h_prio)
        layout.addWidget(g_prio)

        # ── Sub-redes excluídas ───────────────────────────────────────────────
        g_excl = _grupo("Sub-redes Excluídas")
        v_excl = QVBoxLayout(g_excl)
        v_excl.addWidget(_label_ajuda(
            "Qualquer host pertencente a essas sub-redes será ignorado pela topologia. "
            "Útil para excluir faixas como 169.254.0.0/16 (APIPA) ou 10.0.0.0/8."
        ))
        self._lista_excl = QListWidget()
        self._lista_excl.setMaximumHeight(120)
        v_excl.addWidget(self._lista_excl)
        h_excl = QHBoxLayout()
        self._edit_excl = QLineEdit()
        self._edit_excl.setPlaceholderText("ex.: 169.254.0.0/16")
        btn_add_excl = QPushButton("+ Adicionar")
        btn_add_excl.setObjectName("btn_sucesso")
        btn_rem_excl = QPushButton("− Remover")
        btn_rem_excl.setObjectName("btn_perigo")
        btn_add_excl.clicked.connect(self._adicionar_excluida)
        btn_rem_excl.clicked.connect(lambda: self._remover_item(self._lista_excl))
        h_excl.addWidget(self._edit_excl, 1)
        h_excl.addWidget(btn_add_excl)
        h_excl.addWidget(btn_rem_excl)
        v_excl.addLayout(h_excl)
        layout.addWidget(g_excl)

        # ── Filtro por OUI / fabricante ───────────────────────────────────────
        g_oui = _grupo("Filtro por Fabricante (OUI)")
        v_oui = QVBoxLayout(g_oui)
        v_oui.addWidget(_label_ajuda(
            "Se preenchido, apenas dispositivos cujo MAC começa com um desses prefixos "
            "serão exibidos. Deixe vazio para desativar o filtro."
        ))
        self._lista_oui = QListWidget()
        self._lista_oui.setMaximumHeight(100)
        v_oui.addWidget(self._lista_oui)
        h_oui = QHBoxLayout()
        self._edit_oui = QLineEdit()
        self._edit_oui.setPlaceholderText("ex.: b4:2e:99  ou  00:1a:2b")
        btn_add_oui = QPushButton("+ Adicionar")
        btn_add_oui.setObjectName("btn_sucesso")
        btn_rem_oui = QPushButton("− Remover")
        btn_rem_oui.setObjectName("btn_perigo")
        btn_add_oui.clicked.connect(self._adicionar_oui)
        btn_rem_oui.clicked.connect(lambda: self._remover_item(self._lista_oui))
        h_oui.addWidget(self._edit_oui, 1)
        h_oui.addWidget(btn_add_oui)
        h_oui.addWidget(btn_rem_oui)
        v_oui.addLayout(h_oui)
        layout.addWidget(g_oui)

        layout.addStretch()
        scroll.setWidget(conteudo)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def _carregar_valores(self):
        self._lista_prio.clear()
        self._lista_excl.clear()
        self._lista_oui.clear()
        self._edit_prio.clear()
        self._edit_excl.clear()
        self._edit_oui.clear()
        for cidr in self._cfg.subredes_priorizadas:
            self._lista_prio.addItem(cidr)
        for cidr in self._cfg.subredes_excluidas:
            self._lista_excl.addItem(cidr)
        for oui in self._cfg.filtro_oui:
            self._lista_oui.addItem(oui)

    def _validar_cidr(self, texto: str) -> Optional[str]:
        try:
            return str(ipaddress.ip_network(texto.strip(), strict=False))
        except ValueError:
            return None

    def _adicionar_priorizada(self):
        cidr = self._validar_cidr(self._edit_prio.text())
        if not cidr:
            QMessageBox.warning(self, "CIDR inválido",
                                "Digite um CIDR IPv4 válido, ex.: 192.168.1.0/24")
            return
        itens = [self._lista_prio.item(i).text() for i in range(self._lista_prio.count())]
        if cidr not in itens:
            self._lista_prio.addItem(cidr)
        self._edit_prio.clear()

    def _adicionar_excluida(self):
        cidr = self._validar_cidr(self._edit_excl.text())
        if not cidr:
            QMessageBox.warning(self, "CIDR inválido",
                                "Digite um CIDR IPv4 válido, ex.: 169.254.0.0/16")
            return
        itens = [self._lista_excl.item(i).text() for i in range(self._lista_excl.count())]
        if cidr not in itens:
            self._lista_excl.addItem(cidr)
        self._edit_excl.clear()

    def _adicionar_oui(self):
        texto = self._edit_oui.text().strip().lower().replace("-", ":")
        if not texto or len(texto.replace(":", "")) < 4:
            QMessageBox.warning(self, "OUI inválido",
                                "Digite pelo menos 2 octetos do MAC, ex.: b4:2e")
            return
        itens = [self._lista_oui.item(i).text() for i in range(self._lista_oui.count())]
        if texto not in itens:
            self._lista_oui.addItem(texto)
        self._edit_oui.clear()

    def _remover_item(self, lista: QListWidget):
        idx = lista.currentRow()
        if idx >= 0:
            lista.takeItem(idx)

    def _lista_para_lista(self, lista: QListWidget) -> list:
        return [lista.item(i).text() for i in range(lista.count())]

    def coletar_valores(self) -> dict:
        return {
            "subredes_priorizadas": self._lista_para_lista(self._lista_prio),
            "subredes_excluidas":   self._lista_para_lista(self._lista_excl),
            "filtro_oui":           self._lista_para_lista(self._lista_oui),
        }


# ── Aba: Gerenciamento de Hosts ──────────────────────────────────────────────

class _AbaGerenciamento(QWidget):
    def __init__(self, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self._cfg = cfg
        self._montar_ui()
        self._carregar_valores()

    def _montar_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        conteudo = QWidget()
        layout = QVBoxLayout(conteudo)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        # ── Hosts manuais ─────────────────────────────────────────────────────
        g_manual = _grupo("Hosts Adicionados Manualmente")
        v_manual = QVBoxLayout(g_manual)
        v_manual.addWidget(_label_ajuda(
            "Hosts manuais são sempre exibidos na topologia, independentemente "
            "do resultado da varredura ARP. Útil para dispositivos com firewall."
        ))
        self._lista_manual = QListWidget()
        self._lista_manual.setMaximumHeight(150)
        v_manual.addWidget(self._lista_manual)

        # Formulário de adição manual
        form = QFrame()
        form.setStyleSheet("QFrame { border: 1px solid #30363d; border-radius: 4px; padding: 4px; }")
        v_form = QVBoxLayout(form)
        v_form.setSpacing(6)

        h_ip = QHBoxLayout()
        lbl_ip = QLabel("IP:")
        lbl_ip.setFixedWidth(80)
        self._edit_manual_ip = QLineEdit()
        self._edit_manual_ip.setPlaceholderText("ex.: 192.168.1.50")
        h_ip.addWidget(lbl_ip)
        h_ip.addWidget(self._edit_manual_ip)
        v_form.addLayout(h_ip)

        h_host = QHBoxLayout()
        lbl_host = QLabel("Hostname:")
        lbl_host.setFixedWidth(80)
        self._edit_manual_hostname = QLineEdit()
        self._edit_manual_hostname.setPlaceholderText("ex.: Servidor-Principal (opcional)")
        h_host.addWidget(lbl_host)
        h_host.addWidget(self._edit_manual_hostname)
        v_form.addLayout(h_host)

        h_mac = QHBoxLayout()
        lbl_mac = QLabel("MAC:")
        lbl_mac.setFixedWidth(80)
        self._edit_manual_mac = QLineEdit()
        self._edit_manual_mac.setPlaceholderText("ex.: aa:bb:cc:dd:ee:ff (opcional)")
        h_mac.addWidget(lbl_mac)
        h_mac.addWidget(self._edit_manual_mac)
        v_form.addLayout(h_mac)

        h_nota = QHBoxLayout()
        lbl_nota = QLabel("Nota:")
        lbl_nota.setFixedWidth(80)
        self._edit_manual_nota = QLineEdit()
        self._edit_manual_nota.setPlaceholderText("Descrição opcional")
        h_nota.addWidget(lbl_nota)
        h_nota.addWidget(self._edit_manual_nota)
        v_form.addLayout(h_nota)

        h_btn_manual = QHBoxLayout()
        btn_add_manual = QPushButton("+ Adicionar Host Manual")
        btn_add_manual.setObjectName("btn_sucesso")
        btn_rem_manual = QPushButton("− Remover Selecionado")
        btn_rem_manual.setObjectName("btn_perigo")
        btn_add_manual.clicked.connect(self._adicionar_manual)
        btn_rem_manual.clicked.connect(self._remover_manual)
        h_btn_manual.addWidget(btn_add_manual)
        h_btn_manual.addWidget(btn_rem_manual)
        h_btn_manual.addStretch()
        v_form.addLayout(h_btn_manual)
        v_manual.addWidget(form)
        layout.addWidget(g_manual)

        # ── Hosts excluídos ───────────────────────────────────────────────────
        g_excl = _grupo("Hosts Excluídos da Topologia")
        v_excl = QVBoxLayout(g_excl)
        v_excl.addWidget(_label_ajuda(
            "IPs nesta lista não aparecem na topologia, mesmo que sejam detectados. "
            "Use para remover dispositivos irrelevantes ou ruidosos."
        ))
        self._lista_excl_host = QListWidget()
        self._lista_excl_host.setMaximumHeight(120)
        v_excl.addWidget(self._lista_excl_host)

        h_excl = QHBoxLayout()
        self._edit_excl_ip = QLineEdit()
        self._edit_excl_ip.setPlaceholderText("Adicionar IP manualmente: 192.168.1.99")
        btn_add_excl = QPushButton("+ Adicionar")
        btn_add_excl.setObjectName("btn_sucesso")
        btn_rem_excl = QPushButton("− Remover")
        btn_rem_excl.setObjectName("btn_perigo")
        btn_limpar_excl = QPushButton("Limpar Todos")
        btn_add_excl.clicked.connect(self._adicionar_excluido)
        btn_rem_excl.clicked.connect(self._remover_excluido)
        btn_limpar_excl.clicked.connect(self._limpar_excluidos)
        h_excl.addWidget(self._edit_excl_ip, 1)
        h_excl.addWidget(btn_add_excl)
        h_excl.addWidget(btn_rem_excl)
        h_excl.addWidget(btn_limpar_excl)
        v_excl.addLayout(h_excl)
        layout.addWidget(g_excl)

        layout.addStretch()
        scroll.setWidget(conteudo)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def _carregar_valores(self):
        self._lista_manual.clear()
        self._lista_excl_host.clear()
        self._edit_manual_ip.clear()
        self._edit_manual_hostname.clear()
        self._edit_manual_mac.clear()
        self._edit_manual_nota.clear()
        self._edit_excl_ip.clear()
        for h in self._cfg.hosts_manuais:
            item = QListWidgetItem(self._texto_host_manual(h))
            item.setData(Qt.ItemDataRole.UserRole, h)
            self._lista_manual.addItem(item)
        for ip in self._cfg.hosts_excluidos:
            self._lista_excl_host.addItem(ip)

    @staticmethod
    def _texto_host_manual(h: dict) -> str:
        parts = [h.get("ip", "")]
        if h.get("hostname"):
            parts.append(h["hostname"])
        if h.get("mac"):
            parts.append(h["mac"])
        if h.get("nota"):
            parts.append(f"({h['nota']})")
        return "  |  ".join(parts)

    def _adicionar_manual(self):
        ip = self._edit_manual_ip.text().strip()
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            QMessageBox.warning(self, "IP inválido", f"'{ip}' não é um endereço IPv4 válido.")
            return
        hostname = self._edit_manual_hostname.text().strip()
        mac      = self._edit_manual_mac.text().strip()
        nota     = self._edit_manual_nota.text().strip()
        h = {"ip": ip, "hostname": hostname, "mac": mac, "nota": nota}

        # Remove duplicata
        for i in range(self._lista_manual.count()):
            item = self._lista_manual.item(i)
            if item.text().startswith(ip + "  |") or item.text() == ip:
                self._lista_manual.takeItem(i)
                break
        self._lista_manual.addItem(self._texto_host_manual(h))
        # Armazena dado estruturado no UserRole
        item = self._lista_manual.item(self._lista_manual.count() - 1)
        item.setData(Qt.ItemDataRole.UserRole, h)

        self._edit_manual_ip.clear()
        self._edit_manual_hostname.clear()
        self._edit_manual_mac.clear()
        self._edit_manual_nota.clear()

    def _remover_manual(self):
        idx = self._lista_manual.currentRow()
        if idx >= 0:
            self._lista_manual.takeItem(idx)

    def _adicionar_excluido(self):
        ip = self._edit_excl_ip.text().strip()
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            QMessageBox.warning(self, "IP inválido", f"'{ip}' não é um endereço IPv4 válido.")
            return
        itens = [self._lista_excl_host.item(i).text() for i in range(self._lista_excl_host.count())]
        if ip not in itens:
            self._lista_excl_host.addItem(ip)
        self._edit_excl_ip.clear()

    def _remover_excluido(self):
        idx = self._lista_excl_host.currentRow()
        if idx >= 0:
            self._lista_excl_host.takeItem(idx)

    def _limpar_excluidos(self):
        resposta = QMessageBox.question(
            self, "Limpar exclusões",
            "Remover todos os IPs da lista de exclusão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            self._lista_excl_host.clear()

    def _hosts_manuais_da_lista(self) -> list:
        resultado = []
        for i in range(self._lista_manual.count()):
            item = self._lista_manual.item(i)
            dado = item.data(Qt.ItemDataRole.UserRole)
            if dado:
                resultado.append(dado)
            else:
                # Fallback: parsear o texto
                partes = item.text().split("  |  ")
                resultado.append({"ip": partes[0].strip(), "hostname": "", "mac": "", "nota": ""})
        return resultado

    def _hosts_excluidos_da_lista(self) -> list:
        return [self._lista_excl_host.item(i).text() for i in range(self._lista_excl_host.count())]

    def adicionar_ip_excluido_externo(self, ip: str):
        """Chamado externamente (ex.: menu de contexto da topologia) para adicionar um IP."""
        itens = [self._lista_excl_host.item(i).text() for i in range(self._lista_excl_host.count())]
        if ip not in itens:
            self._lista_excl_host.addItem(ip)

    def coletar_valores(self) -> dict:
        return {
            "hosts_manuais":  self._hosts_manuais_da_lista(),
            "hosts_excluidos": self._hosts_excluidos_da_lista(),
        }


# ── Aba: Avançado ─────────────────────────────────────────────────────────────

class _AbaAvancado(QWidget):
    def __init__(self, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self._cfg = cfg
        self._montar_ui()
        self._carregar_valores()

    def _montar_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        conteudo = QWidget()
        layout = QVBoxLayout(conteudo)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        # ── Parâmetros ARP ────────────────────────────────────────────────────
        g_arp = _grupo("Parâmetros de Varredura ARP")
        v_arp = QVBoxLayout(g_arp)

        # Informativo
        info = QLabel(
            "Os parâmetros ARP abaixo são técnicos e afetam diretamente o desempenho "
            "e a precisão da varredura. Modifique apenas se souber o que está fazendo."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #f0883e; font-size: 10px; margin-bottom: 4px;")
        v_arp.addWidget(info)

        campos_arp = [
            ("Batch ARP (hosts por lote):",     "spin_batch",    QSpinBox,       (1,  256, 1,  32,  " hosts")),
            ("Tentativas por host:",             "spin_tent",     QSpinBox,       (1,  10,  1,  2,   " x")),
            ("Intervalo entre pacotes (inter):", "spin_inter",    QDoubleSpinBox, (0.001, 1.0, 0.005, 0.02, " s")),
            ("Pausa entre rodadas:",             "spin_pausa",    QDoubleSpinBox, (0.0, 10.0, 0.1,  1.0,  " s")),
        ]
        self._spin_batch = None
        self._spin_tent  = None
        self._spin_inter = None
        self._spin_pausa = None

        for rotulo, attr, cls, (min_, max_, step, pad, suf) in campos_arp:
            h = QHBoxLayout()
            lbl = QLabel(rotulo)
            lbl.setFixedWidth(230)
            spin = cls()
            spin.setRange(min_, max_)
            if cls == QDoubleSpinBox:
                spin.setSingleStep(step)
                spin.setDecimals(3 if "inter" in attr else 1)
            else:
                spin.setSingleStep(int(step))
            spin.setSuffix(suf)
            spin.setValue(pad)
            spin.setFixedWidth(130)
            h.addWidget(lbl)
            h.addWidget(spin)
            h.addStretch()
            v_arp.addLayout(h)
            setattr(self, f"_{attr}", spin)

        layout.addWidget(g_arp)

        # ── Importar / Exportar ───────────────────────────────────────────────
        g_io = _grupo("Exportar / Importar Configurações")
        v_io = QVBoxLayout(g_io)
        v_io.addWidget(_label_ajuda(
            "Salve suas configurações em um arquivo externo para reutilizá-las "
            "em outros computadores ou reinstalações do NetLab."
        ))
        h_io = QHBoxLayout()
        btn_exportar = QPushButton("Exportar Config")
        btn_importar = QPushButton("Importar Config")
        btn_exportar.clicked.connect(self._exportar)
        btn_importar.clicked.connect(self._importar)
        h_io.addWidget(btn_exportar)
        h_io.addWidget(btn_importar)
        h_io.addStretch()
        v_io.addLayout(h_io)
        layout.addWidget(g_io)

        # ── Sobre as configurações ────────────────────────────────────────────
        g_info = _grupo("Informações")
        v_info = QVBoxLayout(g_info)
        import os
        from utils.config_manager import _caminho_config
        caminho = _caminho_config()
        lbl_caminho = QLabel(f"Arquivo de configuração: {caminho}")
        lbl_caminho.setStyleSheet("color: #6e7681; font-size: 10px;")
        lbl_caminho.setWordWrap(True)
        v_info.addWidget(lbl_caminho)
        layout.addWidget(g_info)

        layout.addStretch()
        scroll.setWidget(conteudo)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def _exportar(self):
        caminho, _ = QFileDialog.getSaveFileName(
            self, "Exportar Configurações", "netlab_config.json",
            "Arquivo JSON (*.json)"
        )
        if caminho:
            ok = self._cfg.exportar(caminho)
            if ok:
                QMessageBox.information(self, "Exportado", f"Configurações salvas em:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível exportar as configurações.")

    def _importar(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self, "Importar Configurações", "",
            "Arquivo JSON (*.json)"
        )
        if caminho:
            ok = self._cfg.importar(caminho)
            if ok:
                QMessageBox.information(
                    self, "Importado",
                    "Configurações importadas com sucesso!\n"
                    "Feche e reabra a janela de configurações para ver os valores atualizados."
                )
            else:
                QMessageBox.critical(self, "Erro", "Falha ao importar o arquivo. Verifique o formato JSON.")

    def _carregar_valores(self):
        self._spin_batch.setValue(self._cfg.obter("arp_batch", 32))
        self._spin_tent.setValue(self._cfg.obter("arp_tentativas", 2))
        self._spin_inter.setValue(self._cfg.obter("arp_inter", 0.02))
        self._spin_pausa.setValue(self._cfg.obter("arp_pausa", 1.0))

    def coletar_valores(self) -> dict:
        return {
            "arp_batch":    self._spin_batch.value(),
            "arp_tentativas": self._spin_tent.value(),
            "arp_inter":    round(self._spin_inter.value(), 3),
            "arp_pausa":    round(self._spin_pausa.value(), 1),
        }


# ── Diálogo principal ─────────────────────────────────────────────────────────

class DialogConfiguracoes(QDialog):
    """
    Janela de configurações avançadas do NetLab.
    Emite `configuracoes_aplicadas` com o dict de configurações ao ser aceito.
    """

    configuracoes_aplicadas = pyqtSignal(dict)

    def __init__(self, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self._cfg = cfg
        self.setWindowTitle("Configurações do NetLab")
        self.setMinimumSize(620, 560)
        self.resize(680, 600)
        self.setStyleSheet(_ESTILO_DIALOG)
        self.setModal(True)
        self._montar_ui()

    def _montar_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 10)
        layout.setSpacing(10)

        # Cabeçalho
        h_cabecalho = QHBoxLayout()
        lbl_titulo = QLabel("Configurações Avançadas")
        lbl_titulo.setStyleSheet(
            "color: #58a6ff; font-size: 15px; font-weight: bold; padding: 4px 0;"
        )
        lbl_sub = QLabel("NetLab Educacional — Controle granular da topologia e varredura")
        lbl_sub.setStyleSheet("color: #8b949e; font-size: 10px;")
        h_cabecalho.addWidget(lbl_titulo)
        h_cabecalho.addStretch()
        layout.addLayout(h_cabecalho)
        layout.addWidget(lbl_sub)
        layout.addWidget(_separador())

        # Abas
        self._abas = QTabWidget()
        self._aba_geral    = _AbaGeral(self._cfg)
        self._aba_filtros  = _AbaFiltros(self._cfg)
        self._aba_gerenc   = _AbaGerenciamento(self._cfg)
        self._aba_avancado = _AbaAvancado(self._cfg)

        self._abas.addTab(self._aba_geral,    "Geral")
        self._abas.addTab(self._aba_filtros,  "Filtros de Rede")
        self._abas.addTab(self._aba_gerenc,   "Gerenciamento")
        self._abas.addTab(self._aba_avancado, "Avançado")
        layout.addWidget(self._abas, 1)

        layout.addWidget(_separador())

        # Botões
        h_btn = QHBoxLayout()
        btn_restaurar = QPushButton("Restaurar Padrões")
        btn_restaurar.setObjectName("btn_perigo")
        btn_aplicar = QPushButton("Aplicar")
        btn_aplicar.setObjectName("btn_primario")
        btn_cancelar = QPushButton("Cancelar")
        btn_restaurar.setFixedHeight(34)
        btn_aplicar.setFixedHeight(34)
        btn_cancelar.setFixedHeight(34)
        btn_restaurar.clicked.connect(self._restaurar_padrao)
        btn_aplicar.clicked.connect(self._aplicar_e_fechar)
        btn_cancelar.clicked.connect(self.reject)
        h_btn.addWidget(btn_restaurar)
        h_btn.addStretch()
        h_btn.addWidget(btn_cancelar)
        h_btn.addWidget(btn_aplicar)
        layout.addLayout(h_btn)

    def adicionar_ip_excluido(self, ip: str):
        """Adiciona um IP à aba de gerenciamento (chamado externamente)."""
        self._aba_gerenc.adicionar_ip_excluido_externo(ip)
        self._abas.setCurrentWidget(self._aba_gerenc)

    def _coletar_tudo(self) -> dict:
        config = {}
        config.update(self._aba_geral.coletar_valores())
        config.update(self._aba_filtros.coletar_valores())
        config.update(self._aba_gerenc.coletar_valores())
        config.update(self._aba_avancado.coletar_valores())
        return config

    def _recarregar_valores_abas(self):
        for aba in (self._aba_geral, self._aba_filtros, self._aba_gerenc, self._aba_avancado):
            carregar = getattr(aba, "_carregar_valores", None)
            if callable(carregar):
                carregar()

    def _restaurar_padrao(self):
        resposta = QMessageBox.question(
            self,
            "Restaurar Padrões",
            "Todas as configurações serão revertidas para os padrões de fábrica.\n"
            "Hosts manuais, filtros e listas de exclusão também serão apagados.\n\n"
            "Deseja continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return

        self._cfg.resetar_para_padrao()
        self._recarregar_valores_abas()
        config = self._coletar_tudo()
        self.configuracoes_aplicadas.emit(config)
        QMessageBox.information(self, "Restaurado", "Configurações padrão restauradas.")

    def _aplicar_e_fechar(self):
        config = self._coletar_tudo()
        self._cfg.atualizar(config)
        self._cfg.salvar()
        self.configuracoes_aplicadas.emit(config)
        self.accept()
