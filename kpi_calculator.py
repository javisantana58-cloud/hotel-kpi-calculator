import pandas as pd
import sys

try:
    # Leer el Excel
    df = pd.read_excel("datos_hotel.xlsx")

    # Verificar que las columnas necesarias existen
    columnas_necesarias = ["Mes", "Habitaciones_disponibles", "Habitaciones_vendidas", "Ingresos_Totales"]
    for col in columnas_necesarias:
        if col not in df.columns:
            print(f"ERROR: Falta la columna '{col}' en el Excel.")
            sys.exit()

    # Verificar que no hay celdas vacías
    if df[columnas_necesarias].isnull().any().any():
        print("ERROR: Hay celdas vacías en el Excel. Revisa los datos.")
        sys.exit()

    # Calcular KPIs
    df["Ocupacion_%"] = (df["Habitaciones_vendidas"] / df["Habitaciones_disponibles"]) * 100
    df["ADR"] = df["Ingresos_Totales"] / df["Habitaciones_vendidas"]
    df["RevPAR"] = df["Ingresos_Totales"] / df["Habitaciones_disponibles"]

    # Redondear
    df["Ocupacion_%"] = df["Ocupacion_%"].round(2)
    df["ADR"] = df["ADR"].round(2)
    df["RevPAR"] = df["RevPAR"].round(2)

    # Mostrar resultados
    print(df[["Mes", "Ocupacion_%", "ADR", "RevPAR"]].to_string(index=False))

    # Resumen
    mejor_mes = df.loc[df["Ocupacion_%"].idxmax(), "Mes"]
    print(f"\n--- RESUMEN ---")
    print(f"Ocupación media: {df['Ocupacion_%'].mean():.1f}%")
    print(f"ADR medio: {df['ADR'].mean():.2f}€")
    print(f"RevPAR medio: {df['RevPAR'].mean():.2f}€")
    print(f"Mejor mes: {mejor_mes} ({df['Ocupacion_%'].max():.1f}% ocupación)")

    # Guardar
    df.to_excel("resultados_kpi.xlsx", index=False)
    print("\nResultados guardados en resultados_kpi.xlsx")

except FileNotFoundError:
    print("ERROR: No se encuentra el archivo datos_hotel.xlsx.")
    print("Asegúrate de que está en la misma carpeta que este programa.")