import pandas as pd
import math
import sys
import os

# -------------------------
# Arguments
# -------------------------
bay2_val = int(sys.argv[1]) if len(sys.argv) > 1 else 5
bay3_val = int(sys.argv[2]) if len(sys.argv) > 2 else 3

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(BASE_DIR, "input", "uploaded_input.xlsx")

# Open workbook ONLY ONCE (faster)
excel = pd.ExcelFile(file_path)

# -------------------------
# Auto Header Detection
# -------------------------
header_cache = {}

def read_sheet(sheet_name, columns):

    # Header already detected
    if sheet_name in header_cache:
        h = header_cache[sheet_name]
        return pd.read_excel(
            excel,
            sheet_name=sheet_name,
            header=h
        )

    # Detect header only once
    for h in range(5):

        try:
            df = pd.read_excel(
                excel,
                sheet_name=sheet_name,
                header=h
            )

            df.columns = df.columns.astype(str).str.strip()

            if all(col in df.columns for col in columns):
                header_cache[sheet_name] = h
                return df

        except:
            pass

    return None

# -------------------------
# Read PLATING sheet
# -------------------------

plating = read_sheet(
    "PLATING TIME",
    ["PART NO", "PLATING"]
)

if plating is None:
    raise Exception("PLATING TIME sheet not found")

plating = plating[
    ["PART NO", "PLATING"]
]

plating.columns = [
    "Part Number",
    "Plating Time"
]

plating["Part Number"] = (
    plating["Part Number"]
    .astype(str)
    .str.strip()
)

all_output = []


# -----------------------------------------
# Process All Stock Sheets
# -----------------------------------------

for sheet in excel.sheet_names:

    # Skip plating sheet
    if sheet.upper() == "PLATING TIME":
        continue

    print("Processing :", sheet)

    try:

        # ==========================
        # FPL TYPE SHEET
        # ==========================

        fpl_columns = [
            "PART NUMBER",
            "CHALLAN QTY IN KGS",
            "Load per batch"
        ]

        df = read_sheet(sheet, fpl_columns)

        if df is not None:

            df = df[fpl_columns].copy()

            df.columns = [
                "Part Number",
                "Quantity",
                "Batch Capacity"
            ]

            df["Quantity"] = pd.to_numeric(
                df["Quantity"],
                errors="coerce"
            )

            df["Batch Capacity"] = pd.to_numeric(
                df["Batch Capacity"],
                errors="coerce"
            )

            df = df.dropna()

            df = df[df["Batch Capacity"] > 0]

            df["Batches"] = (
                df["Quantity"] /
                df["Batch Capacity"]
            ).apply(math.ceil)

            df["BAY"] = 3

            df["Part Number"] = (
                df["Part Number"]
                .astype(str)
                .str.strip()
            )

            df = pd.merge(
                df,
                plating,
                on="Part Number",
                how="left"
            )

            df["Plating Time"] = df["Plating Time"].fillna(0)

            all_output.append(
                df[
                    [
                        "Part Number",
                        "BAY",
                        "Batches",
                        "Plating Time"
                    ]
                ]
            )

            continue


        # ==========================
        # SFL TYPE SHEET
        # ==========================

        sfl_columns = [
            "PART NO",
            "STOCK QTY IN NOS",
            "PART WEIGHT IN KGS",
            "BATCH QTY IN KGS"
        ]

        df = read_sheet(sheet, sfl_columns)

        if df is not None:

            df = df[sfl_columns].copy()

            df.columns = [
                "Part Number",
                "Stock Qty",
                "Part Weight",
                "Batch Qty"
            ]

            for c in [
                "Stock Qty",
                "Part Weight",
                "Batch Qty"
            ]:

                df[c] = pd.to_numeric(
                    df[c],
                    errors="coerce"
                )

            df = df.dropna()

            df = df[df["Batch Qty"] > 0]

            df["Total Weight"] = (
                df["Stock Qty"] *
                df["Part Weight"]
            )

            df["Batches"] = (
                df["Total Weight"] /
                df["Batch Qty"]
            ).apply(math.ceil)

            df["BAY"] = 2

            df["Part Number"] = (
                df["Part Number"]
                .astype(str)
                .str.strip()
            )

            df = pd.merge(
                df,
                plating,
                on="Part Number",
                how="left"
            )

            df["Plating Time"] = df["Plating Time"].fillna(0)

            all_output.append(
                df[
                    [
                        "Part Number",
                        "BAY",
                        "Batches",
                        "Plating Time"
                    ]
                ]
            )

            continue

        print(sheet, "Skipped (Unknown format)")

    except Exception as e:
        print(sheet, e)


# -----------------------------------------
# Merge All Outputs
# -----------------------------------------

if len(all_output) == 0:
    print("No valid stock sheets found.")
    sys.exit()

scheduler_input = pd.concat(
    all_output,
    ignore_index=True
)

scheduler_input.columns = [
    "PART NUMBER",
    "BAY",
    "BATCHES",
    "PLATING IN SECONDS"
]

# Numeric conversion
scheduler_input["BATCHES"] = pd.to_numeric(
    scheduler_input["BATCHES"],
    errors="coerce"
).fillna(0)

scheduler_input["PLATING IN SECONDS"] = pd.to_numeric(
    scheduler_input["PLATING IN SECONDS"],
    errors="coerce"
).fillna(0)

# Remove invalid rows
scheduler_input = scheduler_input[
    scheduler_input["BATCHES"] > 0
]

# Sort Preview
scheduler_input = scheduler_input.sort_values(
    by=[
        "BAY",
        "BATCHES"
    ],
    ascending=[
        True,
        False
    ]
)

# Reset index
scheduler_input.reset_index(
    drop=True,
    inplace=True
)

# -----------------------------------------
# Save Excel
# -----------------------------------------

output_folder = os.path.join(
    BASE_DIR,
    "output"
)

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = os.path.join(
    output_folder,
    "scheduler_input.xlsx"
)

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    scheduler_input.to_excel(
        writer,
        sheet_name="Scheduler Input",
        index=False
    )

print("--------------------------------")
print("Scheduler Input Created")
print(output_file)
print("--------------------------------")
print("Total Parts :", len(scheduler_input))
print("Bay 2 Parts :", len(scheduler_input[scheduler_input["BAY"]==2]))
print("Bay 3 Parts :", len(scheduler_input[scheduler_input["BAY"]==3]))
print("--------------------------------")