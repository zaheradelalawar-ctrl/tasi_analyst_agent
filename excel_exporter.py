"""
Excel Exporter: Generates professional multi-tab executive spreadsheets for TASI institutional consensus.
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class ExecutiveExcelBuilder:
    def __init__(self, output_file: str = "TASI_Institutional_Consensus_Report.xlsx"):
        self.output_file = output_file

    def build(self, datasets: dict) -> str:
        ranked_df = datasets.get("ranked", pd.DataFrame())
        matrix_df = datasets.get("matrix", pd.DataFrame())

        wb = Workbook()
        ws1 = wb.active
        ws1.title = "Executive_Consensus_Ranking"
        ws1.views.sheetView[0].showGridLines = True

        ws2 = wb.create_sheet(title="All_Institutional_Calls")
        ws2.views.sheetView[0].showGridLines = True

        header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        title_font = Font(name="Calibri", size=16, bold=True, color="1B365D")
        subtitle_font = Font(name="Calibri", size=10, italic=True, color="555555")
        thin_border = Border(
            left=Side(style='thin', color='D3D3D3'), right=Side(style='thin', color='D3D3D3'),
            top=Side(style='thin', color='D3D3D3'), bottom=Side(style='thin', color='D3D3D3')
        )
        align_center = Alignment(horizontal="center", vertical="center")
        align_left = Alignment(horizontal="left", vertical="center")
        align_right = Alignment(horizontal="right", vertical="center")

        ws1.append([])
        ws1.cell(row=2, column=1, value="TASI 19-INSTITUTION CONSENSUS & RANKING MATRIX").font = title_font
        ws1.cell(row=3, column=1, value="Multi-Tier Sell-Side Research Aggregation & Target Price Analysis").font = subtitle_font
        ws1.append([])

        headers1 = [
            "Rank", "Ticker", "Company", "Consensus Status", "Positive Firms", 
            "Neutral Firms", "Negative Firms", "Latest Price (SAR)", "Median Target (SAR)", 
            "Implied Upside (%)", "Target Dispersion (%)", "Composite Score", "Consensus Signal"
        ]
        ws1.append(headers1)
        for col_num in range(1, len(headers1) + 1):
            cell = ws1.cell(row=4, column=col_num)
            cell.fill, cell.font, cell.alignment = header_fill, header_font, align_center

        for idx, row in ranked_df.iterrows():
            r_data = [
                row.get("rank", idx + 1), str(row.get("symbol", "")), str(row.get("company", "")),
                str(row.get("status", "")), int(row.get("positive_firms", 0)),
                int(row.get("neutral_firms", 0)), int(row.get("negative_firms", 0)),
                float(row.get("current_price", 0.0)), float(row.get("median_target", 0.0)),
                float(row.get("consensus_upside_pct", 0.0)), float(row.get("target_dispersion_pct", 0.0)),
                float(row.get("composite_score", 0.0)), str(row.get("consensus_signal", ""))
            ]
            ws1.append(r_data)
            row_idx = ws1.max_row
            for c_idx in range(1, len(r_data) + 1):
                cell = ws1.cell(row=row_idx, column=c_idx)
                cell.font, cell.border = Font(name="Calibri", size=11), thin_border
                if c_idx in [1, 2, 4, 13]: cell.alignment = align_center
                elif c_idx == 3: cell.alignment = align_left
                elif c_idx >= 5:
                    cell.alignment = align_right
                    if c_idx in [8, 9]: cell.number_format = "#,##0.00"
                    elif c_idx in [10, 11]: cell.number_format = "0.0%"
                    elif c_idx == 12: cell.number_format = "#,##0.0"

        ws2.append([])
        ws2.cell(row=2, column=1, value="COMPLETE INSTITUTIONAL RESEARCH CALLS LEDGER").font = title_font
        ws2.cell(row=3, column=1, value="Detailed Breakdown of All Analyst Recommendations and 12-Month Target Prices").font = subtitle_font
        ws2.append([])

        headers2 = ["Institution", "Tier", "Ticker", "Company", "Rating", "Current Price (SAR)", "Target Price (SAR)", "Upside (%)", "Report Date"]
        ws2.append(headers2)
        for col_num in range(1, len(headers2) + 1):
            cell = ws2.cell(row=4, column=col_num)
            cell.fill, cell.font, cell.alignment = header_fill, header_font, align_center

        for idx, row in matrix_df.iterrows():
            r_data2 = [
                str(row.get("institution", "")), str(row.get("tier", "")), str(row.get("symbol", "")),
                str(row.get("company", "")), str(row.get("rating", "")),
                float(row.get("current_price", 0.0)), float(row.get("target_price", 0.0)),
                float(row.get("upside_pct", 0.0)), str(row.get("report_date", ""))
            ]
            ws2.append(r_data2)
            row_idx = ws2.max_row
            for c_idx in range(1, len(r_data2) + 1):
                cell = ws2.cell(row=row_idx, column=c_idx)
                cell.font, cell.border = Font(name="Calibri", size=11), thin_border
                if c_idx in [1, 2, 3, 5, 9]: cell.alignment = align_center
                elif c_idx == 4: cell.alignment = align_left
                elif c_idx >= 6:
                    cell.alignment = align_right
                    if c_idx in [6, 7]: cell.number_format = "#,##0.00"
                    elif c_idx == 8: cell.number_format = "0.0%"

        for ws in [ws1, ws2]:
            for col in ws.columns:
                max_len = max((len(str(cell.value)) for cell in col if cell.row > 3 and cell.value), default=12)
                ws.column_dimensions[get_column_letter(col[0].column)].width = max(max_len + 4, 12)

        wb.save(self.output_file)
        return self.output_file