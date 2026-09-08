from pathlib import Path
from datetime import datetime
import html
import duckdb


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DB_PATH = PROJECT_ROOT / "analytics.duckdb"

OUTPUT_PATH = PROJECT_ROOT / "observability_report.html"


# ============================================================
# CONEXÃO COM DUCKDB
# ============================================================

if not DB_PATH.exists():
    raise FileNotFoundError(
        f"Banco não encontrado: {DB_PATH}"
    )

con = duckdb.connect(
    str(DB_PATH),
    read_only=True
)


# ============================================================
# BUSCAR DADOS DE OBSERVABILIDADE
# ============================================================

freshness = con.execute("""
    SELECT
        dataset,
        latest_date,
        check_date,
        days_since_update,
        freshness_status
    FROM main.obs_data_freshness
    ORDER BY dataset
""").fetchall()


volume = con.execute("""
    SELECT
        dataset,
        row_count,
        check_date
    FROM main.obs_data_volume
    ORDER BY dataset
""").fetchall()


health = con.execute("""
    SELECT
        dataset,
        row_count,
        latest_date,
        check_date,
        days_since_update,
        pipeline_status
    FROM main.obs_pipeline_health
    ORDER BY dataset
""").fetchall()


# ============================================================
# MÉTRICAS GERAIS
# ============================================================

total_datasets = len(health)

healthy_datasets = sum(
    1
    for row in health
    if str(row[5]).upper() in ("OK", "HEALTHY")
)

warning_datasets = sum(
    1
    for row in health
    if str(row[5]).upper() == "WARNING"
)

critical_datasets = sum(
    1
    for row in health
    if str(row[5]).upper() == "CRITICAL"
)

total_rows = sum(
    int(row[1])
    for row in volume
    if row[1] is not None
)

generated_at = datetime.now().strftime(
    "%d/%m/%Y %H:%M:%S"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def escape(value):

    if value is None:
        return "-"

    return html.escape(str(value))


def format_date(value):

    if value is None:
        return "-"

    try:
        return value.strftime("%d/%m/%Y")

    except AttributeError:
        return str(value)


def status_badge(status):

    status = str(status).upper()

    if status in ("OK", "HEALTHY"):

        css_class = "ok"

    elif status == "WARNING":

        css_class = "warning"

    else:

        css_class = "critical"

    return f"""
        <span class="badge {css_class}">
            {escape(status)}
        </span>
    """


# ============================================================
# GERAR TABELA — PIPELINE HEALTH
# ============================================================

health_rows = ""

for row in health:

    (
        dataset,
        row_count,
        latest_date,
        check_date,
        days_since_update,
        pipeline_status
    ) = row

    health_rows += f"""
        <tr>

            <td>
                <strong>{escape(dataset)}</strong>
            </td>

            <td>
                {int(row_count):,}
            </td>

            <td>
                {format_date(latest_date)}
            </td>

            <td>
                {escape(days_since_update)} dia(s)
            </td>

            <td>
                {status_badge(pipeline_status)}
            </td>

        </tr>
    """


# ============================================================
# GERAR TABELA — FRESHNESS
# ============================================================

freshness_rows = ""

for row in freshness:

    (
        dataset,
        latest_date,
        check_date,
        days_since_update,
        freshness_status
    ) = row

    freshness_rows += f"""
        <tr>

            <td>
                <strong>{escape(dataset)}</strong>
            </td>

            <td>
                {format_date(latest_date)}
            </td>

            <td>
                {format_date(check_date)}
            </td>

            <td>
                {escape(days_since_update)} dia(s)
            </td>

            <td>
                {status_badge(freshness_status)}
            </td>

        </tr>
    """


# ============================================================
# GERAR TABELA — VOLUME
# ============================================================

volume_rows = ""

for row in volume:

    (
        dataset,
        row_count,
        check_date
    ) = row

    volume_rows += f"""
        <tr>

            <td>
                <strong>{escape(dataset)}</strong>
            </td>

            <td>
                {int(row_count):,}
            </td>

            <td>
                {format_date(check_date)}
            </td>

        </tr>
    """


# ============================================================
# HTML
# ============================================================

html_content = f"""
<!DOCTYPE html>

<html lang="pt-BR">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        CS Analytics - Data Observability
    </title>


    <style>

        * {{
            box-sizing: border-box;
        }}


        body {{

            margin: 0;

            font-family:
                Arial,
                Helvetica,
                sans-serif;

            background: #f4f6f8;

            color: #17202a;

        }}


        .container {{

            max-width: 1200px;

            margin: 0 auto;

            padding: 32px;

        }}


        header {{

            margin-bottom: 28px;

        }}


        h1 {{

            margin: 0 0 8px 0;

            font-size: 30px;

        }}


        .subtitle {{

            color: #6b7280;

            margin: 0;

        }}


        .generated {{

            color: #9ca3af;

            font-size: 13px;

            margin-top: 8px;

        }}


        /* ====================================================
           CARDS
           ==================================================== */


        .cards {{

            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 16px;

            margin-bottom: 28px;

        }}


        .card {{

            background: white;

            border-radius: 12px;

            padding: 20px;

            box-shadow:
                0 2px 8px
                rgba(0, 0, 0, 0.06);

        }}


        .card-title {{

            font-size: 13px;

            color: #6b7280;

            margin-bottom: 10px;

        }}


        .card-value {{

            font-size: 28px;

            font-weight: 700;

        }}


        /* ====================================================
           SECTIONS
           ==================================================== */


        .section {{

            background: white;

            border-radius: 12px;

            padding: 24px;

            margin-bottom: 24px;

            box-shadow:
                0 2px 8px
                rgba(0, 0, 0, 0.06);

        }}


        h2 {{

            margin-top: 0;

            font-size: 20px;

        }}


        .description {{

            color: #6b7280;

            font-size: 14px;

            margin-bottom: 18px;

        }}


        /* ====================================================
           TABLE
           ==================================================== */


        table {{

            width: 100%;

            border-collapse: collapse;

        }}


        th {{

            text-align: left;

            font-size: 12px;

            color: #6b7280;

            text-transform: uppercase;

            letter-spacing: 0.04em;

            padding: 12px;

            border-bottom:
                1px solid #e5e7eb;

        }}


        td {{

            padding: 14px 12px;

            border-bottom:
                1px solid #f0f1f2;

            font-size: 14px;

        }}


        tr:last-child td {{

            border-bottom: none;

        }}


        /* ====================================================
           STATUS
           ==================================================== */


        .badge {{

            display: inline-block;

            padding: 5px 10px;

            border-radius: 999px;

            font-size: 12px;

            font-weight: 700;

        }}


        .ok {{

            background: #dcfce7;

            color: #166534;

        }}


        .warning {{

            background: #fef3c7;

            color: #92400e;

        }}


        .critical {{

            background: #fee2e2;

            color: #991b1b;

        }}


        /* ====================================================
           FOOTER
           ==================================================== */


        .footer {{

            text-align: center;

            color: #9ca3af;

            font-size: 12px;

            padding: 20px;

        }}


        /* ====================================================
           RESPONSIVO
           ==================================================== */


        @media (max-width: 800px) {{

            .cards {{

                grid-template-columns:
                    repeat(2, 1fr);

            }}

        }}


        @media (max-width: 500px) {{

            .container {{

                padding: 16px;

            }}


            .cards {{

                grid-template-columns: 1fr;

            }}

        }}

    </style>

</head>


<body>


<div class="container">


    <!-- =====================================================
         CABEÇALHO
         ===================================================== -->

    <header>

        <h1>
            CS Analytics — Data Observability
        </h1>

        <p class="subtitle">

            Monitoramento de qualidade,
            volume e atualização dos dados.

        </p>

        <p class="generated">

            Relatório gerado em
            {generated_at}

        </p>

    </header>


    <!-- =====================================================
         INDICADORES
         ===================================================== -->

    <div class="cards">


        <div class="card">

            <div class="card-title">

                Datasets monitorados

            </div>

            <div class="card-value">

                {total_datasets}

            </div>

        </div>


        <div class="card">

            <div class="card-title">

                Datasets saudáveis

            </div>

            <div class="card-value">

                {healthy_datasets}

            </div>

        </div>


        <div class="card">

            <div class="card-title">

                Warnings

            </div>

            <div class="card-value">

                {warning_datasets}

            </div>

        </div>


        <div class="card">

            <div class="card-title">

                Registros monitorados

            </div>

            <div class="card-value">

                {total_rows:,}

            </div>

        </div>


    </div>


    <!-- =====================================================
         PIPELINE HEALTH
         ===================================================== -->

    <div class="section">


        <h2>
            Pipeline Health
        </h2>


        <p class="description">

            Visão geral da saúde
            dos principais datasets
            do pipeline.

        </p>


        <table>


            <thead>

                <tr>

                    <th>
                        Dataset
                    </th>

                    <th>
                        Registros
                    </th>

                    <th>
                        Última data
                    </th>

                    <th>
                        Dias sem atualização
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                {health_rows}

            </tbody>


        </table>


    </div>


    <!-- =====================================================
         DATA FRESHNESS
         ===================================================== -->

    <div class="section">


        <h2>
            Data Freshness
        </h2>


        <p class="description">

            Verifica há quantos dias
            cada dataset deixou
            de receber dados.

        </p>


        <table>


            <thead>

                <tr>

                    <th>
                        Dataset
                    </th>

                    <th>
                        Última data
                    </th>

                    <th>
                        Data da verificação
                    </th>

                    <th>
                        Dias sem atualização
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                {freshness_rows}

            </tbody>


        </table>


    </div>


    <!-- =====================================================
         DATA VOLUME
         ===================================================== -->

    <div class="section">


        <h2>
            Data Volume
        </h2>


        <p class="description">

            Quantidade atual de registros
            por dataset monitorado.

        </p>


        <table>


            <thead>

                <tr>

                    <th>
                        Dataset
                    </th>

                    <th>
                        Quantidade de registros
                    </th>

                    <th>
                        Data da verificação
                    </th>

                </tr>

            </thead>


            <tbody>

                {volume_rows}

            </tbody>


        </table>


    </div>


    <div class="footer">

        CS Analytics · dbt + DuckDB ·
        Data Observability

    </div>


</div>


</body>

</html>
"""


# ============================================================
# SALVAR HTML
# ============================================================

OUTPUT_PATH.write_text(
    html_content,
    encoding="utf-8"
)


# ============================================================
# FECHAR CONEXÃO
# ============================================================

con.close()


print()
print("==========================================")
print(" RELATÓRIO GERADO COM SUCESSO")
print("==========================================")
print()
print(f"Arquivo: {OUTPUT_PATH}")
print()