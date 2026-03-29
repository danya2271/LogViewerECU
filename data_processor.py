import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    try:
        # Пробуем разные разделители, часто логи OpenDiag имеют табы или точку с запятой
        df = pd.read_csv(file_path, sep='\t', engine='python', encoding='cp1251')
        if len(df.columns) < 5:
            df = pd.read_csv(file_path, sep=';', engine='python', encoding='cp1251')
        if len(df.columns) < 5:
            df = pd.read_csv(file_path, sep=',', engine='python', encoding='cp1251')
    except Exception as e:
        raise Exception(f"Ошибка чтения файла: {e}")

    df.columns = df.columns.str.strip(' "')
    
    # Очистка от мусора и замена запятых на точки для чисел
    for col in df.columns:
        clean_series = df[col].astype(str).str.replace('"', '').str.strip().str.replace(',', '.')
        df[col] = pd.to_numeric(clean_series, errors='coerce')
        
    return df

def calculate_derived_metrics(df, mapping):
    # Расчет мощности по ДМРВ (грубая оценка: Расход воздуха / 3)
    if 'MAF' in mapping and mapping['MAF'] in df.columns:
        df['Calculated_HP'] = df[mapping['MAF']] / 3.0
    else:
        df['Calculated_HP'] = np.nan
    return df

def get_dyno_data(df, mapping):
    """Возвращает данные для графика Мощность от Оборотов (только при тапке в пол)"""
    if 'RPM' not in mapping or 'TPS' not in mapping or 'Calculated_HP' not in df:
        return None, None
        
    rpm_col = mapping['RPM']
    tps_col = mapping['TPS']
    
    # Берем только моменты, где дроссель открыт более чем на 80%
    wot_mask = df[tps_col] > 80.0
    dyno_df = df[wot_mask].copy()
    
    if dyno_df.empty:
        return None, None
        
    # Сортируем по оборотам для красивого графика
    dyno_df = dyno_df.sort_values(by=rpm_col)
    
    # Сглаживание (скользящая средняя), чтобы убрать шумы
    dyno_df['Calculated_HP_Smooth'] = dyno_df['Calculated_HP'].rolling(window=5, min_periods=1).mean()
    
    return dyno_df[rpm_col], dyno_df['Calculated_HP_Smooth']