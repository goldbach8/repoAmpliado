"""
Aplicación de Procesamiento de Datos - Calculadora de Compras Donaldson
Determina cantidades a comprar por proveedor (México / Polifiltro)
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Calculadora de Compras · Donaldson",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS personalizado - Estética industrial/refinada
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #232636;
    --border: #3a3f58;
    --accent: #f5b800;
    --accent2: #60cfff;
    --text: #f0f2fa;
    --muted: #f0f2fa;
    --success: #5cce8f;
    --error: #f07878;
    --warning: #f5c842;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    font-size: 15px;
    line-height: 1.6;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Header principal */
.app-header {
    background: linear-gradient(135deg, var(--surface) 0%, #1e2235 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.app-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--accent);
    margin: 0;
    letter-spacing: -0.02em;
}
.app-header p {
    color: var(--muted);
    font-size: 0.92rem;
    margin: 0;
    margin-top: 0.3rem;
    line-height: 1.5;
}

/* Cards de sección */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Status badges */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    font-weight: 500;
}
.badge-ok { background: rgba(92,206,143,0.15); color: var(--success); border: 1px solid rgba(92,206,143,0.35); }
.badge-pending { background: rgba(245,184,0,0.12); color: var(--warning); border: 1px solid rgba(245,184,0,0.35); }
.badge-error { background: rgba(240,120,120,0.12); color: var(--error); border: 1px solid rgba(240,120,120,0.35); }

/* Métricas */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.4rem;
    flex-wrap: wrap;
}
.metric-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.9rem 1.3rem;
    flex: 1;
    min-width: 130px;
}
.metric-label {
    font-size: 0.74rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.4;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--accent);
    margin-top: 0.25rem;
}

/* Botones principales */
.stButton > button {
    background: var(--accent) !important;
    color: #0f1117 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.55rem 1.3rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #ffc93d !important;
    transform: translateY(-1px) !important;
}

/* Inputs */
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.84rem !important;
    border-radius: 6px !important;
    line-height: 1.5 !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(240,165,0,0.15) !important;
}

.stSelectbox select, .stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* File uploader */
.stFileUploader {
    background: var(--surface2);
    border: 1px dashed var(--border);
    border-radius: 8px;
}

/* Tablas */
.stDataFrame {
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

/* Separador */
hr { border-color: var(--border) !important; }

/* Step indicator */
.step-indicator {
    font-family: 'IBM Plex Mono', monospace;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.3rem 0.8rem;
    font-size: 0.72rem;
    color: var(--muted);
    margin-bottom: 1rem;
}

/* Info / warning boxes */
.info-box {
    background: rgba(96,207,255,0.08);
    border: 1px solid rgba(96,207,255,0.28);
    border-radius: 6px;
    padding: 0.8rem 1.1rem;
    font-size: 0.88rem;
    color: var(--accent2);
    margin: 0.6rem 0;
    line-height: 1.6;
}
.warn-box {
    background: rgba(245,200,66,0.08);
    border: 1px solid rgba(245,200,66,0.28);
    border-radius: 6px;
    padding: 0.8rem 1.1rem;
    font-size: 0.88rem;
    color: var(--warning);
    margin: 0.6rem 0;
    line-height: 1.6;
}
.success-box {
    background: rgba(92,206,143,0.08);
    border: 1px solid rgba(92,206,143,0.28);
    border-radius: 6px;
    padding: 0.8rem 1.1rem;
    font-size: 0.88rem;
    color: var(--success);
    margin: 0.6rem 0;
    line-height: 1.6;
}


/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface2);
    border-radius: 8px;
    gap: 0;
    padding: 3px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: var(--muted);
    border-radius: 6px;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #0f1117 !important;
    font-weight: 600;
}

/* Sidebar steps */
.sidebar-step {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.6rem 0;
    font-size: 0.87rem;
    border-bottom: 1px solid var(--border);
    line-height: 1.4;
}
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    width: 26px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: var(--muted);
}
.step-num.done { background: rgba(92,206,143,0.15); border-color: var(--success); color: var(--success); }
.step-num.active { background: rgba(245,184,0,0.15); border-color: var(--accent); color: var(--accent); }

/* Override streamlit defaults */
.block-container { padding-top: 1.5rem !important; }
div[data-testid="stExpander"] { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Estado de sesión
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        'repo': None,                  # DataFrame REPO filtrado
        'reserv_mexico': None,         # {codigo: cantidad}
        'reserv_polifiltro': None,
        'bo_mexico': None,
        'bo_polifiltro': None,
        'contratos_vigentes': [],      # lista de DataFrames {codigo, q_fact, q_contrato}
        'contratos_excluir': [],       # lista de DataFrames {codigo, q_3m, q_6m, q_12m}
        'precio_polifiltro': None,     # {codigo: precio}
        'resultado': None,             # DataFrame final
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def parse_paste(text: str, columns: list, sep='\t') -> pd.DataFrame | None:
    """Parsea texto pegado (TSV/CSV) y retorna DataFrame con columnas dadas."""
    try:
        from io import StringIO
        lines = [l for l in text.strip().splitlines() if l.strip()]
        if not lines:
            return None
        # Detectar si tiene header
        first = lines[0].split(sep)
        if len(first) != len(columns):
            # intentar coma
            sep = ','
            first = lines[0].split(sep)
        df = pd.read_csv(StringIO('\n'.join(lines)), sep=sep, header=None, names=columns, dtype=str)
        # Si primera fila parece header, eliminarla
        if df.iloc[0].str.lower().tolist() == [c.lower() for c in columns]:
            df = df.iloc[1:].reset_index(drop=True)
        # Convertir tipos
        for col in columns[1:]:
            df[col] = pd.to_numeric(df[col].str.replace(',', '.'), errors='coerce').fillna(0)
        df[columns[0]] = df[columns[0]].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error al parsear: {e}")
        return None


def badge(status):
    icons = {'ok': ('✓', 'badge-ok', 'Cargado'), 'pending': ('○', 'badge-pending', 'Pendiente'), 'error': ('✕', 'badge-error', 'Error')}
    ic, cls, lbl = icons.get(status, icons['pending'])
    return f'<span class="badge {cls}">{ic} {lbl}</span>'


def status_of(key):
    return 'ok' if st.session_state.get(key) is not None else 'pending'


def to_excel_bytes(dfs: dict) -> bytes:
    """Convierte dict {sheet_name: df} a bytes Excel."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet[:31], index=False)
    return buf.getvalue()


# ─────────────────────────────────────────────
# Sidebar: estado de carga
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:1rem; font-weight:600; color:#f0a500; margin-bottom:1.2rem; letter-spacing:-0.01em;">
        📦 Compras Donaldson
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Estado de carga**")

    items = [
        ("1", "REPO", 'repo'),
        ("2", "Reserv. México", 'reserv_mexico'),
        ("3", "Reserv. Polifiltro", 'reserv_polifiltro'),
        ("4", "BO México", 'bo_mexico'),
        ("5", "BO Polifiltro", 'bo_polifiltro'),
        ("6", "Precio Polifiltro", 'precio_polifiltro'),
    ]

    all_ok = all(st.session_state.get(k) is not None for _, _, k in items)

    for num, label, key in items:
        s = status_of(key)
        num_class = 'done' if s == 'ok' else 'active' if num == '1' else ''
        st.markdown(f"""
        <div class="sidebar-step">
            <div class="step-num {num_class}">{num}</div>
            <span style="flex:1">{label}</span>
            {badge(s)}
        </div>
        """, unsafe_allow_html=True)

    cvs = len(st.session_state['contratos_vigentes'])
    ces = len(st.session_state['contratos_excluir'])
    st.markdown(f"""
    <div class="sidebar-step">
        <div class="step-num {'done' if cvs > 0 else ''}">CV</div>
        <span style="flex:1">Contratos vigentes</span>
        <span class="badge {'badge-ok' if cvs else 'badge-pending'}">{cvs} empresa{'s' if cvs != 1 else ''}</span>
    </div>
    <div class="sidebar-step">
        <div class="step-num {'done' if ces > 0 else ''}">CE</div>
        <span style="flex:1">Contratos a excluir</span>
        <span class="badge {'badge-ok' if ces else 'badge-pending'}">{ces} empresa{'s' if ces != 1 else ''}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if all_ok:
        st.markdown('<div class="success-box">✓ Datos mínimos cargados. Puedes procesar.</div>', unsafe_allow_html=True)
    else:
        pending = sum(1 for _, _, k in items if st.session_state.get(k) is None)
        st.markdown(f'<div class="warn-box">Faltan {pending} archivos requeridos.</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Reiniciar todo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div>
        <h1>📦 Calculadora de Compras — Filtros Donaldson</h1>
        <p>Determina cantidades óptimas a comprar en México y Polifiltro según demanda, stock y contratos.</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Tabs principales
# ─────────────────────────────────────────────
tab_repo, tab_prov, tab_contratos, tab_precios, tab_proceso = st.tabs([
    "📂 REPO", "🏭 Proveedores", "📋 Contratos", "💲 Precios", "⚙️ Procesar"
])


# ═══════════════════════════════════════════════════════
# TAB 1 — REPO
# ═══════════════════════════════════════════════════════
with tab_repo:
    st.markdown('<div class="section-title">📂 Reporte REPO</div>', unsafe_allow_html=True)
    st.markdown("Cargá el archivo Excel exportado del sistema. Se aplicarán filtros automáticos.")

    col_upload, col_info = st.columns([2, 1])
    with col_upload:
        repo_file = st.file_uploader("Archivo Excel REPO (.xlsx / .xls)", type=['xlsx', 'xls'], key='repo_uploader')

    with col_info:
        st.markdown("""
        <div class="info-box">
            <strong>Filtros aplicados:</strong><br>
            • Familia = <code>Filtros</code><br>
            • Subfamilia = <code>Donaldson</code><br>
            • Inactivo = <code>No</code><br>
            • Grupo ≠ DNS-Inmovilizado / DNS-A Demanda
        </div>
        """, unsafe_allow_html=True)

    REPO_COLS = [
        'familia', 'subfamilia', 'grupo', 'inactivo', 'codigo', 'codfabricante',
        'descripcion', 'descripcion2', 'clasificacion', 'consolidado',
        'q_fact_3', 'q_fact_6', 'q_fact_12',
        'en_sv_en_menos_30_dias', 'en_sv_en_mas_30_dias',
        'pc', 'qty_piezas_por_caja'
    ]

    if repo_file:
        try:
            with st.spinner("Procesando REPO..."):
                df_raw = pd.read_excel(repo_file, dtype=str)

            # Normalizar nombres de columna
            df_raw.columns = df_raw.columns.str.strip().str.lower().str.replace(' ', '_')

            missing = [c for c in REPO_COLS if c not in df_raw.columns]
            if missing:
                st.error(f"Columnas faltantes en el archivo: {missing}")
                st.markdown("**Columnas disponibles:**")
                st.code(list(df_raw.columns))
            else:
                df = df_raw[REPO_COLS].copy()

                # Filtros
                mask = (
                    (df['familia'].str.strip().str.lower() == 'filtros') &
                    (df['subfamilia'].str.strip().str.lower() == 'donaldson') &
                    (df['inactivo'].str.strip().str.lower() == 'no') &
                    (~df['grupo'].str.strip().str.lower().isin(['dns - inmovilizado', 'dns - a demanda']))
                )
                df_filtrado = df[mask].copy()

                # Convertir numéricos
                numeric_cols = ['consolidado', 'q_fact_3', 'q_fact_6', 'q_fact_12',
                                'en_sv_en_menos_30_dias', 'en_sv_en_mas_30_dias', 'pc', 'qty_piezas_por_caja']
                for col in numeric_cols:
                    df_filtrado[col] = pd.to_numeric(
                        df_filtrado[col].str.replace(',', '.'), errors='coerce'
                    ).fillna(0)

                df_filtrado['codigo'] = df_filtrado['codigo'].astype(str).str.strip()
                st.session_state['repo'] = df_filtrado

                n_total = len(df_raw)
                n_filtrado = len(df_filtrado)

                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-box"><div class="metric-label">Total registros</div><div class="metric-value">{n_total:,}</div></div>
                    <div class="metric-box"><div class="metric-label">Después de filtros</div><div class="metric-value" style="color:var(--success)">{n_filtrado:,}</div></div>
                    <div class="metric-box"><div class="metric-label">Excluidos</div><div class="metric-value" style="color:var(--muted)">{n_total - n_filtrado:,}</div></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="success-box">✓ REPO cargado y filtrado correctamente.</div>', unsafe_allow_html=True)

                with st.expander("Vista previa (primeras 50 filas)"):
                    st.dataframe(df_filtrado.head(50), use_container_width=True)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

    elif st.session_state['repo'] is not None:
        df_filtrado = st.session_state['repo']
        st.markdown(f'<div class="success-box">✓ REPO ya cargado — {len(df_filtrado):,} registros.</div>', unsafe_allow_html=True)
        with st.expander("Ver datos"):
            st.dataframe(df_filtrado.head(50), use_container_width=True)


# ═══════════════════════════════════════════════════════
# TAB 2 — PROVEEDORES
# ═══════════════════════════════════════════════════════
with tab_prov:
    st.markdown('<div class="section-title">🏭 Disponible y Backorder por Proveedor</div>', unsafe_allow_html=True)
    st.markdown("Pegá los datos directamente desde Excel (dos columnas: código y cantidad).")

    def proveedor_section(title, reserv_key, bo_key, proveedor_label):
        with st.expander(f"**{title}**", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Disponible (Reserv.) — {proveedor_label}**")
                st.markdown('<div class="info-box">Pegá: <code>codigo TAB cantidad</code></div>', unsafe_allow_html=True)
                txt_reserv = st.text_area(
                    f"Datos reserv. {proveedor_label}",
                    height=160,
                    key=f"txt_{reserv_key}",
                    placeholder="P12345\t100\nP67890\t50"
                )
                if st.button(f"Cargar Reserv. {proveedor_label}", key=f"btn_{reserv_key}"):
                    if txt_reserv.strip():
                        df_r = parse_paste(txt_reserv, ['codigo', f'reserv_{proveedor_label.lower()}'])
                        if df_r is not None:
                            st.session_state[reserv_key] = df_r
                            st.success(f"✓ {len(df_r)} registros cargados.")
                        else:
                            st.error("No se pudo parsear. Verificá el formato.")
                    else:
                        st.warning("El campo está vacío.")

                if st.session_state.get(reserv_key) is not None:
                    df_show = st.session_state[reserv_key]
                    st.markdown(f'<div class="success-box">✓ {len(df_show)} registros cargados</div>', unsafe_allow_html=True)
                    st.dataframe(df_show.head(10), use_container_width=True)

            with col2:
                st.markdown(f"**Backorder — {proveedor_label}**")
                st.markdown('<div class="info-box">Pegá: <code>codigo TAB cantidad_bo</code></div>', unsafe_allow_html=True)
                txt_bo = st.text_area(
                    f"Datos BO {proveedor_label}",
                    height=160,
                    key=f"txt_{bo_key}",
                    placeholder="P12345\t20\nP67890\t10"
                )
                if st.button(f"Cargar BO {proveedor_label}", key=f"btn_{bo_key}"):
                    if txt_bo.strip():
                        df_b = parse_paste(txt_bo, ['codigo', f'bo_{proveedor_label.lower()}'])
                        if df_b is not None:
                            st.session_state[bo_key] = df_b
                            st.success(f"✓ {len(df_b)} registros cargados.")
                        else:
                            st.error("No se pudo parsear. Verificá el formato.")
                    else:
                        st.warning("El campo está vacío.")

                if st.session_state.get(bo_key) is not None:
                    df_show = st.session_state[bo_key]
                    st.markdown(f'<div class="success-box">✓ {len(df_show)} registros cargados</div>', unsafe_allow_html=True)
                    st.dataframe(df_show.head(10), use_container_width=True)

    proveedor_section("🇲🇽 México", "reserv_mexico", "bo_mexico", "Mexico")
    proveedor_section("🏢 Polifiltro", "reserv_polifiltro", "bo_polifiltro", "Polifiltro")


# ═══════════════════════════════════════════════════════
# TAB 3 — CONTRATOS
# ═══════════════════════════════════════════════════════
with tab_contratos:
    st.markdown('<div class="section-title">📋 Contratos</div>', unsafe_allow_html=True)

    col_cv, col_ce = st.columns(2)

    # ── Contratos Vigentes ──
    with col_cv:
        st.markdown("**Contratos Vigentes por Empresa**")
        st.markdown('<div class="info-box">Columnas: <code>codigo · q_fact · q_contrato</code></div>', unsafe_allow_html=True)

        n_cv = st.number_input("Número de empresas con contrato vigente", min_value=0, max_value=20, value=len(st.session_state['contratos_vigentes']), step=1, key="n_cv")

        if n_cv != len(st.session_state['contratos_vigentes']):
            # Ajustar lista
            while len(st.session_state['contratos_vigentes']) < n_cv:
                st.session_state['contratos_vigentes'].append(None)
            while len(st.session_state['contratos_vigentes']) > n_cv:
                st.session_state['contratos_vigentes'].pop()

        for i in range(int(n_cv)):
            with st.expander(f"Empresa {i+1}" + (" ✓" if st.session_state['contratos_vigentes'][i] is not None else " ○"), expanded=(i == 0)):
                empresa_name = st.text_input(f"Nombre empresa", key=f"cv_name_{i}", placeholder=f"Empresa {i+1}")
                txt = st.text_area(f"Datos empresa {i+1}", height=130, key=f"cv_txt_{i}",
                                   placeholder="P12345\t50\t60\nP67890\t30\t30")
                if st.button(f"Cargar empresa {i+1}", key=f"cv_btn_{i}"):
                    df_cv = parse_paste(txt, ['codigo', 'q_fact', 'q_contrato'])
                    if df_cv is not None:
                        df_cv['empresa'] = empresa_name or f"Empresa_{i+1}"
                        st.session_state['contratos_vigentes'][i] = df_cv
                        st.success(f"✓ {len(df_cv)} registros")
                    else:
                        st.error("Error al parsear.")
                if st.session_state['contratos_vigentes'][i] is not None:
                    st.dataframe(st.session_state['contratos_vigentes'][i].head(5), use_container_width=True)

    # ── Contratos a Excluir ──
    with col_ce:
        st.markdown("**Contratos a Excluir**")
        st.markdown('<div class="info-box">Columnas: <code>codigo · q_3m · q_6m · q_12m</code></div>', unsafe_allow_html=True)

        n_ce = st.number_input("Número de empresas a excluir", min_value=0, max_value=20, value=len(st.session_state['contratos_excluir']), step=1, key="n_ce")

        if n_ce != len(st.session_state['contratos_excluir']):
            while len(st.session_state['contratos_excluir']) < n_ce:
                st.session_state['contratos_excluir'].append(None)
            while len(st.session_state['contratos_excluir']) > n_ce:
                st.session_state['contratos_excluir'].pop()

        for i in range(int(n_ce)):
            with st.expander(f"Empresa excluir {i+1}" + (" ✓" if st.session_state['contratos_excluir'][i] is not None else " ○"), expanded=(i == 0)):
                empresa_name = st.text_input(f"Nombre empresa excluir", key=f"ce_name_{i}", placeholder=f"Excluir {i+1}")
                txt = st.text_area(f"Datos excluir {i+1}", height=130, key=f"ce_txt_{i}",
                                   placeholder="P12345\t10\t20\t45\nP67890\t5\t10\t22")
                if st.button(f"Cargar excluir {i+1}", key=f"ce_btn_{i}"):
                    df_ce = parse_paste(txt, ['codigo', 'q_3m', 'q_6m', 'q_12m'])
                    if df_ce is not None:
                        df_ce['empresa'] = empresa_name or f"Excluir_{i+1}"
                        st.session_state['contratos_excluir'][i] = df_ce
                        st.success(f"✓ {len(df_ce)} registros")
                    else:
                        st.error("Error al parsear.")
                if st.session_state['contratos_excluir'][i] is not None:
                    st.dataframe(st.session_state['contratos_excluir'][i].head(5), use_container_width=True)


# ═══════════════════════════════════════════════════════
# TAB 4 — PRECIOS POLIFILTRO
# ═══════════════════════════════════════════════════════
with tab_precios:
    st.markdown('<div class="section-title">💲 Lista de Precios Polifiltro</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Columnas: <code>codigo · precio_polifiltro</code></div>', unsafe_allow_html=True)

    txt_precio = st.text_area("Pegá los precios de Polifiltro", height=250, key="txt_precio",
                              placeholder="P12345\t15.50\nP67890\t8.00")
    if st.button("Cargar precios Polifiltro"):
        if txt_precio.strip():
            df_p = parse_paste(txt_precio, ['codigo', 'precio_polifiltro'])
            if df_p is not None:
                st.session_state['precio_polifiltro'] = df_p
                st.markdown(f'<div class="success-box">✓ {len(df_p)} precios cargados.</div>', unsafe_allow_html=True)
                st.dataframe(df_p.head(20), use_container_width=True)
            else:
                st.error("Error al parsear. Verificá el formato.")
        else:
            st.warning("Campo vacío.")

    if st.session_state['precio_polifiltro'] is not None:
        df_show = st.session_state['precio_polifiltro']
        st.markdown(f'<div class="success-box">✓ {len(df_show)} precios ya cargados.</div>', unsafe_allow_html=True)
        with st.expander("Ver precios"):
            st.dataframe(df_show, use_container_width=True)


# ═══════════════════════════════════════════════════════
# TAB 5 — PROCESAR
# ═══════════════════════════════════════════════════════
with tab_proceso:
    st.markdown('<div class="section-title">⚙️ Cálculo y Exportación</div>', unsafe_allow_html=True)

    # Validar requisitos mínimos
    required = {
        'REPO': st.session_state['repo'],
        'Reserv. México': st.session_state['reserv_mexico'],
        'BO México': st.session_state['bo_mexico'],
        'Precio Polifiltro': st.session_state['precio_polifiltro'],
    }
    missing_req = [k for k, v in required.items() if v is None]

    if missing_req:
        st.markdown(f'<div class="warn-box">⚠️ Faltan datos requeridos: <strong>{", ".join(missing_req)}</strong></div>', unsafe_allow_html=True)

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        run = st.button("▶ Calcular y procesar", disabled=bool(missing_req))

    with col_info:
        st.markdown("""
        <div class="info-box">
            El proceso calculará demanda mensual, stock virtual, stock objetivo y 
            cantidades a comprar en México y Polifiltro.
        </div>
        """, unsafe_allow_html=True)

    if run:
        try:
            with st.spinner("Procesando datos..."):

                # ── 1. Base: REPO ──
                df = st.session_state['repo'].copy()

                # ── 2. Merge datos de proveedores ──
                def merge_col(df_base, df_prov, col_name, default=0):
                    if df_prov is not None:
                        df_prov_renamed = df_prov.rename(columns={df_prov.columns[1]: col_name})
                        return df_base.merge(df_prov_renamed[['codigo', col_name]], on='codigo', how='left')
                    else:
                        df_base[col_name] = default
                        return df_base

                df = merge_col(df, st.session_state['reserv_mexico'], 'reserv_mexico')
                df = merge_col(df, st.session_state['bo_mexico'], 'bo_mexico')
                df = merge_col(df, st.session_state['reserv_polifiltro'], 'reserv_polifiltro')
                df = merge_col(df, st.session_state['bo_polifiltro'], 'bo_polifiltro')
                df = merge_col(df, st.session_state['precio_polifiltro'], 'precio_polifiltro')

                # Rellenar NaN
                for col in ['reserv_mexico', 'bo_mexico', 'reserv_polifiltro', 'bo_polifiltro', 'precio_polifiltro']:
                    df[col] = df[col].fillna(0)

                # ── 3. Contratos vigentes ──
                # Se calculan dos agregados separados por código:
                #   a) suma_min_contratos: min(q_fact, q_contrato) por contrato → se usa para
                #      restar de la demanda histórica al calcular demanda sin contratos,
                #      representando lo que efectivamente se facturó dentro del marco del contrato.
                #   b) demanda_mensual_contratos: sum(q_contrato) → demanda comprometida
                #      contractualmente, independiente de lo que se haya facturado.

                cv_list = [c for c in st.session_state['contratos_vigentes'] if c is not None]
                if cv_list:
                    df_cv_all = pd.concat(cv_list, ignore_index=True)

                    # a) Mín(facturado, contrato) — para depurar la demanda histórica
                    df_cv_all['min_cv'] = df_cv_all[['q_fact', 'q_contrato']].min(axis=1)
                    df_min_agg = df_cv_all.groupby('codigo')['min_cv'].sum().reset_index()
                    df_min_agg.rename(columns={'min_cv': 'suma_min_contratos'}, inplace=True)

                    # b) Cantidad en contrato — demanda futura comprometida
                    df_contrato_agg = df_cv_all.groupby('codigo')['q_contrato'].sum().reset_index()
                    df_contrato_agg.rename(columns={'q_contrato': 'demanda_mensual_contratos'}, inplace=True)

                    df = df.merge(df_min_agg, on='codigo', how='left')
                    df = df.merge(df_contrato_agg, on='codigo', how='left')
                else:
                    df['suma_min_contratos'] = 0
                    df['demanda_mensual_contratos'] = 0

                df['suma_min_contratos'] = df['suma_min_contratos'].fillna(0)
                df['demanda_mensual_contratos'] = df['demanda_mensual_contratos'].fillna(0)

                # Procesar contratos a excluir
                ce_list = [c for c in st.session_state['contratos_excluir'] if c is not None]
                if ce_list:
                    df_ce_all = pd.concat(ce_list, ignore_index=True)
                    df_ce_agg = df_ce_all.groupby('codigo')[['q_3m', 'q_6m', 'q_12m']].sum().reset_index()
                    df = df.merge(df_ce_agg, on='codigo', how='left')
                else:
                    df['q_3m'] = 0
                    df['q_6m'] = 0
                    df['q_12m'] = 0
                for c in ['q_3m', 'q_6m', 'q_12m']:
                    df[c] = df[c].fillna(0)

                # ── 4. Demanda mensual sin contratos ──
                # Promedio mensual de facturación neta (descontando lo facturado bajo contrato),
                # luego se resta la demanda_mensual_contratos para aislar la demanda libre de contratos.
                # Se usa suma_min_contratos (no q_contrato) para la depuración histórica, ya que
                # representa lo que realmente se facturó dentro del marco del contrato.
                prom_3  = (df['q_fact_3']  - df['q_3m'])  / 3
                prom_6  = (df['q_fact_6']  - df['q_6m'])  / 6
                prom_12 = (df['q_fact_12'] - df['q_12m']) / 12

                # Promedio de los tres horizontes menos el mínimo facturado bajo contratos vigentes
                df['demanda_mensual_sin_contratos'] = (
                    ((prom_3 + prom_6 + prom_12) / 3) - df['suma_min_contratos']
                ).clip(lower=0)

                # ── 5. Stock virtual ──
                df['stock_virtual'] = (
                    df['consolidado'] +
                    df['en_sv_en_menos_30_dias'] +
                    df['en_sv_en_mas_30_dias'] +
                    df['reserv_mexico'] +
                    df['bo_mexico']
                )

                # ── 6. Diferencia de precio (Polifiltro vs México) ──
                # Valor negativo = Polifiltro más barato. Ej: -10 significa 10% más barato.
                df['diferencia_precio_pct'] = np.where(
                    df['pc'] > 0,
                    (df['precio_polifiltro'] - df['pc']) / df['pc'] * 100,
                    np.nan
                )

                # Clasificación del tramo de precio para decidir dónde y cuánto comprar:
                #   'POLI_FUERTE' : Polifiltro >= 8% más barato  → proporciones máximas en Poli
                #   'POLI_LEVE'   : Polifiltro entre 5.5% y 8% más barato → proporciones intermedias
                #   'MEX'         : diferencia < 5.5%  → todo México
                tiene_precio_poli = df['precio_polifiltro'] > 0
                diff = df['diferencia_precio_pct']

                df['donde_comprar'] = np.where(
                    tiene_precio_poli & (diff <= -8.0),   'POLI_FUERTE',
                    np.where(
                    tiene_precio_poli & (diff <= -5.5),   'POLI_LEVE',
                                                          'MEX'
                ))

                # ── 7. Stock objetivo, casos y proporciones ──
                # Calificaciones premium (mayor rotación / criticidad)
                cal_aa = df['clasificacion'].str.upper().isin(['AA', 'AB', 'AC', 'BA'])

                dms = df['demanda_mensual_sin_contratos']
                dmc = df['demanda_mensual_contratos']

                # ┌──────────────┬──────────────────┬───────────────────────────────────────┐
                # │ Caso         │ Condición        │ Stock objetivo / Proporción           │
                # ├──────────────┼──────────────────┼───────────────────────────────────────┤
                # │ A  (MEX)     │ donde_comprar=MEX│ 6×dms + 4×dmc  |  6x0                │
                # │ B1 (POLI AA) │ POLI_FUERTE + AA │ 8×dms + 4×dmc  |  5x3                │
                # │ B2 (POLI)    │ POLI_FUERTE      │ 7×dms + 4×dmc  |  4x3                │
                # │ C1 (POLI AA) │ POLI_LEVE + AA   │ 8×dms + 4×dmc  |  6x2                │
                # │ C2 (POLI)    │ POLI_LEVE        │ 7×dms + 4×dmc  |  5x2                │
                # └──────────────┴──────────────────┴───────────────────────────────────────┘
                cond_a  = df['donde_comprar'] == 'MEX'
                cond_b1 = (df['donde_comprar'] == 'POLI_FUERTE') &  cal_aa
                cond_b2 = (df['donde_comprar'] == 'POLI_FUERTE') & ~cal_aa
                cond_c1 = (df['donde_comprar'] == 'POLI_LEVE')   &  cal_aa
                cond_c2 = (df['donde_comprar'] == 'POLI_LEVE')   & ~cal_aa

                df['stock_objetivo'] = np.select(
                    [cond_a,        cond_b1,         cond_b2,         cond_c1,         cond_c2],
                    [6*dms+4*dmc,   8*dms+4*dmc,     7*dms+4*dmc,     8*dms+4*dmc,     7*dms+4*dmc],
                    default=6*dms+4*dmc
                )

                df['caso'] = np.select(
                    [cond_a, cond_b1, cond_b2, cond_c1, cond_c2],
                    ['A',    'B1',    'B2',    'C1',    'C2'],
                    default='A'
                )

                df['proporcion'] = np.select(
                    [cond_a, cond_b1, cond_b2, cond_c1, cond_c2],
                    ['6x0',  '5x3',   '4x3',   '6x2',   '5x2'],
                    default='6x0'
                )

                # ── 8. Cantidades a comprar ──
                so  = df['stock_objetivo']
                sv  = df['stock_virtual']
                rp  = df['reserv_polifiltro']
                bop = df['bo_polifiltro']

                # Caso A — todo México, nada en Polifiltro
                qty_mex_a   = (so - sv).clip(lower=0)
                qty_poli_a  = pd.Series(0.0, index=df.index)

                # Caso B1 — proporción 5x3: 5/8 meses en México, 3/8 en Polifiltro
                qty_mex_b1  = (((5 * so) / 8) - sv).clip(lower=0)
                qty_poli_b1 = (so - sv - qty_mex_b1 - rp - bop).clip(lower=0)

                # Caso B2 — proporción 4x3: 4/7 meses en México, 3/7 en Polifiltro
                qty_mex_b2  = (((4 * so) / 7) - sv).clip(lower=0)
                qty_poli_b2 = (so - sv - qty_mex_b2 - rp - bop).clip(lower=0)

                # Caso C1 — proporción 6x2: 6/8 meses en México, 2/8 en Polifiltro
                qty_mex_c1  = (((6 * so) / 8) - sv).clip(lower=0)
                qty_poli_c1 = (so - sv - qty_mex_c1 - rp - bop).clip(lower=0)

                # Caso C2 — proporción 5x2: 5/7 meses en México, 2/7 en Polifiltro
                qty_mex_c2  = (((5 * so) / 7) - sv).clip(lower=0)
                qty_poli_c2 = (so - sv - qty_mex_c2 - rp - bop).clip(lower=0)

                df['qty_comprar_mexico'] = np.select(
                    [cond_a,      cond_b1,      cond_b2,      cond_c1,      cond_c2],
                    [qty_mex_a,   qty_mex_b1,   qty_mex_b2,   qty_mex_c1,   qty_mex_c2],
                    default=qty_mex_a
                )
                df['qty_comprar_polifiltro'] = np.select(
                    [cond_a,      cond_b1,       cond_b2,       cond_c1,       cond_c2],
                    [qty_poli_a,  qty_poli_b1,   qty_poli_b2,   qty_poli_c1,   qty_poli_c2],
                    default=qty_poli_a
                )

                # ── 9. Redondeo al tamaño de caja (ceiling al múltiplo de qty_piezas_por_caja) ──
                # Si qty_piezas_por_caja <= 0 o es NaN, se trata como caja de 1 (sin efecto).
                # Fórmula: ceil(qty / caja) * caja  →  garantiza comprar cajas completas.
                caja = df['qty_piezas_por_caja'].fillna(1).clip(lower=1)

                def redondear_caja(qty_serie, caja_serie):
                    """Redondea cada cantidad hacia arriba al múltiplo de caja más cercano.
                    Si la cantidad es 0, devuelve 0 (no se genera pedido)."""
                    qty = qty_serie.clip(lower=0)
                    redondeado = np.where(
                        qty > 0,
                        np.ceil(qty / caja_serie) * caja_serie,
                        0
                    )
                    return redondeado.astype(int)

                df['qty_comprar_mexico']     = redondear_caja(df['qty_comprar_mexico'],     caja)
                df['qty_comprar_polifiltro'] = redondear_caja(df['qty_comprar_polifiltro'], caja)

                st.session_state['resultado'] = df

            st.markdown('<div class="success-box">✓ Procesamiento completado correctamente.</div>', unsafe_allow_html=True)

        except Exception as e:
            import traceback
            st.error(f"Error durante el procesamiento: {e}")
            st.code(traceback.format_exc())

    # ── Mostrar resultados ──
    if st.session_state['resultado'] is not None:
        df_res = st.session_state['resultado']

        st.markdown("---")
        st.markdown("### Resumen de resultados")

        total_codes = len(df_res)
        mex_codes = (df_res['qty_comprar_mexico'] > 0).sum()
        poli_codes = (df_res['qty_comprar_polifiltro'] > 0).sum()
        total_mex = df_res['qty_comprar_mexico'].sum()
        total_poli = df_res['qty_comprar_polifiltro'].sum()
        monto_mex = (df_res['qty_comprar_mexico'] * df_res['pc']).sum()
        monto_poli = (df_res['qty_comprar_polifiltro'] * df_res['precio_polifiltro']).sum()

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-label">Códigos totales</div>
                <div class="metric-value">{total_codes:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Cód. a comprar MEX</div>
                <div class="metric-value">{mex_codes:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Cód. a comprar POLI</div>
                <div class="metric-value">{poli_codes:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Total und. MEX</div>
                <div class="metric-value">{total_mex:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Total und. POLI</div>
                <div class="metric-value">{total_poli:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Monto MEX ($)</div>
                <div class="metric-value">{monto_mex:,.0f}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Monto POLI ($)</div>
                <div class="metric-value">{monto_poli:,.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Distribución por caso
        caso_counts = df_res['caso'].value_counts()
        st.markdown(
            f"**Distribución por caso:** "
            f"A={caso_counts.get('A',0)} · "
            f"B1={caso_counts.get('B1',0)} · "
            f"B2={caso_counts.get('B2',0)} · "
            f"C1={caso_counts.get('C1',0)} · "
            f"C2={caso_counts.get('C2',0)}"
        )

        with st.expander("📊 Ver tabla completa de resultados"):
            st.dataframe(df_res, use_container_width=True)

        # ── Exportar ──
        st.markdown("---")
        st.markdown("### 📥 Exportar resultados")

        col_ex1, col_ex2 = st.columns(2)

        with col_ex1:
            st.markdown("**Archivo completo con todos los cálculos**")
            excel_full = to_excel_bytes({'Resultados': df_res})
            st.download_button(
                label="⬇ Descargar resultados completos",
                data=excel_full,
                file_name="resultados_compras_completo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with col_ex2:
            st.markdown("**Órdenes de compra por proveedor**")

            # Orden México
            df_mex = df_res[df_res['qty_comprar_mexico'] > 0][[
                'codigo', 'codfabricante', 'descripcion', 'clasificacion', 'caso', 'proporcion',
                'demanda_mensual_sin_contratos', 'demanda_mensual_contratos',
                'stock_virtual', 'stock_objetivo', 'qty_comprar_mexico', 'pc'
            ]].copy()
            df_mex['monto_mexico'] = (df_mex['qty_comprar_mexico'] * df_mex['pc']).round(2)

            # Orden Polifiltro
            df_poli = df_res[df_res['qty_comprar_polifiltro'] > 0][[
                'codigo', 'codfabricante', 'descripcion', 'clasificacion', 'caso', 'proporcion',
                'demanda_mensual_sin_contratos', 'demanda_mensual_contratos',
                'stock_virtual', 'stock_objetivo', 'qty_comprar_polifiltro', 'precio_polifiltro'
            ]].copy()
            df_poli['monto_polifiltro'] = (df_poli['qty_comprar_polifiltro'] * df_poli['precio_polifiltro']).round(2)

            excel_oc = to_excel_bytes({
                'OC México': df_mex,
                'OC Polifiltro': df_poli
            })
            st.download_button(
                label="⬇ Descargar órdenes de compra",
                data=excel_oc,
                file_name="ordenes_compra_proveedores.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Preview OC
        with st.expander("Vista previa: OC México (top 20)"):
            if len(df_mex) > 0:
                st.dataframe(df_mex.head(20), use_container_width=True)
            else:
                st.info("No hay compras a México.")

        with st.expander("Vista previa: OC Polifiltro (top 20)"):
            if len(df_poli) > 0:
                st.dataframe(df_poli.head(20), use_container_width=True)
            else:
                st.info("No hay compras a Polifiltro.")